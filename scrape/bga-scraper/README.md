Scraping BoardGameArena
=======================

1. Use Python 3
2. Install dependencies: `pip3 install -r requirements.txt`
3. Wire it together:

```
from client import HttpClient
from scraper import Scraper

client = HttpClient('username', 'password')
scraper = Scraper(client, '../bga-games/')

client.login()
scraper.loopGameList()
```
