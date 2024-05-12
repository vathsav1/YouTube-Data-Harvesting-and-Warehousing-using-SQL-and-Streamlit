

import googleapiclient.discovery
import streamlit as st
import mysql.connector
import pandas as pd

client = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "tiger",
    database='M9'
)
cursor = client.cursor()

api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyAA3M-mys07tlLFwQUDoR7biOnCGAD0DPo"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)


def channel_data(c_id):
    request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=c_id
    )
    response = request.execute()
    
    data = {
            "channel_id":c_id,
            "channel_name":response['items'][0]['snippet']['title'],
            "channel_views":response['items'][0]['statistics']['viewCount'],
            "channel_descp":response['items'][0]['snippet']['description'],
            "channel_turl":response['items'][0]['snippet']['thumbnails']['default']['url'],
            "channel_theight":response['items'][0]['snippet']['thumbnails']['default']['height'],
            "channel_twidth":response['items'][0]['snippet']['thumbnails']['default']['width'],
            "channel_sub":response['items'][0]['statistics']['subscriberCount'],
            "channel_pub":response['items'][0]['snippet']['publishedAt'],
            "uploads_playlist_id":response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"],
            "total_videos" : response["items"][0]["statistics"]["videoCount"]
            }
    
    return data

def fetch_videos(uploads_playlist_id,title):
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist_id,
        maxResults=10
    )
    response = request.execute()
    videos = []
    for item in response["items"]:
        video_id = item["snippet"]["resourceId"]["videoId"]
        video_title = item["snippet"]["title"]
        videos.append({"video_id": video_id, "channel_id": title, "video_name":video_title})
        # video_title = item["snippet"]["title"]
        # videos.append({"id": video_id, "title": video_title})
    return videos

def fetch_comments(video_id):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=10,  # Adjust as per your requirements
        textFormat="plainText"
    )
    response = request.execute()
    comments = []
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]
        comments.append([
        item["id"],
        video_id,    
        comment['textDisplay'],
        comment['authorDisplayName'],
        comment['publishedAt'],
        comment['likeCount']
        ])

        
    return comments

def fetch_video_details(video_id,title):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        video_details = {}
        if response["items"]:
            item = response["items"][0]
            snippet = item["snippet"]
            content_details = item["contentDetails"]
            statistics = item["statistics"]
            
            video_details['channel_id'] = title
            video_details["video-id"] = video_id
            video_details["title"] = snippet.get("title", "")
            video_details["description"] = snippet.get("description", "")
            video_details["published_date"] = snippet.get("publishedAt", "")
            video_details["view_count"] = statistics.get("viewCount", "")
            video_details["like_count"] = statistics.get("likeCount", "")
            # video_details["dislike_count"] = statistics.get("dislikeCount", "")
            video_details["comment_count"] = statistics.get("commentCount", "")
            video_details["duration"] = content_details.get("duration", "")
            video_details["thumbnail"] = snippet.get("thumbnails", {}).get("default", {}).get("url", "")
            video_details["caption"] = snippet.get("localized", {}).get("title", "")
            
        return video_details

cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels_main (
        channel_id VARCHAR(255) PRIMARY KEY,
        channel_name VARCHAR(255),
        channel_views VARCHAR(255),
        channel_descp TEXT,
        channel_turl VARCHAR(255),
        channel_theight INT,
        channel_twidth INT,
        channel_sub VARCHAR(255),
        channel_pub VARCHAR(255),
        upload_playlist_id VARCHAR(255),
        total_videos VARCHAR(255)
    )
''')

create_table_query = '''
    CREATE TABLE IF NOT EXISTS video_channel (
        video_id VARCHAR(255),
        channel_id VARCHAR(255),
        video_name VARCHAR(255),
        PRIMARY KEY (video_id, channel_id)
    )
'''
cursor.execute(create_table_query)

create_table_query = '''
    CREATE TABLE IF NOT EXISTS comments (
        channel_id VARCHAR(255),
        video_id VARCHAR(255),
        comment TEXT,
        author_name VARCHAR(255),
        date VARCHAR(255),
        like_count INT
    )
