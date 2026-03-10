#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Building executable..."
pyinstaller build.spec --clean

echo "Build complete! Executable located at: dist/PasswordManager"