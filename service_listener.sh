#!/bin/bash
pgrep -f "python tweemanager listener"
if [[ $? -ne 0 ]] ; then
        echo "Restarting cosa.py:     $(date)" >> /var/tmp/py_twee_man.log
        .env/bin/python tweemanager listener &
fi
