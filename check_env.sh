#!/bin/bash
# Diagnostic script to check environment and application structure

echo "=== Environment Diagnostic Tool ==="
echo ""

echo "=== System Information ==="
uname -a
echo ""

echo "=== Current Working Directory ==="
pwd
echo ""

echo "=== Directory Listing ==="
ls -la
echo ""

if [ -d "./app" ]; then
    echo "=== App Directory Content ==="
    ls -la ./app
    
    if [ -f "./app/main.py" ]; then
        echo ""
        echo "=== app/main.py exists! ==="
    else
        echo ""
        echo "ERROR: app/main.py not found!"
    fi
    
    if [ -d "./app/core" ]; then
        echo ""
        echo "=== App Core Directory Content ==="
        ls -la ./app/core
    else
        echo ""
        echo "ERROR: app/core directory not found!"
    fi
else
    echo ""
    echo "ERROR: app directory not found!"
fi

echo ""
echo "=== Environment Variables ==="
env | grep -v PATH | sort
echo ""

echo "=== Python Version ==="
python --version
echo ""

echo "=== Installed Python Packages ==="
pip list
echo ""

echo "=== Network Info ==="
netstat -tuln
echo ""

echo "=== Diagnostic Complete ===" 