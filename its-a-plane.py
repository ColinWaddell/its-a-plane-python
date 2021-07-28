#!/usr/bin/env python
# Display a runtext with double-buffering.
from display import Display


# Main function
if __name__ == "__main__":
    run_text = Display()
    if (not run_text.process()):
        run_text.print_help()
