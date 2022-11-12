#!/usr/bin/env bash
# Filename: dnc.sh
cd ~/prog/vDNC/bin &&
source activate &&
cd ~/prog/dnc

if [[ $1 = 'run' ]]
then
  python manage.py runserver
fi

if [[ $1 = 'pull' ]]
then
  git pull
fi
