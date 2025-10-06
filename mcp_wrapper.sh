#!/bin/bash
cd "/Users/<add_your_folder_here>/terraform-test-mcp"
exec uv run python main.py "$@"