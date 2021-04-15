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

class TestTwitterReader(TestCase):

    def test_read_most_negative_tweets(self):
        from TwitterReader import read_tweets_from_file
        df = read_tweets_from_file(os.path.join(data_dir, 'sample_data', 'test_data.csv'))
        new_df = df.sort_values(by=['sentiment_lstm'])
        most_negative_tweets = new_df['text'].values
        print(most_negative_tweets[0:10])
        return

if __name__ == '__main__':
    unittest.main()
