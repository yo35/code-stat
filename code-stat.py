#!/usr/bin/env python3
################################################################################
#                                                                              #
#   This file is part of Code Stat, a Python script to compute line of code    #
#   metrics on a set of source code files, for several programming languages.  #
#   Copyright (C) 2023-2025  Yoann Le Montagner <yo35 -at- melix.net>          #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#   GNU General Public License for more details.                               #
#                                                                              #
#   You should have received a copy of the GNU General Public License          #
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
#                                                                              #
################################################################################

"""
Compute line of code metrics on source code files, for several programming languages.

Usage:

    python3 code-stat.py <file-or-folder-1> [<file-or-folder-2> [<file-or-folder-3> ...]]

Count the number of source code files passed in argument of the script, and the number of code lines
and comment lines they contain. If a folder is passed in argument of the script, all its content is
analyzed, including recursively the content of its child folders, grandchild folders, etc...

Disclaimer:
The parsing strategy implemented in this script is a (significantly) simplified version of what would be
necessary to implement a real programming language parser. As such, it may not distinguish accurately
between code lines and comment lines in some weird cases (e.g. if a string litteral contains something
that looks as a comment token). Still, when it comes to analyze realistic code bases, these situations
are unlikely to happen frequently.
"""


import os
import re
import sys

from typing import Callable, Optional


class LOCCounter:
    """
    Line of code counter: hold the number of files processed so far, and the respective number of code lines
    and comments they contain.
    """

    def __init__(self, title: str) -> None:
        self.title = title
        self.fileCount = 0
        self.codeLineCount = 0
        self.commentLineCount = 0

    def increment(self, fileCount: int, codeLineCount: int, commentLineCount: int) -> None:
        self.fileCount += fileCount
        self.codeLineCount += codeLineCount
        self.commentLineCount += commentLineCount

    def printStats(self) -> None:
        print(self.title)
        print('-' * len(self.title))
        print('Source files:       {:8d}'.format(self.fileCount))
        print('Code lines:         {:8d}'.format(self.codeLineCount))
        print('Comment lines:      {:8d}'.format(self.commentLineCount))
        if self.codeLineCount == 0:
            print('Comment/code ratio:        - %')
        else:
            print('Comment/code ratio: {:8.0f} %'.format(self.commentLineCount * 100 / self.codeLineCount))

    def isEmpty(self) -> bool:
        return self.fileCount == 0


def noSuchToken() -> Callable[[str], Optional[int]]:
    def fun(line: str) -> Optional[int]:
        return None
    return fun


def findToken(token: str) -> Callable[[str], Optional[int]]:
    def fun(line: str) -> Optional[int]:
        pos = line.find(token)
        return None if pos < 0 else pos
    return fun


def findRegex(pattern: str) -> Callable[[str], Optional[int]]:
    compiledPattern = re.compile(pattern)
    def fun(line: str) -> Optional[int]:
        m = re.search(compiledPattern, line)
        return None if m is None else m.start()
    return fun


def isFalse() -> Callable[[str], bool]:
    def fun(line: str) -> bool:
        return False
    return fun


def isStartingWithToken(token: str) -> Callable[[str], bool]:
    def fun(line: str) -> bool:
        return line.startswith(token)
    return fun


def doProcessFile(
        locCounter: LOCCounter,
        file: str,
        findBeginCommentToken: Callable[[str], Optional[int]] = noSuchToken(),
        findEndCommentToken: Callable[[str], Optional[int]] = noSuchToken(),
        findSingleLineCommentToken: Callable[[str], Optional[int]] = noSuchToken(),
        isMandatoryFirstInstruction: Callable[[str], bool] = isFalse(),
    ) -> None:
    """
    Core processing function.
    """

    codeLineCount = 0
    commentLineCount = 0

    with open(file, 'r') as f:
        withinBlockComment = False
        withinHeader = True
        headerLineCount = 0
        lineIndex = 0 # 1-based index
        for line in f:
            line = line.strip()
            lineIndex += 1

            # Blank line
            if len(line) == 0:
                if not withinBlockComment:
                    withinHeader = False
                    # Header lines are ignored if immediately followed by a blank line.
                continue

            # Within a block comment
            if withinBlockComment:
                if withinHeader:
                    headerLineCount += 1
                else:
                    commentLineCount += 1

            # Regular code
            else:
                beginCommentToken = findBeginCommentToken(line)
                singleLineCommentToken = findSingleLineCommentToken(line)
                if beginCommentToken == 0 or singleLineCommentToken == 0:
                    if withinHeader:
                        headerLineCount += 1
                    else:
                        commentLineCount += 1
                else:
                    codeLineCount += 1
                    if withinHeader and not (lineIndex == 1 and isMandatoryFirstInstruction(line)):
                        withinHeader = False
                        commentLineCount += headerLineCount # Header lines are counted as comment if immediately followed by code.
                if beginCommentToken is not None and (singleLineCommentToken is None or beginCommentToken < singleLineCommentToken):
                    withinBlockComment = True
                    line = line[(beginCommentToken + 1):]

            # Look for the end of the current block comment (and potential following
            # block comments that both begin and end on the current line)
            if withinBlockComment:
                while True:
                    endCommentToken = findEndCommentToken(line)
                    if endCommentToken is None:
                        break
                    line = line[(endCommentToken + 1):]
                    beginCommentToken = findBeginCommentToken(line)
                    singleLineCommentToken = findSingleLineCommentToken(line)
                    if beginCommentToken is None or (singleLineCommentToken is not None and singleLineCommentToken < beginCommentToken):
                        withinBlockComment = False
                        break
                    line = line[(beginCommentToken + 1):]

    # Increment the counter (only at the end, in case of exceptions).
    locCounter.increment(1, codeLineCount, commentLineCount)


