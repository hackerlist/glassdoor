glassdoor
=========

Python API for Glassdoor.com

## Install

From source:
   
    $ clone https://github.com/hackerlist/glassdoor
    $ cd glassdoor
    $ sudo pip install -e .

From pip:

    $ sudo pip install glassdoor

## Use

    >>> from glassdoor import get
    >>> x = get('dropbox')
    >>> x.json()
    {"satisfaction": {"reviews": 1272, "score": [4.1], "%approval": 90}, "ceo": {"reviews": 492, "%approval": 95, "name": "Larry Page", "avatar": "http://media.glassdoor.com/people/ceo/9079/google-larry-page.jpg"}, "meta": {"connections": 909822, "website": "www.google.com", "name": "Google", "location": "Mountain View, CA"}, "salary": [{"position": "Software Engineer", "range": [50000, 275000], "samples": 2761, "mean": 112985}, {"position": "Senior Software Engineer", "range": [63000, 250000], "samples": 192, "mean": 145682}, {"position": "Software Engineer In Test", "range": [62000, 169000], "samples": 184, "mean": 100435}]}   
