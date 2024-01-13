#!/bin/bash
python3 application.py && python3 inactive_application.py 
function handle_interrupt {
    echo "Script interrupted. Exiting..."
    exit 0
}
trap handle_interrupt SIGINT
