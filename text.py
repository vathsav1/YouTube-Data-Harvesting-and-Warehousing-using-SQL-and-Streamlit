import streamlit as st
import mysql.connector

client = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "tiger",
    database='M9'
)
cursor = client.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    )
'''
cursor.execute(create_table_query)


sample_data = [
    ("John", "john@example.com"),
    ("Emma", "emma@example.com"),
    ("Michael", "michael@example.com")
]

# Execute the SQL query to insert data into the users table
insert_query = '''
    INSERT INTO users (username, email) 
    VALUES (%s, %s)
'''

# Loop through the sample data and execute the insert query for each record
for data in sample_data:
    cursor.execute(insert_query, data)


on = st.toggle("What are the names of all the videos and their corresponding channels?")

if on:
    query = '''
        SELECT video_channel.video_name, channels_main.channel_name FROM video_channel LEFT JOIN channels_main ON 
        video_channel.channel_id = channels_main.channel_id
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        st.write("Video name:", row[0])
        st.write("channel name:", row[1])
        st.write()
        

on = st.toggle("Which channels have the most number of videos, and how many videos do they have?")

if on:
    query = '''
        SELECT channel_name, total_videos
        FROM channels_main
        ORDER BY CAST(total_videos AS UNSIGNED) DESC;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        st.write("Channel Name:", row[0])
        st.write("Total Videos:", row[1])
        st.write()

on = st.toggle("What are the top 10 most viewed videos and their respective channels?")

if on:
    query = '''
        SELECT v.view_count, c.channel_name
        FROM videos v
        JOIN channels_main c ON v.channel_id = c.channel_id
        ORDER BY CAST(v.view_count AS UNSIGNED) DESC
        LIMIT 10;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        st.write("view count:", row[0])
        st.write("channel name:", row[1])
        st.write()

on = st.toggle("How many comments were made on each video, and what are their corresponding video names?")

if on:
    query = '''
        SELECT title, comment_count
        FROM videos;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        st.write("Title:", row[0])
        st.write("Comment Count:", row[1])

on = st.toggle("Which videos have the highest number of likes, and what are their corresponding channel names?")

if on:
    query = '''
        SELECT v.*, c.channel_name
        FROM videos v
        JOIN channels_main c ON v.channel_id = c.channel_id
        ORDER BY CAST(v.like_count AS UNSIGNED) DESC, c.channel_name;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        st.write("video name:", row[2])
        st.write("like_count:", row[6])
        st.write("channel name:", row[11])

on = st.toggle("What is the total number of likes and dislikes for each video, and what are their corresponding video names?")

if on:
    query = '''
        SELECT like_count, title
        FROM videos;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        st.write("Like Count:", row[0])
        st.write("Title:", row[1])
        st.write()

on = st.toggle("What is the total number of views for each channel, and what are their corresponding channel names?")

if on:
    query = '''
        SELECT channel_views, channel_name
        FROM channels_main;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        st.write("Channel Views:", row[0])
        st.write("Channel Name:", row[1])
        st.write()

on = st.toggle("What are the names of all the channels that have published videos in the year 2022?")

if on:
    query = '''
        SELECT DISTINCT cm.channel_name, v.published_date
        FROM videos v
        JOIN channels_main cm ON v.channel_id = cm.channel_id
        WHERE SUBSTRING(v.published_date, 1, 4) = '2022';
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        st.write("Channel Name:", row[0])
        st.write("Published Date:", row[1])

on = st.toggle("What is the average duration of all videos in each channel, and what are their corresponding channel names?")

if on:
    query = '''
        SELECT cm.channel_name, AVG(duration_seconds) AS average_duration
    FROM (
        SELECT v.channel_id, 
            TIME_TO_SEC(
                TIMEDIFF(
                    STR_TO_DATE(CONCAT('1970-01-01 ', SUBSTRING(duration, 3)),
                                '%Y-%m-%d %H:%i:%s'),
                    STR_TO_DATE('1970-01-01', '%Y-%m-%d')
                )
            ) AS duration_seconds
        FROM videos v
        WHERE duration IS NOT NULL
            AND duration != ''
    ) AS video_duration
    JOIN channels_main cm ON video_duration.channel_id = cm.channel_id
    GROUP BY video_duration.channel_id;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        st.write("Channel Name:", row[0])
        st.write("Average Duration (seconds):", row[1])


on = st.toggle("Which videos has the highest number of comments, and what are their corresponding channel names?")

if on:
    query = '''
    SELECT cm.channel_name, v.title, v.comment_count
    FROM videos v
    JOIN channels_main cm ON v.channel_id = cm.channel_id
    WHERE v.comment_count = (
        SELECT MAX(comment_count)
        FROM videos
    )
    ORDER BY v.comment_count DESC;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        st.write("Channel Name:", row[0])
        st.write("Title:", row[1])
        st.write("Comment Count:", row[2])



client.commit()

cursor.close()
client.close()