import requests

def get_wikipedia_summary(topic):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('extract', 'No summary available.')
    except requests.exceptions.RequestException as e:
        return f"Error retrieving data from Wikipedia: {e}"

def get_wikipedia_full_article(topic):
    try:
        url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        return url
    except Exception as e:
        return f"Error generating Wikipedia URL: {e}"

def get_wikipedia_data(topic):
    summary = get_wikipedia_summary(topic)
    full_article_url = get_wikipedia_full_article(topic)
    return summary, full_article_url