#!/usr/bin/python3

import json
import os
from pathlib import Path

from message_senders import DiscordSender, FileSender, RemoteFileSender, StdOutSender

from tweet_sender import twitter


def main():
    with open("./cred.json") as f:
        api_keys = json.load(f)
    target = api_keys["target"]
    host = api_keys["host"]
    host_path = api_keys["host_path"]

    senders = [
        FileSender(Path("./tweets.txt")),
        StdOutSender(),
        DiscordSender(api_keys["discord_webhook_url"]),
        RemoteFileSender(host=host, host_path=host_path),
    ]

    tweet_fether = twitter.TweetFetcher(
        api_keys=api_keys,
        target=target,
        senders=senders,
    )
    tweet_fether.send()


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
