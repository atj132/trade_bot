import krakenex
import numpy as np
from pykrakenapi import KrakenAPI


class bot:

    def __init__(self,coin):
        
        self.coin = coin
        self.path = 'C:/Users/Austin/Desktop/trading bot/coins/'  + coin
        self.balance_file = open(self.path + '/balance.txt','r')
        self.balance = float(self.balance_file.read())
        self.mode_file = open(self.path + '/mode.txt','r')
        self.mode = self.mode_file.read()
        self.cbalance_file = open(self.path + '/cbalance.txt','r')
        self.cbalance = float(self.cbalance_file.read())
        

        self.buy_file = open(self.path + '/last_buy.txt','r')
        self.last_buy = float(self.buy_file.read())
        self.buy_file.close()

        self.price = 0


    def get_price(self,kraken):

        


        self.price = float((kraken.get_ticker_information(self.coin.upper() + 'USD'))['b'][0][0])
        
        decide = self.alg()

        return decide

        

    def trade(self,kraken):

        print(self.mode + 'ing ' + self.coin)

        
        if self.mode == 'buy':


            camount = (self.balance- 0.0016*self.balance)/self.price 

            self.mode_file.close()
            self.mode_file = open(self.path + '/mode.txt','w')
            self.mode_file.write('sell')
            self.mode_file.close()
            self.balance_file.close()
            self.balance_file = open(self.path + '/balance.txt','w')
            self.balance_file.write('0')
            self.balance_file.close()
            self.cbalance_file.close()
            self.cbalance_file = open(self.path + '/cbalance.txt','w')
            self.cbalance_file.write(str(camount))
            self.cbalance_file.close()

            self.buy_file = open(self.path + '/last_buy.txt','w')
            self.buy_file.write(str(self.price))
            self.buy_file.close()

            
            

        else:

            amount = self.price*(self.cbalance-0.0016*self.cbalance) 

            print('Profit of ' + str(100*(self.price-self.last_buy)/self.last_buy)+'%')

            self.mode_file.close()
            self.mode_file = open(self.path + '/mode.txt','w')
            self.mode_file.write('buy')
            self.mode_file.close()
            self.balance_file.close()
            self.balance_file = open(self.path + '/balance.txt','w')
            self.balance_file.write(str(amount))
            self.balance_file.close()
            self.cbalance_file.close()
            self.cbalance_file = open(self.path + '/cbalance.txt','w')
            self.cbalance_file.write('0')
            self.cbalance_file.close()

            

            



    def alg(self):

        

        

        values_file = open(self.path + '/current_data.txt','r')
        values = values_file.read().split(',')
        values_file.close()
        

        


        values_file = open(self.path + '/current_data.txt','w')

        if len(values)> 180*2:
            values.remove(values[0])
            

        for i in values:

            if i != '':
                values_file.write(str(i)+',')

        values_file.write(str(self.price))
                
        values_file.close()

        values.append(self.price)

        if len(values)< 10:
            return False

        for i in range(len(values)):
            values[i] = float(values[i])
            

        

        


        
        

        avg = np.average(values)
        std = np.std(values)

        

        upper = avg + std
        lower = avg - 2.5*std

        

        

        if self.mode == 'buy':
            if self.price <= lower and (upper - lower)/lower >= 0.0035:
                return True

            else:
                return False

        else:
            if (self.price-self.last_buy)/self.last_buy >= 0.0035:
                return True

            else:
                return False
            

        

        

        
        
        
        

            
        

        

        
        

        


























        
