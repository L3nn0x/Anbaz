#!/bin/bash

for file in tests/*.a; do
    echo -n -e "testing $file...\t"
    name="${file%.*}"
    frontend_output=$(python -m frontend $file)
    frontend_expected=$(<"$name.ir")
    if [ "$frontend_output" != "$frontend_expected" ]; then
        echo -e "\033[0;31mfrontend FAIL\033[0m"
        continue
    fi

    backend_output=$(cat "$name.ir" | python -m backend)
    backend_expected=$(<"$name.s")
    if [ "$backend_output" != "$backend_expected" ]; then
        echo -e "\033[0;31mbackend FAIL\033[0m"
        continue
    fi
    echo -e "\033[0;32mOK\033[0m"
done
