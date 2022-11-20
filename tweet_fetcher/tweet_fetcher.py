import json
import os
from typing import List

from message_senders import BaseSender
from requests_oauthlib import OAuth1Session


class TweetFetcher:
    api_root = "https://api.twitter.com/2"

    def __init__(
        self,
        api_keys: dict,
        target,
        senders: List[BaseSender],
        max_id=None,
        prefix="",
        since_id_path="since_id",
    ):
        # APIキーの設定
        cons_key = api_keys["cons_key"]
        cons_sec = api_keys["cons_sec"]
        access_token = api_keys["access_token"]
        access_sec = api_keys["access_sec"]
        self.session = OAuth1Session(cons_key, cons_sec, access_token, access_sec)
        self.api_url = f"{self.api_root}/users/{target}/tweets"

        self.prefix = prefix

        if max_id is not None:
            self.since_id = max_id

        self.senders = senders
        self.since_id_path = since_id_path

    def get_tweet(self, max_results=None):
        params = {}
        if max_results is not None:
            params["max_results"] = max_results

        # 前回のツイート取得じに保存したmax_idを取得
        if self.since_id is not None:
            params["since_id"] = self.since_id

        result = self.session.get(self.api_url, params=params)
        result_json = result.json()
        if result_json["meta"]["result_count"] == 0:
            return None

        self.since_id = result_json["meta"]["newest_id"]
        latest_tweets = list(map(lambda t: t["text"], result_json["data"]))
        return latest_tweets

    def send(self):
        tweets = self.get_tweet()
        if tweets is None:
            print("tweets is None")
            return

        tweet = self.prefix + tweets[0]
        for sender in self.senders:
            sender.send(tweet)

    @property
    def since_id(self):
        since_id = self._load()
        if since_id is None:
            return "0"
        return since_id["since_id"]

    @since_id.setter
    def since_id(self, since_id):
        if since_id is None:
            since_id = "0"
        self._dump({"since_id": since_id})

    def _dump(self, obj: dict):
        with open(self.since_id_path, "w") as f:
            json.dump(obj, f)

    def _load(self):
        fname = self.since_id_path
        if not os.path.exists(fname):
            return None

        with open(fname, "r") as f:
            result = json.load(f)
        return result
