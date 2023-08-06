#!/bin/bash

cmd='mkvirtualenv'

if $cmd 1>/dev/null 2>&1; then
    echo "Command is Yes."
else
    echo "Command is No."
fi