def processCFamilyFile(locCounter: LOCCounter, file: str) -> None:
    """
    Process a file with C/C++-like comments (i.e. // for single line comments, /* ... */ for block comments).
    """
    doProcessFile(
        locCounter,
        file,
        findBeginCommentToken = findToken('/*'),
        findEndCommentToken = findToken('*/'),
        findSingleLineCommentToken = findToken('//'),
    )


def processPHPFile(locCounter: LOCCounter, file: str) -> None:
    """
    Process a PHP file (i.e. // for single line comments, /* ... */ for block comments,
    and possibly a <?php instruction on the first line).
    """
    doProcessFile(
        locCounter,
        file,
        findBeginCommentToken = findToken('/*'),
        findEndCommentToken = findToken('*/'),
        findSingleLineCommentToken = findToken('//'),
        isMandatoryFirstInstruction = isStartingWithToken('<?php'),
    )


def processCSSFile(locCounter: LOCCounter, file: str) -> None:
    """
    Process a CSS file (/* ... */ for block comments, no single line comments).
    """
    doProcessFile(
        locCounter,
        file,
        findBeginCommentToken = findToken('/*'),
        findEndCommentToken = findToken('*/'),
    )


def processScriptFamilyFile(locCounter: LOCCounter, file: str) -> None:
    """
    Process a file whose comments start with a hash character (#).
    """
    doProcessFile(
        locCounter,
        file,
        findSingleLineCommentToken = findToken('#'),
    )


def processFortranFile(locCounter: LOCCounter, file: str) -> None:
    """
    Process a Fortran 90 file (comments start with an exclamation mark character).
    Comments starting with !DIR$, !$OMP, etc... are counted as code (compiler directives).
    """
    doProcessFile(
        locCounter,
        file,
        findSingleLineCommentToken = findRegex('!(?!\\w+\\$|\\$\\w+)'),
    )


def processSQLFile(locCounter: LOCCounter, file: str) -> None:
    """
    Process a SQL file (comments start with two hyphen characters).
    """
    doProcessFile(
        locCounter,
        file,
        findSingleLineCommentToken = findToken('--'),
    )


def processPascalFile(locCounter: LOCCounter, file: str) -> None:
    """
    Process a Pascal file ( (* ... *) or { ... } for block comments, // for single line comments).
    Comments starting with a $ character are counted as code (compiler directives).
    """
    doProcessFile(
        locCounter,
        file,
        findBeginCommentToken = findRegex('(?:\\(\\*|{)(?!\\$)'),
        findEndCommentToken = findRegex('(?:\\*\\)|})'),
        findSingleLineCommentToken = findToken('//'),
    )


def run(filesOrDirectories: list[str]) -> None:
    """
    Script entry point.
    """

    counters: list[LOCCounter] = []
    extensionToAction: dict[str, Callable[[str], None]] = {}

    def registerLanguage(title: str, processFun: Callable[[LOCCounter, str], None], extensions: list[str]) -> None:
        counter = LOCCounter(title)
        action = lambda file: processFun(counter, file)
        counters.append(counter)
        for extension in extensions:
            if extension in extensionToAction:
                raise ValueError('Extension conflict: ' + extension)
            extensionToAction[extension] = action

    # Register the supported languages.
    registerLanguage('C/C++'            , processCFamilyFile     , [ '.c', '.cpp', '.cxx', '.cc', '.h', '.hpp', '.hxx', '.hh' ])
    registerLanguage('C#'               , processCFamilyFile     , [ '.cs' ])
    registerLanguage('CSS'              , processCSSFile         , [ '.css' ])
    registerLanguage('CUDA'             , processCFamilyFile     , [ '.cu', '.cuh' ])
    registerLanguage('Fortran 90'       , processFortranFile     , [ '.f90' ])
    registerLanguage('Java'             , processCFamilyFile     , [ '.java' ])
    registerLanguage('JavaScript'       , processCFamilyFile     , [ '.js', '.jsx', '.cjs', '.mjs' ])
    registerLanguage('Kotlin'           , processCFamilyFile     , [ '.kt' ])
    registerLanguage('Pascal'           , processPascalFile      , [ '.pas' ])
    registerLanguage('PHP'              , processPHPFile         , [ '.php' ])
    registerLanguage('Python'           , processScriptFamilyFile, [ '.py' ])
    registerLanguage('SQL'              , processSQLFile         , [ '.sql' ])
    registerLanguage('TypeScript'       , processCFamilyFile     , [ '.ts', '.tsx', '.cts', '.mts' ])
    registerLanguage('Unix shell script', processScriptFamilyFile, [ '.sh', '.bash', '.csh', '.ksh', '.zsh' ])

    # Visit recursively all the files and folders passed on the command line.
    toProcess = [os.path.abspath(f) for f in filesOrDirectories]
    errorCount = 0
    while len(toProcess) != 0:
        path = toProcess.pop()
        try:
            if os.path.isdir(path):
                toProcess.extend([os.path.join(path, f) for f in os.listdir(path)])
            elif os.path.isfile(path):
                filename, extension = os.path.splitext(path)
                extension = extension.lower()
                if extension in extensionToAction:
                    extensionToAction[extension](path)
        except Exception:
            errorCount += 1
            print('Error with {:s}'.format(path), file = sys.stderr)
    if errorCount > 0:
        print('{:d} error(s) encountered'.format(errorCount), file = sys.stderr)

    # Print the result.
    print()
    allCountersAreEmpty = True
    for counter in counters:
        if not counter.isEmpty():
            allCountersAreEmpty = False
            counter.printStats()
            print()
    if allCountersAreEmpty:
        print('No source code file found')
        print()


# Invoke the script entry point.
if __name__ == '__main__':
    run(sys.argv[:0:-1])
