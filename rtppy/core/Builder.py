try:
    from termcolor import colored
except ImportError as i_error:
    import pip
    pip.main(['install', 'termcolor'])
    from termcolor import colored
import argparse
import json
import os
import pdt_tests.pdtAggregateKeys
import pdt_tests.pdtAggregatePlan
import pdt_tests.pdtAggregateProgram
import psa_tests.psaAggregateDbase

from core import InputParms
from pdt_tests.AbendRestart import AbendRestart
from pdt_tests.StartCollection import StartStopCollection
from pdt_tests.IntervalCompare import IntervalCompare
from pdt_tests.pdtExceptions import PdtExceptions
from pdt_tests.pdtLockRelease import LockRelease
from pdt_tests.pdtSQLText import SqlText
from psa_tests.PsaSamplingBoundary import PsaSamplingBoundary
from rtpj_tests.RTPJExec import RTPJExec
from rtptest_tests.rtptest import Rtptest


def create_aggregate_subclass(test_parms_dict, connection_instance, input_arg_dict):
    """
    For Aggregate Compare test type. Interrogates the "level" parameter and creates the appropriate
    Aggregate Compare subclass instance to be returned to the :py:Builder.py:build_tests.

    :param test_parms_dict:
    :param connection_instance:
    :param input_arg_dict:
    :return: Appropriate aggregate compare subclass instance based on the "level"
    """

    rc, level_value = InputParms.InputParms.check_json_parm(test_parms_dict, connection_instance, 'level')
    level_value = level_value.lower()
    if rc and level_value == 'plan':
        aggregate_compare_subclass = pdt_tests.pdtAggregatePlan.AggregatePlan(test_parms_dict, connection_instance, input_arg_dict, level_value)
        return aggregate_compare_subclass
    elif rc and level_value == 'program':
        aggregate_compare_subclass = pdt_tests.pdtAggregateProgram.AggregateProgram(test_parms_dict, connection_instance, input_arg_dict, level_value)
        return aggregate_compare_subclass
    elif rc and level_value == 'keys':
        aggregate_compare_subclass = pdt_tests.pdtAggregateKeys.AggregateKeys(test_parms_dict, connection_instance, input_arg_dict, level_value)
        return aggregate_compare_subclass
    elif rc and level_value == 'dbase':
        aggregate_compare_subclass = psa_tests.psaAggregateDbase.AggregateDbase(test_parms_dict, connection_instance, input_arg_dict, level_value)
        return aggregate_compare_subclass
    else:
        InputParms.InputParms.no_required_parameter('level')


