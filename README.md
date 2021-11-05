# OpenSea-NFT-Monitor

Small program to monitor the NFT marketplace, Opensea.io
> Alerts the user for Price Changes via Discord

## Installation

```cmd
1) Download ZIP or git clone https://github.com/h0se69/OpenSea-NFT-Montior.git
2) pip install -r requirements.txt
3) Open OpenSea-NFT-Monitor/Monitor
4) Update setting.json & Collections.txt info
5) run the file: run.py
```

## Usage

```
Collections.txt = Insert collection link or collection slug (https://opensea.io/collection/cryptopunks or cryptopunks)
Settings.json = Delay + Discord Webhook (delay is in ms)

Uses the OpenSea Event API (https://docs.opensea.io/reference/retrieving-asset-events)
> Stores NFT data into database (SQLite)
> Sends Discord Webhook when a New NFT is listed or Price Change occurs for the Collections saved
```

## Future Ideas | Additional Notes
```
> Can run 0ms delay, OpenSea does not seem to throttle Localhost
> Enable user to Delete collections stored in Database (instead of deleting DB)
> Monitor user wallets
> This is barebones, works but can be greatly improved
> |Experimenting with how Monitors function|
```
