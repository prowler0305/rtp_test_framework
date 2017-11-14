from core.Factories import Factory
from core.History import History
from core.InputParms import InputParms
from core.common import CommonNav


class IntervalCompare(History):
    """
    Document this class
    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        History.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.baseline_datastore = None
        self.baseline_vcat = None
        self.baseline_interval_date = None
        self.baseline_interval_time = None
        self.baseline_interval_date_2 = None
        self.baseline_interval_time_2 = None
        self.product_code = None
        self.view_by = None
        self.view_type = None
        self.key_option = None
        self.view_option = None
        self.range_pct = 10
        self.result_sets_row_mapping = {}

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """
        expected_parms = ['baseline_datastore', 'baseline_vcat', 'baseline_interval_date', 'baseline_interval_time',
                          'view_by']
        optional_parms = ['range_pct', 'view_type', 'key_option', 'baseline_interval_date_2', 'baseline_interval_time_2'
                          , 'view_option']

        super(IntervalCompare, self).build_test()

        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'baseline_datastore':
                    self.baseline_datastore = value
                    self.expected_parms_dict[parm] = value
                elif parm == 'baseline_vcat':
                    self.baseline_vcat = value
                    self.expected_parms_dict[parm] = value
                elif parm == 'baseline_interval_date':
                    self.baseline_interval_date = value
                    self.expected_parms_dict[parm] = value
                elif parm == 'baseline_interval_time':
                    self.baseline_interval_time = value
                    self.expected_parms_dict[parm] = value
                elif parm == 'view_by':
                    self.view_by = value.upper()
                    self.expected_parms_dict[parm] = value
                else:
                    continue
            else:
                InputParms.no_required_parameter(parm)

        for opt_parm in optional_parms:
            rc, value = self.get_parm_value(opt_parm)
            if opt_parm == 'range_pct':
                if rc:
                    self.range_pct = int(value)
                    self.optional_parms_dict[opt_parm] = self.range_pct
                else:
                    self.default_parms_dict[opt_parm] = self.range_pct
            elif opt_parm == 'view_type':
                if rc:
                    self.view_type = value
                    self.optional_parms_dict[opt_parm] = value
                else:
                    if self.product_code == 'PDT':
                        self.view_type = 'A'
                    else:
                        self.view_type = 'O'
                    self.default_parms_dict[opt_parm] = self.view_type
            elif opt_parm == 'key_option':
                if rc:
                    self.key_option = value
                    self.optional_parms_dict[opt_parm] = value
                else:
                    self.default_parms_dict[opt_parm] = self.key_option
            elif opt_parm == 'baseline_interval_date_2':
                if rc:
                    self.baseline_interval_date_2 = value
                    self.optional_parms_dict[opt_parm] = value
            elif opt_parm == 'baseline_interval_time_2':
                if rc:
                    self.baseline_interval_time_2 = value
                    self.optional_parms_dict[opt_parm] = value
            elif opt_parm == 'view_option' and self.product_code == 'PSA' and self.view_by == 'T':
                if rc:
                    self.view_option = value
                    self.optional_parms_dict[opt_parm] = value
            else:
                continue

    def execute_test(self):
        """
        Uses the RTP product class and methods to create two results sets from the Interval Statement Summary Displays.
        Then compares all the data between the two results sets and produces a Comparison Report and up to two Rows Not
        Found reports.
        :return: 0(zero) - All the metric data between the two results sets compared either matches or fits between the
                           indicated range percentage.
                -1 - Either the data comparison failed and produced a report or a Rows not Found report was produced
        """
        """
        Step 1
        ------------
        How to get to the Statement Summary Display for an interval by:

            1) Creating an instance of the NavPDT class using the following parameters:
                a) the LPAR that will be used.
                b) the userid that will be used to log in.
                c) sets the DB2 ssid that will be used for that instance
                c) sets the default current datastore to be used.
                d) default current interval date and time to be used.
            2) Call the function that goes to the Detector Main panel for the release environment requested or use the
               default release if there isn't one specified.
            3) Request to go to the SSID historical interval data panels (option 2) and select either the datastore
               that was set when creating the NavPdt class instance or a different datastore by overriding the
               method parameter. Which gives the "Interval Summary Display" for that datastore.
            4) Select the interval in that datastore that was set when creating the NavPdt class instance or
               override it using the overriding parameters.
            5) Change the View By to navigate to.
            6) Create an entire result set of data for every column and every row for the "view by" Summary display
               requested.
        """

        self.check_if_output_file_needed('interval_compare')
        
        CommonNav.print_test_start_end('Interval Compare', file_name=self.output_directory)

        self.parameter_summary()
        nav_current = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                               ssid=self.connection.get_ssid(), userid=self.connection.get_userid(),
                                               current_datastore=self.current_datastore,
                                               current_interval_date=self.current_interval_date,
                                               current_interval_time=self.current_interval_time,
                                               current_vcat=self.current_vcat, output_directory=self.output_directory,
                                               debug_mode=self.debug_mode)

        nav_current.start_product(release_environment=self.product_release)

        nav_current.select_datastore()

        nav_current.select_interval(v_type=self.view_type, interval_date_2=self.current_interval_date_2,
                                    interval_time_2=self.current_interval_time_2)

        nav_current.view_by(self.view_by)

        if self.key_option is not None:
            nav_current.view_key(self.key_option)
        if self.view_option is not None:
            nav_current.psa_view_option(self.view_option)
        current_sum_result = nav_current.build_display_table()

        """
        Step 2
        ----------
        Same as Example 1 above but -
            1) Creates a new NavPdt instance that uses the same emulator but the baseline datastore
            2) Uses baseline current interval date/time parameters to create a different result set of that intervals
               data for the interval.
        """
        if self.connection.get_ssid2() is None:
            nav_base = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                                ssid=self.connection.get_ssid(), userid=self.connection.get_userid(),
                                                current_datastore=self.baseline_datastore,
                                                current_interval_date=self.baseline_interval_date,
                                                current_interval_time=self.baseline_interval_time,
                                                current_vcat=self.baseline_vcat, output_directory=self.output_directory,
                                                debug_mode=self.debug_mode)
        else:
            nav_base = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                                ssid=self.connection.get_ssid2(), userid=self.connection.get_userid(),
                                                current_datastore=self.baseline_datastore,
                                                current_interval_date=self.baseline_interval_date,
                                                current_interval_time=self.baseline_interval_time,
                                                current_vcat=self.baseline_vcat, output_directory=self.output_directory,
                                                debug_mode=self.debug_mode)

        # if self.product_release is not None:
        #     nav_base.product_main(change_ssid=True)
        # else:
        #     nav_base.product_main(change_ssid=True)
        nav_base.product_main()

        nav_base.select_datastore()

        nav_base.select_interval(v_type=self.view_type, interval_date_2=self.baseline_interval_date_2,
                                 interval_time_2=self.baseline_interval_time_2)

        nav_base.view_by(self.view_by)
        if self.key_option is not None:
            nav_base.view_key(self.key_option)
        if self.view_option is not None:
            nav_current.psa_view_option(self.view_option)
        baseline_sum_result = nav_base.build_display_table()

        """
        Step 3
        ----------
        Compare all the data between the two different result sets.

        3 separate reports with be generated if necessary:
            1) A report that identifies by column name and row for those that fail the comparison.
            2) Two separate reports that show the rows that were not found, by row number, for the:
                a) Current Datastore
                b) Baseline Datastore
        """
        compare_tuple = current_sum_result.compare_results(baseline_sum_result, self.range_pct,
                                                           file_name=self.output_directory,
                                                           specific_column_name=self.specific_column_to_compare)
        # Save the matching rows dictionary to class variable
        self.result_sets_row_mapping = compare_tuple[1]
        if len(compare_tuple[2]) > 0:
            current_sum_result.rows_not_found_report(compare_tuple[2], nav_current.datastore_name,
                                                     nav_current.interval_date, nav_current.interval_time,
                                                     file_name=self.output_directory)
        if len(compare_tuple[3]) > 0:
            baseline_sum_result.rows_not_found_report(compare_tuple[3], nav_base.datastore_name,
                                                      nav_base.interval_date, nav_base.interval_time,
                                                      file_name=self.output_directory)

        CommonNav.print_test_start_end('Interval Compare', output_type='end',
                                       file_name=self.output_directory)

        # Check comparison status and return Interval Compare return code.
        if compare_tuple[0]:
            return True, self.output_directory
        else:
            return False, self.output_directory

            # Rough cut of collection initialization logic
            # startup_list = ['01', '05', 'N', 'N', '02', '10', 'N', 'MY.HLQ', 'TESTDS', 'N']
            # navigate_pdt.ptg2_em.app.ispf_command('5', expect_panelid='PDTC0001')
            # collection_display_field = navigate_pdt.get_first_field(text_before_input_field='Interval Time')
            # startup_list_index = 0
            # while True:
            #     collection_display_field.fill(startup_list[startup_list_index])
            #     collection_display_field = collection_display_field.next()
            #     startup_list_index += 1
            #     if collection_display_field is None:
            #         break
            #
            # CommonNav.nav_screen_capture(navigate_pdt.ptg2_em)

            # if navigate_pdt.pdt_terminate_collection():
            #     print("we stopped the collection")
            #     return
            # else:
            #     return -1
            # Below are other examples of the methods available in the column info and Result framework classes.
            # """
            # Example 3
            # ----------
            # For every column in the current_statement_sum result set write its information to a file
            # """
            # for column, col_obj in current_sum_result.columns.items():
            #     if current_sum_result.columns.keys().index(column) == 0:
            #         col_obj.display_col_info(display_type='write', file_name='myfile')
            #     else:
            #         col_obj.display_col_info(display_type='write', file_name='myfile', print_mode='a')

            # """
            # Example 4
            # ----------
            # Write out all of the data for both intervals Statement Summary displays to a file
            # """
            # myfile = open('myfile', 'a')
            # myfile.write('\nDisplaying all Statement summary data for Datastore %s: Interval Date %s: Interval Time %s\n' %
            #              (navigate_pdt.datastore_name, navigate_pdt.interval_date, navigate_pdt.interval_time))
            # myfile.close()
            # current_statement_sum.display_all_rows(display_type='write', file_name='myfile', print_mode='a')
            #
            # myfile = open('myfile', 'a')
            # myfile.write('\nDisplay all Statement summary data for Datastore %s: Interval Date %s: Interval Time %s:\n' %
            #              (nav_pdt2.datastore_name, nav_pdt2.interval_date, navigate_pdt.interval_time))
            # myfile.close()
            # baseline_statement_sum.display_all_rows(display_type='write', file_name='myfile', print_mode='a')

            # """
            # Example 6
            # ----------
            # Getting a specific row of data for the SQL column out of the "current datastore"
            # """
            # print('Data in SQL column Row number 2 is %s' % current_statement_sum.get_row_data('SQL', 2))
            #
            # """
            # Example 7
            # Show drill down ability to specific plan, program, and other line command options. Finally error if invalid line
            # command option given.
            # """
            # CommonNav.nav_screen_capture(navigate_pdt.ptg2_em)
            # CommonNav.nav_screen_back(navigate_pdt.ptg2_em)
            # navigate_pdt.pdt_interval()
            # navigate_pdt.pdt_select_planname('PSAAD190')
            # if navigate_pdt.pdt_select_program('SA$CDB', line_command='S'):
            #     CommonNav.nav_screen_back(navigate_pdt.ptg2_em)
            #
            # if navigate_pdt.pdt_select_program('SA$CDB', line_command='Q'):
            #     CommonNav.nav_screen_back(navigate_pdt.ptg2_em)
            #
            # if navigate_pdt.pdt_select_program('SA$CDB', line_command='D'):
            #     while True:
            #         if not CommonNav.nav_page_down(navigate_pdt.ptg2_em):
            #             break


