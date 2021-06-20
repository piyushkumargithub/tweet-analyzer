import streamlit as st
import tweepy
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
#import config
from functions import *
import json



consumerKey = st.secrets.consumerKey
consumerSecret = st.secrets.consumerSecret
accessToken = st.secrets.accessToken
accessTokenSecret =st.secrets.accessTokenSecret





try:
    #Create the authentication object
    authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

    # Set the access token and access token secret
    authenticate.set_access_token(accessToken, accessTokenSecret)

    # Creating the API object while passing in auth information
    api = tweepy.API(authenticate, wait_on_rate_limit = True)
    api.verify_credentials()
    st.write("Connected to twitter")

except:
    st.write("Error during connection with twitter")




#plt.style.use('fivethirtyeight')







def app(choice):


    st.title("Twitter Activity Analyzer")









    if choice=="Tweet Analyzer":

        st.subheader("Analyze the tweets of some famous personalities")

        st.subheader("Following are the tasks performed: ")

        st.write("1. Fetches the 5 most recent tweets from the provided twitter handel")
        st.write("2. Generates a Word Cloud from the recent tweets")
        st.write("3. Performs Sentiment Analysis")





        raw_text = st.text_area("Enter the exact twitter handle of the Personality (with or without @)")



        st.markdown("You can select different activities from the selectbox")

        Analyzer_choice = st.selectbox("Select the Activities",  ["Show Recent Tweets","Generate WordCloud" ,"Visualize the Sentiment Analysis"])


        if st.button("Analyze"):


            if Analyzer_choice == "Show Recent Tweets":

                st.success("Fetching last 5 Tweets")


                def Show_Recent_Tweets(raw_text):

                    # Extract 5 tweets from the twitter user
                    posts = api.user_timeline(screen_name=raw_text, count = 5, lang ="en", tweet_mode="extended")


                    def get_tweets():

                        l=[]
                        i=1
                        for tweet in posts[:5]:
                            l.append(str(i)+". "+tweet.full_text+"\n")
                            i+=1
                        return l

                    recent_tweets=get_tweets()
                    return recent_tweets

                recent_tweets= Show_Recent_Tweets(raw_text)

                st.write("\n".join(recent_tweets))



            elif Analyzer_choice=="Generate WordCloud":

                st.success("Generating the Word Cloud")

                def gen_wordcloud():

                    posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")


                    # Create a dataframe with a column called Tweets
                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


                    # Clean the tweets
                    df['Tweets'] = df['Tweets'].apply(cleanTxt)


                    # word cloud visualization
                    allWords = ' '.join([twts for twts in df['Tweets']])
                    wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
                    plt.imshow(wordCloud, interpolation="bilinear")
                    plt.axis('off')
                    plt.savefig('WC.jpg')
                    img= Image.open("WC.jpg")
                    return img

                img=gen_wordcloud()

                st.image(img)



            else:




                def Plot_Analysis():

                    st.success("Generating Visualization for Sentiment Analysis")




                    posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])



                    # Clean the tweets by applying functions from functions module
                    df['Tweets'] = df['Tweets'].apply(cleanTxt)




                    # Create two new columns 'Subjectivity' & 'Polarity' by applying functions from functions module
                    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
                    df['Polarity'] = df['Tweets'].apply(getPolarity)


                    # create a new column based on polarity score by applying functions from functions module
                    df['Analysis'] = df['Polarity'].apply(getAnalysis)


                    return df



                df= Plot_Analysis()



                st.write(sns.countplot(x=df["Analysis"],data=df))


                st.pyplot(use_container_width=True)





    elif choice=="Generate Twitter Data":

        st.subheader("This tool fetches the tweets from the twitter handel & Performs the following tasks")

        st.write("1. Converts it into a DataFrame")
        st.write("2. Cleans the text")
        st.write("3. Analyzes Subjectivity of tweets and adds an additional column for it")
        st.write("4. Analyzes Polarity of tweets and adds an additional column for it")
        st.write("5. Analyzes Sentiments of tweets and adds an additional column for it")






        user_name = st.text_area("*Enter the exact twitter handle of the Personality (without @)*")

        st.markdown("<--------     Also Do checkout the another cool tool from the sidebar")

        count=st.slider("How many tweets to fetch",min_value=10,max_value=100)


        def get_data(user_name,count):

            posts = api.user_timeline(screen_name=user_name, count = count, lang ="en", tweet_mode="extended")

            df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

            # Clean the tweets
            df['Tweets'] = df['Tweets'].apply(cleanTxt)

            # Create two new columns 'Subjectivity' & 'Polarity' by applying functions from functions module
            df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
            df['Polarity'] = df['Tweets'].apply(getPolarity)

            # create a new column based on polarity score by applying functions from functions module
            df['Analysis'] = df['Polarity'].apply(getAnalysis)
            return df


        if st.button("Show Data"):

            st.success(f"Fetching Last {count} Tweets")

            df=get_data(user_name,count)

            st.write(df)




    # if watch trending is used
    elif choice=="Watch trending":
        st.subheader("To see what is trending around")

        #country with woeid
        country={"World":1,"India":23424848,"US":23424977,"Germany":23424829,"Australia":23424748,"UK":23424975}

        choosen_country=st.selectbox("Choose location",list(country.keys()))

        location=country[choosen_country]



        trend_count=st.slider("How many top tweets to fetch",min_value=5,max_value=20)
        trends_result = api.trends_place(location)
        if st.button("Show top {} trending".format(trend_count)):
            li=list()
            i=1
            for trend in trends_result[0]["trends"][:trend_count]:
                li.append(str(i)+". "+cleanTxt(trend["name"]))
                i+=1
            st.write("\n\n".join(li))


        def genWordCloud():
            li=list()
            for trend in trends_result[0]["trends"][:50]:
                li.append(cleanTxt(trend["name"]))

            str=" ".join(li)
            res_list = [s for s in re.split("([A-Z][^A-Z]*)", str) if s]
            # word cloud visualization
            allWords = ' '.join(res_list)
            wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
            plt.imshow(wordCloud, interpolation="bilinear")
            plt.axis('off')
            plt.savefig('WC.jpg')
            img= Image.open("WC.jpg")
            return img



        if st.button("Make word cloud of trending topics"):
            img=genWordCloud()
            st.image(img)

    st.subheader(':sunglasses: ------------------- Made By SM,PKS and TT ----------------- :sunglasses:')































if __name__ == "__main__":
    app()
