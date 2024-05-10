This is a simple python script to streamline starting and ending timewarrior
intervals.

Requirements:

- dmenu
- timewarrior
- dwmblocks & associated blockscript (optional)

Various parameters are configurable in the `config.json` file

- `data_dir` is where timewarrior saves data; by default this is
  `~/.local/share/timewarrior/data/`
- `signal` is the value set in dwmblocks if you have a block script for 
  timewarrior
- `threshold` defines the minimum time since the start of an entry in
  minutes before the entry will be saved to the database.