class Builder(object):
    """
    Static class that contains different methods to parse the command line arguments and JSON input file. Also contains
    methods to build connection and test objects from the parsing of the command line and JSON input file.
    arguments.
    """
    test_class_dict = {'interval compare': IntervalCompare,
                       'aggregate compare': create_aggregate_subclass,
                       'psa sampling boundary': PsaSamplingBoundary,
                       'start collection': StartStopCollection, 'rtptest': Rtptest, 'stop collection': StartStopCollection,
                       'abend restart': AbendRestart, 'exceptions': PdtExceptions, 'distributed sql': RTPJExec,
                       'lock release': LockRelease, 'sql text': SqlText}

    file_path = None

    @staticmethod
    def parse_input_parameters():
        """
        Parses the command line arguments.

        :return: dictionary of command line arguments.
        """
        parser = argparse.ArgumentParser(description='Real Time Performance Automation Tests')
        parser.add_argument('-p', nargs='?', const='descriptions', choices=['descriptions', 'raw'], help='Print just the descriptions or the entire contents in the JSON file specified by --file argument. Use -p=raw to print entire JSON file contents. Defaults to just print descriptions.'),
        parser.add_argument('-lp', '--lpar')
        parser.add_argument('-usr', '--userid')
        parser.add_argument('-ss', '--ssid')
        parser.add_argument('-ss2', '--ssid2')
        parser.add_argument('-bld', '--baseline_datastore')
        parser.add_argument('-bv', '--baseline_vcat')
        parser.add_argument('-cud', '--current_datastore')
        parser.add_argument('-cv', '--current_vcat')
        parser.add_argument('-bid', '--baseline_interval_date')
        parser.add_argument('-bid2', '--baseline_interval_date_2')
        parser.add_argument('-bit', '--baseline_interval_time')
        parser.add_argument('-bit2', '--baseline_interval_time_2')
        parser.add_argument('-cid', '--current_interval_date')
        parser.add_argument('-cid2', '--current_interval_date_2')
        parser.add_argument('-cit', '--current_interval_time')
        parser.add_argument('-cit2', '--current_interval_time_2')
        parser.add_argument('-vb', '--view_by')
        parser.add_argument('-vt', '--view_type')
        parser.add_argument('-vo', '--view_option')
        parser.add_argument('-env', '--environment')
        parser.add_argument('-rp', '--range_pct')
        parser.add_argument('--column')
        parser.add_argument('-pln', '--plan')
        parser.add_argument('-pgm', '--program')
        parser.add_argument('-kv', '--key_value')
        parser.add_argument('-ko', '--key_option')
        parser.add_argument('-db', '--dbname')
        parser.add_argument('-lc', '--line_command')
        parser.add_argument('-col', '--collid')
        parser.add_argument('-con', '--connection_type')
        parser.add_argument('-auto', '--auto_submit')
        parser.add_argument('-cor', '--corrid')
        parser.add_argument('-sql', '--sqlid')
        parser.add_argument('-rpt', '--repeat')
        parser.add_argument('-wkst', '--workstation')
        parser.add_argument('-sd', '--seed')
        parser.add_argument('-mpp', '--multiple_plan_packages')
        parser.add_argument('-mth', '--multithreading')
        parser.add_argument('-wtc', '--wait_to_complete')
        parser.add_argument('--include_plan')
        parser.add_argument('--dataset_name')
        parser.add_argument('--xman')
        parser.add_argument('--xmanargs')
        parser.add_argument('--samp')
        parser.add_argument('--debug')
        parser.add_argument('--itime')
        parser.add_argument('--t_limit')
        parser.add_argument('--high_level')
        parser.add_argument('--abend_in')
        parser.add_argument('--num_ar')
        parser.add_argument('--collection_profile')
        parser.add_argument('--rtpj_file')
        parser.add_argument('--rtpj_library')
        parser.add_argument('--rtpj_sync')
        parser.add_argument('--rtpj_log_level')
        parser.add_argument('--output_location')
        parser.add_argument('-f', '--file', required=True)
        args = vars(parser.parse_args())  # transform namespace object into a dictionary object
        return args  # return dictionary

    @staticmethod
    def parse_json_input(file_name=None):
        """
        Opens the input file requested that is written in JSON format and loads the JSON format input parameters into a
        root dictionary node. The root dictionary will contain two separate objects, a connection dictionary object and
        a list(i.e. array) of test parameters dictionary objects. These two high level objects will be returned.

        :param file_name: JSON file name including the location if not located in the default "python_test_library"
                            directory.
        :return: connection node and test parameters node
        """

        if '/' in file_name or '\\' in file_name:
            Builder.file_path = file_name
        else:
            Builder.file_path = os.path.join(os.path.dirname(__file__), '..', 'python_test_library', file_name)

        with open(Builder.file_path) as f:
            root_node = json.load(f)

        connection_node = root_node.get('connection')  # connection node is a dictionary
        test_parms_node = root_node.get('tests')  # tests node is a list of dictionaries

        return connection_node, test_parms_node

    @staticmethod
    def build_connection(connection_node, input_arg_dict):
        """
        Creates and returns an instance of :py:class Connection. See documentation of class Connection for details
        :param connection_node: dictionary of connection information from a JSON file
        :param input_arg_dict: dictionary of override parameters from the command line
        :return: instance of :py:class Connection
        """
        conn = Connection(connection_node, input_arg_dict)
        return conn

    @staticmethod
    def build_tests(test_node, input_arg_dict, connection_instance):
        """
        Takes the test node(i.e. array) that is parsed from the JSON input file and parses it into separate tests
        identified by the 'test_type' parameter.

        Once identified creates an instance of that test class passing the dictionary of test parameters, connection
        instance, and dictionary of command line arguments passed in. Then calls that test instance build method and
        adds the test instance to the test list that is returned.

        :param test_node: array (i.e. python list) of test parameters
        :param input_arg_dict: dictionary of override parameters from the command line
        :param connection_instance: instance of :py:Class BuildConnection
        :return list of test objects
        """
        test_list = []
        for test_dict in test_node:
                if "test_type" in test_dict:
                    test_class_key = test_dict.get('test_type')
                    if test_class_key in Builder.test_class_dict:
                        test_instance = Builder.test_class_dict.get(test_class_key)(test_dict, connection_instance, input_arg_dict)
                        test_instance.build_test()
                        test_list.append(test_instance)
                    else:
                        print("'%s' is not a known test_type" % test_class_key)
                else:
                    raise KeyError("Key: test_type not found in input JSON file test parameters")
        return test_list

    @staticmethod
    def description_output(test_node, input_arg_dict):
        """
        For every test in the JSON file that has a description parameter print its description or print raw contents.
        :param test_node: test object from JSON file.
        :param input_arg_dict: dictionary of command line arguments
        :return: Nothing
        """

        p_option_value = input_arg_dict.get('p')

        if p_option_value == 'descriptions':
            for test_dict in test_node:
                if "description" in test_dict:
                    print(test_dict.get("description"))
        else:
            with open(Builder.file_path) as f:
                file_contents = f.read()
            print(file_contents)


