#!/bin/bash

run() {
    if ! pgrep -f $1; then
        $@ &
    fi
}

run picom
run dunst
$HOME/.config/conky/conky-min.sh &