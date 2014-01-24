#-*- coding: utf-8 -*-

"""
    glassdoor
    ~~~~~~~~~
    Glassdoor unofficial API

    :copyright: (c) 2012 by Hackerlist, Inc
    :license: BSD, see LICENSE for more details.
"""

import json
import requests
from functools import partial
from BeautifulSoup import BeautifulSoup
from utils import intify, tryelse

GLASSDOOR_API = 'http://www.glassdoor.com/Reviews'

def get(company='', company_slug=''):
    """Performs a HTTP GET for a glassdoor page and returns json"""
    if not company and not company_slug:
        raise Exception("glassdoor.gd.get(company='', company_uri=''): "\
                            " company or company_uri required")
    params = 'clickSource=searchBtn&typedKeyword=&sc.keyword=%s' % company \
        if not company_slug else ''
    api_uri = company_slug or 'company-reviews.htm'
    url = '%s/%s?%s' % (GLASSDOOR_API, api_uri, params)
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    return parse(soup)

def parse_meta(soup):
    data = {'website': '',
            'name': '',
            'location': '',
            'logo': '',
            'connections': None,
            'reviews': None,
            'score': None,
            }

    def _reviews(soup):
        selector_outer = {'class': 'numReviews subtle'}
        selector = {'class': 'txtShadowWhite'}
        reviews_outer = soup.findAll('span', selector_outer)[0]
        reviews = reviews_outer.findAll('span', selector)[0]
        return intify(reviews.text)

    def _score(soup):
        selector = {'class': 'h2 tightVert tightHorz notranslate'}
        score = soup.findAll('span', selector)[0].findAll('strong')[0]
        return float(score.text)

    def _details(soup):
        details = {}
        soup = soup.findAll('div', {'id': 'InfoDetails'})
        if soup:
            metas = soup[0].findAll('div', {'class': 'empInfo cf'})
            for meta in metas:
                label = str(meta.findAll('label')[0].text)
                value = str(meta.findAll('span')[0].text)
                details[label] = value
        return details

    def _connections(soup):
        selector_div = {'id': 'OverviewInsideConnections'}
        selector_tt = {'class': 'notranslate'}
        connections_div = soup.findAll('div', selector_div)
        connections_tt = connections_div[0].findAll('tt', selector_tt)
        connections = connections_tt[0].text
        return intify(connections)

    def _logo(soup):
        selector = {'class': 'sqLogo tighten medSqLogo'}
        logo = soup.findAll('span', selector)[0].findAll('img')[0]['src']
        return logo

    def _website(soup):
        selector = {'class': 'website notranslate txtShadowWhite'}
        website = soup.findAll('span', selector)[0].text
        return website

    def _name(soup):
        selector = {'class': 'i-emp'}
        name = soup.findAll('tt', selector)[0].text
        return name

    def _location(soup):
        location = soup.findAll('span', {'class': 'value i-loc'})[0].text
        return location

    def _size(soup):
        selector_div = {'class': 'moreData margTop5 subtle'}
        selector = {'class': 'notranslate'}
        size_div = soup.findAll('div', selector_div)[0]
        sizes = size_div.findAll('tt', selector)
        return [intify(size.text) for size in sizes]

    data['connections'] = tryelse(partial(_connections, soup), default=0)
    data['website'] = tryelse(partial(_website, soup), default='')
    data['name'] = tryelse(partial(_name, soup), default='')
    data['location'] = tryelse(partial(_location, soup), default='')
    data['size'] = tryelse(partial(_size, soup), default=[None, None])
    data['reviews'] = tryelse(partial(_reviews, soup), default=None)
    data['logo'] = tryelse(partial(_logo, soup), default=None)
    data['score'] = tryelse(partial(_score, soup), default=None)
    data.update(_details(soup))
    return data

def parse_satisfaction(soup):
    """
    """
    data = {'ratings': 0,
            'score': None,
            }

    def _ratings(soup):
        """Number of times this company has been rated by employees"""
        ratings = soup.findAll('h3')[0]
        selector = {'class': 'notranslate'}
        ratings = ratings.findAll('span', selector)[0]
        return intify(ratings.text.strip())

    def _score(soup):                            
        selector = {'class': 'gdRatingValueBar gdrHighmed'}
        score = soup.findAll('span', selector)[0]
        return float(score.text)

    _soups = soup.findAll('div', {'id': 'EmployerRatings'})

    if _soups:
        _soup = _soups[0]
        data['ratings'] = tryelse(partial(_ratings, _soup),
                                  default=data['ratings'])
        data['score'] = tryelse(partial(_score, _soup),
                                default=data['score'])
    return data

