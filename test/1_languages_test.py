################################################################################
#                                                                              #
#   This file is part of Code Stat, a Python script to compute line of code    #
#   metrics on a set of source code files.                                     #
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
	processingFunction(counter, os.path.join(os.path.dirname(__file__), 'assets', 'languages', filename))
	return counter


def test_C():
	counter = computeLOCCounter('c.c', codeStat.processCFamilyFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 8
	assert counter.commentLineCount == 5


def test_CPlusPlus():
	counter = computeLOCCounter('cplusplus.cpp', codeStat.processCFamilyFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 8
	assert counter.commentLineCount == 5


def test_CSharp():
	counter = computeLOCCounter('csharp.cs', codeStat.processCFamilyFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 9
	assert counter.commentLineCount == 5


def test_CSS():
	counter = computeLOCCounter('css.css', codeStat.processCSSFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 3
	assert counter.commentLineCount == 1


def test_CUDA():
	counter = computeLOCCounter('cuda.cu', codeStat.processCFamilyFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 9
	assert counter.commentLineCount == 4


def test_Fortran90():
	counter = computeLOCCounter('fortran90.f90', codeStat.processFortranFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 14
	assert counter.commentLineCount == 5


def test_Java():
	counter = computeLOCCounter('java.java', codeStat.processCFamilyFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 9
	assert counter.commentLineCount == 5


def test_JavaScript():
	counter = computeLOCCounter('javascript.js', codeStat.processCFamilyFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 6
	assert counter.commentLineCount == 5


def test_Kotlin():
	counter = computeLOCCounter('kotlin.kt', codeStat.processCFamilyFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 7
	assert counter.commentLineCount == 5


def test_Pascal():
	counter = computeLOCCounter('pascal.pas', codeStat.processPascalFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 9
	assert counter.commentLineCount == 5


def test_PHP():
	counter = computeLOCCounter('php.php', codeStat.processPHPFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 6
	assert counter.commentLineCount == 4


def test_Python():
	counter = computeLOCCounter('python.py', codeStat.processScriptFamilyFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 7
	assert counter.commentLineCount == 2


def test_SQL():
	counter = computeLOCCounter('sql.sql', codeStat.processSQLFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 6
	assert counter.commentLineCount == 1


def test_TypeScript():
	counter = computeLOCCounter('typescript.ts', codeStat.processCFamilyFile)
	assert counter.fileCount == 1
	assert counter.codeLineCount == 4
	assert counter.commentLineCount == 4
