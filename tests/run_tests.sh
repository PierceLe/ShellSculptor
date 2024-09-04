#!/bin/bash
TEST_DIR_PATH=~/Desktop/year-2/sem1/info1112/ass1/ShellSculptor/tests
PROGRAM_PATH=~/Desktop/year-2/sem1/info1112/ass1/ShellSculptor/mysh.py

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
TEST_NUMBER=1

for test_folder in "$TEST_DIR_PATH"/*/; do
    folder_name=$(basename "$test_folder")
    echo "Start running tests in $folder_name folder"

    # Loop over each .in file in the test folder
    for test_input_file in "$test_folder"/*.in; do
        echo "Start running test $TEST_NUMBER"

        # Define the paths for the output files
        expected_output_file="${test_input_file%.in}.out"  # Expected output file
        actual_output_file="${test_input_file%.in}.actual" # Actual output file

        # Run the commands in the .in file by feeding them to mysh.py and append output
        # Ensure --runtest flag is used to properly format output in test mode
        python3 $PROGRAM_PATH --runtest < "$test_input_file" > "$actual_output_file"

        # Compare the actual output with the expected output
        if diff -q "$actual_output_file" "$expected_output_file" > /dev/null; then
            echo "[PASS] Test $TEST_NUMBER"
        else
            echo "[FAIL] Test $TEST_NUMBER"
            echo "DIFF"
            diff -u "$expected_output_file" "$actual_output_file" | \
                        grep -vE '^(---|\+\+\+|@@)' | sed -n '/echo/,$p' | awk \
                        -v red="$RED" -v green="$GREEN" -v nc="$NC" \
                        '{
                            if ($1 ~ /^-/) {print red $0 nc}
                            else if ($1 ~ /^\+/) {print green $0 nc}
                            else {print $0}
                        }'
        fi

        TEST_NUMBER=$(expr $TEST_NUMBER + 1)
    done
done