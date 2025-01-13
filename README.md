This is a python script I use to streamline starting and ending timewarrior
intervals.

Requirements:

- dmenu (or compatible replacement like wmenu)
- timewarrior
- dwmblocks & associated blockscript (optional)

Various parameters are configurable in the `config.json` file

- `data_dir` is where the script should look for timewarrior data; by default this is
  `~/.local/share/timewarrior/data/`
- `signal` is the value set in your status bar if you have a block script for
  timewarrior
- `threshold` cancels intervals less than x minutes.
