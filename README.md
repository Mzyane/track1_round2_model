# DRYAD – Track 1 Farmland Segmentation

## Overview
This repository contains the Round 2 submission for the DRYAD team in the Gaofen Image Dataset competition.  
We focus on **Track 1 (Farmland)**, supporting **SDG 2 – Zero Hunger** by enabling farmland extraction and monitoring.

## Repository Structure

track1_round2_model/
├── .gitlab-ci.yml        # CI/CD pipeline config
├── Dockerfile            # Environment setup
├── requirements.txt      # Dependencies (pinned versions)
├── run.sh                # Entry point script
├── README.md             # Documentation
│
├── models/               # Trained weights
│   └── farmland.pth
│
├── inference.py          # Inference pipeline (reads /input, writes /output/result.json)
├── scan_files.py         # Helper to list input files
├── train.py              # Training script (local use only)
├── model.py              # UNet definition


## Input Format
The competition platform mounts the following into `/input`:
- `/input/test_point.csv`
- `/input/region_test/*.tiff`

## Output Format
The pipeline writes results to `/output/result.json`.  
Each entry contains:
- `filename`: image name
- `shape`: mask dimensions
- `unique_values`: pixel values present
- `valid`: compliance flag (True if 512×512 and values ∈ {0,1})

## Running Locally
To test before submission:
```bash
# Build Docker image
docker build -t dryad_track1 .

# Run container with mounted input/output
docker run --rm -v $(pwd)/sample_input:/input -v $(pwd)/sample_output:/output dryad_track1
"# track1_round2_model" 
