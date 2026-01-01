################################################################################
#                                                                              #
#   This file is part of Code Stat, a Python script to compute line of code    #
#   metrics on a set of source code files, for several programming languages.  #
#   Copyright (C) 2023-2026  Yoann Le Montagner <yo35 -at- melix.net>          #
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


import importlib
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
codeStat = importlib.import_module('code-stat')


def computeLOCCounter(filename, processingFunction):
    """
    Analyze the file corresponding to the given filename with the given processing function
    (which must be one of the codeStat.process***File(..) function), and return a LOCCounter object
    with the LOC stats collected on the file.
    """
    counter = codeStat.LOCCounter('Testing')
    processingFunction(counter, os.path.join(os.path.dirname(__file__), 'assets', 'samples', filename))
    return counter


def test_blank_before_first_block_comment():
    counter = computeLOCCounter('blank_before_first_block_comment.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 3
    assert counter.commentLineCount == 4


def test_blank_before_first_line_comment():
    counter = computeLOCCounter('blank_before_first_line_comment.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 3
    assert counter.commentLineCount == 2


def test_blank_within_file_header():
    counter = computeLOCCounter('blank_within_file_header.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 3
    assert counter.commentLineCount == 0


def test_no_blank_after_first_comment():
    counter = computeLOCCounter('no_blank_after_first_comment.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 3
    assert counter.commentLineCount == 5


def test_code_after_block_comment():
    counter = computeLOCCounter('code_after_block_comment.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 2
    assert counter.commentLineCount == 1


def test_mixing_block_comment_and_code_1():
    counter = computeLOCCounter('mixing_block_comment_and_code_1.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 3
    assert counter.commentLineCount == 2


def test_mixing_block_comment_and_code_2():
    counter = computeLOCCounter('mixing_block_comment_and_code_2.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 3
    assert counter.commentLineCount == 1


def test_mixing_block_comment_and_code_3():
    counter = computeLOCCounter('mixing_block_comment_and_code_3.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 3
    assert counter.commentLineCount == 3


def test_mixing_block_comment_and_code_4():
    counter = computeLOCCounter('mixing_block_comment_and_code_4.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 3
    assert counter.commentLineCount == 2


def test_nested_block_comment_1():
    counter = computeLOCCounter('nested_block_comment_1.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 4
    assert counter.commentLineCount == 1


def test_nested_block_comment_2():
    counter = computeLOCCounter('nested_block_comment_2.cpp', codeStat.processCFamilyFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 3
    assert counter.commentLineCount == 2


def test_Fortran_compiler_directives():
    counter = computeLOCCounter('compiler_directives.f90', codeStat.processFortranFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 5
    assert counter.commentLineCount == 0


def test_Pascal_compiler_directives_with_braces():
    counter = computeLOCCounter('compiler_directive_braces.pas', codeStat.processPascalFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 4
    assert counter.commentLineCount == 0


def test_Pascal_compiler_directives_with_parentheses():
    counter = computeLOCCounter('compiler_directive_parentheses.pas', codeStat.processPascalFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 4
    assert counter.commentLineCount == 0


def test_Pascal_compiler_directives_with_slashes():
    counter = computeLOCCounter('compiler_directive_slashes.pas', codeStat.processPascalFile)
    assert counter.fileCount == 1
    assert counter.codeLineCount == 3
    assert counter.commentLineCount == 1
