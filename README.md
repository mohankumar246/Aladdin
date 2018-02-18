# Aladdin #


>Copyright (c) 2017-2018 Mohankumar Nekkarakalaya

>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

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
# install from PyPI read requirements.txt
pip install -r requirements.txt
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
