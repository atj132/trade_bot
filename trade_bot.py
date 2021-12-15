import krakenex
import numpy as np
from pykrakenapi import KrakenAPI
import time


class bot:

    def __init__(self,coin):
        
        self.coin = coin
        self.starting_balance = 500
        self.balance = self.starting_balance
        self.mode = 'buy'
        self.cbalance = 0
        self.profit = 0
        self.period = 14
        self.values = []
        self.rsi_values = []
        self.price = 0
        self.k_values = []
        
        

    def get_price(self,kraken):

        
        
        self.price = float((kraken.get_ticker_information(self.coin.upper() + 'USD'))['c'][0][0])
        
        decide = self.alg()

        return decide

        

    def trade(self,kraken):

        print(self.mode + 'ing ' + self.coin)

        
        if self.mode == 'buy':


            self.cbalance = (self.balance- 0.0026*self.balance)/self.price
            self.mode = 'sell'

            

            

        else:
            self.mode = 'buy'

            amount = self.price*(self.cbalance-0.0026*self.cbalance)

            

            print('Profit of ' + str(100*(amount-self.balance)/self.balance)+'%')
            print('Now have: $' + str(amount))

            self.balance = amount

            self.profit = str(100*(amount-self.starting_balance)/self.starting_balance)
            

            

            



    def alg(self):
        

        self.values.append(self.price)

        if len(self.values) < 20:
            return False
        if len(self.values) > 20:
            self.values = self.values[1:]


        differences = []

        avg = np.average(self.values)
        std = np.std(self.values)

        upper = avg + 2*std
        lower = avg - 2*std
        
        
        for i in range(14):
            diff = (self.values[i] - self.values[i+1])/self.values[i]
            differences.append(diff)

        

        avg_gain = 0
        avg_loss = 0
        gain_count = 0
        loss_count = 0

        for i in differences:
            if i > 0:
                gain_count += 1
                avg_gain += i


            else:
                loss_count += 1
                avg_loss += i

        if loss_count >0:

            avg_loss = -avg_loss/loss_count
            
            if gain_count > 0:
                avg_gain = avg_gain/gain_count

            if avg_loss > 0:

                rsi = 100 - 100/(1+(avg_gain/avg_loss))

            else:
                rsi = 100
        
            
        else:
            
            rsi = 100

        


        up_limit = 70
        low_limit = 30

        self.rsi_values.append(rsi)

        if len(self.rsi_values) < 14:
            return False
        if len(self.rsi_values) > 14:
            self.rsi_values = self.rsi_values[1:]

        min_rsi = min(self.rsi_values)
        max_rsi = max(self.rsi_values)

        if max_rsi != min_rsi:

            stoch_rsi = 100*(rsi-min_rsi)/(max_rsi-min_rsi)

        else:
            return False

        

        self.k_values.append(stoch_rsi)

        if len(self.k_values) < 3:
            return False
        if len(self.k_values) > 3:
            self.k_values = self.k_values[1:]

        D = sum(self.k_values)/3

        
        

        
                


        if self.mode == 'buy':

            if (stoch_rsi >= D and stoch_rsi <= low_limit) and self.price <= lower:
                return True
            else:
                return False

        else:

            

            

            if (stoch_rsi <= D and stoch_rsi >= up_limit) and self.price >= upper:
                return True
            else:
                return False

            
        

        

        
        

        


























        
