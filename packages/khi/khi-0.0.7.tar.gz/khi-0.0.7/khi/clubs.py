import sys
import getopt
import urllib3
from bs4 import BeautifulSoup

_URL='http://www.kmc.gos.pk/Contents.aspx?id=83'

def count(u=_URL):
    http = urllib3.PoolManager();
    u = http.request(url=u, method='get')
    bs = BeautifulSoup(u.data, 'html.parser')
    return len(bs.body.table.contents[7].table.tbody.find_all('tr')) - 1


def get(u=_URL):
    http = urllib3.PoolManager();
    u = http.request(url=u, method='get')
    bs = BeautifulSoup(u.data, 'html.parser')
    count = len(bs.body.table.contents[7].table.tbody.find_all('tr')) - 1
    i=1
    clubs = []
    while i <= count:
        node = bs.body.table.contents[7].table.tbody.find_all('tr')[i]
        clubs.append(node.contents[3].text.strip())
        i=i+1

    return count, clubs

def view(u=_URL):
    c, p = get(u)

    print('TOTAL CLUBS: {}'.format(c))
    print('----------------')

    i = 1
    for pl in p:
        print('{}. {}'.format(str(i).zfill(2), pl))
        i = i+1
