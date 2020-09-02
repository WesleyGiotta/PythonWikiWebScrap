from urllib.request import urlopen
from bs4 import BeautifulSoup
import re 


# final version
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
        if state == "TOTALS:\n" or state == "Totals\n" or state == "U.S Total"or state == "U.S. Total"or state == "U.S. total":
            break
        else:
            if "Democratic" in party: # make sure same party in each column for all tables
                data_e.append((year, state.replace('\n',''), votes1, elec1, votes2, elec2))
            else:
                data_e.append((year, state.replace('\n',''), votes2, elec2, votes1, elec1))
    return data_e



# newer version
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
        if state == "TOTALS:\n" or state == "Totals\n" or state == "U.S Total"or state == "U.S. Total":
            break
        else:
            if "Democratic" in party: # make sure same party in each column for all tables
                data_e.append((year, state.replace('\n',''), votes1, elec1, votes2, elec2))
            else:
                data_e.append((year, state.replace('\n',''), votes2, elec2, votes1, elec1))
    return data_e






# new try
def election_data(url):
    html = urlopen(url)
    bs = BeautifulSoup(html,'html.parser')
    table = bs.find("table", {'class':'wikitable sortable'}).find_all('tr')
    row0 = table[0].find_all(['td','th'])
    party = row0[1].text
    data_e = []
    for i in range(2,100):
        row = table[i].find_all(['td','th'])
        state = row[0].text
        votes1 = row[2].text.replace(',','').replace('\n','')
        elec1 = row[4].text.replace(',','').replace('\n','')
        votes2 = row[5].text.replace(',','').replace('\n','')
        elec2 = row[7].text.replace(',','').replace('\n','')
        year = re.findall(r'\d+', url)
        if state == "TOTALS:\n":
            break
        else:
            if "Democratic" in party:
                data_e.append((year, state.replace('\n',''), votes1, elec1, votes2, elec2))
            else:
                data_e.append((year, state.replace('\n',''), votes2, elec2, votes1, elec1))
    return data_e
    


# original try
def election_data(url):
    html = urlopen(url)
    bs = BeautifulSoup(html,'html.parser')
    table = bs.find("table", {'class':'wikitable sortable'}).find_all('tr')
    # grabs the first row with states
    row = table[5].find_all(['td','th'])
    # grabs a column from that row
    state = row[0].text
    votes1 = row[2].text.replace(',','').replace('\n','')
    elec1 = row[4].text.replace(',','').replace('\n','')
    votes2 = row[5].text.replace(',','').replace('\n','')
    elec2 = row[7].text.replace(',','').replace('\n','')
    # adding a year column to make joins easier
    year = re.findall(r'\d+', url)
    return year, state, votes1, elec1, votes2, elec2





# see which party
def election_data(url):
    html = urlopen(url)
    bs = BeautifulSoup(html,'html.parser')
    table = bs.find("table", {'class':'wikitable sortable'}).find_all('tr')
    # grabs the first row with states
    row = table[0].find_all(['td','th'])
    party = row[2].text
    return party

test = election_data(election[0])

# determine which party
if "Democrat" in test:
    print(1)
else: print(2)


############################################################################################

# census
# new
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
        if year in pop:
            pop = row[2].text.replace(',','').replace('\n','')
        else:
            pop = row[3].text.replace(',','').replace('\n','')
        data_c.append((year, state, pop))
    return data_c

census_data(census[1])

# original
def census_data(url):
    html = urlopen(url)
    bs = BeautifulSoup(html,'html.parser')
    table = bs.find("table", {'class':'wikitable sortable'}).find_all('tr')
    # grabs the first row with states
    data_c = []
    for i in range(1, 51):
        row = table[i].find_all(['td','th'])
        # grabs a column from that row
        state = row[1].text.replace('\n','').replace('\xa0','')
        pop = row[2].text.replace(',','').replace('\n','')
        # adding a year column to make joins easier
        year = re.findall(r'\d+', url)[0]
        data_c.append((year, state, pop))
    return data_c


