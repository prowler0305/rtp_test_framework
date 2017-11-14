from ptg2.zos.jesutil import *
from ptg2.context import set_system
from ptg2.context import set_userid
import argparse


def main():

    parser = argparse.ArgumentParser(description='Start/Stop Started Tasks')
    parser.add_argument('-l', '--lpar', required=True, help='A comma separated list of LPARs.')
    parser.add_argument('-u', '--user', required=True, help='The user ID to be used.')
    parser.add_argument('-s', '--stc', required=True, help='The started task name.')
    parser.add_argument('-sa', '--start-argument', required=False, help='The STC start arguments.', default=None)
    parser.add_argument('-a', '--action', required=True, help="Valid actions are 'start' or 'stop'.")
    args = vars(parser.parse_args())  # transform namespace object into a dictionary object

    action = args.get('action').upper()

    if action == 'START':
        start_stc(args)
    elif action == 'STOP':
        stop_stc(args)
    else:
        print('Invalid action command.  Must be either start or stop.')

    return

def start_stc(args):
    """
    Executes start commands.
    """

    systems = get_systems(args)
    stc = args.get('stc')
    user = args.get('user')

    # Execute the start command on each system
    for system in systems:
        print('Starting STC: %s on System: %s for User: %s' % (stc, system, user))
        set_system(system)
        set_userid(user)
        s = StartedTask(stc)
        s.start(args.get('start_argument'))


def stop_stc(args):
    """
    Executes stop commands.
    """
    systems = get_systems(args)
    stc = args.get('stc')
    user = args.get('user')

    # Execute the stop command on each system
    for system in systems:
        print('Stopping STC: %s on System: %s for User: %s' % (stc, system, user))
        set_system(system)
        set_userid(user)

        s = StartedTask(stc)
        s.stop()


def get_systems(args):
    return args.get('lpar').split(",", args.get('lpar').count(','))


if __name__ == "__main__":
    main()
