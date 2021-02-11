#!/bin/sh

# Scripts adapted from Gist repo (https://gist.github.com/stefansundin/9059706)

# Install in current Git repo only

GIT_DIR=`git rev-parse --git-common-dir 2> /dev/null`

echo
echo

if [ "$GIT_DIR" == "" ]; then
  echo "This does not appear to be a git repo."
  exit 1
fi

if [ -f "$GIT_DIR/hooks/prepare-commit-msg" ]; then
  echo "There is already a prepare-commit-msg hook installed. Delete it first."
  echo
  echo "    rm '$GIT_DIR/hooks/prepare-commit-msg'"
  echo
  exit 2
fi

cp hooks/prepare-commit-msg "$GIT_DIR/hooks/prepare-commit-msg"

chmod +x "$GIT_DIR/hooks/prepare-commit-msg"

echo
echo "You're all set! Happy hacking!"

exit 0