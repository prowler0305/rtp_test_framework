import os
import sys
import time
from ptg2.common import is_jenkins
from core.InputParms import InputParms
from core.common import CommonNav


class BaseTest(object):
    """
    Base class in which other specific product test classes inherit. This class can and will contain either generic
    methods or methods in which are overloaded by specific test class methods.
    """
    output_file_opened = False
    output_directory = None

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        self.dict_parms = test_parms_dict
        self.connection = connection_instance
        self.command_line_overrides = input_arg_dict
        self.expected_parms_dict = {}  # dictionary of required parms and their values
        self.optional_parms_dict = {}  # dictionary of optional parms and their values
        self.default_parms_dict = {}
        self.type_of_parameter_dict = {'required': self.expected_parms_dict, 'default': self.default_parms_dict,
                                       'optional': self.optional_parms_dict}
        self.product_release = 'R19'
        self.product_code = None
        self.debug_mode = 'N'
        self.output_location = None
        self.specific_column_to_compare = None
        self.common_expected_parms_list = ['lpar', 'ssid', 'userid', 'product_code']
        self.common_optional_parms_list = ['environment', 'debug', 'output_location', 'ssid2', 'column']

    def build_test(self):
        """
        Check and set all the expected and optional parameters that are for all tests.
        :return:
        """

        for parm in self.common_expected_parms_list:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'product_code':
                    self.product_code = value.upper()

                self.expected_parms_dict[parm] = value
            else:
                InputParms.no_required_parameter(parm)

        for parm in self.common_optional_parms_list:
            rc, value = self.get_parm_value(parm)
            if parm == 'environment':
                if rc:
                    self.product_release = value
                    self.optional_parms_dict[parm] = value
                else:
                    self.default_parms_dict[parm] = self.product_release
            elif parm == 'debug':
                if rc:
                    if value == 'Y' or value == 'y':
                        self.debug_mode = value
                        self.optional_parms_dict[parm] = value
            elif parm == 'output_location':
                if rc:
                    self.output_location = value
                    self.optional_parms_dict[parm] = value
            elif parm == 'column':
                if rc:
                    self.specific_column_to_compare = value
                    self.optional_parms_dict[parm] = value

    def get_parm_value(self, parameter_to_find):
        """
        Checks the parameters passed in on the command line (if any) and in the JSON file for the parameter requested.
        :param parameter_to_find: name of the parameter to find. (e.g. current_datastore)
        :return: returns a tuple - (True, parameter value) or (False, "")
        """

        rc, value = InputParms.check_override_parm(self.command_line_overrides, parameter_to_find)
        if not rc:
            rc, value = InputParms.check_json_parm(self.dict_parms, self.connection, parameter_to_find)
        return rc, value

    def check_if_output_file_needed(self, name_to_call_file):
        """
        If the parameter output_location has been given a path and the output file hasn't already been opened by a
        previous similar test then call common routine to set the file directory where output will be written and set
        global class flag that output file has been opened in case JSON file has more than 1 of the same kind of test.
        :param name_to_call_file:
        :return: nothing
        """
        if self.output_location is not None:
            if not BaseTest.output_file_opened:
                BaseTest.output_directory, file_was_opened = self.setup_output_file(self.output_location, name_to_call_file)
                BaseTest.output_file_opened = file_was_opened
            else:
                return
        else:
            return

    def parameter_summary(self):
        """
        Calls the static method print_parameter_summary for each of the BaseTest parameter dictionaries defined.
        :return:
        """

        for param_type, param_dict in self.type_of_parameter_dict.items():
            self.print_parameter_summary(param_dict, parameter_type=param_type, output_file=self.output_directory)

    @staticmethod
    def setup_output_file(workspace_path, file_name):
        """
        See if the directory and file exists. If it doesn't it creates the output directory in the path
        and either way creates the output file or clears it if it already exists. Returns the path where the output 
        should be written.

        :param workspace_path: directory path where output should be located.
        :param file_name: The name of the file the output will be written to.
        :return: tuple(output directory path to be used, file opened)
        """
        file_open = False
        directory_location = workspace_path + '/' + 'python_test_output'

        if is_jenkins():
            if not os.path.exists(directory_location):
                os.makedirs(directory_location)

            directory_location += '/' + file_name + '.txt'
            with open(directory_location, mode='w') as (output_file):
                output_file.write(' \n')
                file_open = True
        else:
            if not os.path.exists(directory_location):
                os.makedirs(directory_location)

            directory_location += '/' + file_name + '.txt'
            with open(directory_location, mode='w') as (output_file):
                output_file.write(' \n')
                file_open = True

        return directory_location, file_open

    @staticmethod
    def print_parameter_summary(parameter_dict, parameter_type='required', output_file=None):
        """
        Outputs a summary of the parameters and their values.

        :param parameter_dict: a dictionary of parameter names (key), and their values
        :param parameter_type: indicates whether the parameters in the dictionary are 'required', 'default, or 'optional'
        :param output_file: Optional - If provided will write the summary to the file indicated, otherwise prints to the
                                        console.
        :return: Nothing
        """

        if parameter_type == 'required':
            parameter_title = 'Required Parameters:'
        elif parameter_type == 'optional':
            parameter_title = 'Optional Parameters:'
        elif parameter_type == 'default':
            parameter_title = 'Default Parameters:'
        else:
            print('parameter_type - %s not an option.' % parameter_type)
            return

        title_len = len(parameter_title)
        dashes = '-' * title_len

        if len(parameter_dict) > 0:
            if output_file is None:
                print('\n' + parameter_title)
                print(dashes)
                for parm, value in parameter_dict.items():
                    if parm == 'options':
                        for options_parms, options_values in value.items():
                            print('%s: %s' % (options_parms, options_values))
                    else:
                        print('%s: %s' % (parm, value))
                print(dashes)
            else:
                with open(output_file, mode='a') as (out):
                    out.write('\n' + parameter_title)
                    out.write('\n' + dashes)
                    for parm, value in parameter_dict.items():
                        out.write('\n %s: %s' % (parm, value))
                    out.write('\n' + dashes)

    @staticmethod
    def raise_row_not_found_exception(navigation_instance, string_to_print):
        """
        Throws a ValueError exception and will access and print the current screen the navigation instances's emulator
        instance is looking at.
        :param navigation_instance:
        :param string_to_print: A text string to print along with the current screen
        :return:
        """

        navigation_instance.ptg2_em.screen.print_screen(fields=False)
        raise ValueError('%s' % string_to_print)

    @staticmethod
    def countdown_timer(seconds_to_wait, watch_timer=True):
        """
        Wait based on the number of seconds requested and optional show the count down.

        :param seconds_to_wait: number of seconds to wait for.
        :param watch_timer: If true prints the timer as it counts down each second.
        :return:
        """

        if watch_timer:
            print("Waiting for %s seconds." % seconds_to_wait)
        for t in range(seconds_to_wait, 0, -1):
            if watch_timer:
                sys.stdout.write("\r%d" % t)
                sys.stdout.flush()
            time.sleep(1)
        if watch_timer:
            sys.stdout.write("\n")
            sys.stdout.flush()

    @staticmethod
    def db2_ver_mod_csect_name(mod_string, ssid, csect_string=None):
        """
        Returns the DB2 specific module and csect name (if provided)

        :param mod_string: A RTP product db2 version specific module name string without the version (i.e. 'PDTDIUC')
        :param csect_string: A RTP product db2 version csect name string without the version (i.e. 'DT$DIUC')
        :param ssid: SSID of the db2 version (i.e. 'D11A')
        :return: Tuple - (module_name, None) or (module_name, csect_name)
        """

        ssid_version = CommonNav.db2_version(ssid)
        module_name = mod_string + ssid_version[1]
        if csect_string is None:
            return module_name, None
        else:
            csect_name = csect_string + ssid_version[1]
            return module_name, csect_name
