################################################################################
#                                                                              #
#   This file is part of Code Stat, a Python script to compute line of code    #
#   metrics on a set of source code files, for several programming languages.  #
#   Copyright (C) 2023-2024  Yoann Le Montagner <yo35 -at- melix.net>          #
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


import os
import subprocess


def checkContentOfStd(expectedContent, actualContent, label):
    """Ensure that the given actual content matches the expected content."""

    actualLines = actualContent.splitlines()
    actualLineIndex = 0

    def isEndOfActualContent():
        return actualLineIndex > len(actualLines)

    def getCurrentActualLine():
        return actualLines[actualLineIndex - 1].strip()

    def goToNextNonBlankActualLine():
        nonlocal actualLineIndex
        while True:
            actualLineIndex += 1
            if isEndOfActualContent() or len(getCurrentActualLine()) != 0:
                break

    lineIndex = 0 # 1-based index
    for line in expectedContent:
        line = line.strip()
        lineIndex += 1

        # Skip blank lines.
        if len(line) == 0:
            continue

        # Compare the current (expected) line with the next non-blank line in actual content.
        goToNextNonBlankActualLine()
        assert not isEndOfActualContent(), 'Unexpected end of content for ' + label + ' at line ' + str(lineIndex)
        assert getCurrentActualLine() == line, 'Unexpected content for ' + label + ' at line ' + str(lineIndex)

    # Ensure that nothing remains in the actual content.
    goToNextNonBlankActualLine()
    assert isEndOfActualContent(), 'Unexpected content for ' + label + ' at the end of the output'


def getExpectedStdout():
    with open(os.path.join(os.path.dirname(__file__), 'assets', 'end2end.txt'), 'r') as f:
        return f.readlines()


def getExpectedStderr():
    return [
        'Error with ' + getUnreadableFilePath(),
        '1 error(s) encountered',
    ]


def getUnreadableFilePath():
    return os.path.join(os.path.dirname(__file__), 'assets', 'languages', 'unreadable-file.py')


def setup_module(module):
    unreadableFile = getUnreadableFilePath()
    with open(unreadableFile, 'w') as f:
        f.writelines([
            '# This file is not readable (000 permission).\n'
            'print("Hello World!")\n'
        ])
    os.chmod(unreadableFile , 0o000) # Make the file unreadable.


def teardown_module(module):
    unreadableFile = getUnreadableFilePath()
    os.remove(unreadableFile)


def test_end_to_end():

    targetDirectory = os.path.join('test', 'assets', 'languages')
    commandLine = 'python3 code-stat.py ' + targetDirectory
    result = subprocess.run(commandLine, capture_output = True, text = True, shell = True)

    assert result.returncode == 0

    # Check standard output.
    expectedStdout = getExpectedStdout()
    checkContentOfStd(expectedStdout, result.stdout, 'stdout')

    # Check standard error.
    expectedStderr = getExpectedStderr()
    checkContentOfStd(expectedStderr, result.stderr, 'stderr')
