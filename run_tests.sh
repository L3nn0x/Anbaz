#!/bin/bash

for file in tests/*.a; do
    echo -n -e "testing $file...\t"
    frontend_output=$(python -m frontend $file)
    frontend_expected=$(<"$file.ir")
    if [ "$frontend_output" != "$frontend_expected" ]; then
        echo -e "\033[0;31mfrontend FAIL\033[0m"
        continue
    fi

    backend_output=$(cat "$file.ir" | python backend.py)
    backend_expected=$(<"$file.ir.s")
    if [ "$backend_output" != "$backend_expected" ]; then
        echo -e "\033[0;31mbackend FAIL\033[0m"
        continue
    fi
    echo -e "\033[0;32mOK\033[0m"
done
