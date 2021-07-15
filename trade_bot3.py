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
        self.buy = 0


    def get_price(self,kraken):

        


        self.price = float((kraken.get_ticker_information(self.coin.upper() + 'USD'))['c'][0][0])
        
        decide = self.alg()

        return decide

        

    def trade(self,kraken):

        


        if self.mode == 'buy':
            self.mode_file.close()

            buying = kraken.add_standard_order(pair = self.coin.upper() + 'USD',type = 'buy',ordertype = 'limit',volume = str(self.balance/self.price),price =  str(self.buy),offlags = 'post')
            self.buy_file = open(self.path + '/last_buy.txt','w')
            self.buy_file.write(str(self.buy))
            self.buy_file.close()
            self.mode_file = open(self.path + '/mode.txt','w')
            self.mode_file.write('trade')
            self.mode_file.close()

            order_file = open(self.path+'\buy_info.txt','w')
            order_file.write(buying['txid'][0])
            order_file.close()
            

            

        
        elif self.mode == 'trade':

            self.buy_file = open(self.path + '/last_buy.txt','r')
            self.buy = self.buy_file.write(str(self.buy))
            self.buy_file.close()


            camount = (self.balance- 0.0016*self.balance)/self.last_buy

            selling = kraken.add_standard_order(pair = self.coin.upper() + 'USD',type = 'sell',ordertype = 'limit',volume = camount,price =  str(self.last_buy + self.last_buy*0.0035),offlags = 'post')

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

            sell_file = open(self.path + '/last_sell.txt','w')
            sell_file.write(str(self.last_buy + self.last_buy*0.0035))
            sell_file.close()

            order_file = open(self.path+'/sell_info.txt','w')
            order_file.write(selling['txid'][0])
            order_file.close()

            
            

        else:

            sell_file = open(self.path + '/last_sell.txt','r')
            last_sell = sell_file.read()
            sell_file.close()

            amount = last_sell*(self.cbalance-0.0016*self.cbalance) 

            print('Profit of ' + str(100*(last_sell-self.last_buy)/self.last_buy)+'%')

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

        if len(values)< 50:
            return False

        for i in range(len(values)):
            values[i] = float(values[i])
            

        

        


        
        

        avg = np.average(values)
        std = np.std(values)

        

        upper = avg + std
        lower = avg - 2.5*std

        

        

        

        if self.mode == 'buy':
            if (upper - lower)/lower >= 0.0035:
                self.buy = avg - 2.7*std
                return True

            else:
                return False

        elif self.mode == 'trade':

            order_file = open(self.path+'\buy_info.txt','r')
            order_info = order_file.read()
            order_file.close()

            check_order = kraken.query_orders_info(order)
            
            if check_order == 'closed':
                return True

            else:
                return False

        else:

            order_file = open(self.path+'\sell_info.txt','r')
            order_info = order_file.read()
            order_file.close()

            check_order = kraken.query_orders_info(order)

            
            if check_order == 'closed':
                return True

            else:
                return False

        

        

        
        
        
        

            
        

        

        
        

        


























        
