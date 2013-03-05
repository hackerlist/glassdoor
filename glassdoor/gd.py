import requests
from BeautifulSoup import BeautifulSoup

def GET(company, parse=False):
    """Performs a HTTP GET for a glassdoor page and return
    BeautifulSoup
    """
    params = 'clickSource=searchBtn&typedKeyword=&sc.keyword=%s' % company
    r = requests.get('http://www.glassdoor.com/GD/Reviews/company-reviews.htm?' + params)
    soup = BeautifulSoup(r.content)
    return soup

def GETjson(company, raw=True):
    """Gets a parsed, json version of a glassdoor page.

    :param raw: if raw, return as json, else as python dict
    """
    return parse(GET(company), raw=raw)

def parse(soup, raw=False):
    """
    """
    def intify(s):
        return int(s.replace(',', ''))
    sat_reviews = soup.findAll('span', {'itemprop': 'reviewCount'})[0].text
    sat_score = soup.findAll('span', {'class': 'ratingValue notranslate '})[0].text
    sat_approval = soup.findAll('span', {'class': 'minor gdrHigh'})[0].findAll('tt', {'class': 'notranslate'})[0].text
    ceo = soup.findAll('div', {'class': 'ceoRating cf'})[0]
    ceo_name = ceo.findAll('h4', {'class': 'ceoName notranslate'})[0].text
    ceo_reviews = ceo.findAll('span', {'class': 'numCEORatings minor'})[0].findAll('tt', {'class': 'notranslate'})[0].text
    ceo_avatar = ceo.findAll('img', {'class': 'headshot photo'})[0]['src']
    ceo_approval = ceo.findAll('span', {'class': 'approvalPercent'})[0].findAll('tt', {'class': 'notranslate'})[0].text
    conn = soup.findAll('div', {'id': 'OverviewInsideConnections'})[0].findAll('tt', {'class': 'notranslate'})[0].text
    salary_mean = soup.findAll('td', {'class': 'mean'})[1].text
    return {'satisfaction': {'score': float(sat_score),
                             'reviews': intify(sat_reviews),
                             '%approval': intify(sat_approval)
                             },
            'ceo': {'reviews': intify(ceo_reviews),
                    '%approval': intify(ceo_approval),
                    'avatar': ceo_avatar,
                    'name': ceo_name
                    },
            'connections': intify(conn),
            'salary': {'mean': salary_mean + '.00'}
            }
