#!/bin/bash

pip install coveralls
gem install github-linguist -v 7.12.2
coverage run --source=graal run_tests.py
