from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

alliances = [
    'Oneworld',
    'Star_Alliance',
    'SkyTeam',
    'Vanilla_Alliance',
    'U-FLY_Alliance',
    'Value_Alliance',
    ]

def get_info():
    URL = 'https://en.wikipedia.org/wiki/Airline_alliance'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, features='html.parser')
    return soup

def get_members(soup, alliance_name):
    alliance_members = []
    members_container = soup.find('span', {'id': alliance_name}).find_next('div', class_='div-col columns column-width')
    link_elems = members_container.find_all('a')
    for member in link_elems:
        if member.parent.name != 'span':
            alliance_members.append(member['title'])
    return alliance_members

@app.route('/')
def list_members():
    soup = get_info()
    all_members = {}
    for a in alliances:
        all_members[a] = get_members(soup, a)
    return render_template('index_temp.html', all_members=all_members)


if __name__ == '__main__':
    #app.run()
    with app.app_context():
        soup = get_info()
        all_members = {}
        for a in alliances:
            all_members[a] = get_members(soup, a)
        rendered = render_template('index_temp.html', \
            title = "Airline Alliance Members", \
            all_members = all_members)
        with open('index.html', 'w') as fout:
            fout.write(rendered)