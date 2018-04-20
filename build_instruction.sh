#! /bin/bash

docker build -f ./Dockerfile -t "python_for_analyis" .

docker run -it --rm -l "python for analysis" --dns=127.0.1.1 python:2.7-stretch bash

# To save the img run
docker save


docker run -it --rm python:2.7