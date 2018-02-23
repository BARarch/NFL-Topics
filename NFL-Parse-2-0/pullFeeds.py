import pandas as pd
from datetime import datetime
import itemQuery as iq
import articleParse as ap
from timeit import default_timer as timer
import subprocess
import modelGS as mgs
import psycopg2
import config as config
from googleapiclient.errors import HttpError
import corpus as cp
from quivtimer import ticToc

#import httplib2
#from apiclient import discovery

#%run modelInit.py

def getFeeds():
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ/edit#gid=0
    """
    credentials = get_credentials()
    http = credentials.authorize(mgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = mgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #specify sheetID and range
    spreadsheetId = '1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ'
    rangeName = 'RSS LIST!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Done')

    return values

def writeLinkData(dataColumns):
    """Google Sheets API Code.

    Writes all team news link data from RSS feed to the NFL Team Articles speadsheet.
    https://docs.google.com/spreadsheets/d/1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ/edit#gid=0
    """
    credentials = get_credentials()
    http = credentials.authorize(mgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = mgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheet_id = '1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ'
    value_input_option = 'RAW'
    rangeName = 'Sheet1!A2'
    values = dataColumns
    body = {
          'values': values
    }
    
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
                                                    valueInputOption=value_input_option, body=body).execute()

    return result


def get_runs():
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ/edit#gid=0
    """
    credentials = get_credentials()
    http = credentials.authorize(mgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = mgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #specify sheetID and range
    spreadsheetId = '1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ'
    rangeName = 'RUNS!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Done')

    return values

def write_run_row(rowNum, runInfo):
    """Google Sheets API Code.

    Writes all team news link data from RSS feed to the NFL Team Articles speadsheet.
    https://docs.google.com/spreadsheets/d/1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ/edit#gid=0
    """
    credentials = get_credentials()
    http = credentials.authorize(mgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = mgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheet_id = '1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ'
    value_input_option = 'RAW'
    rangeName = 'RUNS!A' + str(rowNum)
    values = runInfo
    body = {
          'values': values
    }
    
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
                                                    valueInputOption=value_input_option, body=body).execute()

    return result




def sheetColumns(record):
    if record['new']:
        return [record['pubDate'], record['team'], record['title'], record['type'], record['link'], record['discription'], record['creator'], 'new']
    else:
        return [record['pubDate'], record['team'], record['title'], record['type'], record['link'], record['discription'], record['creator'], '']
    
def sheetColumns2ndAttempt(record):
    maxDiscriptionSize = 3000
    try:
        if len(record['discription']) > maxDiscriptionSize:
            discription = ''
            #print("Discrption on " + record['pubDate'])
            #print("from the " + record['team'] + " was too large")
        else:
            discription = record['discription']
    except TypeError:
        discription = record['discription']
        
    if record['new']:
        return [record['pubDate'], record['team'], record['title'], record['type'], record['link'], discription, record['creator'], 'new']
    else:
        return [record['pubDate'], record['team'], record['title'], record['type'], record['link'], discription, record['creator'], '']

def sheetColumnsNoDiscription(record):
    if record['new']:
        return [record['pubDate'], record['team'], record['title'], record['type'], record['link'], '', record['creator'], 'new']
    else:
        return [record['pubDate'], record['team'], record['title'], record['type'], record['link'], '', record['creator'], '']
    
    
def getTime(date):
    return datetime.strptime(date[:25], '%a, %d %b %Y %H:%M:%S')

def feedFrame(feedRow, cursor):
    noNew = 0
    elms = 0
    teamFeed =  [{'pubDate':record[0], 
                  'team':feedRow[1], 
                  'title':record[1], 
                  'type':feedRow[2], 
                  'link':record[2], 
                  'discription':record[3], 
                  'creator':record[4]
                 } for record in iq.recordsFromFeed(feedRow[3])]
    for elm in teamFeed:
        # Check for element in the Database, if not there set 'new' flag
        cursor.execute("SELECT * FROM nfl_team_articles WHERE title = '%s'" % (sqlString(elm['title'])))
        elm['new'] = not cursor.fetchall()
        if elm['new']:
            noNew += 1
        elms += 1
    
    if noNew == elms:
        print('team: '+ feedRow[1] + ' ' + feedRow[0] + '    ' + '\t' + str(noNew) + '/' + str(elms) + '\t' + "MAX")
    else:    
        print('team: '+ feedRow[1] + ' ' + feedRow[0] + '    ' + '\t' + str(noNew) + '/' + str(elms))        
    return teamFeed

