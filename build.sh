#! /bin/bash

pyinstaller ./app.spec
cp .env ./dist/
cp README.md ./dist/
