Roster Genius takes your schedule from myPage and converts it into a nice .ics file for Calendar to use.

It is built in Python using Django, with a small bit of Javascript for the bookmarklet.

After shutting rostergeni.us down, I thought it would be best to release it's source code for others to use or run. The code isnt the best quality, nor is it the cleanest, but it's something. I don't intend on supporting or updating it much, but any pull requests are welcome.

## Getting started

To run this locally on your own computer, you'll first need a bit of setup (if you've done this before, feel free to skip) from Terminal. Copy and paste the lines without a hash, one at a time

```
# Move into your home folder
cd ~

# Create a folder called Development, and move into it
mkdir Development
cd Development

# Create a folder to contain [Python virtual envionments](http://www.virtualenv.org/en/latest/)
mkdir venvs

# Install the [Python package manager](https://pip.readthedocs.org/en/latest/) (its like the App store for Python programming)
sudo easy_install pip

# Install [virtualenv](http://www.virtualenv.org/en/latest/) for sandboxing
sudo pip install virtualenv

# Create a sandbox and activate a sandbox to run roster genius within
virtualenv venvs/rostergenius
source ~/Development/venvs/rostergenius/bin/activate
```

Then download the roster genius source code and set it up:

```
# Download roster genius. This may bring up a dialog to install the developer tools. Install them.
git clone git@github.com:joshhunt/rostergenius.git

# Move into the rostergenius folder
cd rostergenius

# Install the dependencies required by roster genius
pip install -r requrements.txt

# Create the roster genius database
./manage.py syncdb
```

Assuming that completed without any errors, every time you want to start roster genius, run in Terminal:

```
# Activate the roster genius sandbox
source ~/Development/venvs/rostergenius/bin/activate

# Move into the roster genius folder and start the server.
cd ~/Development/rostergenius
./manage.py runserver 0.0.0.0:8000
```


Once done, you can access roster genius at http://localhost:8000/
