import Algorithmia
from django.conf import settings


class Algorithm:
    @classmethod
    def search(self, tweet_content, algo_path):
        client = Algorithmia.client(settings.ALGORITHMIA_API_KEY)
        algo = client.algo(algo_path)
        return (algo.pipe(tweet_content))
