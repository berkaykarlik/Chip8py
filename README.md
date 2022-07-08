# Chip8py

<p float="left">
<img src="../assets/invader.png?raw=true"  width="300" height="150" />
<img src="../assets/petdog.png?raw=true"  width="300" height="150"  />
</p>


Just a hobby project to learn basics of emulation.
It should be able to run chip-8 ROM's on pc when completed and debugged.
Warning: I'm still working on bug fixes, see issues for known bugs.

### Installation
* `git clone --recursive https://github.com/berkaykarlik/CHIP-8-interpreter.git`
* Optional but recommended: `python -m venv venv`
* Activate venv:
  * For windows run: `.\venv\Scripts\activate`
  * Linux or MacOS: `source ./venv/bin/activate`
* `pip install -r requirements.txt`

### Running

* If you followed the optional venv step, you need to activate venv whenever you open a new terminal.

* Run this command from the root (top level) of this repo:
`python main.py path_to_ROM_file`

* Roms under ``./roms` are tested and works... well mostly.

* if you clonned the repo recursively, as described in installation steps, There are roms from the archieve under: `roms\chip8Archive\roms`. However most of them won't work. I'm not sure why. They might be written for other chip8 versions.

### Keys
Every game has different set of controls, I mapped the 16 buttons to the keys in table below.
Relative order of keys is preserved.
|   |   |   |   |
|---|---|---|---|
| 1 | 2 | 3 | 4 |
| q | w | e | r |
| a | s | d | f |
| z | x | c | v |
### Sources

These are the sources I used, many thanks to:

* Tobias V. Langhoff, check out his [guide](https://tobiasvl.github.io/blog/write-a-chip-8-emulator/)
* Thomas P. Greene, check out cowgod's [guide](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM)


### Roms

I have included some roms I found as freeware from David Winter's site and chip8Archive repository.
See roms/README for links. I made no modifications and have no claims on them.
