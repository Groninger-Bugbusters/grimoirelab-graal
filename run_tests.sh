#!/bin/bash


cd tests
coverage run --source=graal run_tests.py
