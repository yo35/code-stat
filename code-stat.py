#!/usr/bin/env python3
################################################################################
#                                                                              #
#   This file is part of Code Stat, a Python script to compute line of code    #
#   metrics on a set of source code files, for several programming languages.  #
#   Copyright (C) 2023  Yoann Le Montagner <yo35 -at- melix.net>               #
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


class LOCCounter:
    """
    Line of code counter: hold the number of files processed so far, and the respective number of code lines
    and comments they contain.
    """

    def __init__(self, title):
        self.title = title
        self.fileCount = 0
        self.codeLineCount = 0
        self.commentLineCount = 0

    def printStats(self):
        print(self.title)
        print('-' * len(self.title))
        print('Source files:       {:8d}'.format(self.fileCount))
        print('Code lines:         {:8d}'.format(self.codeLineCount))
        print('Comment lines:      {:8d}'.format(self.commentLineCount))
        if self.codeLineCount == 0:
            print('Comment/code ratio:        - %')
        else:
            print('Comment/code ratio: {:8.0f} %'.format(self.commentLineCount * 100 / self.codeLineCount))

    def isEmpty(self):
        return self.fileCount == 0


def doProcessFile(locCounter, file, findBeginCommentToken, findEndCommentToken, findSingleLineCommentToken, isMandatoryFirstInstruction):
    """
    Core processing function.
    """

    locCounter.fileCount += 1
    with open(file, 'r') as f:
        withinBlockComment = False
        withinHeader = True
        lineIndex = 0 # 1-based index
        for line in f:
            line = line.strip()
            lineIndex = lineIndex + 1

            # Blank line
            if len(line) == 0:
                if not withinBlockComment:
                    withinHeader = False
                continue

            # Within a block comment
            if withinBlockComment:
                if not withinHeader:
                    locCounter.commentLineCount += 1

            # Regular code
            else:
                beginCommentToken = findBeginCommentToken(line)
                singleLineCommentToken = findSingleLineCommentToken(line)
                if beginCommentToken == 0 or singleLineCommentToken == 0:
                    if not withinHeader:
                        locCounter.commentLineCount += 1
                else:
                    locCounter.codeLineCount += 1
                    if withinHeader and not (lineIndex == 1 and isMandatoryFirstInstruction(line)):
                        withinHeader = False
                if beginCommentToken != None and (singleLineCommentToken == None or beginCommentToken < singleLineCommentToken):
                    withinBlockComment = True
                    line = line[(beginCommentToken + 1):]

            # Look for the end of the current block comment (and potential following
            # block comments that both begin and end on the current line)
            if withinBlockComment:
                while True:
                    endCommentToken = findEndCommentToken(line)
                    if endCommentToken == None:
                        break
                    line = line[(endCommentToken + 1):]
                    beginCommentToken = findBeginCommentToken(line)
                    singleLineCommentToken = findSingleLineCommentToken(line)
                    if beginCommentToken == None or (singleLineCommentToken != None and singleLineCommentToken < beginCommentToken):
                        withinBlockComment = False
                        break
                    line = line[(beginCommentToken + 1):]


def noSuchToken():
    def fun(line):
        return None
    return fun


def findToken(token):
    def fun(line):
        pos = line.find(token)
        return None if pos < 0 else pos
    return fun


def findRegex(pattern):
    def fun(line):
        m = re.search(pattern, line)
        return None if m == None else m.start()
    return fun


def isFalse():
    def fun(line):
        return False
    return fun


def isStartingWithToken(token):
    def fun(line):
        return line.startswith(token)
    return fun


def processCFamilyFile(locCounter, file):
    """
    Process a file with C/C++-like comments (i.e. // for single line comments, /* ... */ for block comments).
    """
    doProcessFile(locCounter, file, findToken('/*'), findToken('*/'), findToken('//'), isFalse())


def processPHPFile(locCounter, file):
    """
    Process a PHP file (i.e. // for single line comments, /* ... */ for block comments, and possibly a <?php instruction on the first line).
    """
    doProcessFile(locCounter, file, findToken('/*'), findToken('*/'), findToken('//'), isStartingWithToken('<?php'))


def processCSSFile(locCounter, file):
    """
    Process a CSS file (/* ... */ for block comments, no single line comments).
    """
    doProcessFile(locCounter, file, findToken('/*'), findToken('*/'), noSuchToken(), isFalse())


def processScriptFamilyFile(locCounter, file):
    """
    Process a file whose comments start with a hash character (#).
    """
    doProcessFile(locCounter, file, noSuchToken(), noSuchToken(), findToken('#'), isFalse())


def processFortranFile(locCounter, file):
    """
    Process a Fortran 90 file (comments start with an exclamation mark character).
    Comments starting with !DIR$, !$OMP, etc... are counted as code (compiler directives).
    """
    doProcessFile(locCounter, file, noSuchToken(), noSuchToken(), findRegex('!(?!\\w+\\$|\\$\\w+)'), isFalse())


def processSQLFile(locCounter, file):
    """
    Process a SQL file (comments start with two hyphen characters).
    """
    doProcessFile(locCounter, file, noSuchToken(), noSuchToken(), findToken('--'), isFalse())


def processPascalFile(locCounter, file):
    """
    Process a Pascal file ( (* ... *) or { ... } for block comments, // for single line comments).
    Comments starting with a $ character are counted as code (compiler directives).
    """
    doProcessFile(locCounter, file, findRegex('(?:\\(\\*|{)(?!\\$)'), findRegex('(?:\\*\\)|})'), findToken('//'), isFalse())


if __name__ == '__main__':

    counters = []
    extensionToAction = {}

    def registerLanguage(title, processFun, extensions):
        counter = LOCCounter(title)
        action = lambda file: processFun(counter, file)
        counters.append(counter)
        for extension in extensions:
            if extension in extensionToAction:
                raise ValueError('Extension conflict: ' + extension)
            extensionToAction[extension] = action

    # Register the supported languages.
    registerLanguage('C/C++'     , processCFamilyFile     , [ '.c', '.cpp', '.cxx', '.cc', '.h', '.hpp', '.hxx', '.hh' ])
    registerLanguage('C#'        , processCFamilyFile     , [ '.cs' ])
    registerLanguage('CSS'       , processCSSFile         , [ '.css' ])
    registerLanguage('CUDA'      , processCFamilyFile     , [ '.cu', '.cuh' ])
    registerLanguage('Fortran 90', processFortranFile     , [ '.f90' ])
    registerLanguage('Java'      , processCFamilyFile     , [ '.java' ])
    registerLanguage('JavaScript', processCFamilyFile     , [ '.js', '.jsx', '.mjs' ])
    registerLanguage('Kotlin'    , processCFamilyFile     , [ '.kt' ])
    registerLanguage('Pascal'    , processPascalFile      , [ '.pas' ])
    registerLanguage('PHP'       , processPHPFile         , [ '.php' ])
    registerLanguage('Python'    , processScriptFamilyFile, [ '.py' ])
    registerLanguage('SQL'       , processSQLFile         , [ '.sql' ])
    registerLanguage('TypeScript', processCFamilyFile     , [ '.ts', '.tsx', '.mts' ])

    # Visit recursively all the files and folders passed on the command line.
    toProcess = [os.path.abspath(f) for f in sys.argv[:0:-1]]
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
