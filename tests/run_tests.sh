#!/bin/bash
TEST_DIR_PATH=~/Desktop/year-2/sem1/info1112/ass1/ShellSculptor/tests
PROGRAM_PATH=~/Desktop/year-2/sem1/info1112/ass1/ShellSculptor/mysh.py

# Color codes
RED='\033[0;31m'   # Red for incorrect output (.actual)
GREEN='\033[0;32m' # Green for missing correct output (.out)
WHITE='\033[0;37m'  # White for neutral terminal output
NC='\033[0m'  # No color

# Find total test cases
TOTAL_TESTS=$(find "$TEST_DIR_PATH" -type f -name "*.in" | wc -l | tr -d ' ')
CURRENT_TEST=1
PASSED_TESTS=0

# Run tests
for test_folder in "$TEST_DIR_PATH"/*/; do
    folder_name=$(basename "$test_folder" | sed -e 's/_/ /g' -e 's/\b\(.\)/\u\1/g')
    for test_input_file in "$test_folder"/*.in; do
        file_name=$(basename "$test_input_file" .in | sed -e 's/_/ /g' -e 's/\b\(.\)/\u\1/g')

        echo -ne "${WHITE}Test $CURRENT_TEST: [$folder_name]: $file_name ...${NC}"

        # Define paths for expected and actual outputs
        expected_output_file="${test_input_file%.in}.out"
        actual_output_file="${test_input_file%.in}.actual"

        # Run the program and capture the output
        python3 "$PROGRAM_PATH" --runtest < "$test_input_file" > "$actual_output_file"

        # Compare the actual output with the expected output
        if diff -q "$actual_output_file" "$expected_output_file" > /dev/null; then
            echo -e " ${GREEN}v${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            echo -e " ${RED}X${NC}"
            echo -e "${WHITE}Differences:${NC}"

            # Show differences in color, green for missing lines and red for incorrect lines
            diff -u "$expected_output_file" "$actual_output_file" | grep -vE '^(---|\+\+\+|@@)' | \
            awk -v red="$RED" -v green="$GREEN" -v nc="$NC" \
                '{if ($1 ~ /^-/) {sub(/^./, "+", $0); print green $0 nc} else if ($1 ~ /^\+/) {sub(/^./, "-", $0); print red $0 nc}}'
        fi

        CURRENT_TEST=$((CURRENT_TEST + 1))
    done
done


# Summary
if [ "$PASSED_TESTS" -eq "$TOTAL_TESTS" ]; then
    echo -e "${GREEN}Test completed: $PASSED_TESTS/$TOTAL_TESTS${NC}"
else
    echo -e "${RED}Test completed: $PASSED_TESTS/$TOTAL_TESTS${NC}"
fi