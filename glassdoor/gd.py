import requests
from BeautifulSoup import BeautifulSoup

def GET(company):
    """
    """
    params = 'clickSource=searchBtn&typedKeyword=&sc.keyword=%s' % company
    r = requests.get('http://www.glassdoor.com/GD/Reviews/company-reviews.htm?' + params)
    return BeautifulSoup(r.content)
    
def parse(soup):
    """
    """
    pass
