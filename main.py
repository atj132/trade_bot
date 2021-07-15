import trade_bot as tb
import time
import krakenex
from pykrakenapi import KrakenAPI
import keyboard


api = krakenex.API()
kraken = KrakenAPI(api)


#list of crypto to use
crypto_list = ('btc','eth','ada','doge','xrp','dot','uni','bch','sol','ltc')

#time between looking at prices
wait_time = 1

path = 'C:/Users/Austin/Desktop/trading bot/coins/'

for i in crypto_list:
    file = open(path + i + '/current_data.txt','w')
    file.close()

for i in crypto_list:
    file = open(path + i + '/all_data.txt','w')
    file.close()


stop = False
def onkeypress(event):
    global stop
    if event.name == '=':
        stop = True

keyboard.on_press(onkeypress)

def cash_out(cryptos):

    print('Cashing out')

    coins = cryptos

    rem_coins = 0


    while rem_coins < 10:

        for j in coins:
            
            trader = tb.bot(j)
            if trader.mode == 'buy':
                rem_coins += 1

            else:
                if trader.get_price(kraken):
                    trader.trade(kraken)

            time.sleep(wait_time)

        
        rem_coins = 0

        


    print('Cashed Out')




while 1==1:

    try:
        for i in crypto_list:
            trader = tb.bot(i)
        
            if trader.get_price(kraken):
                trader.trade(kraken)

            time.sleep(wait_time)
        if stop:
            cash_out(crypto_list)
            break

        




            
    except:
        break











    
    
