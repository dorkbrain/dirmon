# dirmon
A simple Python script that can be run as a systemd service that can watch for file system changes inside a target directory and execute commands on create/modify/delete events.

# Requirements
This Python3 script requires the inotify package

`python3 -m pip install inotfiy`

# Command line
`dirmon.py --target <directory> --create <createscript> --modify <modifyscript> --delete <deletescript>`

# Arguments passed to scripts
|position|description|
|:---:|:---|
| Arg1 | Event Type (CREATE/MODIFY/DELETE) |
| Arg2 | Directory of object triggering the event |
| Arg3 | Filename of object triggering the change |
| Arg4 | Full path of the object triggering the change |