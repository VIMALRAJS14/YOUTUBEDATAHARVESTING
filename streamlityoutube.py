import streamlit as st
import youtubedata
st.header("YOUTUBE DATA HARVESTING AND WAREHOUSING")
def main():
    channelid=st.text_input("enter channel id")
    if st.button("start uploading"):
        result=youtubedata.start(channelid)
        st.write(result)
    tables=st.radio(
        "select table to view",
        ["channeltable","playlisttable","videostable","commentstable"],index=None)
    if tables == "channeltable":
        output=youtubedata.showchanneltable()
        st.dataframe(output)
    if tables == "playlisttable":
        output=youtubedata.showplaylisttable()
        st.dataframe(output)
    if tables == "videostable":
        output=youtubedata.showvideostable()
        st.dataframe(output)
    if tables == "commentstable":
        output=youtubedata.showcommentstable()
        st.dataframe(output)
    query1='1. What are the names of all the videos and their corresponding channels?'
    query2='2. Which channels have the most number of videos, and how many videos do they have?'
    query3='3. What are the top 10 most viewed videos and their respective channels?'
    query4='4. How many comments were made on each video, and what are their corresponding video names?'
    query5='5. Which videos have the highest number of likes, and what are their corresponding channel names?'
    query6='6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?'
    query7='7. What is the total number of views for each channel, and what are their corresponding channel names?'
    query8='8. What are the names of all the channels that have published videos in the year 2022?'
    query9='9. What is the average duration of all videos in each channel, and what are their corresponding channel names?'
    query10='10.Which videos have the highest number of comments, and what are their corresponding channel names?'
    queries=st.selectbox("select query to execute",
                        (query1,query2,query3,query4,query5,query6,query7,query8,query9,query10),index=None)
    if queries==query1:
        output=youtubedata.query1()
        st.dataframe(output)        
    if queries==query2:
        output=youtubedata.query2()
        st.dataframe(output) 
    if queries==query3:
        output=youtubedata.query3()
        st.dataframe(output) 
    if queries==query4:
        output=youtubedata.query4()
        st.dataframe(output) 
    if queries==query5:
        output=youtubedata.query5()
        st.dataframe(output) 
    if queries==query6:
        output=youtubedata.query6()
        st.dataframe(output) 
    if queries==query7:
        output=youtubedata.query7()
        st.dataframe(output) 
    if queries==query8:
        output=youtubedata.query8()
        st.dataframe(output) 
    if queries==query9:
        output=youtubedata.query9()
        st.dataframe(output) 
    if queries==query10:
        output=youtubedata.query10()
        st.dataframe(output) 
main()
