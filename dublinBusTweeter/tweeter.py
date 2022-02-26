from os import path
import tweepy
from tkinter import *


# This saves the auth file created during installation
def saveFile():
    consumer_key = entry_consumer_key.get()
    consumer_secret = entry_consumer_secret.get()
    bearer_token = entry_bearer_token.get()
    access_token = entry_access_token.get()
    access_token_secret = entry_access_token_secret.get()
    bus_stops = entry_Bus_Stops.get()
    f = open("auth.py", "w")
    f.write("consumer_key = \"" + str(consumer_key) + "\"\n")
    f.write("consumer_secret = \"" + str(consumer_secret) + "\"\n")
    f.write("bearer_token = \"" + str(bearer_token) + "\"\n")
    f.write("access_token = \"" + str(access_token) + "\"\n")
    f.write("access_token_secret  = \"" + str(access_token_secret) + "\"\n")
    f.write("bus_stops = \"" + str(bus_stops) + "\"")
    f.close()
    root.quit()


# Tweets out a message
def tweet(message):
    client = tweepy.Client(consumer_key=consumer_key,
                           consumer_secret=consumer_secret,
                           access_token=access_token,
                           access_token_secret=access_token_secret)
    try:
        response = client.create_tweet(text=message)
    except:
        print("Duplicate Tweet")


# Not used (maybe in the next version)
def get_tweet(user):
    client = tweepy.Client(bearer_token)
    query = 'from:' + user
    tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],
                                         max_results=100)
    for tweet in tweets.data:
        return tweet.text


# Breaks Tweets up
def splitIntoTweet(header, x):
    X = 1
    combineItems = "Tweet " + str(X) + "/Y for " + header + "\n"
    tweets = []
    for item in x:
        combineItems += item
        combineItems += "\n"
        currentSize = len(combineItems)
        if currentSize > 240:
            combineItems.replace(item, "")
            tweets.append(combineItems)
            X += 1
            combineItems = "Tweet " + str(X) + "/Y for " + header + "\n"
    for n in range(len(tweets)):
        tweets[n] = tweets[n].replace("Y", str(X - 1))
    tweets.reverse()
    return tweets


# Installation
# Creates a window that asks for KEYS and STOPS to monitor
if not path.exists("auth.py"):
    root = Tk()
    root.geometry("320x200")
    root.title("Installing")

    label_consumer_key = Label(root, text="Consumer Key: ")
    label_consumer_key.grid(row=0, column=0)
    entry_consumer_key = Entry(root, width=30)
    entry_consumer_key.grid(row=0, column=1)

    label_consumer_secret = Label(root, text="Consumer Secret: ")
    label_consumer_secret.grid(row=1, column=0)
    entry_consumer_secret = Entry(root, width=30)
    entry_consumer_secret.grid(row=1, column=1)

    label_access_token = Label(root, text="Access Token: ")
    label_access_token.grid(row=2, column=0)
    entry_access_token = Entry(root, width=30)
    entry_access_token.grid(row=2, column=1)

    label_access_token_secret = Label(root, text="Access Token Secret: ")
    label_access_token_secret.grid(row=3, column=0)
    entry_access_token_secret = Entry(root, width=30)
    entry_access_token_secret.grid(row=3, column=1)

    label_bearer_token = Label(root, text="Bearer Token: ")
    label_bearer_token.grid(row=4, column=0)
    entry_bearer_token = Entry(root, width=30)
    entry_bearer_token.grid(row=4, column=1)

    label_Bus_Stops = Label(root, text="Bus Stops To Monitor: ")
    label_Bus_Stops.grid(row=5, column=0)
    entry_Bus_Stops = Entry(root, width=30)
    entry_Bus_Stops.grid(row=5, column=1)

    ButtonSaveAndExit = Button(root, text="Save And Exit", command=saveFile)
    ButtonSaveAndExit.grid(row=6, column=1)

    root.mainloop()
else:
    from auth import *
