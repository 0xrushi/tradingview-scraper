from websocket import create_connection
import json
import random
import string
import re
import pandas as pd
import csv
import argparse
from datetime import datetime
from time import localtime

# init argparser
args = argparse.ArgumentParser()

args.add_argument("-n", "--symbol", help="symbol", required=True)
args.add_argument("-s", "--silent", help="silent", action="store_true")
args.add_argument("-o", "--output", help="output", required=False)
args.add_argument("-q", "--quit", help="quit on first reponse", action="store_true")

symbol = args.parse_args().symbol
silent = args.parse_args().silent
output = args.parse_args().output
exitoninput = args.parse_args().quit

def filter_raw_message(text):
    try:
        found = re.search('"m":"(.+?)",', text).group(1)
        found2 = re.search('"p":(.+?"}"])}', text).group(1)
        print(found)
        print(found2)
        return found1, found2
    except AttributeError:
        print("error")
    

def generateSession():
    stringLength=12
    letters = string.ascii_lowercase
    random_string= ''.join(random.choice(letters) for i in range(stringLength))
    return "qs_" +random_string

def generateChartSession():
    stringLength=12
    letters = string.ascii_lowercase
    random_string= ''.join(random.choice(letters) for i in range(stringLength))
    return "cs_" +random_string

def prependHeader(st):
    return "~m~" + str(len(st)) + "~m~" + st

def constructMessage(func, paramList):
    #json_mylist = json.dumps(mylist, separators=(',', ':'))
    return json.dumps({
        "m":func,
        "p":paramList
        }, separators=(',', ':'))

def createMessage(func, paramList):
    return prependHeader(constructMessage(func, paramList))

def sendRawMessage(ws, message):
    ws.send(prependHeader(message))

def sendMessage(ws, func, args):
    ws.send(createMessage(func, args))

# Initialize the headers needed for the websocket connection
headers = json.dumps({
    # 'Connection': 'upgrade',
    # 'Host': 'data.tradingview.com',
    'Origin': 'https://data.tradingview.com'
    # 'Cache-Control': 'no-cache',
    # 'Upgrade': 'websocket',
    # 'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    # 'Sec-WebSocket-Key': '2C08Ri6FwFQw2p4198F/TA==',
    # 'Sec-WebSocket-Version': '13',
    # 'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56',
    # 'Pragma': 'no-cache',
    # 'Upgrade': 'websocket'
})

    
# Then create a connection to the tunnel
ws = create_connection(
    'wss://data.tradingview.com/socket.io/websocket',headers=headers)

session= generateSession()
if not silent:
    print("session generated {}".format(session))

chart_session= generateChartSession()
if not silent:
    print("chart_session generated {}".format(chart_session))

# Then send a message through the tunnel 
sendMessage(ws, "set_auth_token", ["unauthorized_user_token"])
sendMessage(ws, "chart_create_session", [chart_session, ""])
sendMessage(ws, "quote_create_session", [session])
sendMessage(ws,"quote_set_fields", [session,"ch","chp","current_session","description","local_description","language","exchange","fractional","is_tradable","lp","lp_time","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume","currency_code","rchp","rtc"])
sendMessage(ws, "quote_add_symbols",[session, symbol, {"flags":['force_permission']}])
sendMessage(ws, "quote_fast_symbols", [session,symbol])

#st='~m~140~m~{"m":"resolve_symbol","p":}'
#p1, p2 = filter_raw_message(st)
sendMessage(ws, "resolve_symbol", [chart_session,"symbol_1","={\"symbol\":\"" + symbol + "\",\"adjustment\":\"splits\",\"session\":\"extended\"}"])
if not silent:
    sendMessage(ws, "create_series", [chart_session, "s1", "s1", "symbol_1", "1", 5000])
#sendMessage(ws, "create_study", [chart_session,"st4","st1","s1","ESD@tv-scripting-101!",{"text":"BNEhyMp2zcJFvntl+CdKjA==_DkJH8pNTUOoUT2BnMT6NHSuLIuKni9D9SDMm1UOm/vLtzAhPVypsvWlzDDenSfeyoFHLhX7G61HDlNHwqt/czTEwncKBDNi1b3fj26V54CkMKtrI21tXW7OQD/OSYxxd6SzPtFwiCVAoPbF2Y1lBIg/YE9nGDkr6jeDdPwF0d2bC+yN8lhBm03WYMOyrr6wFST+P/38BoSeZvMXI1Xfw84rnntV9+MDVxV8L19OE/0K/NBRvYpxgWMGCqH79/sHMrCsF6uOpIIgF8bEVQFGBKDSxbNa0nc+npqK5vPdHwvQuy5XuMnGIqsjR4sIMml2lJGi/XqzfU/L9Wj9xfuNNB2ty5PhxgzWiJU1Z1JTzsDsth2PyP29q8a91MQrmpZ9GwHnJdLjbzUv3vbOm9R4/u9K2lwhcBrqrLsj/VfVWMSBP","pineId":"TV_SPLITS","pineVersion":"8.0"}])


# Printing all the result
a=""
while True:
    try:
        result = ws.recv()
        if not silent:
            print(result)
        if silent:
            if not re.search(r'"lp":(.*?),', result) is None:
                print(re.search(r'"lp":(.*?),', result).group(1))
                if exitoninput:
                    exit(0)
        a=a+result+"\n"
        if output:
            with open(output,"a") as ww:
                ww.write(result)
                ww.close()
    except Exception as e:
        print(e)
        break
