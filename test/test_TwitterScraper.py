from unittest import TestCase
import os, sys, logging, unittest
# Setup logger    
logging.basicConfig(level=logging.WARNING)
logging.addLevelName(logging.WARNING, "\033[93m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[91m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
# Setup paths    
this_files_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.abspath(os.path.join(this_files_dir, os.pardir, 'src'))
data_dir = os.path.abspath(os.path.join(this_files_dir, os.pardir, 'data'))
sys.path.append(modules_dir)

import tweepy

class TestTwitterScraper(TestCase):

    def test_stream_tweets(self):
        from TwitterScraper import TwitterScraper
        from TwitterScraper import start_stream
        output_file = os.path.join(data_dir, 'sample_data', 'test_data.csv')
        myScraper = TwitterScraper(output_csv_file=output_file, time_limit_seconds=10)
        start_stream(myScraper, languages=["en"], track_topics=["kamala"])
        return

if __name__ == '__main__':
    unittest.main()
