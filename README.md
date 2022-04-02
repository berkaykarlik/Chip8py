# Chip8py

Just a hobby project to learn basics of emulation.
It should be able to run chip-8 ROM's on pc when completed and debugged.
Warning: I'm still working on bug fixes, see issues for known bugs.

### Installation
* `git clone --recursive https://github.com/berkaykarlik/CHIP-8-interpreter.git`
* Optional but recommended: `python -m venv venv`
* `pip install -r requirements.txt`

### Running

* Run this command from the root (top level) of this repo:
`python main.py path_to_ROM_file`

* if you clonned the repo recursively, as described in installation steps, roms are under: `roms\chip8Archive\roms`

### Keys

|   |   |   |   |   |
|---|---|---|---|---|
| 1 | 2 | 3 | 4 |   |
| q | w | e | r |   |
| a | s | d | f |   |
| z | x | c | v |   |
### Sources

These are the ones I used, many thanks to:

* Tobias V. Langhoff, check out his [guide](https://tobiasvl.github.io/blog/write-a-chip-8-emulator/)
* Thomas P. Greene, check out cowgod's [guide](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM)
