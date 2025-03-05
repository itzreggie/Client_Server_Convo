import requests

def get_wikipedia_summary(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('extract', 'No summary available.')
    else:
        return 'Error retrieving data from Wikipedia.'

def get_wikipedia_full_article(topic):
    url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
    return url

def get_wikipedia_data(topic):
    summary = get_wikipedia_summary(topic)
    full_article_url = get_wikipedia_full_article(topic)
    return summary, full_article_url