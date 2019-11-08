import argparse

from realsteel import robot


def REAL_STEEL_EXPERIENCE():
    """
    The primary real steel experience 
    """
    pass


def DEV_ARM_HARDWARE():
    """
    Launches the mirroring program connected to a physical device 
    """
    pass


def DEV_ARM_SOFTWARE():
    """
    Launches the mirroring program with just a software robot
    """
    pass





parser = argparse.ArgumentParser(description='Launch the Real Steel Experience')

parser.add_argument('--dev', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='Run the Real Steel experience in developer mode')

parser.add_argument('--prod', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='Run the Real Steel experience in prod/demo mode')

parser.add_argument('--software', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help="Use only software displays")

parser.add_argument('--hardware', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

parser.add_argument('--urdf', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='specify a custom urdf file to generate the robot from')


if __name__ == "__main__":
    # Currently just bypasses into dev-software 
    robot.ROBOT().start()

    pass