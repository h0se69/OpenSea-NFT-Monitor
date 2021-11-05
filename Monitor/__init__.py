import os
import sqlite3

def startDatabase():
    baseDir = os.path.abspath(os.path.dirname(__file__))
    connection = sqlite3.connect(os.path.join(baseDir,'collectionData.db'))
    cur = connection.cursor()

    # Create new database table
    try:
        cur.execute('''CREATE TABLE nfts (
            name text,
            collection text,
            price text,
            imageLink text,
            purchaseLink text,
            timestamp text
        )''')
    except sqlite3.OperationalError:
        # If database table exists it ignores and goes on
        pass

    return connection, cur