# Opensea Sales tracker bot 

Twitter sales bot deploy opn opense V2 api and twitter V2 API KEY, this bot track the collections sales on opensea and post it on X(Formal Twitter), after every 60 sec its fetch data from opensea api if any sales made it will post on X(Formal Twitter). There is duplicate tweet checker which see if same tweet made already it return duplicate Tweet if not it post the tweet, function is local checker its added becauce twitter api have limit so if its continue checking by calling api of twitter there is chance to get rate limit.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python 3.x
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) (for deployment)

### Installing

1. Clone the repository:

```bash
git clone https://github.com/zenoUsman/opensea-sales-tracker-Twitter.git
cd opensea-sales-tracker-Twitter

2. Install dependencies 
pip install -r requirements.txt


3.Create a .env file in the project root and add the necessary environment variables:
BEARER_TOKEN=your_twitter_bearer_token
CONSUMER_KEY=your_twitter_consumer_key
CONSUMER_SECRET=your_twitter_consumer_secret
ACCESS_TOKEN_KEY=your_twitter_access_token_key
ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
X_API_KEY=your_opensea_api_key

4. Update the Procfile with your script name:
web: python your_script_name.py

5. Run the Flask app locally with the following command:
python your_script_name.py
Visit http://localhost:5000 in your browser to view the app.

6. Deployment
Deploy your app to Heroku following these steps:

Create a Heroku account if you don't have one.
Log in to Heroku in the terminal:

command: heroku login
1.1 Create a new Heroku app:
command: heroku create
1.2 Push your code to Heroku:
command: git push heroku master
1.3 Open your deployed app:
command: heroku open
