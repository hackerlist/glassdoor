glassdoor
=========

Python API for Glassdoor.com

## Install

From source:
   
    $ clone https://github.com/hackerlist/glassdoor
    $ cd glassdoor
    $ sudo pip install .

From pip:

    $ sudo pip install glassdoor

## Use

    >>> from glassdoor import get
    >>> x = get('dropbox')
    >>> x
    {'ceo': {'%approval': 100,
             'avatar': 'http://media.glassdoor.com/people/ceo/415350/dropbox-drew-houston.jpg',
	     'name': 'Drew Houston',
             'reviews': 14},
     'meta': {'Competitors': 'Unknown',
              'Founded': 'Unknown',
              'Industry': 'Computer Software',
              'Type': 'Company - Private',
              'connections': 0,
              'location': 'San Francisco, CA',
              'name': 'Dropbox',
              'reviews': 16,
              'score': 4.6,
              'size': (None, None),
              'website': 'www.dropbox.com'},
              'salary': [{'mean': 112688,
                          'position': 'Software Engineer',
                          'range': (100000, 138000),
                          'samples': 4},
                         {'mean': 78912,
                          'position': 'Software Engineer',
                          'range': (69840, 87996),
                          'samples': 2},
                         {'mean': 60892,
                          'position': 'Technical Support Engineer',
                          'range': (56000, 66000),
                          'samples': 2}],
     'satisfaction': {'ratings': 16, 'score': 4.6}}
