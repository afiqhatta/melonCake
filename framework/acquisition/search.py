import pandas as pd
from bs4 import BeautifulSoup
from multiprocessing import Pool
import interface.data.acquisition.pulling as dg

"""

"""

test_csv = '/Users/ahmadafiqhatta/Documents/ML/loggr/interface/data/url_generate/sources/source_search.csv'


class SearchScraper(object):
    """
    Multi-threaded scraper to get data from search fields in newspapers
    """

    def __init__(self, csv_file, search_term):
        self.csv_file = csv_file
        self.df = pd.DataFrame()
        self.search_term = search_term

    def set_df(self):
        self.df = pd.read_csv(test_csv)
        return self

    def set_search_term(self, delimiter):
        self.search_term = delimiter.join(self.search_term.split(' '))
        return self

    @staticmethod
    def extract(text, span, class_):
        if class_ == 'None':
            return BeautifulSoup(str(text), features="html.parser").find(span).text
        else:
            return BeautifulSoup(str(text), features="html.parser").find(span, class_).text

    def construct_url(self, location, page_number):
        pass

    def one_page(self, location, page_number):
        data = self.df.iloc[location]
        self.set_search_term(data['delimiter'])
        url = str(data['url']).format(SEARCHTERM=self.search_term, PAGE=page_number)

        results = dg.pull_element(url, data['sec_span'], data['sec_class'], True)
        articles = []
        for i in range(0, len(results)):
            title = self.extract(results[i], data['line_span'], data['line_class'])
            description = self.extract(results[i], data['desc_span'], data['desc_class'])
            date = self.extract(results[i], data['date_span'], data['date_class'])
            content = {'paper': data['paper'], 'title': title, 'description': description, 'date':date}
            articles.append(content)
        return articles

    def multiple_pages(self, location, pages):
        data = self.df.iloc[location]
        self.set_search_term(data['delimiter'])
        arg_list = [(location, page) for page in pages]

        print(arg_list)

        with Pool(len(pages)) as p:
            packed_data = p.starmap(self.one_page, arg_list)

        return [item for sublist in packed_data for item in sublist]


class SearchScrape(object):

    def __init__(self, url_pattern: str, pages: list, term: list, delimiter: str):
        self.url_pattern = url_pattern
        self.pages = pages
        self.term = term
        self.delimiter = delimiter


if __name__ == "__main__":

    a = SearchScraper(test_csv, 'anwar ibrahim').set_df().one_page(0, 2)
    print((SearchScraper(test_csv, 'anwar ibrahim').set_df().multiple_pages(0, [1, 2, 3, 4, 5])))
