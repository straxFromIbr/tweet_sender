import json
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

import requests


class Sender(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def send(self, text: str):
        pass


class DiscordSender(Sender):
    def __init__(self, api_key):
        self.api_key = api_key

    def send(self, text: str):
        headers = {"Content-Type": "application/json"}
        data = {}
        data["content"] = text
        response = requests.post(self.api_key, json.dumps(data), headers=headers)
        return response


class FileSender(Sender):
    def __init__(self, path: Path):
        self.path = path

    def send(self, text: str):
        with open(self.path, "a") as f:
            f.write(text + "\n")


class StdOutSender(Sender):
    def __init__(self, *args, **kwargs):
        pass

    def send(self, text: str):
        print(text)


class RemoteFileSender(Sender):
    def __init__(self, host: str, host_path: str):
        self.host = host
        self.path = host_path

    def send(self, text: str):
        cmd = self._build_command(text)
        subprocess.run(cmd)

    def _build_command(self, text: str):
        text = text.replace("\n", r"\n")
        base_cmd = f"ssh {self.host} 'echo -e \"{text.strip()}\" >> {self.path}'"
        cmd = ["sh", "-c", base_cmd]
        return cmd
