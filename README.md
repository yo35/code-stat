Code Stat
=========

Count the number of code lines and comment lines on a set of source code files, and report the result.


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
Java       | `.java`
C/C++      | `.c` `.cpp` `.cxx` `.cc` `.h` `.hpp` `.hxx` `.hh` `.cu` `.cuh`
C#         | `.cs`
JavaScript | `.js` `.jsx` `.mjs`
TypeScript | `.ts` `.tsx` `.mts`
PHP        | `.php`
CSS        | `.css`
Python     | `.py`
Fortran 90 | `.f90`
SQL        | `.sql`
Pascal     | `.pas`

Only files having one of the above-mentionned extensions are analyzed.
