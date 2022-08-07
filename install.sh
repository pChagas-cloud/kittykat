#!/usr/bin/bash

mkdir bin
mkdir $HOME/$(whoami)/.config/todo-python/tasklist
cp main.py bin/kittykat
cp bin/kittykat $HOME/.local/bin/
