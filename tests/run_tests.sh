#!/bin/bash

TEST_DIR_PATH=~/Desktop/year-2/sem1/info1112/ass1/ShellSculptor/tests
PROGRAM_PATH=~/Desktop/year-2/sem1/info1112/ass1/ShellSculptor/mysh.py

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
WHITE='\033[0;37m'
NC='\033[0m'


TOTAL_TESTS=$(find "$TEST_DIR_PATH" -type f -name "*.in" | wc -l | tr -d ' ')
CURRENT_TEST=1
PASSED_TESTS=0


capitalize() {
    echo "$1" | awk '{for(i=1;i<=NF;i++){$i=toupper(substr($i,1,1)) tolower(substr($i,2))}; print}'
}


# print actual and expected when test fail (Fail)
print_diff() {
    echo -e "${WHITE}DiFF:${NC}"

    # Show differences in color (green for missing lines and red for incorrect lines)
    diff -u "$1" "$2" | grep -vE '^(---|\+\+\+|@@)' | \
    awk -v red="$RED" -v green="$GREEN" -v nc="$NC" \
        '{if ($1 ~ /^-/) {sub(/^./, "+", $0); print green $0 nc} else if ($1 ~ /^\+/) {sub(/^./, "-", $0); print red $0 nc}}'

    echo -e "${WHITE}EXPECTED:${NC}"
    while IFS= read -r line; do
        echo -e "${WHITE}$line${NC}"
    done < "$1"

    echo -e "${WHITE}ACTUAL:${NC}"
    while IFS= read -r line; do
        echo -e "${WHITE}$line${NC}"
    done < "$2"
}

# Run tests
for test_folder in "$TEST_DIR_PATH"/*/; do
    folder_name=$(basename "$test_folder" | tr '_' ' ')
    folder_name=$(capitalize "$folder_name")  # Capitalize each word
    for test_input_file in "$test_folder"/*.in; do
        file_name=$(basename "$test_input_file" .in | tr '_' ' ')
        file_name=$(capitalize "$file_name")

        echo -ne "${WHITE}Test $CURRENT_TEST: [$folder_name]: $file_name ...${NC}"

        # Paths for expected and actual outputs
        expected_output_file="${test_input_file%.in}.out"
        actual_output_file="${test_input_file%.in}.actual"

        # Run the program and capture the output
        python3 "$PROGRAM_PATH" --runtest < "$test_input_file" > "$actual_output_file"

        # Compare outputs
        if diff -q "$actual_output_file" "$expected_output_file" > /dev/null; then
            echo -e " ${GREEN}v${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            echo -e " ${RED}X${NC}"
            print_diff "$expected_output_file" "$actual_output_file"
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