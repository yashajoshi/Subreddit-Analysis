import datetime
import unittest
import json
import finalproject
from finalproject import *
import secrets
import config



class Testing_Import_files(unittest.TestCase):
    def setUp(self):
        self.reddit = open("secrets.py")
        self.config = open("config.py")

    def test_files_renamed(self):
        self.assertTrue(self.reddit.read(), "Change name of 'secret_sample.py' to 'secrets.py'")
        self.assertTrue(self.config.read(), "Change name of 'config_sample.py' to 'config.py'")

    def test_reddit_creds(self):
        self.assertNotEqual(secrets.client_id, "", "Make sure to fill in client_id on file called secrets")
        self.assertNotEqual(secrets.client_secret, "", "Make sure to fill in client_secret on file called secrets")
        self.assertNotEqual(secrets.username, "", "Make sure to fill in your reddit username on file called secrets")
        self.assertNotEqual(secrets.password, "", "Make sure to fill in your reddit account password on file called secrets")

    def test_config_creds(self):
        self.assertNotEqual(config.db_name, "", 'Fill in db_name in config file')
        self.assertNotEqual(config.db_user, "", 'Fill in db_name in config file')

    def tearDown(self):
        self.reddit.close()
        self.config.close()


class Testing_Posting_Class(unittest.TestCase):
    def setUp(self):
        self.f = open("sample_reddit_post.json", "r")
        self.json = self.f.read()
        self.p_dict = json.loads(self.json)
        self.post_inst = Post(self.p_dict)

    def test_get_subreddit(self):
        self.assertEqual({'subreddit': 'redditdev'}, self.post_inst.get_subreddit())

    def test_contains(self):
        self.assertFalse(self.post_inst.__contains__())

    def test_repr(self):
        self.assertEqual(self.post_inst.__repr__(), "redditdev: Title - 'Error with PRAW' has a score of 5")

    def test_instance_assignment(self):
        self.assertEqual(self.post_inst.title, "Error with PRAW")
        self.assertEqual(self.post_inst.gilded, 0)
        self.assertEqual(self.post_inst.score, 5)
        self.assertEqual(self.post_inst.subreddit, "redditdev")
        self.assertEqual(self.post_inst.kind, "Link")

    def tearDown(self):
        self.f.close()

class Test_timer_functions(unittest.TestCase):
    def test_token_timer(self):
        self.t = os.path.getctime('creds.json')
        self.created_time = datetime.fromtimestamp(self.t)
        self.now = datetime.now()
        self.delta = self.now - self.created_time
        self.delta_in_seconds = self.delta.seconds
        self.check = check_token_time()
        if self.delta_in_seconds <= 3600:
            self.assertFalse(self.check)
        else:
            self.assertTrue(self.check)

    def test_cache_timer(self):
        self.t = os.path.getctime('cache_contents.json')
        self.created_time = datetime.fromtimestamp(self.t)
        self.now = datetime.now()
        self.delta = self.now - self.created_time
        self.delta_in_days = self.delta.days
        self.check = check_token_time()
        if self.delta_in_days <= 1:
            self.assertTrue(self.check)
        else:
            self.assertFalse(self.check)

class Test_Make_Request(unittest.TestCase):
    def setUp(self):
        start_reddit_session()
        self.request = make_request('Art')
        self.post_dict = self.request['data']['children'][0]
        self.post_inst = Post(self.post_dict)
        self.token = open('creds.json')

    def test_live_request_dict(self):
        self.assertEqual({'subreddit': 'Art'}, self.post_inst.get_subreddit())

    def test_live_repr(self):
        self.assertEqual(self.post_inst.__repr__(), "{0}: Title - '{1}' has a score of {2}".format(self.post_inst.subreddit, self.post_inst.title, self.post_inst.score))

    def test_save_token(self):
        self.assertTrue(self.token.read())

    def test_live_instance_constructor(self):
        self.assertIsInstance(self.post_inst.title, str)
        self.assertIsInstance(self.post_inst.score, int)
        self.assertIsInstance(self.post_inst.subreddit, str)
        self.assertIsInstance(self.post_inst.kind, str)
        self.assertTrue(len(self.post_inst.title) <= 255)
        self.assertIsInstance(self.post_inst.gilded, int)
        self.assertIsInstance(self.post_inst.time_created, float)

    def tearDown(self):
        self.request
        self.post_dict
        self.post_inst
        self.token.close()

class Test_Plot_Output(unittest.TestCase):
    def setUp(self):
        #plot()
        self.f = open("subreddit_analysis.html")
        self.read = self.f.read()

    def test_plot(self):
        self.assertTrue(self.read)

    def test_plot_template(self):
        self.assertTrue("""{"title": "Cumulative Scores of Top 24 Hour Postings Per Subreddit Page""", self.read)

    def tearDown(self):
        self.f.close()


if __name__ == '__main__':
    unittest.main(verbosity = 2)