# Aladdin #


##A crypto currency trading bot ##
This also a wrapper for the api calls of different exchanges.

Because different exchanges have their own set of calls to do trades or query info.

This makes it difficult to write a bot as an individual needs to spend time in reading their docs.

This uses the python libraries available for exchanges, unifies them to make it easier to write bots.

Currently supports gdax, kraken and bittrex.


### How do I get set up? ###

- Install python 3.5, python-virtualenv and python-pip.
- Create a project directory and pull the source
- Setup a virtual env in the terminal:

```bash
export VIRTUAL_ENV=.virtualenv/aladdin
mkdir -p $VIRTUAL_ENV
virtualenv --python=/usr/bin/python3.5 $VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate
# install from PyPI
pip install requests pprint krakenex gdax python-bittrex
```


To deactivate the virtual env cmd in terminal:  
```bash
deactivate
```

Run this command everytime:
```bash
source .virtualenv/aladdin/bin/activate
```

There will be a better way, soon. <br />
Something called brew automatically calls activate. Haven't looked into it yet.

To run tests:

Update the exchange keys.

Change your working directory to "tests" folder

Run a test case Ex: arbitrage_no_transfer.py.







### Contribution guidelines ###

to do

### Who do I talk to? ###
