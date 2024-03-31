#!/usr/bin/env python3
### TODO: Make script calls async/non-blocking???
import os
import sys
import inotify.adapters
import logging
import argparse
import subprocess

# Function to start watching a directory for changes
def watch_directory(directory, log, scripts):
  notify = inotify.adapters.Inotify()
  notify.add_watch(directory)
  log.info(f"Watching {directory} for changes")

  try:
    # Use the event_gen context manager to continue to read results
    for event in notify.event_gen():
      # Make sure the event variable is set to something
      if event is not None:
        (_, type_names, path, filename) = event
        fullPath = os.path.join(path, filename)
        # Check for create events
        if "IN_CREATE" in type_names:
          log.info(f"File created: {fullPath}")
          # Check if we were given a script for this event, if so then execute it
          if scripts['create'] is not None:
            script = f"{scripts['create']} CREATE {fullPath}"
            log.info(f"Executing: {script}")
            log.info(subprocess.getoutput(script))

        # Check for delete events
        if "IN_DELETE" in type_names:
          log.info(f"File deleted: {fullPath}")
          # Check if we were given a script for this event, if so then execute it
          if scripts['delete'] is not None:
            script = f"{scripts['delete']} DELETE {fullPath}"
            log.info(f"Executing: {script}")
            log.info(subprocess.getoutput(script))

        # Check for modify events
        if "IN_MODIFY" in type_names:
          log.info(f"File modified: {fullPath}")
          # Check if we were given a script for this event, if so then execute it
          if scripts['modify'] is not None:
            script = f"{scripts['modify']} MODIFY {fullPath}"
            log.info(f"Executing: {script}")
            log.info(subprocess.getoutput(script))
  finally:
    # We've exited the context manager loop at this point so stop watching the directory
    notify.remove_watch(directory)

# Main entry point
if __name__ == "__main__":
  # Setup the arg parser
  parser = argparse.ArgumentParser(description="Export CP policy as CSV")
  parser.add_argument("-t", "--target", type=str, required=True,  help="Full path of the directory to monitor for changes.")
  parser.add_argument("-c", "--create", type=str, required=False, help="Script to run when objects are created.")
  parser.add_argument("-m", "--modify", type=str, required=False, help="Script to run when objects are modified.")
  parser.add_argument("-d", "--delete", type=str, required=False, help="Script to run when objects are deleted.")
  parser.add_argument("-a", "--all",    type=str, required=False, help="Script to run when objects are created, modified, or deleted.")
  args = parser.parse_args()

  # Stuff scripts into a dict so that they can be overwritten by the --all argument
  scripts = {
    "create": args.create,
    "modify": args.modify,
    "delete": args.delete
  }

  # If --all is specified copy the script to all entries in the dict
  if args.all is not None:
    scripts["create"] = args.all
    scripts["modify"] = args.all
    scripts["delete"] = args.all

  # Commented the below code so that if no script is specified for an event then we'll only log the event and take no other action
  # if not (scripts["create"] or scripts["modify"] or scripts["delete"]):
  #   print("You must spcify at least one script to run when an event is triggered.")
  #   exit(1)

  # Change directory to script path so locations are relative to this script
  os.chdir(os.path.dirname(__file__))

  # Configure the logger to print to stdout and info level or above
  log = logging.getLogger('workdir')
  log.addHandler(logging.StreamHandler(sys.stdout))
  log.setLevel(logging.INFO)

  try:
    # Start watching the directory
    watch_directory(args.target, log, scripts)
  except KeyboardInterrupt:
    # Catch SIGINT or Ctrl+C
    log.info("\nCaught SIGINT/Ctrl+C, quitting...\n")
    sys.exit(0)
  except Exception as e:
    # Catch any unexpected exceptions
    log.error(f"Caught error: {e}")
    sys.exit(1)