#!/bin/bash
set -e  # stop on first error

echo "🔍 Listing input files..."
python3 scan_files.py

echo "🚀 Starting inference..."
python3 inference.py --data_dir /input --result_dir /output

echo "✅ Pipeline finished, results written to /output/result.json"
