import unittest
from unittest.mock import patch, Mock
from functions import (research, search_from_reddit, search_from_arxiv,
                        keywords_to_list, create_corpus, read_corpus)

class TestYourFunctions(unittest.TestCase):

    @patch('praw.Reddit')
    def test_search_from_reddit(self, mock_reddit):
        # Mocking praw.Reddit pour simuler des requetes 
        mock_instance = mock_reddit.return_value
        mock_instance.subreddit.return_value.search.return_value = [
            self.create_mock_post("Title 1", "Text 1"),
            self.create_mock_post("Title 2", "Text 2")
        ]

        result = search_from_reddit("test", 2)
        # print(result)
        self.assertEqual(len(result) > 0, True)

    def test_search_from_arxiv(self):
        result = search_from_arxiv("test", 2)
        self.assertTrue(len(result) > 0, True)

    def test_keywords_to_list(self):
        result = keywords_to_list("word1,word2,word3")
        expected_result = ["word1", "word2", "word3"]
        self.assertEqual(result, expected_result)

    def test_create_corpus(self):
        result = create_corpus()
        self.assertTrue(result is not None)

    def test_read_corpus(self):
        result = read_corpus()
        self.assertTrue(result is not None)

    # creation de mock pour simuler reddit
    def create_mock_post(self, title, text):
        mock_post = Mock()
        mock_post.title = title
        mock_post.selftext = text
        return mock_post

if __name__ == '__main__':
    unittest.main()
