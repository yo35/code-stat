#!/usr/bin/env python3

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
		print(''.join(['-' for i in range(len(self.title))]))
		print('Source files:       {:6d}'.format(self.fileCount))
		print('Code lines:         {:6d}'.format(self.codeLineCount))
		print('Comment lines:      {:6d}'.format(self.commentLineCount))
		if self.codeLineCount == 0:
			print('Comment/code ratio:      - %')
		else:
			print('Comment/code ratio: {:6.0f} %'.format(self.commentLineCount * 100 / self.codeLineCount))

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


counters = {
	'Java'       : LOCCounter('Java'),
	'C'          : LOCCounter('C/C++'),
	'CSharp'     : LOCCounter('C#'),
	'JavaScript' : LOCCounter('JavaScript'),
	'TypeScript' : LOCCounter('TypeScript'),
	'PHP'        : LOCCounter('PHP'),
	'CSS'        : LOCCounter('CSS'),
	'Python'     : LOCCounter('Python'),
	'Fortran'    : LOCCounter('Fortran'),
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
	'.ts'   : lambda file: processCLikeFile(counters['TypeScript'], file),
	'.tsx'  : lambda file: processCLikeFile(counters['TypeScript'], file),
	'.php'  : lambda file: processCLikeFile(counters['PHP'], file),
	'.css'  : lambda file: processCLikeFile(counters['CSS'], file, False),
	'.py'   : lambda file: processScriptFile(counters['Python'], file),
	'.f90'  : lambda file: processFortranFile(counters['Fortran'], file),
	'.sql'  : lambda file: processSqlFile(counters['SQL'], file),
}

toProcess = [os.path.abspath(f) for f in sys.argv[:0:-1]]
while len(toProcess) != 0:
	path = toProcess.pop()
	if os.path.isdir(path):
		toProcess.extend([os.path.join(path, f) for f in os.listdir(path)])
	elif os.path.isfile(path):
		filename, extension = os.path.splitext(path)
		if extension in extensionToCounter:
			extensionToCounter[extension](path)

for counter in counters.values():
	if not counter.isEmpty():
		counter.printStats()
		print()