#!/usr/bin/env python3
################################################################################
#                                                                              #
#   This script computes line of code metrics on a set of source code files.   #
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

# Usage:
#
#   python3 code-stat.py <file-or-folder-1> [<file-or-folder-2> [<file-or-folder-3> ...]]
#
# Count the number of source code files passed in argument of the script, and the number of code lines
# and comment lines they contain. If a folder is passed in argument of the script, all its content is
# analyzed, including recursively the content of its child folders, grandchild folders, etc...


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


def processCLikeFile(locCounter, file, allowCPPSingleLineComment=True):
	"""
	Process a file with C/C++-like comments (i.e. // for single line comments, /* ... */ for block comments).
	"""

	locCounter.fileCount += 1
	with open(file, 'r') as f:
		withinBlockComment = False
		withinHeader = True
		for line in f:
			line = line.strip()

			# Blank line
			if len(line) == 0:
				if not withinBlockComment:
					withinHeader = False
				continue

			# Within a block comment
			if withinBlockComment:
				if not withinHeader:
					locCounter.commentLineCount += 1
				if '*/' in line:
					withinBlockComment = False

			# Regular code
			else:
				if re.search('^/[/*]' if allowCPPSingleLineComment else '^/\*', line):
					if not withinHeader:
						locCounter.commentLineCount += 1
				else:
					withinHeader = False
					locCounter.codeLineCount += 1
				if '/*' in line and not '*/' in line:
					withinBlockComment = True


def processSingleLineCommentFile(locCounter, file, commentCharacter):
	"""
	Process a file that have only single line comments. 
	"""

	locCounter.fileCount += 1
	with open(file, 'r') as f:
		withinHeader = True
		for line in f:
			line = line.strip()

			# Blank line
			if len(line) == 0:
				withinHeader = False
				continue

			# Regular code
			if line.startswith(commentCharacter):
				if not withinHeader:
					locCounter.commentLineCount += 1
			else:
				withinHeader = False
				locCounter.codeLineCount += 1


def processScriptFile(locCounter, file):
	"""
	Process a file whose comments start with a hash character (#).
	"""
	processSingleLineCommentFile(locCounter, file, '#')


def processFortranFile(locCounter, file):
	"""
	Process a Fortran 90 file (comments start with an exclamation mark character).
	"""
	processSingleLineCommentFile(locCounter, file, '!')


def processSqlFile(locCounter, file):
	"""
	Process a SQL file (comments start with two hyphen characters).
	"""
	processSingleLineCommentFile(locCounter, file, '--')


if __name__ == '__main__':

	counters = {
		'Java'       : LOCCounter('Java'),
		'C'          : LOCCounter('C/C++'),
		'CSharp'     : LOCCounter('C#'),
		'JavaScript' : LOCCounter('JavaScript'),
		'TypeScript' : LOCCounter('TypeScript'),
		'PHP'        : LOCCounter('PHP'),
		'CSS'        : LOCCounter('CSS'),
		'Python'     : LOCCounter('Python'),
		'Fortran'    : LOCCounter('Fortran 90'),
		'SQL'        : LOCCounter('SQL'),
	}

	extensionToCounter = {
		'.java' : lambda file: processCLikeFile(counters['Java'], file),
		'.c'    : lambda file: processCLikeFile(counters['C'], file),
		'.cpp'  : lambda file: processCLikeFile(counters['C'], file),
		'.h'    : lambda file: processCLikeFile(counters['C'], file),
		'.hpp'  : lambda file: processCLikeFile(counters['C'], file),
		'.cu'   : lambda file: processCLikeFile(counters['C'], file),
		'.cuh'  : lambda file: processCLikeFile(counters['C'], file),
		'.cs'   : lambda file: processCLikeFile(counters['CSharp'], file),
		'.js'   : lambda file: processCLikeFile(counters['JavaScript'], file),
		'.jsx'  : lambda file: processCLikeFile(counters['JavaScript'], file),
		'.mjs'  : lambda file: processCLikeFile(counters['JavaScript'], file),
		'.ts'   : lambda file: processCLikeFile(counters['TypeScript'], file),
		'.tsx'  : lambda file: processCLikeFile(counters['TypeScript'], file),
		'.mts'  : lambda file: processCLikeFile(counters['TypeScript'], file),
		'.php'  : lambda file: processCLikeFile(counters['PHP'], file),
		'.css'  : lambda file: processCLikeFile(counters['CSS'], file, False),
		'.py'   : lambda file: processScriptFile(counters['Python'], file),
		'.f90'  : lambda file: processFortranFile(counters['Fortran'], file),
		'.sql'  : lambda file: processSqlFile(counters['SQL'], file),
	}

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
				if extension in extensionToCounter:
					extensionToCounter[extension](path)
		except Exception:
			errorCount += 1
			print('Error with {:s}'.format(path), file=sys.stderr)
	if errorCount > 0:
		print('{:d} error(s) encountered'.format(errorCount), file=sys.stderr)

	# Print the result.
	print()
	allCountersAreEmpty = True
	for counter in counters.values():
		if not counter.isEmpty():
			allCountersAreEmpty = False
			counter.printStats()
			print()
	if allCountersAreEmpty:
		print('No source code file found')
		print()
