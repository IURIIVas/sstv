import argparse


class ArgParser:

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            prog="Slow-scan television coder/decoder",
        )

        self._args_add()
        self._args = self._parser.parse_args()

    @property
    def args(self):
        return self._args

    def _args_add(self):
        self._parser.add_argument(
            '-m', '--mode',
            type=str,
            help='Mode name'
        )
        self._parser.add_argument(
            '-c',
            action='store_true',
            help='Code image file'
        )
        self._parser.add_argument(
            '-d',
            action='store_true',
            help='Decode sound file'
        )
        self._parser.add_argument(
            '-sr',
            type=int,
            help='sample rate in Hz'
        )

        self._parser.add_argument(
            '-f',
            type=str,
            help='File path'
        )
