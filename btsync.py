import os
import sys
import json
import argparse
import subprocess as sp


DEFAULT_CONF_DIR = os.path.join(os.environ["HOME"], ".btback")


def parse_args(args=None):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t", "--true-run",
        help="Really run sync. Default: dry run.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-u", "--up",
        help="Sync up. Default: sync down.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        '--conf-dir',
        help=f"Configuration directory. Default: {DEFAULT_CONF_DIR}",
        type=str,
        default=DEFAULT_CONF_DIR,
    )

    parser.add_argument(
        '--element',
        help="Which element to sync. Default: home.",
        type=str,
        default="home",
    )

    if args is None:
        args = sys.argv[1:]

    return parser.parse_args(args)


class Sync:

    CONF_FN = "conf.json"

    def __init__(self, opts):
        self.opts = opts
        self._conf = None

    @property
    def command(self):
        cmd = ["rsync", "-rltuvh", "--progress", "--delete"]

        if self.dry_run:
            cmd.append("--dry-run")

        cmd.append(f"--exclude-from={self.exclude}")
        cmd.append(f"{self.source}/")
        cmd.append(f"{self.destination}/")

        return cmd

    def run_command(self):
        s = sp.Popen(self.command)
        s.communicate()

    @property
    def exclude(self):
        fn = f"{self.element}.{self.direction}.exclude"
        path = os.path.join(self.conf_dir, fn)

        if not os.path.isfile(path):
            raise FileExistsError(f"Required exclude file '{path}' not found!")

        return path

    @property
    def conf_dir(self):
        return self.opts.conf_dir

    @property
    def dry_run(self):
        return not self.opts.true_run

    @property
    def element(self):
        return self.opts.element

    @property
    def direction(self):
        """Which way we are syncing, up or down."""

        if self.opts.up:
            return "up"

        return "down"

    @property
    def conf_path(self):
        return os.path.join(self.conf_dir, self.CONF_FN)

    @property
    def conf(self):
        if self._conf is None:
            with open(self.conf_path) as f:
                self._conf = json.load(f)

        return self._conf

    @property
    def source(self):
        src = self.conf.get("elements", {}).get(self.element, {}).get("src_dir")
        if src is None:
            raise KeyError(f"Configuration file '{self.conf_path}' has no source dir for element '{self.element}'")

        return src

    @property
    def destination(self):
        dest = self.conf.get("elements", {}).get(self.element, {}).get("dest_dir")
        if dest is None:
            raise KeyError(f"Configuration file '{self.conf_path}' has no destination dir for element '{self.element}'")

        return self.conf["destination"] + dest


def main(opts):
    sync = Sync(opts)
    sync.run_command()


if __name__ == "__main__":
    options = parse_args()
    main(options)

