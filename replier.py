import tweepy, time
import random
from pycoingecko import CoinGeckoAPI
from xd import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET

cg = CoinGeckoAPI()
nombreUsuario = "@musthavean"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
mentions = api.mentions_timeline()
secs=10
ARCHIVO = 'ultima_id.txt'

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
    print('banca wacho...', flush=True)
    ultima_id = devolver_ultima_id(ARCHIVO)
    mentions = api.mentions_timeline(ultima_id,tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        ultima_id = mention.id
        guardar_ultima_id(ultima_id, ARCHIVO)

        if nombreUsuario in mention.full_text.lower():
            iq=str(random.randint(80,120))
            btc=cg.get_coin_by_id(id='bitcoin')
            eth=cg.get_coin_by_id(id='ethereum')

            print('ahi vamos', flush=True)
            print('respondiendo...', flush=True)
            api.update_status('@'+str(mention.user.screen_name)+' hola, tu iq es de ' + iq + ', el bitcoin (dato no menor) esta: $' + str(btc['market_data']['current_price']['usd']) + ' y el ether: $' + str(eth['market_data']['current_price']['usd']), in_reply_to_status_id=mention.id)

while True:
    responderTweets()
    time.sleep(secs)