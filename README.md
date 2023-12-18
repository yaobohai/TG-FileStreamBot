## TG-FileStreamBot

部署该服务,实现通过转发文件给Bot的形式返回文件直链,更方便的将TG的内容共享&下载。

### 部署服务

```sh
git clone https://github.com/EverythingSuckz/TG-FileStreamBot
cd TG-FileStreamBot
python3 -m venv ./venv
. ./venv/bin/activate
pip3 install -r requirements.txt
python3 -m WebStreamer
```

and to stop the whole bot,
 do <kbd>CTRL</kbd>+<kbd>C</kbd>

> **If you wanna run this bot 24/7 on the VPS, follow thesesteps.**
> ```sh
> sudo apt install tmux -y
> tmux
> python3 -m WebStreamer
> ```
> now you can close the VPS and the bot will run on it.

### Deploy using Docker
First clone the repository
```sh
git clone https://github.com/EverythingSuckz/TG-FileStreamBot
cd TG-FileStreamBot
```
then build the docker image
```sh
docker build . -t stream-bot
```
now create the `.env` file with your variables. and start your container:
```sh
docker run -d --restart unless-stopped --name fsb \
-v /PATH/TO/.env:/app/.env \
-p 8000:8000 \
stream-bot
```

your `PORT` variable has to be consistent with the container's exposed port since it's used for URL generation. so remember if you changed the `PORT` variable your docker run command changes too. (example: `PORT=9000` -> `-p 9000:9000`)

if you need to change the variables in `.env` file after your bot was already started, all you need to do is restart the container for the bot settings to get updated:
```sh
docker restart fsb
```

### Deploy using docker-compose
First install docker-compose. For debian based, run 
```sh
sudo apt install docker-compose -y
```
Afterwards, clone the repository
```sh
git clone https://github.com/EverythingSuckz/TG-FileStreamBot
cd TG-FileStreamBot
```
No need to create .env file, just edit the variables in the docker-compose.yml

Now run the compose file
```sh
sudo docker compose up -d
```

## Setting up things

If you're locally hosting, create a file named `.env` in the root directory and add all the variables there.
An example of `.env` file:

```sh
API_ID=452525
API_HASH=esx576f8738x883f3sfzx83
BOT_TOKEN=55838383:yourtbottokenhere
MULTI_TOKEN1=55838383:yourfirstmulticlientbottokenhere
MULTI_TOKEN2=55838383:yoursecondmulticlientbottokenhere
MULTI_TOKEN3=55838383:yourthirdmulticlientbottokenhere
BIN_CHANNEL=-100
PORT=8080
FQDN=yourserverip
HAS_SSL=False
```

### Mandatory Vars
Before running the bot, you will need to set up the following mandatory variables:

- `API_ID` : This is the API ID for your Telegram account, which can be obtained from my.telegram.org.

- `API_HASH` : This is the API hash for your Telegram account, which can also be obtained from my.telegram.org.

- `BOT_TOKEN` : This is the bot token for the Telegram Media Streamer Bot, which can be obtained from [@BotFather](https://telegram.dog/BotFather).

- `BIN_CHANNEL` :  This is the channel ID for the log channel where the bot will forward media messages and store these files to make the generated direct links work. To obtain a channel ID, create a new telegram channel (public or private), post something in the channel, forward the message to [@missrose_bot](https://telegram.dog/MissRose_bot) and **reply the forwarded message** with the /id command. Copy the forwarded channel ID and paste it into the this field.

### Optional Vars
In addition to the mandatory variables, you can also set the following optional variables:

- `ALLOWED_USERS`: The user Telegram IDs of users to which the bot only reply to.
> **Note**
> Leave this field empty and anyone will be able to use your bot instance.
> You may also add multiple users by adding the IDs separated by comma (,)

- `HASH_LENGTH` : This is the custom hash length for generated URLs. The hash length must be greater than 5 and less than 64.


- `SLEEP_THRESHOLD` : This sets the sleep threshold for flood wait exceptions that occur globally in the bot instance. Requests that raise flood wait exceptions below this threshold will be automatically invoked again after sleeping for the required amount of time. Flood wait exceptions requiring longer waiting times will be raised. The default value is 60 seconds. Better leave this field empty.


- `WORKERS` : This sets the maximum number of concurrent workers for handling incoming updates. The default value is 3.


- `PORT` : This sets the port that your webapp will listen to. The default value is 8080.


- `WEB_SERVER_BIND_ADDRESS` : This sets your server bind address. The default value is 0.0.0.0.

- `NO_PORT` : This can be either True or False. If set to True, the port will not be displayed.
> **Note**
> To use this setting, you must point your `PORT` to 80 for HTTP protocol or to 443 for HTTPS protocol to make the generated links work.

- `FQDN` :  A Fully Qualified Domain Name if present. Defaults to `WEB_SERVER_BIND_ADDRESS`

- `HAS_SSL` : This can be either True or False. If set to True, the generated links will be in HTTPS format.

- `KEEP_ALIVE`: If you want to make the server ping itself every `PING_INTERVAL` seconds to avoid sleeping. Helpful in PaaS Free tiers. Defaults to `False`

- `PING_INTERVAL` : The time in ms you want the servers to be pinged each time to avoid sleeping (If you're on some PaaS). Defaults to `1200` or 20 minutes.

- `USE_SESSION_FILE` : Use session files for client(s) rather than storing the pyrogram sqlite database in the memory

### For making use of Multi-Client support

> **Note**
> What it multi-client feature and what it does? <br>
> This feature shares the Telegram API requests between other bots to avoid getting floodwaited (A kind of rate limiting that Telegram does in the backend to avoid flooding their servers) and to make the server handle more requests. <br>

To enable multi-client, generate new bot tokens and add it as your environmental variables with the following key names. 

`MULTI_TOKEN1`: Add your first bot token here.

`MULTI_TOKEN2`: Add your second bot token here.

you may also add as many as bots you want. (max limit is not tested yet)
`MULTI_TOKEN3`, `MULTI_TOKEN4`, etc.

> **Warning**
> Don't forget to add all these bots to the `BIN_CHANNEL` for the proper functioning

## How to use the bot

> **Warning**
> Before using the  bot, don't forget to add all the bots (multi-client ones too) to the `BIN_CHANNEL` as an admin
 
`/start` : To check if the bot is alive or not.

To get an instant stream link, just forward any media to the bot and boom, the bot instantly replies a direct link to that Telegram media message.