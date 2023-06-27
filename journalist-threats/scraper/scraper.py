# Scrape twitter with snscrape
import pandas as pd
import snscrape.modules.twitter as sntwitter

accounts = [
    {
        "name": "Jeroen Wollaars",
        "username": "wol",
        "slug": "jeroen_wollaars",
        "twitter": "https://twitter.com/wol"
    },
    {
        "name": "Sinan Can",
        "username": "sinancan77",
        "slug": "sinan_can",
        "twitter": "https://twitter.com/sinancan77"
    },
    {
        "name": "Wafa Al Ali",
        "username": "alaliwafa",
        "slug": "wafa_al_ali",
        "twitter": "https://twitter.com/alaliwafa"
    },
    {
        "name": "Leen Vervaeke",
        "username": "leenvervaeke",
        "slug": "leen_vervaeke",
        "twitter": "https://twitter.com/leenvervaeke"
    },
    {
        "name": "Yelle Tieleman",
        "username": "YelleTieleman",
        "slug": "yelle_tieleman",
        "twitter": "https://twitter.com/YelleTieleman"
    }
]

for account in accounts:
    print(f"Scraping {account['name']}...")
    scraper = sntwitter.TwitterSearchScraper(f"to:{account['username']}")
    tweets = []

    for i, tweet in enumerate(scraper.get_items()):
        print(tweet.rawContent)
        if i < 1000:
            tweets.append({
                "text": tweet.rawContent,
                "date": tweet.date,
                "url": tweet.url,
                "from": tweet.user.username
            })
        else:
            break

    print(f"Found {len(tweets)} tweets for {account['name']}")
    df = pd.DataFrame(tweets)
    df.to_csv(f"../tweets/{account['slug']}.csv", index=False)
        