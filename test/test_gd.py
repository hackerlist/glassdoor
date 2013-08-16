import unittest
import os
import glassdoor

stdkeys = ['ceo', 'salary', 'satisfaction', 'connections']

class TestGD(unittest.TestCase):

    def test_getjson(self):
        gd = glassdoor.parse(glassdoor.get('dropbox'))
        try:
            self.assertTrue(all([k in gd.keys() for k in stdkeys]),
                            'Missing Keys')
        except Exception as e:
            raise Exception('GETjson failed: %s' % e)
        