def parse_ceo(soup):
    data = {'reviews': 0,
            '%approval': None,
            'avatar': '',
            'name': ''
            }

    def _name(soup):
        selector = {'class': 'ceoName notranslate'}
        return soup.findAll('h4', selector)[0].text

    def _reviews(soup):
        selector_span = {'class': 'numCEORatings minor'}
        selector_tt = {'class': 'notranslate'}        
        reviews_span = soup.findAll('span', selector_span)[0]
        reviews_tt = reviews_span.findAll('tt', selector_tt)[0]
        reviews = reviews_tt.text
        return intify(reviews)

    def _avatar(soup):
        selector_div = {'id': 'CEOHeadShot'}
        avatar_div = soup.findAll('div', selector_div)[0]
        avatar = avatar_div.findAll('img')[0]
        return avatar['src']

    def _approval(soup):
        selector_span = {'class': 'approvalPercent'}
        selector_tt = {'class': 'notranslate'}
        approval_span = soup.findAll('span', selector_span)[0]
        approval_tt = approval_span.findAll('tt', selector_tt)[0]
        approval = approval_tt.text
        return intify(approval)

    _soups = soup.findAll('div', {'class': 'ceoRating cf'})
    if _soups:
        _soup = _soups[0]
        data['name'] = tryelse(partial(_name, _soup),
                               default='')
        data['reviews'] = tryelse(partial(_reviews, _soup),
                                  default=0)
        data['avatar'] = tryelse(partial(_avatar, _soup),
                                 default='')
        data['%approval'] = tryelse(partial(_approval, _soup),
                                    default=None)
    return data

def parse_salary(soup):
    data = []

    def _samples(soup):
        selector = {'class': 'rowCounts'}
        rows = soup.findAll('p', selector)[0]
        samples = rows.findAll('tt')[0].text
        return intify(samples)

    def _position(soup):
        selector = {'class': 'i-occ'}
        position_tt = soup.findAll('tt', selector)[0]
        position = position_tt.text
        return position

    def _mean(soup):
        """Calculates the mean of this row and return an indicator for
        the period, i.e. whether its for a monthly period, as opposed
        to yearly.
        """
        selector_td = {'class': 'mean'}
        selector_span = {'class': 'minor'}
        mean_td = soup.findAll('td', selector_td)[0]
        mean_span = mean_td.findAll('span', selector_span)[0]
        mean = mean_span.text
        monthly = True if "mo" in mean else False
        mean = intify(mean) * 12 if monthly else intify(mean)
        return mean, monthly

    def _range(soup):
        selector_low = {'class': 'lowValue'}
        selector_high = {'class': 'highValue'}
        low = row.findAll('div', selector_low)[0].text
        high = row.findAll('div', selector_high)[0].text
        return low, high

    def _normalize(range_, monthly):
        """nomalize: multiply ranges by # months or by $1k"""
        period = 12 if monthly else 1000
        low, high = (intify(v) * period for v in range_)
        return low, high

    _soups = soup.findAll('table', {'id': 'SalaryChart'})
    if _soups:
        _soup = _soups[0]
        for row in _soup.findAll('tr')[1:]:
            try:
                mean, monthly = _mean(row)
                low, high = _normalize(_range(row), monthly)
                data.append({'position': _position(row),
                             'samples': _samples(row),
                             'mean': mean,
                             'range': (low, high)
                             })
            except Exception as e:
                print e
    return data

def parse_suggestions(soup):
    def _suggestions(soup):
        """Suggests similar/related companies to query"""
        selector_id = {'id': 'SearchResults'}
        selector_h3 = {'class': 'tightTop'}
        companies_div = soup.findAll('div', selector_id)[0]
        companies = companies_div.findAll('h3', selector_h3)
        suggestions = [company.text for company in companies]
        return suggestions

    return {'error': 'company not found',
            'suggestions': _suggestions(soup)
            }

def direct_match(soup):
    """Predicate which answers whether an exact company match is found
    or whether there are suggestions."""
    return not soup.findAll('div', {'class': 'sortBar'})

def exact_match(soup):
    """Predicate which answers whether an exact match exists. If an
    exact match exists, company's uri is returned. Assumes if there
    are multiple 'exact matches' that the first is correct.

    usage:
        >>> exact_match(soup)
        
    """
    selector_suggestions = {'class': 'companyData'}
    selector_exact = {'class' : 'chickletExactMatch chicklet'}

    suggestions = soup.findAll('div', selector_suggestions)
    if suggestions:
        top_suggestion = suggestions[0]
        if top_suggestion.findAll('i', selector_exact):
            company_link = top_suggestion.findAll('a')[3]
            company_slug = company_link['href'].split("/")[-1]
            print company_slug
            return company_slug

def parse(soup):
    """
    If none found, show top recommendations as json list
    """
    if direct_match(soup):
        return {'satisfaction': parse_satisfaction(soup),
                'ceo': parse_ceo(soup),
                'meta': parse_meta(soup),
                'salary': parse_salary(soup)
                }

    company_slug = exact_match(soup)
    if company_slug:
        # Perform a new search, using exact match company_slug
        return get(company_slug=company_slug)
    
    return parse_suggestions(soup)
