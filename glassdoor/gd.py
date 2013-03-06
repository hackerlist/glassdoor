import requests
from BeautifulSoup import BeautifulSoup
from utils import intify, tryelse
from functools import partial
import json

def get(company):
    """Performs a HTTP GET for a glassdoor page and returns
    BeautifulSoup with a .json() method
    """
    params = 'clickSource=searchBtn&typedKeyword=&sc.keyword=%s' % company
    r = requests.get('http://www.glassdoor.com/GD/Reviews/company-reviews.htm?' + params)
    soup = BeautifulSoup(r.content)
    soup.json = partial(parse, soup, raw=True)
    return soup

def parse_meta(soup):
    return {'connections': tryelse(lambda: intify(soup.findAll('div', {'id': 'OverviewInsideConnections'})[0]\
                                              .findAll('tt', {'class': 'notranslate'})[0].text), 0),
            'website': tryelse(lambda: soup.findAll('span', {'class': 'website notranslate'})[0].text, ''),
            'name': tryelse(lambda: soup.findAll('tt', {'class': 'i-emp'})[0].text, ''),
            'location': tryelse(lambda: soup.findAll('span', {'class': 'i-loc'})[0].text, ''),
            }

def parse_satisfaction(soup):
    """
    """
    _soups = soup.findAll('div', {'class': 'employerSatisfaction'})
    _data = {'reviews': 0,
             'score': None,
             '%approval': None,
             }
    if _soups:
        _soup = _soups[0]
        _data['reviews'] = tryelse(lambda: intify(soup.findAll('span', {'itemprop': 'reviewCount'})[0].text), _data['reviews'])
        _data['score'] = tryelse(lambda: float(soup.findAll('span', {'class': 'ratingValue notranslate '})[0].text), _data['score']),
        _data['%approval'] = tryelse(lambda: intify(soup.findAll('span', {'class': 'minor gdrHigh'})[0]\
                                                        .findAll('tt', {'class': 'notranslate'})[0].text), _data['%approval'])
    return _data

def parse_ceo(soup):
    _soups = soup.findAll('div', {'class': 'ceoRating cf'})
    _data = {'reviews': 0,
             '%approval': None,
             'avatar': '',
             'name': ''
             }
    if _soups:
        _soup = _soups[0]
        _data['name'] = _soup.findAll('h4', {'class': 'ceoName notranslate'})[0].text
        _data['reviews'] = intify(_soup.findAll('span', {'class': 'numCEORatings minor'})[0].findAll('tt', {'class': 'notranslate'})[0].text)
        _data['avatar'] = _soup.findAll('img', {'class': 'headshot photo'})[0]['src']
        _data['%approval'] = intify(_soup.findAll('span', {'class': 'approvalPercent'})[0].findAll('tt', {'class': 'notranslate'})[0].text)
    return _data

def parse_salary(soup):
    _soups = soup.findAll('table', {'id': 'SalaryChart'})
    _data = []
    if _soups:
        _soup = _soups[0]
        for row in _soup.findAll('tr')[1:]:
            try:
                _data.append({'position': row.findAll('tt', {'class': 'i-occ'})[0].text,
                              'samples': intify(row.findAll('p', {'class': 'rowCounts'})[0].findAll('tt')[0].text),
                              'mean': intify(row.findAll('td', {'class': 'mean'})[0].findAll('span', {'class': 'minor'})[0].text),
                              'range': (intify(row.findAll('div', {'class': 'lowValue'})[0].text) * 1000,
                                        intify(row.findAll('div', {'class': 'highValue'})[0].text) * 1000)
                              })
            except Exception as e:
                print e
    return _data

def parse(soup, raw=False):
    """
    """
    data = {'satisfaction': parse_satisfaction(soup),
            'ceo': parse_ceo(soup),
            'meta': parse_meta(soup),
            'salary': parse_salary(soup)
            }
    if raw:
        return json.dumps(data)
    return data
