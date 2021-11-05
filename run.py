from Monitor.opensea import monitorCollection_Name
from threading import Thread
import json, os,time

def readFiles(): 
    with open("Monitor\settings.json") as settingsFile:
        settingsFileData = json.load(settingsFile)
        try:
            delay = settingsFileData['Settings']['Monitor Delay']
            webhook = settingsFileData['Settings']['Webhook']
        except:
            print('Error Reading Settings File... Please make sure Settings are set accordingly.')
            os._exit(1)
    startTimestamp = time.time()

    with open('Monitor\CollectionsList.txt', 'r') as file:
        while True:
            collectionName = file.readline().strip()
            if not collectionName:
                break
            if('https://opensea.io/collection/' in collectionName):
                collectionName = collectionName[30:]
                Thread(target=monitorCollection_Name, args=(collectionName, delay, webhook, startTimestamp,)).start()
                pass
            else:
                Thread(target=monitorCollection_Name, args=(collectionName, delay, webhook, startTimestamp,)).start()
                pass
readFiles()