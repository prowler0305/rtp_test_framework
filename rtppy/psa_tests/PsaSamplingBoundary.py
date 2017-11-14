# Python imports
import os
import time
import sys
import collections
import logging

# PTG2 imports
from ptg2.zos.jesutil import send_mvs_command, StartedTask
from ptg2.context import set_system, set_userid
from ptg2.zos.jes import Job, short_system_name, JobException, jcl_strip, parse_jcl
from ptg2.common import is_jenkins

# RTPPY imports
from core.common import CommonNav
from core.BaseTest import BaseTest
from core.Psa_nav import NavPsa
from core.Rtp_Java import RtpJava
from core.InputParms import InputParms


class PsaSamplingBoundary(BaseTest):
    """
    Document this class
    """
    output_file_opened = False
    output_directory = None
    test_name = 'PsaSamplingBoundary'

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        BaseTest.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.baseline_datastore = None
        self.baseline_vcat = None
        self.baseline_interval_date = None
        self.baseline_interval_time = None
        self.current_datastore = None
        self.current_vcat = None
        self.current_interval_date = None
        self.current_interval_time = None
        self.view_by = None
        self.view_type = None
        self.range_pct = None
        self.product_release = None
        self.debug_mode = 'N'
        self.output_location = None
        self.specific_column_to_compare = None
        self.result_sets_row_mapping = {}
        self.keyset = None
        self.options = None
        self.samp = 100
        self.repeat = 1
        self.results = None
        self.xman = None
        self.xmanargs = None
        self.minimum = None
        self.results_file = None
        self.expected_parms_dict = {}  # dictionary of required parms and their values
        self.optional_parms_dict = {}  # dictionary of optional parms and their values

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """

        expected_parms = ['current_datastore', 'current_vcat', 'xman', 'samp',
                          'view_by', 'lpar', 'ssid', 'userid', 'keyset', 'options']

        for parm in expected_parms:
            rc, value = InputParms.check_override_parm(self.command_line_overrides, parm)
            if not rc:
                rc, value = InputParms.check_json_parm(self.dict_parms, self.connection, parm)
                if not rc:
                    InputParms.no_required_parameter(parm)
                    continue

            if parm == 'baseline_datastore':
                self.baseline_datastore = value
                self.expected_parms_dict[parm] = value
            elif parm == 'baseline_vcat':
                self.baseline_vcat = value
                self.expected_parms_dict[parm] = value
            elif parm == 'current_datastore':
                self.current_datastore = value
                self.expected_parms_dict[parm] = value
            elif parm == 'current_vcat':
                self.current_vcat = value
                self.expected_parms_dict[parm] = value
            elif parm == 'view_by':
                self.view_by = value
                self.expected_parms_dict[parm] = value
            elif parm == 'keyset':
                self.keyset = value
                self.expected_parms_dict[parm] = value
            elif parm == 'options':
                self.options = value
                self.expected_parms_dict[parm] = value
            elif parm == 'xman':
                self.xman = value
                self.expected_parms_dict[parm] = value
            elif parm == 'samp':
                self.samp = int(value)
                self.expected_parms_dict[parm] = int(value)
            else:
                continue

        optional_parms = ['ssid2', 'range_pct', 'environment', 'debug', 'column',
                          'view_type', 'output_location', 'repeat', 'xmanargs', 'minimum']
        for opt_parm in optional_parms:
            rc, value = InputParms.check_override_parm(self.command_line_overrides, opt_parm)
            if not rc:
                rc, value = InputParms.check_json_parm(self.dict_parms, self.connection, opt_parm)
                # If optional parameter either doesn't exist or was specified with no value. Print out warning
                # message and optionally set a default value.
                if not rc:
                    if opt_parm == 'range_pct':
                        self.range_pct = 1
                        self.optional_parms_dict[opt_parm] = self.range_pct
                        print('For view_by = %s.' % self.view_by),
                        InputParms.no_optional_parameter(opt_parm, str(self.range_pct) + '%')

                    elif opt_parm == 'environment':
                        InputParms.no_optional_parameter(opt_parm, 'frameworks default release')
                    else:
                        continue
                else:
                    self.set_optional_parm_value(opt_parm, value)
            else:
                self.set_optional_parm_value(opt_parm, value)

    def set_optional_parm_value(self, opt_parm, value):
        """
        Sets optional parm values
        :param opt_parm:  The name of the optional parm.
        :param value: The value.
        :return: No return value
        """
        if opt_parm == 'range_pct':
            self.range_pct = float(value)
            self.optional_parms_dict[opt_parm] = value
        elif opt_parm == 'environment':
            self.product_release = value
            self.optional_parms_dict[opt_parm] = value
        elif opt_parm == 'debug':
            if value == 'Y' or value == 'y':
                self.debug_mode = value
        elif opt_parm == 'column':
            self.specific_column_to_compare = value
            self.optional_parms_dict[opt_parm] = value
        elif opt_parm == 'view_type':
            self.view_type = value
            self.optional_parms_dict[opt_parm] = value
        elif opt_parm == 'baseline_interval_date':
            self.baseline_interval_date = value
            self.expected_parms_dict[opt_parm] = value
        elif opt_parm == 'baseline_interval_time':
            self.baseline_interval_time = value
            self.expected_parms_dict[opt_parm] = value
        elif opt_parm == 'current_interval_date':
            self.current_interval_date = value
            self.expected_parms_dict[opt_parm] = value
        elif opt_parm == 'current_interval_time':
            self.current_interval_time = value
            self.expected_parms_dict[opt_parm] = value
        elif opt_parm == 'output_location':
            self.output_location = value
        elif opt_parm == 'repeat':
            self.repeat = value
        elif opt_parm == 'minimum':
            self.minimum = value
        elif opt_parm == 'xmanargs':
            self.xmanargs = value
        else:
            pass

    def execute_test(self):
        """
        Executes the PSA Sampling Boundary test.;
        :return: 0(zero) - The test successfully completed and all values fell within the appropriate ranges.
                -1 - The test has failed.
        """

        # Supported sampling rates and the required minimum getpages for accurate counts.
        samp_rates = collections.OrderedDict([(100, 10000), (50, 10000), (25, 30000),
                                              (12, 70000), (6, 150000), (3, 300000)])

        # Process minimum override
        if self.minimum is not None:
            samp_rates[self.samp] = self.minimum

        if self.output_location is not None:
            CommonNav.create_dir(self.output_location)
            f_name = "{:s}{:d}_{:d}{:s}".format(PsaSamplingBoundary.test_name, self.samp, samp_rates[self.samp], ".csv")
            self.results_file = CommonNav.create_file_path(self.output_location, f_name)
            CommonNav.delete_file(self.results_file)

        CommonNav.print_test_start_end('PsaSamplingBoundary', file_name=PsaSamplingBoundary.output_directory)

        BaseTest.print_parameter_summary(self.expected_parms_dict, output_file=PsaSamplingBoundary.output_directory)
        BaseTest.print_parameter_summary(self.optional_parms_dict, parameter_type='optional',
                                         output_file=PsaSamplingBoundary.output_directory)

        # Set the lpar and userid
        set_system(self.connection.get_lpar())
        set_userid(self.connection.get_userid())

        if self.xman is not None:
            s = StartedTask(self.xman)
            if not s.is_running():
                s.start(self.xmanargs)

        # Execute the desired RTPJ program to check if the objects exist
        rc = RtpJava.execute_rtpj('RTPJ_Object_Check.JSON',
                                  ssid=self.connection.get_ssid(),
                                  userid=self.connection.get_userid())

        # Create the required Test objects if they don't exist.
        if rc != 0:
            # Create the test objects
            rc = RtpJava.execute_rtpj('RTPJ_Create_4K_Rows.JSON',
                                      ssid=self.connection.get_ssid(),
                                      userid=self.connection.get_userid())

        if rc != 0:
            print("RTPJ Failed to create the required test objects. Aborting Test.")
            raise Exception("An error occurred while executing the RTPJ framework to create the required test objects.")

        if self.debug_mode is not 'N':
            navigate_psa = NavPsa(self.connection.get_lpar(), self.connection.get_ssid(), self.connection.get_userid(),
                                  datastore_name=self.current_datastore, interval_date=self.current_interval_date,
                                  interval_time=self.current_interval_time, vcat=self.current_vcat,
                                  output_file=PsaSamplingBoundary.output_directory, debug_mode=self.debug_mode)
        else:
            navigate_psa = NavPsa(self.connection.get_lpar(), self.connection.get_ssid(), self.connection.get_userid(),
                                  datastore_name=self.current_datastore, interval_date=self.current_interval_date,
                                  interval_time=self.current_interval_time, vcat=self.current_vcat,
                                  output_file=PsaSamplingBoundary.output_directory)

        print("Running PSA Sampling boundary test with Sampling Rate %s%%" % self.samp)
        # Test Elapsed time tracker
        start = time.time()
        b_list = None
        # If test level optional parameter "environment" specified override method default parameter. Otherwise let it
        # default.
        try:
            if self.product_release is not None:
                navigate_psa.start_psa(release_environment=self.product_release)
            else:
                navigate_psa.start_psa()

            # Stop PSA Collection
            print('Stopping PSA collection on: %s' % self.connection.get_ssid().upper())
            navigate_psa.psa_terminate_collection()
            print('Waiting 20 seconds for PSA collection to terminate.')
            time.sleep(20)

            # Start PSA Collection
            print("Starting the PSA collection using sampling rate: %s%%" % self.samp)
            self.options.update({'samp': self.samp})
            navigate_psa.psa_start_collection(self.options)

            # Access the current interval data
            navigate_psa.psa_main_menu_option('1', None)

            # Access the Table Display
            navigate_psa.psa_view_by('T')

            # Calculate the number of 10,000 getpages needed to reach the minimum GP count.
            min_gp = samp_rates.get(self.samp)  # Get the minimum getpages for the current sample rate
            # Set primary keys to locate
            self.results = self.build_keys_dict()

            for i in range(0, self.repeat):

                # Start Background activity process
                b_list = self.start_background_process(min_gp)

                # Execute the desired RTPJ program
                rc = RtpJava.execute_rtpj('PSA_Samp_{0}K_GP_Test.JSON'.format(int(min_gp/1000)),
                                          ssid=self.connection.get_ssid(),
                                          userid=self.connection.get_userid())

                # rc = RtpJava.execute_rtpj('PSA_Samp50_10K_GP_Test.JSON',
                #                           ssid=self.connection.get_ssid(),
                #                           userid=self.connection.get_userid())

                # Check the RTPJ return code.
                if rc != 0:
                    raise Exception("An error occurred while executing the RTPJ framework. Aborting Test.")

                # Wait for PSA on first execution.
                if i == 0:
                    print('Waiting 10 seconds for PSA to update table names.')
                    time.sleep(10)  # Wait for PSA to update the table name(s).

                # Refresh the table display
                navigate_psa.refresh()

                # Build the table result
                result = navigate_psa.build_display_table()

                # init row dictionary
                row_ids = result.init_rows_not_found()

                # Process all key_sets
                for col_keys in self.keyset:

                    # locate the matching row
                    row = result.find_key_row(row_ids, col_keys)

                    # Validate the desired row was found.
                    if row == -1:
                        raise Exception("Matching Row was not found.")

                    # Get the getpage value from the matching row
                    getpages = result.get_row_data('GETPAGE', row)

                    # Update the value in the result
                    self.update_results(col_keys, getpages)

                # Stop background activity process
                print("Stopping RTPJ background activity process.")
                self.stop_background_process(b_list)

            # Stop the PSA Collection
            print('Stopping PSA collection on: %s' % self.connection.get_ssid().upper())
            navigate_psa.psa_terminate_collection()

            # Validate the results
            print('Validating Getpage Counts for Sampling Rate: %s%%' % self.samp)
            test = self.validate_getpages(min_gp)

            # Calculate test elapsed time
            total_time = time.time() - start
            CommonNav.println('Total Test Execution Time: {:f}'.format(total_time))

            # Logoff user session
            navigate_psa.stop_emulator()

            return test, self.output_location

        except Exception as e:
            navigate_psa.stop_emulator()  # Try to logoff the user session.
            if b_list is not None:
                self.stop_background_process(b_list)  # Stop the background activity process
            raise e

    def build_keys_dict(self):
        """
        Builds a dictionary of key values from the .json file "keys" node.
        Also builds a result bucket for each key row.
        :return: a column key dictonary of (column name, value).
        """
        getpage_results = collections.OrderedDict()

        for keys in self.keyset:
            name = ''
            for k, v in keys.items():
                name += v
            getpage_results.update({name: []})  # Initialize row getpage result dictionary
        return getpage_results

    def validate_getpages(self, expected):
        """
        Validates the getpage results and prints them.
        :param expected:
        :param rate:
        :return:
        """

        if self.results_file is not None:
            print("Writing results to file: %s" % self.results_file)

        total = 0
        failed = 0
        pct = self.range_pct / 100.0
        lbound = int(expected - (expected * pct))
        hbound = int(expected + (expected * pct))
        failed_list = []

        verdict = True
        result_count = 0
        CommonNav.println('Object, Run, Expected Getpages, Actual Getpages, Accuracy, Rate, Pass/Fail ', self.results_file)
        for key, result in self.results.items():
            result_count += len(result)
            for j, actual in enumerate(result):
                acc = (100.0 - ((abs(expected - actual)/float(expected)) * 100.0))
                temp = "{:s}, {:d}, {:d}, {:d}, {:f}%, {:d}, {:s}"
                pf = 'Passed'

                if actual < lbound or actual > hbound:
                    failed += 1
                    pf = 'Failed'
                    line = temp.format(key, j, expected, actual, round(acc, 2), self.samp, pf)
                    failed_list.append(line)
                else:
                    line = temp.format(key, j, expected, actual, round(acc, 2), self.samp, pf)

                CommonNav.println(line, self.results_file)
                total += actual

        if failed > result_count * .05:
            res_msg = "Total Runs: {:d} Total Failed: {:d}".format(result_count, failed)
            CommonNav.println(res_msg)
            verdict = False

        CommonNav.println("Total Getpages Counted: {:d}".format(total))
        CommonNav.println("Total passed: {:d} Total Failed {:d}".format(result_count - failed, failed))

        # Print out the specific failures (if any).
        if len(failed_list) > 0:
            CommonNav.println('', self.results_file)
            CommonNav.println('Failed Tests', self.results_file)
            CommonNav.println('Object, Run, Expected Getpages, Actual Getpages, Accuracy, Rate, Pass/Fail ', self.results_file)
            CommonNav.printlns(failed_list, self.results_file)

        if verdict:
            CommonNav.println("Final Result: PASSED")
        else:
            CommonNav.println("Final Result: FAILED")

        return verdict

    def concat_dict_keys(self, dict):
        """
        Concatenates the keys of a dictionary into a single string.
        :param dict: The dictionary
        :return: The concatenated string
        """
        value = ''
        for key, val in dict.items():
            value += val
        return value

    def update_results(self, col_keys, getpages):
        """
        Updates the current tests results for a specific row.
        :param col_keys:
        :param index:
        :param getpages:
        :return:
        """

        key_str = self.concat_dict_keys(col_keys)
        gp_list = self.results.get(key_str)
        prev_gp = 0

        if len(gp_list) > 0:
            for pages in gp_list:
                prev_gp += pages

        gp_list.append(getpages - prev_gp)
        self.results[key_str] = gp_list

    def start_background_process(self, min_gp):
        # Kickoff background activity
        print("Starting RTPJ Background SQL Activity process.")
        b_list = []
        # b = RtpJava.execute_rtpj('PSA_Samp_Background_Activity_Test.JSON',
        #                          ssid=self.connection.get_ssid(),
        #                          userid=self.connection.get_userid(),
        #                          sync=False)
        # b_list.append(b)

        b = RtpJava.execute_rtpj('PSA_Samp_Background_Activity_Tables_Test.JSON',
                                 ssid=self.connection.get_ssid(),
                                 userid=self.connection.get_userid(),
                                 sync=False)
        b_list.append(b)

        b = RtpJava.execute_rtpj('PSA_Samp_Background_Activity_Database_Test.JSON',
                                 ssid=self.connection.get_ssid(),
                                 userid=self.connection.get_userid(),
                                 sync=False)
        b_list.append(b)

        # Execute the desired RTPJ program
        b = RtpJava.execute_rtpj('PSA_Samp_{0}K_GP_B_Test.JSON'.format(int(min_gp/1000)),
                                  ssid=self.connection.get_ssid(),
                                  userid=self.connection.get_userid(), sync=False)

        b_list.append(b)
        time.sleep(5)

        return b_list

    def stop_background_process(self, b_list):
        if b_list is not None:
            for b in b_list:
                b.kill()


