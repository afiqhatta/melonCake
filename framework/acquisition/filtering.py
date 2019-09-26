import os
from dateutil.parser import parse
from bs4 import BeautifulSoup
from bs4.element import Comment
from framework.acquisition.pulling import get_all_text

"""
    Search for codified html and remove "{" characters 
    Isolate text lines
    sort it 
    use both 
"""


class HtmlClean(object):
    """
    Filters html from multiple formats into clean versions
    """

    def __init__(self, text: str):
        self.text = text

    @staticmethod
    def list_join(texts: list) -> str:
        return u"\n".join(t for t in texts)

    @staticmethod
    def is_date(string, fuzzy=False):
        try:
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    @staticmethod
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(self):
        soup = BeautifulSoup(self.text, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        self.text = u"\n".join(t.strip() for t in visible_texts)
        return self

    @staticmethod
    def contains_words(self, string):
        for word in self.keywords:
            if word in string:
                return True
        return False

    def start_on_date(self, text: str) -> str:
        text_list = text.splitlines()
        for i in range(0, len(text_list)):
            if self.is_date(text_list[i]):
                text_list = text_list[i:]
                break
        return u"\n".join(t for t in text_list)

    def end_on_date(self, text: str) -> str:
        return u"\n".join(t for t in self.start_on_date(u"\n"
                                                        .join(t for t in text.splitlines()[::-1])).splitlines()[::-1])

    def trim_ends(self):
        self.text = self.end_on_date(self.start_on_date(self.text))
        return self

    def remove_spaces(self):
        self.text = os.linesep.join([s for s in self.text.splitlines() if s])
        return self

    def remove_all_duplicate_lines(self):
        seen, duplicates = set(), set()
        unique = list()
        for line in self.text.splitlines():
            if not self.is_date(line):
                seen.add(line) if line not in seen else duplicates.add(line)
        for line in self.text.splitlines():
            if line not in duplicates:
                unique.append(line)
        self.text = self.list_join(unique)
        return self

    def remove_duplicate_lines(self):
        seen = list()
        for line in self.text.splitlines():
            if not self.is_date(line):
                if line not in seen:
                    seen.append(line)
            else:
                seen.append(line)
        self.text = self.list_join(list(seen))
        return self

    def get_filtered_text(self):
        self.trim_ends()
        self.remove_spaces()
        self.remove_duplicate_lines()
        return self


html = get_all_text('https://uk.reuters.com/search/news?blob=malaysia')
filter_obj = HtmlClean(html)
print(filter_obj.get_filtered_text().text)
