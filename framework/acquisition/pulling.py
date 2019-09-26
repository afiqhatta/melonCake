import requests
from bs4 import BeautifulSoup


class Chunk:
    """
    Scrape and find elements from a chunk of a website.

    Example usage:
    star_chunk = Chunk('https://www.thestar.com.my/').get()
    print(star_chunk.find('h2', 'f28').text)
    """

    def __init__(self, url):
        self.url = url
        self.text = self.test()
        self.content = self.get()
        self.raw = None

    def test(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        return requests.get(self.url, headers=headers).text

    def get(self):
        return BeautifulSoup(self.test(), 'html.parser')

    def pull_element(self, span, class_):
        if class_ != 'None':
            return self.get().find(span, class_).text
        else:
            return self.get().find(span).text

    def find(self, span, class_):
        self.raw = self.content.find_all(span, class_)
        return self.content.find_all(span, class_)

    def attr(self, element):
        return self.raw.get(element)


def test(url):
    """
    Grabs all text from page
    :param url:
    :return:
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

