## What it does

**SimpleFileOrganizer** is a simple script that, if placed inside a folder and executed, can categorize each file inside it, by following the rules of a "paths" JSON dictionary file (placed in the same folder).

## Usage

Run the script in the command line, like
```
python file_org.py -pd
``` 
a prompt will be received before moving the files in their "category" folder (e.g mp4 will be moved to Video, mp3 to Music, etc, just change the JSON as much as you want).
You can add a ``` -pd ``` argument while calling to print directories.

## Notes/Bugs

Currently it only works with the current program directory, but I'm planning to extend this to subdirectories.