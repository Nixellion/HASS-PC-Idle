import os
import time
from requests import get, post

import win32api

import yaml

rp = realpath = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(rp, "config.yaml"), "r", encoding='utf-8', errors='ignore') as f:
    config = yaml.load(f)

def getIdleTime():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0

def trigger(action):
    print (action)
    headers = {
        'Authorization': 'Bearer {}'.format(config['token']),
        'content-type': 'application/json',
    }
    
    for entity_id in config['home_assistant_booleans']:
        url = "{}/services/input_boolean/{}".format(config['endpoint_url'], action)
        data = {"entity_id":"input_boolean.{}".format(entity_id)}
        #print ("    ", action, url, data)
        response = post(url, headers=headers, json=data)
        #print("    ", response.text)
    
    


idle = False
    
while True:
    idle_for = getIdleTime()
    

    
    if idle_for > config['idle_if_seconds']:

        if not idle:
            trigger('turn_on')
            idle = True
            
    else:
        if idle:
            trigger('turn_off')
            idle = False
            
    #config['idle_if_seconds']
    time.sleep(config['interval'])





