import requests as r
import time

def sendWebhook(itemStatus, name, oldPrice, collection, price, imageLink, purchaseLink, webhook):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Accept": "application/json"
     }
    webhookData = {
    "content": None,
    "embeds": [
        {
            "title": f'{itemStatus}: {name}',
            "url": purchaseLink,
            "color": 10658466,
            "fields": [
                {
                "name": "Collection",
                "value": collection,
                "inline": True
                },
                {
                "name": "Product Name",
                "value": name
                },
                {
                "name": "Old Price",
                "value": f"{oldPrice}Ξ",
                "inline": True
                },
                {
                "name": "New Price",
                "value": f"{price}Ξ",
                "inline": True
                },
                {
                "name": "Links",
                "value": f"[Purchase Link]({purchaseLink})"
                }
            ],
            "footer": {
                "text": f"VoirIO: {time.time()}",
                "icon_url": "https://i.ytimg.com/vi/0Hp2owcwacM/maxresdefault.jpg"
            },
            "image": {
                "url": imageLink
            },
            "thumbnail": {
                "url": "https://i.ytimg.com/vi/0Hp2owcwacM/maxresdefault.jpg"
            }
        }
        ] 
    }
    r.post(webhook,json=webhookData,headers=headers)
