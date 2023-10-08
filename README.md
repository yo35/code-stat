Code Stat
=========

Count the number of code lines and comment lines on a set of source code files, and report the result.

[![Run tests](https://github.com/yo35/code-stat/actions/workflows/main.yml/badge.svg)](https://github.com/yo35/code-stat/actions/workflows/main.yml)


Install
-------

Just download [code-stat.py](code-stat.py). No extra package/file/dependency/stuff/... is required.


Usage
-----

```
python3 code-stat.py <file-or-folder-1> [<file-or-folder-2> [<file-or-folder-3> ...]]
```

Count the number of source code files passed in argument of the script, and the number of code lines
and comment lines they contain. If a folder is passed in argument of the script, all its content is
analyzed, including recursively the content of its child folders, grandchild folders, etc...


Supported languages
-------------------

Language   | File extensions
-----------|----------------
C/C++      | `.c` `.cpp` `.cxx` `.cc` `.h` `.hpp` `.hxx` `.hh`
C#         | `.cs`
CSS        | `.css`
CUDA       | `.cu` `.cuh`
Fortran 90 | `.f90`
Java       | `.java`
JavaScript | `.js` `.jsx` `.mjs`
Kotlin     | `.kt`
Pascal     | `.pas`
PHP        | `.php`
Python     | `.py`
SQL        | `.sql`
TypeScript | `.ts` `.tsx` `.mts`

Only files having one of the above-mentionned extensions are analyzed.
