# line-of-code
This is a Python script to count line of code under specified directory.

Borrow from https://code.activestate.com/recipes/580709-lines-of-code-loc/

* Author: Bob Yang
* Create Time: 2022-05-06
* Description:

Basic Lines-Of-Code counter in Python source files, reporting the
number of blank, comment and source code lines and total number of
lines in all java files scanned.

Usage example:

```
% python locs.py -rec ./Projects
343 *.java files in: ['D:\\projects\\Projects']
5868 blank (10.6%), 12843 comment (23.2%), 36728 source (66.2%), 49571 source+comment (89.4%), 55439 total lines
(0.241 secs, 229978 lines/sec)
Extract all src into ./all_src.txt

Scan multiple directory
% python3 locs.py -rec ./Projects ./Projects2
343 *.java files in: ['D:\\projects\\Projects']
5868 blank (10.6%), 12843 comment (23.2%), 36728 source (66.2%), 49571 source+comment (89.4%), 55439 total lines
(0.241 secs, 229978 lines/sec)
Extract all src into ./all_src.txt

Statistic line of code and extract all java source code to one big file './all_src.java'
% python locs.py -rec -ext ./Projects
343 *.java files in: ['D:\\projects\\Projects']
5868 blank (10.6%), 12843 comment (23.2%), 36728 source (66.2%), 49571 source+comment (89.4%), 55439 total lines
(0.241 secs, 229978 lines/sec)
Extract all src into ./all_src.txt

% python3 locs.py -h
usage: locs.py [-help] [-recurse] [-extract] [-verbose] <file_or_dir_name> ...
```

Tested with 64-bit Python 3.6 on Windows 10 only.
