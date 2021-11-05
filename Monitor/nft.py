class NFT():
    def __init__(self, name, collection, price, imageLink, purchaseLink, timestamp):
        self.name = name
        self.collection = collection
        self.price = price
        self.imageLink = imageLink
        self.purchaseLink = purchaseLink
        self.timestamp = timestamp
    def __repr__(self):
        return f'NFT: Name: {self.name}, Price: {self.price})'
