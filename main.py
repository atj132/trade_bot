import trade_bot as tb
import time
import krakenex
from pykrakenapi import KrakenAPI
import keyboard


api = krakenex.API()
kraken = KrakenAPI(api)


#list of crypto to use
crypto_list = ['btc','eth','ada','doge','xrp','dot','uni','bch','sol','ltc']

bot1 = tb.bot(crypto_list[0])
bot2 = tb.bot(crypto_list[1])
bot3 = tb.bot(crypto_list[2])
bot4 = tb.bot(crypto_list[3])
bot5 = tb.bot(crypto_list[4])
bot6 = tb.bot(crypto_list[5])
bot7 = tb.bot(crypto_list[6])
bot8 = tb.bot(crypto_list[7])
bot9 = tb.bot(crypto_list[8])
bot10 = tb.bot(crypto_list[9])

bot_list = [bot1,bot2,bot3,bot4,bot5,bot6,bot7,bot8,bot9,bot10]


#time between looking at prices
wait_time = 6



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

        rem_coins = 0

        for j in coins:
            
            
            if j.mode == 'buy':
                rem_coins += 1

            else:
                if j.get_price(kraken):
                    j.trade(kraken)

            time.sleep(wait_time)

        
        

        


    print('Cashed Out')
    for i in coins:
        print("----------")
        print(i.coin + " stats")
        print("Final balance: "+str(i.balance))
        print("Final profit: " +i.profit)
        


while 1==1:

    try:
        for i in bot_list:
            
        
            if i.get_price(kraken):
                i.trade(kraken)

            time.sleep(wait_time)
        if stop:
            cash_out(bot_list)
            break

        




            
    except:
        print('oops')
        break











    
    
