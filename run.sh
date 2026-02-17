#!/bin/bash
# Quick start script for running the zombie simulation

echo "=== A Sim with Zombies in It ==="
echo "Setting up environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

# Run the simulation
echo "Starting simulation..."
python3 simulation.py
