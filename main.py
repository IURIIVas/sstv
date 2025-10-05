from src.utils.argparser import ArgParser
from src.modes.robot.robot_8_bw import Robot8Bw


class SlowScanTelevision:

    def __init__(self):
        parser = ArgParser()
        self._args = parser.args

    def run(self):
        mode = Robot8Bw(self._args.f, self._args.sr)

        mode.code()


if __name__ == '__main__':
    sstv = SlowScanTelevision()
    sstv.run()
