glassdoor
=========

Python API for Glassdoor.com

## Install

    $ clone https://github.com/hackerlist/glassdoor
    $ cd glassdoor
    $ sudo pip install -e .

## Use

    In [1]: from glassdoor import GETjson
    In [2]: x = GETjson('dropbox')
    In [3]: x
    Out[3]: 
    {'ceo': {'%approval': 100,
      'avatar': u'http://media.glassdoor.com/people/ceo/415350/dropbox-drew-houston.jpg',
      'name': u'Drew Houston',
      'reviews': 14},
     'connections': 382,
     'salary': {'mean': u'$112,688.00'},
     'satisfaction': {'%approval': 88, 'reviews': 16, 'score': 4.6}}
   
