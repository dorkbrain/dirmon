# dirmon
A simple Python script that can be run as a systemd service that can watch for file system changes inside a target directory and execute commands on create/modify/delete events.

# Requirements
This Python3 script requires the inotify package

`python3 -m pip install inotfiy`

# Command line
`dirmon.py --target <directory> --create <createscript> --modify <modifyscript> --delete <deletescript> --all <allscript>`

# Arguments passed to scripts
|position|description|
|:---:|:---|
| Arg1 | Event Type (CREATE/MODIFY/DELETE) |
| Arg2 | Full path of the object triggering the change |

# Usage
```usage: dirmon.py [-h] -t TARGET [-c CREATE] [-m MODIFY] [-d DELETE] [-a ALL]

Monitor a directory for changes and execute scripts based on events

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Full path of the directory to monitor for changes.
  -c CREATE, --create CREATE
                        Script to run when objects are created.
  -m MODIFY, --modify MODIFY
                        Script to run when objects are modified.
  -d DELETE, --delete DELETE
                        Script to run when objects are deleted.
  -a ALL, --all ALL     Script to run when objects are created, modified, or deleted.```