from ptg2.context import get_userid
from ptg2.zos.jesutil import *
from ptg2.user_input import user_input


def ask_user():

    lpar = user_input('Set LPAR to interact with(i.e. ca31) ')
    user_action = user_input('S - Start or P - for Stop ')
    user_action = user_action.lower()
    user_xman = user_input('Name of Xmanager to start? ')
    rc = use_lpar(lpar)
    if rc:
        return True, user_xman, user_action
    else:
        return False


def use_lpar(lpar_name):

    set_system(lpar_name)
    ca_system_connected = get_system()
    if ca_system_connected == lpar_name:
        print ('Connection not establish, LPAR name %s is incorrect.' % ca_system_connected)
        return False
    else:
        print("Connected to %s" % ca_system_connected)
        return True


def start_xman(xman):

    stc = StartedTask(xman)

    if not stc.is_running():
        print ("Xman: %s is not running." % xman)
        print ("Starting Xman now.....")
        stc.start(skip_check=True)

        if stc.is_running():
            print ('Xman: %s has started successfully.' % xman)
    else:
        print('Xmanager: %s is already started.' % xman)

    return


def stop_xman(xman):

    stc = StartedTask(xman)

    if not stc.is_running():
        print ("Xman: %s is not running." % xman)
    else:
        print('Stopping Xmanager now......')
        stc.stop()

    return

if __name__ == "__main__":
    rc, xman_stc_name, action = ask_user()
    while not rc:
        rc, xman_stc_name, action = ask_user()
    if action == 's':
        start_xman(xman_stc_name)
    if action == 'p':
        stop_xman(xman_stc_name)