'''
cursor.execute(create_table_query)

create_table_query = '''
    CREATE TABLE IF NOT EXISTS videos (
        channel_id VARCHAR(255),
        video_id VARCHAR(255),
        title VARCHAR(255),
        description TEXT,
        published_date VARCHAR(255),
        view_count VARCHAR(255),
        like_count VARCHAR(255),
        comment_count VARCHAR(255),
        duration VARCHAR(255),
        thumbnail VARCHAR(255),
        caption TEXT
    )
'''
cursor.execute(create_table_query)


def st1(title):
    data = channel_data(title)
    playlist = data["uploads_playlist_id"]
    insert_query = '''
        INSERT INTO channels_main (
            channel_id, channel_name, channel_views, channel_descp,
            channel_turl, channel_theight, channel_twidth, channel_sub,
            channel_pub, upload_playlist_id, total_videos
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
# Prepare the data to be inserted
    data_to_insert = (
        data['channel_id'], data['channel_name'], data['channel_views'],
        data['channel_descp'], data['channel_turl'], data['channel_theight'],
        data['channel_twidth'], data['channel_sub'], data['channel_pub'],
        data['uploads_playlist_id'], data['total_videos']
    )

    # Execute the query with the data
    cursor.execute(insert_query, data_to_insert)
    return playlist

def st2(uploads_playlist_id, title):
    data1 = fetch_videos(uploads_playlist_id,title)
    df2 = pd.DataFrame(data1,columns=['video_id','channel_id','video_name'])
    for _, row in df2.iterrows():
        video_id = row['video_id']
        channel_id = row['channel_id']
        video_name = row['video_name']
        insert_query = "INSERT INTO video_channel (video_id, channel_id, video_name) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (video_id, channel_id, video_name))
    return df2

def st3(video_id):
    comments = fetch_comments(video_id)
    df = pd.DataFrame(comments,columns=['channel_id','video_id','comment','author_name','date','like_count'])

    for _, row in df.iterrows():
        insert_query = "INSERT INTO comments (channel_id, video_id, comment, author_name, date, like_count) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (row['channel_id'], row['video_id'], row['comment'], row['author_name'], row['date'], row['like_count']))

def st4(video_ids, title):
    a = fetch_video_details(video_ids, title)

    insert_query = '''
        INSERT INTO videos 
        (channel_id, video_id, title, description, published_date, view_count, like_count, comment_count, duration, thumbnail, caption) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    # Execute the insert query with the data from dictionary `a`
    cursor.execute(insert_query, (
        a['channel_id'], 
        video_ids, 
        a['title'], 
        a['description'], 
        a['published_date'], 
        a['view_count'], 
        a['like_count'], 
        a['comment_count'], 
        a['duration'], 
        a['thumbnail'], 
        a['caption']
    ))


def st0(title):
    playlist = st1(title)
    df2 = st2(playlist, title)
    for chan in df2['video_id'].values:
        st3(chan)
    for chan in df2['video_id'].values:
        st4(chan, title)

def printing(is_clicked, title):
    data = channel_data(title)
    image_url = data['channel_turl']
    st.image(image_url, caption='Profile Image')
    st.write(data['channel_name'])
    st.write(data['channel_sub'])
    st.write(data['channel_descp'])


st.subheader('YOUTUBE CHANNEL LINK', divider='rainbow')
title = st.text_input("ENTER HERE", "")
data = channel_data(title)
on = st.toggle("slide to store")
if on:
    st0(title)
    st.write("succesfully stored")
col1, col2 = st.columns([1, 3])
with col1:
    st.button("reset",type="primary")
with col2:
    is_clicked = st.button("preview")
if is_clicked:
    printing(is_clicked, title)
# title = st.text_input("enter the url address")
# st0(title)

client.commit()

cursor.close()
client.close()