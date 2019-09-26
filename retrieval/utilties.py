import requests
from

def test(url):
    """
    Grabs the entire html string from a given url using the requests package.
    We require a header dictionary because for some reason this is a requirement for scraping!

    :param url: a url
    :return: a text string of often messy html, which we need to parse in BeautifulSoup.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    return requests.get(url, headers=headers).text


def get(url):
    """
    Parses this into BeautifulSoup form
    """
    return BeautifulSoup(test(url), 'html.parser')


def pull_element(url, span, class_, multiple=False):
    if class_ != 'None':
        if multiple:
            return get(url).find_all(span, class_)
        else:
            return get(url).find(span, class_).text
    else:
        if multiple:
            return get(url).find_all(span)
        else:
            return get(url).find(span).text


def pull(name, url, span, class_):
    content = {'paper': name, 'headline': pull_element(url, span, class_)}
    return content


def get_all_text(url):
    return get(url).text
