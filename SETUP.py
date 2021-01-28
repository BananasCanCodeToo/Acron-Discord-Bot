import pickle
import datetime

time = datetime.datetime.now() - datetime(hours=24)

with open('ping.data','wb') as f:
    pickle.dump(time, f)
