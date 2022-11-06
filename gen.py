from message_senders import DiscordSender
import json
import subprocess


class TextGenerator:
    def __init__(self, host: str, host_path: str, gen_script_path: str):
        self.host = host
        self.remote_result_path = host_path
        self.gen_script_path = gen_script_path

    def gen(self):
        # Generate
        cmd = self._build_gen_cmd()
        subprocess.run(cmd)

        # Get result from remote host
        cmd = self._build_get_cmd()
        subprocess.run(cmd)

        # Get result from file to string
        with open("generated.txt") as f:
            text = f.read()
        text = text.strip()
        return text

    def _build_gen_cmd(self):
        base_cmd = f"ssh {self.host} '{self.gen_script_path}'"
        base_cmd += ">/dev/null"
        cmd = ["bash", "-c", base_cmd]
        return cmd

    def _build_get_cmd(self):
        base_cmd = f"scp {self.host}:{self.remote_result_path} ./generated.txt"
        base_cmd += ">/dev/null"
        cmd = ["bash", "-c", base_cmd]
        return cmd


def main():
    with open("./cred.json") as f:
        api_keys = json.load(f)

    host = api_keys["host"]
    remote_result_path = api_keys["remote_result_path"]
    gen_script_path = api_keys["gen_script_path"]

    generator = TextGenerator(host, remote_result_path, gen_script_path)
    sender = DiscordSender(api_keys["discord_webhook_url"])

    generated_tweet = generator.gen()
    generated_tweet = "[GPT2 GENERATED] " + generated_tweet
    # sender.send(generated_tweet)
    print(generated_tweet)


if __name__ == "__main__":
    main()
