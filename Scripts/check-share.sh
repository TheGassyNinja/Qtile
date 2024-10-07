#!/bin/bash

file="$HOME/Projects/Share/"

if [ -d "$file" ]; then
    echo -e "\n󰡰 "
else
    echo -e "\n󰱟 "
    notify-send -u critical "\nShare not mounted"
fi