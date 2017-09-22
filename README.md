# Nepal Idol Auto Voter

This script is a PoC for auto-voting using a list of names and using one of the [disposable mail
providers](http://mailnesia.com/). This script was not used for misusing the voting but was built for PoC.
I was voting for Menuka Paudel at that time but this was not used for auto-voting (well maybe 5 votes or so).

I don't think this works any longer but am keeping this as a reference for people who might be interested to take a look
at. The way voting worked changed later and which I believe was still misusable, I didn't have time and motivation to pursue anymore.

### Setup

- clone this repo
- `pip install -r requirements.txt`
- update `nepali-names.txt` to include as many names as possible. One source is to use [nepali-names](https://github.com/techgaun/nepali-names)
- `python vote.py`
- Note: This is heavily untested code

### Author

- [techgaun](https://github.com/techgaun)
