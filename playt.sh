#!/bin/bash

# Play agent against specified program
# Example:
# ./playt.sh ./agent.py "./src/lookt -d 1" 54321
# ./playt.sh ./agent.py "./src/lookt -d 2" 54322
# ./playt.sh ./agent.py "./src/lookt -d 3" 54323
# ./playt.sh ./agent.py "./src/lookt -d 4" 54324
# ./playt.sh ./agent.py "./src/lookt -d 5" 54325
# ./playt.sh ./agent.py "./src/lookt -d 6" 54326

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <player1> <player2> <port>" >&2
  exit 1
fi

./src/servt -p $3 & sleep 0.5
$1 -p $3 & sleep 0.5
$2 -p $3 
