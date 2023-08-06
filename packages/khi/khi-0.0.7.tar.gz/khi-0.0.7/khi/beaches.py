import sys
import getopt
import urllib3
from bs4 import BeautifulSoup

_URL='http://www.kmc.gos.pk/Contents.aspx?id=82'

def count(u=_URL):
    count, _ = get()
    return count

def get(u=_URL):
    http = urllib3.PoolManager();
    u = http.request(url=u, method='get')
    bs = BeautifulSoup(u.data, 'html.parser')
    bids = bs.body.find_all('td', attrs = {'style':'text-align: center;'})
    l = t.find_all('tr')[1].text.upper().split('\n')
    l = [ i for i in l if i.strip()]
    return len(l), l

def view(u=_URL):
    c, p = get(u)

    print('TOTAL DISTRICTS: {}'.format(c))
    print('----------------')

    i = 1
    for pl in p:
        print('{}. {}'.format(str(i).zfill(2), pl))
        i = i+1
