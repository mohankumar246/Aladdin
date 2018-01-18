# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

This is for creating a crypto currency trading bot.

### How do I get set up? ###

- Install python 3.5, python-virtualenv and python-pip.
- Create a project directory and pull the source
- Setup a virtual env in the terminal:
# bootstrap virtualenv
export VIRTUAL_ENV=.virtualenv/aladdin
mkdir -p $VIRTUAL_ENV
virtualenv --python=/usr/bin/python3.5 $VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate
# install from PyPI
pip install krakenex
pip install gdax
pip install requests
pip install pprint

To deactivate the virtual env cmd in terminal:  deactivate

Run this command everytime:
source .virtualenv/aladdin/bin/activate

There will be a better way, soon. Something called brew automatically calls activate. Havent looked into it yet.


### Contribution guidelines ###

to do

### Who do I talk to? ###

talk to us