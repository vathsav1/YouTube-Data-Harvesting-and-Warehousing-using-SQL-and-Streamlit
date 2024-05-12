# YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit


Problem Statement:
The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application should have the following features:
Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, likes, comments of each video) using Google API.
Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
Option to store the data in a MYSQL.
Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.

Approach:
1.Set up a Streamlit app: Streamlit is a great choice for building data visualization and analysis tools quickly and easily. You can use Streamlit to create a simple UI where users can enter a YouTube channel ID, view the channel details, and select channels to migrate to the data warehouse.
2.Connect to the YouTube API: You'll need to use the YouTube API to retrieve channel and video data. You can use the Google API client library for Python to make requests to the API.
3.Store and Clean data : Once you retrieve the data from the YouTube API, store it in a suitable format for temporary storage before migrating to the data warehouse. You can use pandas DataFrames or other in-memory data structures.
4.Migrate data to a SQL data warehouse: After you've collected data for multiple channels, you can migrate it to a SQL data warehouse. You can use a SQL database such as MySQL or PostgreSQL for this.
5.Query the SQL data warehouse: You can use SQL queries to join the tables in the SQL data warehouse and retrieve data for specific channels based on user input. You can use a Python SQL library such as SQLAlchemy to interact with the SQL database.
6.Display data in the Streamlit app: Finally, you can display the retrieved data in the Streamlit app. You can use Streamlit's data visualization features to create charts and graphs to help users analyze the data.
Overall, this approach involves building a simple UI with Streamlit, retrieving data from the YouTube API, storing the data SQL as a warehouse, querying the data warehouse with SQL, and displaying the data in the Streamlit app.



Example SQL Tables:

![image](https://github.com/vathsav1/YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit/assets/152419328/627b5875-33e0-4601-88f9-74ccc7c007ce)

![image](https://github.com/vathsav1/YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit/assets/152419328/4b534aa1-cc04-4be9-a397-a6a20fb51132)

![image](https://github.com/vathsav1/YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit/assets/152419328/1c989e00-85e5-4ded-9b93-204e817cce8a)

PREVIEW OF THE PROJECT


![image](https://github.com/vathsav1/YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit/assets/152419328/7f1655e4-6137-4b43-a4de-ef8c21e42a00)

![image](https://github.com/vathsav1/YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit/assets/152419328/77c175ca-8a07-4a82-b5df-34614b7b27a0)

![image](https://github.com/vathsav1/YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit/assets/152419328/61f856d2-bc50-42ae-a99c-43d93c303116)



THANK YOU