class Connection(object):
    """
    Connection class that represents the information needed to connect to the mainframe and the DB2 subsystem to
     interact with for a set of tests.
    """
    def __init__(self, connection_node, input_arg_dict):
        """
        :param connection_node: dictionary of connection information from the JSON File
        :param input_arg_dict: dictionary of override parameters from the command line
        """
        self.connection = connection_node
        self.override_dict = input_arg_dict

    def get_lpar(self):
        """
        Determines the correct LPAR to return by interrogating if the -lp or --lpar= parameter was given on the command
        line, if not then looks and returns the LPAR specified in the JSON file in the connection section.
        :return: LPAR to connect to (i.e. ca31, ca11)
        """

        if self.override_dict.get('lpar'):
            return self.override_dict.get('lpar')
        else:
            return self.connection.get('lpar')

    def get_ssid(self):
        """
        Determines the correct SSID to return by interrogating if the -ss or --ssid= parameter was given on the command
        line, if not then looks and returns the ssid specified in the JSON file in the connection section.
        :return: DB2 SSID to use
        """

        if self.override_dict.get('ssid'):
            return self.override_dict.get('ssid')
        else:
            return self.connection.get('ssid')

    def get_ssid2(self):
        """
        Determines the correct SSID2 to return by interrogating if the -ss or --ssid2= parameter was given on the command
        line, if not then looks and returns the ssid2 specified in the JSON file in the connection section.
        :return: DB2 SSID2 to use
        """

        if self.override_dict.get('ssid2'):
            return self.override_dict.get('ssid2')
        else:
            return self.connection.get('ssid2')

    def get_userid(self):
        """
        Determines the correct userid to return by interrogating if the -usr or --userid= parameter was given on the
        command line, if not then looks and returns the userid specified in the JSON file in the connection section.
        :return: Userid to use to connect to the mainframe.
        """

        if self.override_dict.get('userid'):
            return self.override_dict.get('userid').lower()
        else:
            return self.connection.get('userid').lower()
