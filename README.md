# tradingview-scraper 2020

## Install imports
```
pip install -r requirements.txt
```

## Run
```
python main.py
```

### Want to add something? file a PR and join this discord 
https://discord.gg/p77FMCBg


### Have a tradingview username and password?

```
def get_auth_token():
    sign_in_url = 'https://www.tradingview.com/accounts/signin/'
    username = 'username'
    password = 'password'
    data = {"username": username, "password": password, "remember": "on"}
    headers = {
        'Referer': 'https://www.tradingview.com'
    }
    response = requests.post(url=sign_in_url, data=data, headers=headers)
    auth_token = response.json()['user']['auth_token']    
    return auth_token
```
 Then send a message through the tunnel 
sendMessage(ws, "set_auth_token", ["auth_token"])

ws = create_connection(
    'wss://data.tradingview.com/socket.io/websocket?from=chart/XXyour_chartXX/&date=XXXX_XX_XX-XX_XX',headers=headers)

```
result = ws.recv()
if re.search('~m~\\d+~m~~h~\\d+', result):
            #Send ping message
            ws.send(result)
``` 
