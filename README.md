Roster Genius takes your schedule from myPage and converts it into a nice .ics file for Calendar to use.

It is built in Python using Django, with a small bit of Javascript for the bookmarklet.

After shutting rostergeni.us down, I thought it would be best to release it's source code for others to use or run. The code isnt the best quality, nor is it the cleanest, but it's something. I don't intend on supporting or updating it much, but any pull requests are welcome.

## Getting started

To run this locally on your own computer, you'll first need a bit of setup (if you've done this before, feel free to skip) from Terminal:

```
cd ~
mkdir Development
cd Development
mkdir venvs
sudo easy_install pip
pip install virtualenv
virtualenv venvs/rostergenius
source ~/Development/venvs/rostergenius/bin/activate
```

Then download the roster genius source code and set it up:

```
git clone git@github.com:joshhunt/rostergenius.git
cd rostergenius
pip install -r requrements.txt
./manage.py syncdb
```

Assuming that completed without any errors, every time you want to start roster genius, run in Terminal:

```
source ~/Development/venvs/rostergenius/bin/activate
cd ~/Development/rostergenius
./manage.py runserver 0.0.0.0:8000
```
