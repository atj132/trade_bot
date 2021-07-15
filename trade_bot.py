import krakenex
import numpy as np
import matplotlib.pyplot as plt
from pykrakenapi import KrakenAPI
import time


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

        


    def get_price(self,kraken):

        


        self.price = float((kraken.get_ticker_information(self.coin.upper() + 'USD'))['c'][0][0])
        
        decide = self.alg()

        return decide

        

    def trade(self,kraken):

        print(self.mode + 'ing ' + self.coin)

        
        if self.mode == 'buy':


            camount = (self.balance- 0.0026*self.balance)/self.price 

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

            values_file = open(self.path + '/current_data.txt','w')
            values_file.write(str(self.price))
            values_file.close()

            

        else:

            amount = self.price*(self.cbalance-0.0026*self.cbalance) 

            print('Profit of ' + str(100*(self.price-self.last_buy)/self.last_buy)+'%')
            print('Now have: $' + str(amount))

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

            values_file = open(self.path + '/current_data.txt','w')
            values_file.write(str(self.price))
            values_file.close()

            



    def alg(self):

        

        all_data_file = open(self.path + '/all_data.txt','r')
        all_data = all_data_file.read().split(',')
        all_data_file.close()

        values_file = open(self.path + '/current_data.txt','r')
        values = values_file.read().split(',')
        values_file.close()

        all_data_file = open(self.path + '/all_data.txt','w')      


        values_file = open(self.path + '/current_data.txt','w')

        if len(all_data)> 180:
            all_data.remove(all_data[0])

        for i in all_data:

            if i != '':
                all_data_file.write(str(i)+',')

        for i in values:

            if i != '':
                values_file.write(str(i)+',')

        

        all_data.append(self.price)

        for i in range(len(all_data)):
            if all_data[i] != '':
                all_data[i] = float(all_data[i])
        for i in range(len(values)):
            if values[i] != '':
                values[i] = float(values[i])

        if len(all_data) > 170:
            
            avg = np.average(all_data)
            values.append(avg)

            values_file.write(str(avg))

            
        all_data_file.write(str(self.price))
                
        values_file.close()
        all_data_file.close()

        
    
        

        if len(values) <3:

            
            return False

        for i in range(len(all_data)):
            all_data[i] = float(all_data[i])

        
        


        y_values = np.array(values).astype(float)

        

        x_values = np.array(range(len(y_values)))

        
        fit = np.polyfit(x_values,y_values,2)

        crit_point_x = -fit[1]/(2*fit[0])

        rd_deriv = fit[0]

        nd_deriv = fit[1]

        crit_point_y = fit[0]*crit_point_x**2 + fit[1]*crit_point_x + fit[2]

        
        

        

        if self.mode == 'buy':

            if rd_deriv <= 0:

                values_file = open(self.path + '/current_data.txt','w')

                for i in x_values:
                    if i > len(values)/2:
                        values_file.write(str(values[i-1]) + ',')
                        
                
                values_file.write(str(self.price))
                values_file.close()
 

                return False


        

           
            
            elif crit_point_x > x_values[-1]:

                

                if nd_deriv >= 0:
                    values_file = open(self.path + '/current_data.txt','w')

                    for i in x_values:
                        if i > len(values)/2:
                            values_file.write(str(values[i-1]) + ',')
                
                    values_file.write(str(self.price))
                    values_file.close()
 

                    return False

                else:
                
                    return True

            elif crit_point_y >= self.price:
                return True

            else:
                return False
                

            



        else:

            #if(self.price-self.last_buy)/self.last_buy < -0.05:
                #print('whoops')
                #return True

            if rd_deriv >= 0:
                
                values_file = open(self.path + '/current_data.txt','w')
                for i in x_values:
                    if i > len(values)/2:
                        values_file.write(str(values[i-1]) + ',')
                values_file.write(str(self.price))
                values_file.close()


                return False
            
            elif (self.price-self.last_buy)/self.last_buy < 0.01:
                return False

            elif crit_point_x > x_values[-1]:
                return True

            elif crit_point_y <= self.price:
                return True

            else:
                return False

            
        

        

        
        

        


























        
