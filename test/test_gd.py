import unittest
import os
import glassdoor

stdkeys = ['satisfaction', 'meta']

class TestGD(unittest.TestCase):

    def test_getjson(self):
        g = glassdoor.get('dropbox')
        print g
        try:
            self.assertTrue(all([k in g.keys() for k in stdkeys]),
                            'Missing Keys')
        except Exception as e:
            raise Exception('GETjson failed: %s' % e)
        
