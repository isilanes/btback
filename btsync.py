import os
import sys
import argparse


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

    def __init__(self, opts):
        self.opts = opts

    @property
    def command(self):
        cmd = ["rsync", "-rltuvh", "--progress", "--delete"]

        if self.dry_run:
            cmd.append("--dry-run")

        return cmd
        #cmd = "rsync -rltuvh --progress --delete rpi:/backup/all/home/isilanes/ --exclude-from=up.exclude"

    @property
    def exclude(self):
        fn = f"{self.element}.{self.way}.exclude"
        return os.path.join(self.conf_dir, fn)

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
    def way(self):
        """Which way we are syncing, up or down."""

        if self.opts.up:
            return "up"

        return "down"


def main(opts):
    sync = Sync(opts)
    print(sync.command)


if __name__ == "__main__":
    options = parse_args()
    main(options)

