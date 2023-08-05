[![Build Status](https://api.travis-ci.com/eroberson/py_tweet_format.svg?branch=main)](https://travis-ci.org/eroberson/py_tweet_format)

# Python Tweet Formatter
Python tool for formatting a text file into a set of tweets.

## Installation
Use of virtual environments recommended.

```bash
pip install py_tweet_format
```

Or local user install:

```bash
pip install --user py_tweet_format
```

Or install from GitHub clone:

```bash
git clone https://github.com/eroberson/py_tweet_format.git
cd py_tweet_format
pip install .
```

## Usage
Take a text file input and parse into a set of tweets with default values for size of tweet and length of automatically shortened URLs. This will keep a tweet no larger than 280 characters, shorten URLs to 23 characters, remove extra spaces, remove newlines, and number the tweets.

```bash
py_tweet_format input_file.txt output_file.txt
```

Use a shorter limit of 140 instead of the default 280 character limit.

```bash
py_tweet_format --max_chunk_length 140 input_file.txt output_file.txt
```

Keep extra spaces and newlines from the origin text.

```bash
py_tweet_format --keep_extra_spaces --keep_newlines input_file.txt output_file.txt
```

Don't number tweets and use a different shortened URL length.

```bash
py_tweet_format --no_numbers --shortened_url_length 25 input_file.txt output_file.txt
```
