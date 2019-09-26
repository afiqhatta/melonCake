import pandas as pd
from multiprocessing import Pool
from . import pulling as pl


class HeadlineGrabber(object):
    """
    API for pulling headlines from a list of identified tags from the csv.

    Example usage with a csv:

    csv = '/Users/ahmadafiqhatta/Documents/ML/loggr/interface/data/url_generate/sources/source_locations.csv'
    print(HeadlineGrabber(csv).set_df().pull_headlines())

    """
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = pd.DataFrame()

    def set_df(self):
        self.df = pd.read_csv(self.csv_file)
        return self

    def pull_headlines_simple(self):
        items = []

        for i in range(0, len(self.df)):
            data = self.df.iloc[i]
            print(data['paper'])
            content = {}
            chunk = pl.Chunk(data['url'])
            content['paper'] = data['paper']
            content['headline'] = chunk.pull_element(data['head_span'], data['head_class'])
            items.append(content)
        return items

    def pull_headlines(self):
        data = self.df.values.tolist()
        with Pool(len(self.df)) as p:
            return p.starmap(pl.pull, data)

    # csv = '/Users/ahmadafiqhatta/Documents/ML/loggr/interface/data/url_generate/sources/source_locations.csv'
    # # print(HeadlineGrabber(csv).set_df().pull_headlines())
