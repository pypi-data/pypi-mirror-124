#!/bin/bash
set -e

main() {
  build_distributions
  upload_distributions
}

build_distributions() {
  mkdir -p dist
  rm dist/*
  python setup.py sdist bdist_wheel
}

upload_distributions() {
  twine upload dist/* --skip-existing
}

main
