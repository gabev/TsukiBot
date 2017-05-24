import psycopg2
import numpy as np

from datetime import datetime, timedelta

class s_command():

    def __init__(self, coin):
        self.coin = coin

    # Update the current data to file
    def writeToFile(self, timef):
        conn = psycopg2.connect("dbname=volumes user=tsukibot")   
        cur = conn.cursor()    
        
        SQL = "SELECT sub.type, SUM(sub.volumebtc) FROM (SELECT * FROM poloniex WHERE coin = %s and time > CURRENT_TIMESTAMP - INTERVAL '%s minutes') sub GROUP BY type;"

        cur.execute(SQL, (self.coin, int(timef)))
         
        buy = cur.fetchone()[1]
        sell = cur.fetchone()[1]
        
        # Write the format

        response = '\n**' + self.coin + '** (since approx. ' + str(timef) +' min. ago)\n__Volume__ (BTC)\n :large_blue_circle: BUY: `' + str(buy) + "` \n :red_circle: SELL: `" + str(sell) + "` \n\nNet difference: `" + str(buy-sell) + '`\nRatio: `' + str(   int((buy-sell)/(buy+sell) * 10000)/100.0  ) + ' %`';
        response += '\n`Press cross to delete this message. Avoid spam.`'

        cur.close()
        return response 
