#!/bin/bash
project_dir="$( cd "$( dirname "$0" )" && pwd)"
mkdir -p "$project_dir/logs"
"$project_dir/.venv/bin/python" "$project_dir/src/etl_pipeline.py" >> "$project_dir/logs/etl.log" 2>&1
