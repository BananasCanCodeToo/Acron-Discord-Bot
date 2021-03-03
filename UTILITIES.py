import yaml
import json
import datetime
import pickle
from datetime import timedelta

# Does logs with fomrat: "[ACTION] <time> > <user> <log>"
def log(log, user=''):
    x = datetime.datetime.now()
    if user != '':
        print(f'[ACTION] {x.strftime("%H:%M:%S")} > {user.name}#{user.discriminator} {log}')
        with open('LOG.txt','a') as f:
            f.write(f'\n[ACTION] {x.strftime("%H:%M:%S")} > {user.name}#{user.discriminator} {log}')

    else:
        print(f'[ACTION] {x.strftime("%H:%M:%S")} > {log}')
        with open('LOG.txt','a') as f:
            f.write(f'\n[ACTION] {x.strftime("%H:%M:%S")} > {log}')

# Does logs with fomrat: "[DEBUG] <time> > <user> <log>"
def debuglog(log, user=''):
    x = datetime.datetime.now()
    if user != '':
        print(f'[DEBUG] {x.strftime("%H:%M:%S")} > {user.name}#{user.discriminator} {log}')
        with open('LOG.txt','a') as f:
            f.write(f'\n[DEBUG] {x.strftime("%H:%M:%S")} > {user.name}#{user.discriminator} {log}')

    else:
        print(f'[DEBUG] {x.strftime("%H:%M:%S")} > {log}')
        with open('LOG.txt','a') as f:
            f.write(f'\n[DEBUG] {x.strftime("%H:%M:%S")} > {log}')

# Gets the logs in the log file
def getlogs():
    with open('LOG.txt','r') as f:
        logs = f.read()
    return logs

# Simple function to say the bot is online (for the ready() function)
def startLog(bot):
    x = datetime.datetime.now()
    print(f'[DEBUG] {x.strftime("%H:%M:%S")} > Bot is Online ({bot.user.name}#{bot.user.discriminator})')
    with open('LOG.txt','a') as f:
        f.write(f'\n\n\n\n[DATE] {x.strftime("%Y.%m.%d")}\n[DEBUG] {x.strftime("%H:%M:%S")} > Bot is Online ({bot.user.name}#{bot.user.discriminator})')


# Reads the admin file
def admins():
    with open('admins.txt') as f:
        admins = f.read().split('\n')
    return admins

def getadmin(user):
    t = False
    with open('admins.txt') as f:
        admins = f.read().split('\n')
    for i in admins:
        if i == '':
            continue
        elif i[0] == '#':
            continue
        elif user.id == int(i):
            t = True
    return t

# Reads the settings
def settings():
    with open('SETTINGS.txt','r') as f:
        settings = yaml.load(f,Loader=yaml.FullLoader)
    return settings

# Reads the game file
def r_games():
    with open('games.data','r') as f:
        games = json.load(f)
    return games

# Writes to the game file
def w_games(id, data):
    with open('games.data','r') as f:
        games = json.load(f)
    if data != 'pop':
        games[f"{id}"] = data
    else:
        games.pop(f'{id}')
    with open('games.data','w') as f:
        json.dump(games, f, indent=4)

# Reads the possible game file
def r_pgames():
    with open('pgames.data','r') as f:
        pgames = json.load(f)
    return pgames

# Writes to the possible game file
def w_pgames(id, data='pop'):
    with open('pgames.data','r') as f:
        pgames = json.load(f)
    if data != 'pop':
        pgames[f"{id}"] = data
    else:
        pgames.pop(f'{id}')
    with open('pgames.data','w') as f:
        json.dump(pgames, f, indent=4)

# Determines the most recent ping and returns true if the bot can ping
def ping():
    currentPing = datetime.datetime.now()
    with open('SETTINGS.txt','r') as f:
        settings = yaml.load(f,Loader=yaml.FullLoader)
        timeout = settings['PING_TIMEOUT']
    with open('ping.data','rb') as f:
        pastPing = pickle.load(f)
    if type(pastPing) == datetime.datetime:
        if currentPing > pastPing + timedelta(minutes=timeout):
            with open('ping.data','wb') as f:
                pickle.dump(currentPing, f)
            return True
        else:
            return False
    else:
        with open('ping.data','wb') as f:
            pickle.dump(currentPing, f)
        return False

class help:
    def admin():
        with open('help/admin.txt') as f:
            return f.read()
    def help():
        with open('help/help.txt') as f:
            return f.read()

#########################################
#    Developed by BananasCanCodeToo     #
# https://github.com/BananasCanCodeToo/ #
#########################################
