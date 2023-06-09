#!/usr/bin/bash
pip install -r requirements.txt
echo "Starting install Style...."
cd ./assets/pyqt-stylesheets-master/pyqt-stylesheets-master
python setup.py build
python setup.py install

cd ../../..