def feedFrame2(feedRow, cursor):
    noNew = 0
    elms = 0
    teamFeed =  [{'pubDate':record[0], 
                  'team':feedRow[1], 
                  'title':record[1], 
                  'type':feedRow[2], 
                  'link':record[2], 
                  'discription':record[3], 
                  'creator':record[4]
                 } for record in iq.recordsFromFeed(feedRow[3])]
    for elm in teamFeed:
        # Check for element in the Database, if not there set 'new' flag
        cursor.execute("SELECT * FROM team_articles WHERE title = '%s'" % (sqlString(elm['title'])))
        elm['new'] = not cursor.fetchall()
        if elm['new']:
            noNew += 1
        elms += 1
        
    if (noNew == elms) & (elms != 0):
        print('team: '+ feedRow[1] + ' ' + feedRow[0] + '    ' + '\t' + str(noNew) + '/' + str(elms) + '\t' + "MAX" + '\t' + feedRow[2])
    else:    
        print('team: '+ feedRow[1] + ' ' + feedRow[0] + '    ' + '\t' + str(noNew) + '/' + str(elms))        
    return teamFeed

def sqlString(stg):
    return stg.replace("'", "''")

def pushRecord(feeds, cursor, conn):
    '''
        Push all article records into Postgres
    '''

    
    cursor.execute("SELECT id from nfl_team_articles order by id desc limit 1");
    lastId = cursor.fetchall()[0][0]
    
    pushedElms = 0
    feed = 0
    for elm in reversed(feeds):
        #print("feed: " + str(feed) )
        #cursor.execute("SELECT * FROM nfl_team_articles WHERE title = '%s'" % (sqlString(elm['title'])))
        #elm['new'] = not cursor.fetchall()
        feed += 1

        if elm['new']:
            pushedElms += 1
            lastId += 1
            cursor.execute(
                "INSERT INTO nfl_team_articles (Date, Team, Title, Type, Link, Discription, Creator, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                (elm['pubDate'], elm['team'], elm['title'], elm['type'], elm['link'], elm['discription'], elm['creator'], lastId))
    
    conn.commit()
    print(str(pushedElms) + " new records intserted into team-articles")
    
    return lastId

def pushRecord2(feeds, cursor, conn):
    '''
        Push all article records into team_articles Postgres table with auto id incrementer
    '''
    
    lastId = 0   
    pushedElms = 0
    feed = 0
    for elm in reversed(feeds):

        feed += 1

        if elm['new']:
            pushedElms += 1
            lastId += 1
            cursor.execute(
                "INSERT INTO team_articles (Date, Team, Title, Type, Link, Discription, Creator) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                (elm['pubDate'], elm['team'], elm['title'], elm['type'], elm['link'], elm['discription'], elm['creator']))
    
    conn.commit()
    print(str(pushedElms) + " new records intserted into nfl-team-articles")
    
    return pushedElms

def pushCorpus(links):
    '''
        For each link 
        1) extract article text
        2) clean it
        3) push the text the word count and the foreign key to news_corpus table
    '''
    
    conn = config.connect()
    cursor = conn.cursor()
    pushedElms = 0
    
    for elm in links:
        link = elm[1]
        clean = cl.parseForCorpus(link)
        cursor.execute(
        "INSERT INTO news_corpus (article_text, word_count, article_id) VALUES (%s, %s, %s);",
        (clean[0], clean[1], elm[0]))
        pushedElms += 1
     
    conn.commit()
    print(str(pushedElms) + " new records intserted into news_corpus")
    
    cursor.close()
    conn.close()
    
    return pushedElms



# Step 0 Initialize Models
tic = ticToc()
get_credentials = mgs.modelInit()
conn = config.connect()
cursor = conn.cursor()


# Step 1 Load Feed Information
feeds = getFeeds()

# Step 2 Pull all feeds from RSS Lins Using feedFrame()
data = []
for feedRow in feeds:
    if feedRow[3] == 'null':
        continue
    data.extend(feedFrame2(feedRow, cursor))
    #print('team: '+ feedRow[1] + ' ' + feedRow[0] )

# Step 3 Sort the Data by pubData push to Postgress and DataFrame the result    
dataSorts = sorted(data, key=lambda k: getTime(k['pubDate']), reverse=True)
noNewArticles = pushRecord2(dataSorts, cursor, conn)

cursor.close()
conn.close()

df = pd.DataFrame(dataSorts)

# Step 4 Write the Result to the NFL Feeds Speadsheet.
try:
    writeLinkData([sheetColumns(record) for record in dataSorts])
except HttpError:
    print("Large Discriptions")
    writeLinkData([sheetColumns2ndAttempt(record) for record in dataSorts])
    print('There were large discriptions in some of the cells which did cause some problems, upload completed with them removed from the table write')
finally:
    print('Complete')

# Step 5 Update Corpus Table with new news article Data
cp.corpusNewArticles() 

size = cp.dbSize() 

print ("Collection Size:" + '\t' + size[0])
print ("Team Corpus:" + '\t' + '\t'+ size[1])


# Step 6 Send Completion Report
row = len(get_runs()) + 2

completionTime = datetime.now().strftime("%a %b %d, %Y  %H:%M")
noArticles = noNewArticles
collectionSize = size[0]
teamCorpusSize = size[1]
duration = tic.toc()
print('Completed in ' + duration)

write_run_row(row, [[completionTime, duration, noArticles, collectionSize, teamCorpusSize]])


