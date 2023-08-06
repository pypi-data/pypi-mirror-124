# Tweets Cleaner

This package will help you and save your time for cleaning text data from twitter, let's dive in

```bash
pip3 install tweets_cleaner
```

or contribute to this project

```bash
git clone https://github.com/rizki4106/tweets_cleaner.git
```

## Features

This package can be remove any charater such as :

- punctuation
- emoji
- user
- retweet tags
- urls
- number
- white space

## Example

```python
from tweets_cleaner.helper import clean_tweets

# example tweets data
data = "Can’t wait to be in Genshin Impact Rolling on the 🤣"

# show the result
print(clean_tweets(data))
```
