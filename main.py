from dublinBusTweeter import busScraper
from dublinBusTweeter import tweeter
from dublinBusTweeter.busScraper import busStops
from auth import bus_stops
import time

monitoredBusStops = busStops(bus_stops)  # Monitor the Bus Stops defined in the auth.py config file

print("Start Monitor")
while True:
    monitoredBusStops.printTweets()  # Print the tweets
    monitoredBusStops.tweet()  # Tweet the tweets
    time.sleep(30)  # Wait 30 seconds
