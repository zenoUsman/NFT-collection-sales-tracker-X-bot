from flask import Flask, jsonify
import tweepy
import requests
from datetime import datetime, timedelta
from pytz import UTC
from dotenv import load_dotenv
from time import sleep
from urllib.parse import quote
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN_KEY")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
opensea_api_key = os.getenv("X_API_KEY")

# Authenticate with Twitter using tweepy.Client
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True
)
posted_tweets = set()

# Function to check if a tweet is a duplicate
def is_duplicate_tweet(tweet_text):
    return tweet_text in posted_tweets

# Function to format and send tweet
def format_and_send_tweet(event):
    asset = event.get('nft', {})
    asset_name = asset.get('name', 'Unknown Asset')
    opensea_link = asset.get('opensea_url', '')

    total_price = event.get('payment', {}).get('quantity', 0)

    # Convert total_price to float if it's a string
    if isinstance(total_price, str):
        total_price = float(total_price)

    total_price_in_eth = total_price / 1e18  # Convert total price to Ether

    asset_symbol = event.get('payment', {}).get('symbol', 'Matic')

    # Use current time if 'created_date' is not available in the API response
    created = datetime.now(UTC)

    # Use quote from urllib.parse
    opensea_link = quote(opensea_link)

    tweet_text = f"{asset_name} bought for ({total_price_in_eth} {asset_symbol}) {opensea_link}"

    if not is_duplicate_tweet(tweet_text):
        try:
            # Post tweet using tweepy.Client
            tweet = client.create_tweet(text=tweet_text)
            print("Tweet created successfully:", tweet_text)

            # Add the tweet content to the set of posted tweets
            posted_tweets.add(tweet_text)
        except tweepy.TweepError as te:
            print(f"Error creating tweet: {te}")
    else:
        print("Duplicate content. Skipping tweet.")

# Poll OpenSea every 60 seconds & retrieve all sales for a given collection
# in either the time since the last sale OR in the last minute
def poll_opensea():
    last_sale_time = datetime.now(UTC) - timedelta(seconds=59)
    max_retries = 5  # Maximum number of retries
    specific_unix_timestamp = 1704945107

    while max_retries > 0:
        try:
            response = requests.get(
                f"https://api.opensea.io/api/v2/events/collection/cool-bullz-2?after={int(last_sale_time.timestamp())}&event_type=sale",
                headers={"X-API-KEY": opensea_api_key},
            )
            response.raise_for_status()
            
            events = response.json().get('asset_events', [])

            sorted_events = sorted(events, key=lambda x: x.get('created_date', ''))

            print(f"{len(events)} sales since the last one...")

            for event in sorted_events:
                format_and_send_tweet(event)

        except requests.RequestException as re:
            print(f"Error in OpenSea API request: {re}")
            max_retries -= 1
            
            sleep(10)
            continue

        # Sleep for 60 seconds before the next iteration
        sleep(60)

    print("Max retries reached. Exiting.")

# Define Flask routes
@app.route("/")
def home():
    return "Flask app is running!"

@app.route("/start_polling")
def start_polling():
    poll_opensea()
    return "Polling started!"

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
