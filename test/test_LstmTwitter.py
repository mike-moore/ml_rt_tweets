from unittest import TestCase
import os, sys, logging, unittest
# Setup logger    
logging.basicConfig(level=logging.WARNING)
logging.addLevelName(logging.WARNING, "\033[93m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[91m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
# Setup paths    
this_files_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.abspath(os.path.join(this_files_dir, os.pardir, 'src'))
sys.path.append(modules_dir)

class TestLstmTwitter(TestCase):

    def test_predict_tweet_sentiment(self):
        from LstmTwitter import predict_tweet_sentiment
        sentiment = predict_tweet_sentiment("I'm happy you're here!")
        self.assertAlmostEqual(0.99, sentiment, 1)
        sentiment = predict_tweet_sentiment("I'm pissed off!")
        self.assertAlmostEqual(0.01, sentiment, 1)
        return

if __name__ == '__main__':
    unittest.main()
