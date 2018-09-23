# honorifics [![](https://img.shields.io/badge/python-3.5+-blue.svg)](https://docs.python.org/3.5/index.html)
Manages honorifics and timing quirks in subtitles.

## scripts/

Scripts can run by in-system Python. All scripts reads from stdin and output to stdout.

##### subtitles.py

Read line by line.
If in line is text between marks {\*}...{\*...} then swap it. 
Marks can be changed by providing arguments to class TextSwapperInMark constructor in script.

##### timing_offset.py

For SubStation Alfa (V4 & V4+) file. Optional argument: -fps

Read all input once as lines.
If in dialogue event line at the end of Text field is {+|- number cs|ms|frame|frames}  
e.g. `{+5 frames}` then shift accordingly Start and End time field.
Default frame rate is 23.976.

### Examples

`python3 ./scripts/subtitles.py < input > output`

`python3 ./scripts/timing_offset.py -fps 29.97 < input.ass > output.ass`

### Useful tools

[Meld](http://meldmerge.org/)

## Developing notes

For developing purposes it is recommended to use [virtual environments](https://docs.python.org/3.6/library/venv.html).

Code in `honorifics/` should be covered by tests. Type hinting is preferred. [PEP 8](https://www.python.org/dev/peps/pep-0008/) to style.