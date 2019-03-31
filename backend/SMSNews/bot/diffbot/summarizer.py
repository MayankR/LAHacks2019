from .client import DiffbotClient,DiffbotCrawl
from .config import API_TOKEN
import requests
import requests_cache

def get_summaries(urls, idx):
    diffbot = DiffbotClient()
    token = "938ec1c1e025fccdcd9188c7e1a0af8a"
    version = 2
    api = "article"

    summaries = []
    # for url in urls:

    url = urls[idx]

    requests_cache.install_cache('demo_cache')

    print("sending text request")
    response = diffbot.request(url, token, api, version=2)
    if 'text' not in response:
        return ""
    if len(response['text']) < 50:
        return ""
        
    news = response['text'][:2000]
    print("got text response")
    
    print("sending summary request")
    r = requests.post(
        "https://api.deepai.org/api/summarization",
        data={'text': news,},
        headers={'api-key': '4abc8c08-2f63-4ff5-8431-529d10eef026'}
    )
    
    summary = r.json()['output']
    print("got summary response")
    # summaries.append(summary)

    return summary