import json
import random
import string
import time

import dateutil.parser
import requests as r

from Monitor import *
from Monitor.discord import *
from Monitor.nft import NFT


def monitorCollection_Name(collectionName, delay, webhook,startTimestamp):
    connection, cur = startDatabase()

    while True:
        randomOrigin = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 30))
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Origin": randomOrigin,
            "Accept": "application/json"
        }
        url = f'https://api.opensea.io/api/v1/events?collection_slug={collectionName}&event_type=created&only_opensea=false&offset=0&limit=20'
        response = r.get(url,headers=headers)
        try:
            jsonData = json.loads(response.text)
        except json.decoder.JSONDecodeError or TypeError:
            monitorCollection_Name(collectionName, delay, webhook)

        for nftData in jsonData['asset_events']:
            try:
                def nameG():
                    name = nftData['asset']['name']
                    while(name is None):
                        name = str(nftData['asset']['asset_contract']['name'])
                        name = name + '_' +str(nftData['asset']['token_id'])
                        return name
                    return name

                name = nameG()

                def priceG():
                    price = nftData['ending_price']
                    while(price is None):
                        price = nftData['ending_price']
                        price = str(float(price) / 1000000000000000000)
                        return price
                    price = str(float(price) / 1000000000000000000)
                    return price
                price = priceG()

                cur.execute("SELECT * FROM nfts WHERE name=?", (name,))
                storedData = cur.fetchone()

                if(storedData is not None): #Already in DB
                    cur.execute("SELECT timestamp FROM nfts WHERE name=?", (name, ))
                    databaseTime = cur.fetchone()[0]
                    timestamp = dateutil.parser.parse(str(nftData['created_date']))
                    timestamp = str((timestamp.timestamp() * 1000) - 25200000)[0:10]

                    if(float(timestamp) > float(databaseTime)):
                        #Updates DB with new info
                        cur.execute("SELECT price FROM nfts WHERE name=?", (name, )) 
                        oldPrice = cur.fetchone()[0]
                        cur.execute("UPDATE nfts SET price=?, timestamp=? WHERE name=?", (price,timestamp,name ))
                        connection.commit()
                        try:
                            imageLink = str(nftData['asset']['image_url'])
                            collection = str(nftData['asset']['asset_contract']['symbol'])
                            timestamp = dateutil.parser.parse(str(nftData['created_date']))
                            timestamp = str((timestamp.timestamp() * 1000) - 25200000)[0:10]
                            purchaseLink = str(nftData['asset']['permalink'])     
                        except:
                            continue

                        print(f'Updated List, {name}, Old Price: {oldPrice}, New Price: {price}')

                        itemStatus = "Price Change"
                        sendWebhook(itemStatus, name, oldPrice, collection, price, imageLink, purchaseLink, webhook)
                    else:
                        continue
                else: #Not in DB will add to DB
                    try:
                        imageLink = str(nftData['asset']['image_url'])
                        collection = str(nftData['asset']['asset_contract']['symbol'])
                        timestamp = dateutil.parser.parse(str(nftData['created_date']))
                        timestamp = str((timestamp.timestamp() * 1000) - 25200000)[0:10]
                        purchaseLink = str(nftData['asset']['permalink'])     
                    except:
                        print('error adding to DB!')
                        continue

                    if(float(timestamp) < float(startTimestamp)):
                        nft_Info = NFT(name, collection, price, imageLink, purchaseLink, timestamp)
                        cur.execute("INSERT INTO nfts VALUES (?, ?, ?, ? ,?, ?)",  (nft_Info.name, nft_Info.collection, 
                                                                                    nft_Info.price, nft_Info.imageLink, 
                                                                                    nft_Info.purchaseLink, nft_Info.timestamp))
                        connection.commit()
                        print(f'ADDED {name} to DB!')
                        continue
                    else:
                        nft_Info = NFT(name, collection, price, imageLink, purchaseLink, timestamp)
                        cur.execute("INSERT INTO nfts VALUES (?, ?, ?, ? ,?, ?)",  (nft_Info.name, nft_Info.collection, 
                                                                                    nft_Info.price, nft_Info.imageLink, 
                                                                                    nft_Info.purchaseLink, nft_Info.timestamp))
                        connection.commit(name, collection, price, imageLink, purchaseLink)
                        
                        # Send Webhook new listing
                        itemStatus = "New Listing"
                        oldPrice = "NFS"
                        sendWebhook(itemStatus, name, oldPrice, collection, price, imageLink, purchaseLink, webhook)
                        continue
            except:
                continue
        print(f'Sleeping {delay}ms')
        time.sleep(delay/1000)
