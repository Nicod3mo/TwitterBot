import tweepy, time
import random
from pycoingecko import CoinGeckoAPI
from xd import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
import requests

cg = CoinGeckoAPI()
nombreUsuario = "@musthavean"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
mentions = api.mentions_timeline()
secs=10
ARCHIVO = 'ultima_id.txt'
phrasesJson = requests.get("https://philosophy-quotes-api.glitch.me/quotes").json()

def devolver_ultima_id(ARCHIVO):
    f_read = open(ARCHIVO, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def guardar_ultima_id(ultima_id, ARCHIVO):
    f_write = open(ARCHIVO, 'w')
    f_write.write(str(ultima_id))
    f_write.close()
    return

def responderTweets():
    print('espera...', flush=True)
    ultima_id = devolver_ultima_id(ARCHIVO)
    mentions = api.mentions_timeline(ultima_id,tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        ultima_id = mention.id
        guardar_ultima_id(ultima_id, ARCHIVO)

        if nombreUsuario in mention.full_text.lower():
            #45 citas distintas
            citaRand = random.randint(0, 45)
            btc=cg.get_coin_by_id(id='bitcoin')
            eth=cg.get_coin_by_id(id='ethereum')

            print('Mention found!', flush=True)
            print('responding...', flush=True)
            statusTweet = str('@' + str(mention.user.screen_name) + " \"" + phrasesJson[citaRand]['quote'] + "\"\n -" + phrasesJson[citaRand]['source'] + "\n\n" + 'btc: $' + str(btc['market_data']['current_price']['usd']) + ' eth: $' + str(eth['market_data']['current_price']['usd']))
            api.update_status(statusTweet, in_reply_to_status_id=mention.id)

while True:
    responderTweets()
    time.sleep(secs)