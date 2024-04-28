import googleapiclient.discovery
import isodate
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
api_service_name = "youtube"
api_version = "v3"
apikey="AIzaSyAs-6vWveOKwzrzbxGacCNnpOWTtDJ9lbE"
youtube = googleapiclient.discovery.build(
api_service_name, api_version, developerKey=apikey)
mydb=mysql.connector.connect(host="localhost",user="root",password="")
mycursor=mydb.cursor(buffered=True)
engine=create_engine(f"mysql+mysqlconnector://root@localhost:3306/trialyoutube")
def channeldetails(channelid):
    request = youtube.channels().list(part="snippet,contentDetails,statistics",id=channelid)
    response = request.execute()
    channel_name=[]
    channelid=[]
    description=[]
    playlist_id=[]
    viewcount=[]
    subscribercount=[]
    videocount=[]
    channel_name.append(response['items'][0]['snippet']['title'])
    channelid.append(response['items'][0]['id'])
    description.append(response['items'][0]['snippet']['description'])
    playlist_id.append(response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
    viewcount.append(response['items'][0]['statistics']['viewCount'])
    subscribercount.append(response['items'][0]['statistics']['subscriberCount'])
    videocount.append(response['items'][0]['statistics']['videoCount'])
    channeltable={'channel_name':channel_name,'channelid':channelid,'description':description,'playlist_id':playlist_id,'viewcount':viewcount,'subscribercount':subscribercount,'videocount':videocount}
    return channeltable
def playlistdetails(channelid):
       request = youtube.playlists().list(part="snippet,contentDetails",maxResults=100,channelId=channelid)
       response = request.execute()
       numberofplaylist=len(response['items'])
       i=0
       playlistid=[]
       playlistname=[]
       channelid=[]
       channelname=[]
       for i in range(0,numberofplaylist):
            playlistid.append(response['items'][i]['id'])
            playlistname.append(response['items'][i]['snippet']['title'])
            channelid.append(response['items'][i]['snippet']['channelId'])
            channelname.append(response['items'][i]['snippet']['channelTitle'])
           
       playlisttable={'playlistname':playlistname,'playlistid':playlistid,'channelname':channelname,'channelid':channelid}
       return playlisttable
def videoids(playlistid):
    videoid=[]
    next_page_token=None
    for i in playlistid:
       while True:
        request = youtube.playlistItems().list(part="snippet,contentDetails",playlistId=i,pageToken=next_page_token)
        response = request.execute()
        for item in response['items']:
          videoid.append(item['snippet']['resourceId']['videoId'])
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
          break
    return videoid
def videodetails(videoid,channelid):
    published_at=[]
    videoname=[]
    videodescription=[]
    videothumbnail=[]
    videotags=[]
    duration=[]
    viewcount=[]
    likecount=[]
    favoritecount=[]
    commentcount=[]
    captionstatus=[]
    channelname1=[]
    videoids=[]
    for v in videoid:
          request = youtube.videos().list(part="snippet,contentDetails,statistics",id=v)
          response = request.execute()
          published_at.append(isodate.parse_datetime(response['items'][0]['snippet']['publishedAt'][:-1]))
          videoname.append(response['items'][0]['snippet']['title'])
          videoids.append(v)
          videodescription.append(response['items'][0]['snippet']['title'])
          channelname1.append(''.join(channelid))
          videothumbnail.append(response['items'][0]['snippet']['thumbnails']['default']['url'])
          duration.append(str(isodate.parse_duration(response['items'][0]['contentDetails']['duration'])))
          viewcount.append(response['items'][0]['statistics']['viewCount'])
          if 'likeCount' in response['items'][0]['statistics'].keys():
             likecount.append(response['items'][0]['statistics']['likeCount'])
          else:
             likecount.append(0)
          favoritecount.append(response['items'][0]['statistics']['favoriteCount'])
          if 'commentCount' in  response['items'][0]['statistics'].keys():
             commentcount.append(response['items'][0]['statistics']['commentCount'])
          else:
              commentcount.append(0)
          captionstatus.append(response['items'][0]['contentDetails']['caption'])
          if 'tags' in (response['items'][0]['snippet'].keys()):
              videotags.append(','.join(response['items'][0]['snippet']['tags']))
          else:
              videotags.append('NOT EXISTS') 
    
    videotable={'videoname':videoname,'videoid':videoids,'videodescription':videodescription,'channelname':channelname1,'published_at':published_at,'videothumbnail':videothumbnail,'videotags':videotags,'duration':duration,'viewcount':viewcount,'likecount':likecount,'favoritecount':favoritecount,'commentcount':commentcount,'captionstatus':captionstatus}
    return videotable
def commentdetails(videoid,channelname):
    commentid=[]
    channelname1=[]
    videoidl=[]
    commenttext=[]
    commentauthor=[]
    commentpublishedat=[]
    for v in videoid:
       try:
         request = youtube.commentThreads().list(part="snippet",maxResults=100,order="time",videoId=v)
         response = request.execute()
         for c in range(0,len(response['items'])):
            commentid.append(response['items'][c]['id'])
            channelname1.append(''.join(channelname))
            videoidl.append(response['items'][c]['snippet']['topLevelComment']['snippet']['videoId'])
            commenttext.append(response['items'][c]['snippet']['topLevelComment']['snippet']['textOriginal'])
            commentauthor.append(response['items'][c]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
            commentpublishedat.append(isodate.parse_datetime(response['items'][c]['snippet']['topLevelComment']['snippet']['publishedAt'][:-1]))
       except:
            commentid.append("comments turned off")
            channelname1.append(''.join(channelname))
            videoidl.append("Comments turned off")
            commenttext.append("Comments turned off")
            commentauthor.append("Comments turned off")
            commentpublishedat.append("Comments turned off")
    commentstable={'commentid':commentid,'channelname':channelname1,'videoid':videoidl,'commenttext':commenttext,'commentauthor':commentauthor,'commentpublishedat':commentpublishedat}
    return commentstable



def start(channelid):
    chadet=channeldetails(channelid)
    chapla=playlistdetails(channelid)
    chavidid=videoids(chadet['playlist_id'])
    videodet=videodetails(chavidid,chadet['channel_name'])
    commentdet=commentdetails(chavidid,chadet['channel_name'])
    channel_table=pd.DataFrame(chadet)
    playlist_table=pd.DataFrame(chapla)
    videos_table=pd.DataFrame.from_dict(videodet)
    comments_table=pd.DataFrame.from_dict(commentdet)
    mycursor.execute("create database if not exists trialyoutube")
    mycursor.execute("create table if not exists trialyoutube.channeltable (channel_name VARCHAR(255),channelid VARCHAR(255) PRIMARY KEY,description TEXT,playlist_id VARCHAR(255),viewcount BIGINT,subscribercount INT,videocount INT )")
    mycursor.execute("create table if not exists trialyoutube.playlisttable (playlistname VARCHAR(255),playlistid VARCHAR(255),channelname VARCHAR(255),channelid VARCHAR(255))")
    mycursor.execute("create table if not exists trialyoutube.videotable (videoname TEXT,videoid VARCHAR(255),videodescription TEXT,channelname VARCHAR(255),published_at DATETIME,videothumbnail VARCHAR(255),videotags TEXT,duration VARCHAR(255),viewcount BIGINT,likecount BIGINT,favoritecount INT,commentcount INT,captionstatus VARCHAR(255))")
    mycursor.execute("create table if not exists trialyoutube.commentstable(commentid VARCHAR(255),channelname VARCHAR(255),videoid VARCHAR(255),commenttext TEXT,commentauthor VARCHAR(255),commentpublishedat DATETIME)")
    try:
       channel_table.to_sql('channeltable',con=engine,if_exists='append',index=False)
    except:
       output="already exist"
       return output
    else:
       playlist_table.to_sql('playlisttable',con=engine,if_exists='append',index=False)
       videos_table.to_sql('videotable',con=engine,if_exists='append',index=False,chunksize=1000)
       comments_table.to_sql('commentstable',con=engine,if_exists='append',index=False,chunksize=1000)
       engine.dispose()
       output="successfully inserted"
       return output
def showchanneltable():
    mycursor.execute("select * from trialyoutube.channeltable")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records
def showplaylisttable():
    mycursor.execute("select * from trialyoutube.playlisttable")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records
def showvideostable():
    mycursor.execute("select * from trialyoutube.videotable")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records
def showcommentstable():
    mycursor.execute("select * from trialyoutube.commentstable")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records
def query1():
    mycursor.execute("select videoname,channelname from trialyoutube.videotable")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records   
def query2():
    mycursor.execute("select channelname,count(*) as max from trialyoutube.videotable GROUP BY channelname ORDER BY max DESC LIMIT 1")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records  
def query3():
    mycursor.execute("select channelname,videoname,viewcount from trialyoutube.videotable order by viewcount DESC LIMIT 10")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records  
def query4():
    mycursor.execute("select videoname,commentcount from trialyoutube.videotable")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records  
def query5():
    mycursor.execute("select channelname,videoname,likecount from trialyoutube.videotable ORDER BY likecount DESC LIMIT 10")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records  
def query6():
    mycursor.execute("select videoname,likecount from trialyoutube.videotable")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records  
def query7():
    mycursor.execute("select channel_name,viewcount from trialyoutube.channeltable")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records  
def query8():
    mycursor.execute("select channelname from trialyoutube.videotable WHERE published_at between '2022-01-01' and '2022-12-31' GROUP BY channelname")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records  
def query9():
    mycursor.execute("select channelname,SEC_TO_TIME(AVG(TIME_TO_SEC(duration))) as avg_duration from trialyoutube.videotable GROUP BY channelname")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records   
def query10():
    mycursor.execute("select videoname,channelname,commentcount from trialyoutube.videotable ORDER BY commentcount DESC LIMIT 5")
    data=mycursor.fetchall()
    output=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    records=output.to_records(index=False)
    return records   