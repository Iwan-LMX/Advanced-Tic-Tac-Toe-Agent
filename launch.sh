#!/bin/bash

# Initialize variables
port=32345

# Function to calculate and display the win rate
calculate_and_print_win_rate() {
  local win_count=$1
  local total_runs=$2
  local dep=$3
  
  if [ $total_runs -gt 0 ]; then
    local win_rate=$(echo "scale=2; $win_count * 100 / $total_runs" | bc)
    echo "Temporary win rate for department $dep after $total_runs runs: $win_rate%"
  else
    echo "No games have been run for department $dep."
  fi
}

# Loop through departments 1 to 11
for dep in {4..11}; do
  win_count=0
  total_runs=0

  # Each department should run 100 times
  for (( i=1; i<=100; i++ )); do
    # Run the command and capture the output
    output=$(./playt.sh "./dumbIwan/AlphaBeta.py" "./src/lookt -d $dep" $port)
    last_line=$(echo "$output" | tail -n 1)

    # Increment total runs
    ((total_runs++))
    
    # Check the last line and count wins
    if [[ "$last_line" == "Yay!! We win!! :)" ]]; then
      ((win_count++))
    fi

    # Calculate and print the win rate every 10 runs
    if (( i % 10 == 0 )); then
      calculate_and_print_win_rate $win_count $total_runs $dep
    fi

    # Increment port for the next run
    ((port++))
  done

  # Calculate and print final win rate for this department
  echo "Final win rate for department $dep:"
  calculate_and_print_win_rate $win_count $total_runs $dep
done