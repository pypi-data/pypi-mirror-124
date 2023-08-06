#!/bin/bash


rm -fr dist/*
python setup.py bdist_wheel
pip install --force-reinstall dist/pyftdc-0.0.10-cp39-cp39-macosx_11_0_x86_64.whl
#pip install --force-reinstall dist/pyftdc-0.0.8-cp38-cp38-linux_x86_64.whl
