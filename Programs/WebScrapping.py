# Webscrapping Final Project

# Get urls for elections.
# Elections are every 4 years so add 4 to each election year
# then change the year in the url since they are all the same except year.
def election_url(start, end):
    years = []
    url = []
    while start <= end:
        years.append(start)
        start = start + 4
    for year in years:
        url.append("https://en.wikipedia.org/wiki/"+str(year)+"_United_States_presidential_election")
    return url

election = election_url(1972, 2016)        


# Get urls for Census.
# Census every 10 years so add 10 to each census year
# then change the year in the url since they are all the same except year.
def census_url(start, end):
    years = []
    url = []
    while start <= end:
        years.append(start)
        start = start + 10
    for year in years:
        url.append("https://en.wikipedia.org/wiki/"+str(year)+"_United_States_Census")
    return url

census = census_url(1970, 2010) 


############################################################################################

# , 'style':"text-align:right"
# Get data election
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re 

def election_data(url):
    html = urlopen(url)
    bs = BeautifulSoup(html,'html.parser')
    table = bs.find("table", {'class':'wikitable sortable','style':['text-align:right','text-align:right;']}).find_all('tr')
    # determine the party in column 1
    row0 = table[0].find_all(['td','th'])
    party = row0[1].text
    # Grab the data
    data_e = []
    for i in range(2,100):
        row = table[i].find_all(['td','th'])
        state = row[0].text
        votes1 = row[2].text.replace(',','').replace('\n','')
        if '%' in votes1:
            votes1 = row[1].text.replace(',','').replace('\n','')
            elec1 = row[3].text.replace(',','').replace('\n','').replace('\xa0','0').replace('–','0').replace('-','0')
            votes2 = row[4].text.replace(',','').replace('\n','')
            elec2 = row[6].text.replace(',','').replace('\n','').replace('\xa0','0').replace('–','0').replace('-','0')
        else:
            elec1 = row[4].text.replace(',','').replace('\n','').replace('\xa0','0').replace('–','0').replace('-','0')
            votes2 = row[5].text.replace(',','').replace('\n','')
            elec2 = row[7].text.replace(',','').replace('\n','').replace('\xa0','0').replace('–','0').replace('-','0')
        year = re.findall(r'\d+', url)[0]
        if "otal" in state or "OTAL" in state:
            break
        else:
            if "Democratic" in party: # make sure same party in each column for all tables
                data_e.append((year, state.replace('\n',''), votes1, elec1, votes2, elec2))
            else:
                data_e.append((year, state.replace('\n',''), votes2, elec2, votes1, elec1))
    return data_e

# test to see if it works
election_data(election[11])

# iterate over all the election urls
data_election=[]
for i in range(0, len(election)):
    data_election = data_election + election_data(election[i])


# Get data census
def census_data(url):
    html = urlopen(url)
    bs = BeautifulSoup(html,'html.parser')
    table = bs.find("table", {'class':'wikitable sortable'}).find_all('tr')
    # grabs the first row with states
    data_c = []
    # adding a year column to make joins easier
    year = re.findall(r'\d+', url)[0]
    for i in range(1, 51):
        row = table[i].find_all(['td','th'])
        # grabs a column from that row
        state = row[1].text.replace('\n','').replace('\xa0','')
        pop = row[2].text.replace(',','').replace('\n','')
        # check for correct column
        if year in pop:
            pop = row[2].text.replace(',','').replace('\n','')
        else:
            pop = row[3].text.replace(',','').replace('\n','')
        data_c.append((year, state, pop))
    return data_c

# test to see if it works
census_data(census[4])

# iterate over all the census urls
data_census=[]
for i in range(0, len(census)):
    data_census = data_census + census_data(census[i])
    

############################################################################################


# SQL database
import sqlite3 as db

conn = db.connect('./Data/USA_Voting.db') # make sure to set dirctory to outside /Data
c = conn.cursor()

# Create Tables
c.execute('''CREATE TABLE IF NOT EXISTS Election 
          (year integer, state text, Dvote float, Delectoral float, Rvote float, Relectoral float);''')
c.execute('''CREATE TABLE IF NOT EXISTS Census 
          (year integer, state text, population float);''')

# Stop duplicates
c.execute('''CREATE UNIQUE INDEX Indx_elec ON Election(year, state);''')
c.execute('''CREATE UNIQUE INDEX Indx_cen ON Census(year, state);''')

# insert data into tables
insert_elec = '''INSERT INTO Election VALUES(?,?,?,?,?,?);'''
insert_cen = '''INSERT INTO Census VALUES(?,?,?);'''

c.executemany(insert_elec, data_election)
c.executemany(insert_cen, data_census)


# select fraction of people voting for Regan (republican) 1980
frac_1980 = c.execute('''SELECT Census.state, round(Rvote/population, 4) AS Rfraction
          FROM ELECTION
          JOIN Census
          ON Election.state = Census.state
          WHERE Census.year = 1980 AND Election.year = 1980
          ORDER BY Rfraction;''')
frac_1980.fetchall()


conn.commit()

conn.close()



