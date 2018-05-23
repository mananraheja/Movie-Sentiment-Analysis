# libraries to include
import re
import tweepy
import matplotlib.pyplot as plt
from tweepy import OAuthHandler
from textblob import TextBlob
import pandas as pd
from youtube import youtube_search
import omdb  # to access imdb API
import pandas as pd  # for data array handling
from bs4 import BeautifulSoup  # for website parsing and scraping (rotten tomatoes)
import requests  # for http access
import numpy as np

# making a generic twitter class for sentiment analysis
class TwitterClient(object):
    
    # class constructor
    def __init__(self):
        
        # keys and tokens from the developer console
        consumer_key = 'nEO5EZpVBNe1NuZ0H0Hpkqae3'
        consumer_secret = '6uxcNCxHZWR9X9fji6uRn8LA3s1JTscf2vg89mkCYbkZY4JUTT'
        access_token = '298403978-dFLlbaYtt62pA8FlrJUonGI1lLvLGWbsMpMRnOS9'
        access_token_secret = 'Dmoo99m4tV4u6lmxEoZvbSO3dyUsMVKGBwQnxWtzzP9uf'
        
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        
        except:
            print("Error: Authentication Failed!")
    
    def clean_tweet(self, tweet):
        # utility function to clean tweets by removing hyperlinks, special characters etc using regex
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    # main function to get tweets and parse them
    def get_tweet_sentiment(self, tweet):
        
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        
    def get_tweets(self, query, count = 10):
        
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

def youtube()        
    test = youtube_search("Deadpool 2: The Final Trailer")
    df = pd.DataFrame(data=test)
    df.head()

    df1 = df[['title','viewCount','channelTitle','commentCount','likeCount','dislikeCount','tags','favoriteCount','videoId','channelId','categoryId']]
    df1.columns = ['Title','viewCount','channelTitle','commentCount','likeCount','dislikeCount','tags','favoriteCount','videoId','channelId','categoryId']
    #assigning column names
    df1.head()

    #import numpy as np
    numeric_dtype = ['viewCount','likeCount','dislikeCount']
    for i in numeric_dtype:
        df1[i] = df[i].astype(int)

    movie = df1[df1['Title']=='Deadpool 2: The Final Trailer']
    movie.head()

    pos, neg, neut = 0, 0, 0
    positive = df1['likeCount']
    Negative = df1['dislikeCount']
    total    = df1['viewCount']

    #summing the list
    for i in range(len(positive)):
        pos += positive[i]
        neg += Negative[i]
        neut += (total[i] - positive[i] - Negative[i])

    total = pos+ neg + neut
    pos = 100 * pos / total
    neg = 100 * neg / total
    neut = 100 * neut / total
    slices = [pos + 0.6*neut, neg+ 0.4*neut]
    cols = ['gold','red']
    feedback = ['Positive Review','Negative Review']
    plt.pie(slices, labels = feedback, colors = cols, startangle = 90, shadow = True, explode = (0.1, 0.1), autopct = '%1.1f%%')
    plt.axis('equal')
    plt.title('Sentiment Pie Chart')
    plt.show()
    res=[pos+0.6*neut,neg+0.4*neut,pos+neg+neut]
    return res

def rotten_tomatoes()
    title = "Deadpool 2"
    tomato_base_url = 'https://www.rottentomatoes.com/m/'
    tomato_url = tomato_base_url + re.sub(':', '', re.sub(' ', '_', title))
    soup = BeautifulSoup(requests.get(tomato_url).text)  # rotten tomatoes: website parse tree

    s = str(soup.find('span', {'class': 'superPageFontColor'}).contents[0])

    RT_user_rating = int(re.findall(r'\d+', s)[0])
    RT_prof_score = int(min(soup.find('span', {'class': 'meter-value superPageFontColor'}).contents[0]))
    print(RT_prof_score)

    rt_user_neg = 100 - RT_user_rating
    rt_prof_neg = 100 - RT_prof_score
    labels = 'user_pos', 'user_neg'

    sizes = RT_user_rating, rt_user_neg
    cols = ['gold', 'red']
    feedback = ['positive reviews', 'negative reviews']
    explode = (0.1, 0.1)
    plt.pie(sizes, explode=explode, colors=cols, startangle=90, shadow=True)
    plt.axis('equal')
    plt.title('sentiments')
    plt.show()

    sizes = RT_prof_score, rt_prof_neg
    cols = ['green', 'blue']
    feedback = ['positive reviews', 'negative reviews']
    explode = (0.1, 0.1)
    plt.pie(sizes, explode=explode, colors=cols, startangle=90, shadow=True)
    plt.axis('equal')
    plt.title('sentiments')
    plt.show()
    result=[(RT_user_rating+RT_prof_score)/200,(rt_user_neg+RT_prof_neg)/200]
    return result

# Main Driver Function
if __name__ == "__main__":
    # creating object of TwitterClient class
    api = TwitterClient()
    
    # calling function to get tweets
    tweets = api.get_tweets(query = 'Deadpool 2', count = 200000000)
    
    # picking positive tweets from tweeats
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    
    # picking -ve tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    
    # percentage of +ve tweets
    print("Positive Tweets Percentage: {} %".format(100*(len(ptweets))/(len(ntweets) + len(ptweets))))
    
    # percentage of -ve tweets
    print("Negative Tweets Percentage: {} %".format(100*len(ntweets)/(len(ptweets) + len(ntweets))))
    
    # making a Pie Chart for the data
    positives = 100 * (0.6 * (len(tweets) - len(ptweets) - len(ntweets)) + len(ptweets)) / len(tweets)
    negatives = 100 * (0.4 * (len(tweets) - len(ptweets) - len(ntweets)) + len(ntweets)) / len(tweets)

    slices = [positives, negatives]
    cols = ['g','r']
    feedback = ['Positive Review','Negative Review']
    plt.pie(slices, labels = feedback, colors = cols, startangle = 90, shadow = True, explode = (0.1, 0.1), autopct = '%1.1f%%')
    plt.title('Sentiment Pie Chart')
    plt.show()
    twitter_result=[positives,negatives,positives+negatives]

    youtube_result=youtube()

    rotten_tomatoes=rotten_tomatoes()

    final_result=twitter_result+youtube_result

    final_result_percentage=[final_result[0]/final_result[2],final_result[1]/final_result[2]]

    final_percentages=[(final_result_percentage[0]+rotten_tomatoes[0])/200,(final_result_percentage[1]+rotten_tomatoes[1])/200]

    feedback = ['Final Positive Review','Final Negative Review']
    plt.pie(final_percentages, labels = feedback, colors = cols, startangle = 90, shadow = True, explode = (0.1, 0.1), autopct = '%1.1f%%')
    plt.title('Sentiment Pie Chart')
    plt.show()
