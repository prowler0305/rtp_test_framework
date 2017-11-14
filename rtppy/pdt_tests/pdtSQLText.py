import collections

from ptg2.zos.emul_common import EmulatorException
from core.Factories import Factory
from core.History import History
from core.InputParms import InputParms
from core.Results import Results
from core.common import CommonNav


class SqlText(History):
    """
    Class that encompasses validating SQL Text.
    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        History.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.line_command_string = None
        self.line_command_list = []
        self.view_type = None
        self.plan = None
        self.program = None
        self.collid = None
        self.text_type = 'static'
        self.sql_line_command = 'S'
        self.sql_text_dict = {}
        self.user_supplied_text_dict = None
        self.user_text_supplied = False
        self.user_text_not_matched_dict = {}

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """
        expected_parms = ['plan', 'program']
        optional_parms = ['text_type', 'text list']

        super(SqlText, self).build_test()

        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'plan':
                    if value == 'ALL':
                        self.program = 'ALL'
                        self.default_parms_dict['program'] = self.program
                    self.plan = str(value).upper()
                    self.expected_parms_dict[parm] = self.plan
                elif parm == 'program':
                    self.program = str(value).upper()
                    self.expected_parms_dict[parm] = self.program
                    if self.program != 'ALL':
                        rc, value = self.get_parm_value('collid')
                        if rc:
                            self.collid = str(value).upper()
                            self.expected_parms_dict[parm] = self.collid
                        else:
                            InputParms.no_required_parameter('collid')
                else:
                    continue
            else:
                InputParms.no_required_parameter(parm)

        for opt_parm in optional_parms:
            rc, value = self.get_parm_value(opt_parm)
            if opt_parm == 'text_type':
                if rc:
                    if value.lower() == 'static':
                        self.default_parms_dict[opt_parm] = self.text_type
                    elif value.lower() == 'dynamic':
                        self.text_type = value.lower()
                        self.sql_line_command = 'Q'
                        self.optional_parms_dict[opt_parm] = self.text_type
                    else:
                        InputParms.parameter_value_not_valid('text_type', value.lower(), 'static or dynamic')
                else:
                    self.default_parms_dict[opt_parm] = self.text_type
            elif opt_parm == 'text list':
                if rc:
                    self.user_supplied_text_dict = value
                    self.user_text_supplied = True
                    self.user_text_not_matched_dict = self.user_supplied_text_dict
                    self.optional_parms_dict[opt_parm] = self.user_supplied_text_dict
            else:
                continue

    def execute_test(self):
        """
        Tries and access the SQL Text display for the statements under a given plan and program(s)
        """

        overall_rc = True
        dict_of_statement_result_sets = {}

        self.check_if_output_file_needed('sql_text_compare')

        CommonNav.print_test_start_end('SQL Text', file_name=self.output_directory)

        self.parameter_summary()

        # Temporary code until support is put in for plan: "ALL" for sql text.
        if self.plan == 'ALL':
            no_plan_all_error = "Value of 'ALL' for parameter 'plan' not currently supported. Please specify a planname."
            raise ValueError(no_plan_all_error)
        nav = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                       ssid=self.connection.get_ssid(), userid=self.connection.get_userid(),
                                       current_datastore=self.current_datastore, current_interval_date=self.current_interval_date,
                                       current_interval_time=self.current_interval_time, current_vcat=self.current_vcat,
                                       output_directory=self.output_directory, debug_mode=self.debug_mode)

        nav.start_product(release_environment=self.product_release)

        nav.select_datastore()

        nav.select_interval(v_type=self.view_type, interval_date_2=self.current_interval_date_2,
                            interval_time_2=self.current_interval_time_2)

        if nav.select_row(self.plan):
            if self.program != 'ALL':
                if nav.select_row(self.program, line_command=self.sql_line_command, additional_column_name='COLLID', additional_row_identifier=self.collid):
                    get_sql_text_rc, statements_result_set = self.get_all_statements_sql_text(nav)
                    if not get_sql_text_rc:
                        overall_rc = False
                    else:
                        if self.user_supplied_text_dict is not None:
                            if not self.compare_sql_text(statements_result_set):
                                overall_rc = False
                    if statements_result_set.sql_text_report_header(for_plan=self.plan, for_program=self.program,
                                                                    user_text_supplied=self.user_text_supplied, report_type=self.text_type):
                        statements_result_set.sql_text_report(statement_result_set_check=False)
                else:
                    if self.text_type == 'dynamic' and 'DT518I' not in nav.message_container:
                        overall_rc = False
                    # If we are testing dynamic text indicated by the user and doing a "Q" on the program received an
                    # error message indicating no dynamic SQL text to display then we will do an "S" on the program so
                    # that we can get the SQL Call type, STMT#, and SECT# to still put in the SQL Text report at the end
                    # if self.text_type == 'dynamic':
                    #     nav.select_row(self.program, additional_column_name='COLLID', additional_row_identifier=self.collid)
                    #     statements_result_set = nav.build_display_table(build_display_logging=False)
                    #     # get_sql_text_rc, statements_result_set = self.get_all_statements_sql_text(nav)
                    #     if statements_result_set.sql_text_report_header(for_plan=self.plan, for_program=self.program,
                    #                                                     user_text_supplied=self.user_text_supplied, report_type=self.text_type):
                    #         statements_result_set.sql_text_report(statement_result_set_check=False)
            else:
                prog_result_set = nav.build_display_table(build_display_logging=False)
                prog_col_obj = prog_result_set.columns.get('PROGRAM')
                for row in prog_col_obj.data.keys():
                    program_name = prog_result_set.get_row_data('PROGRAM', row)
                    collid = prog_result_set.get_row_data('COLLID', row)
                    if nav.select_row(program_name, line_command=self.sql_line_command, additional_column_name='COLLID', additional_row_identifier=collid):
                        get_sql_text_rc, statements_result_set = self.get_all_statements_sql_text(nav)
                        dict_of_statement_result_sets[program_name] = statements_result_set
                        if not get_sql_text_rc:
                            overall_rc = False
                        else:
                            # dict_of_statement_result_sets[program_name] = statements_result_set
                            if self.user_supplied_text_dict is not None:
                                if not self.compare_sql_text(statements_result_set):
                                    overall_rc = False
                        CommonNav.nav_screen_back(nav.ptg2_em, out_file=self.output_directory)
                    else:
                        if self.text_type == 'dynamic' and 'DT518I' not in nav.message_container:
                            overall_rc = False
                        # If we are testing dynamic text indicated by the user and doing a "Q" on the program received an
                        # error message indicating no dynamic SQL text to display then we will do an "S" on the program so
                        # that we can get the SQL Call type, STMT#, and SECT# to still put in the SQL Text report at the end
                        # if self.text_type == 'dynamic':
                        #     nav.select_row(program_name, additional_column_name='COLLID', additional_row_identifier=collid)
                        #     statements_result_set = nav.build_display_table(build_display_logging=False)
                        #     dict_of_statement_result_sets[program_name] = statements_result_set
                        #     CommonNav.nav_screen_back(nav.ptg2_em, out_file=self.output_directory)
                for prog, result_set in dict_of_statement_result_sets.items():
                    if result_set.sql_text_report_header(for_plan=self.plan, for_program=prog,
                                                         user_text_supplied=self.user_text_supplied, report_type=self.text_type):
                        result_set.sql_text_report(statement_result_set_check=False)
        else:
            raise EmulatorException(message='Planname %s not found.' % self.plan, screen=nav.ptg2_em.screen)

        if self.user_text_not_matched_dict:
            self.text_not_found_report()

        CommonNav.print_test_start_end('SQL Text', output_type='end',
                                       file_name=self.output_directory)

        nav.stop_emulator()

        if overall_rc:
            return True, self.output_directory
        else:
            return False, self.output_directory

    def get_all_statements_sql_text(self, nav):
        """
        Does a "Q" line command for static SQL statements and retrieves the SQL text for the statement by adding a Text
        column info object to the result sets 'columns' dictionary.

        :return: Tuple(return code, statement display result set)
        """

        statement_result_set = nav.build_display_table(build_display_logging=False)
        statement_info_obj = statement_result_set.columns.get('SQL_CALL')
        sql_text_rc = True
        if self.text_type == 'dynamic':
            statement_field_obj = nav.get_first_field(text_before_input_field='Interval Date =>')
        for row in statement_info_obj.data.keys():
            if self.text_type == 'static':
                sql_call_type = statement_result_set.get_row_data('SQL_CALL', row)
                stmt_num = statement_result_set.get_row_data('STMT#', row)
                select_row_rc = nav.select_row(sql_call_type, line_command='Q',
                                               additional_column_name='STMT#', additional_row_identifier=stmt_num)

                if select_row_rc and nav.ptg2_em.app.ispf_panelid != 'PDTQ0029':
                    sql_text = nav.get_sql_text()
                    statement_result_set.add_column_to_result_set('TEXT', 2097152, 0, 0, 'string')
                    text_col_obj = statement_result_set.columns.get('TEXT')
                    text_col_obj.add_column_value(row - 1, sql_text)
                    CommonNav.nav_screen_back(nav.ptg2_em, out_file=self.output_directory)
                    CommonNav.nav_freeze_unfreeze_column(nav.ptg2_em, 'STMT#', command='unfreeze')
                else:
                    if nav.ptg2_em.app.ispf_panelid == 'PDTQ0029':
                        select_row_rc = False
                        CommonNav.nav_screen_back(nav.ptg2_em, self.output_directory)
                        CommonNav.nav_freeze_unfreeze_column(nav.ptg2_em, 'STMT#', command='unfreeze')
                    else:
                        pass
            else:
                statement_field_obj.fill(self.sql_line_command)
                CommonNav.nav_screen_capture(nav.ptg2_em, file_name=self.output_directory)
                nav.ptg2_em.app.ispf_submit()
                CommonNav.nav_screen_capture(nav.ptg2_em, file_name=self.output_directory)
                if len(nav.ptg2_em.screen.messages) == 0:
                    select_row_rc = True
                    sql_text = nav.get_sql_text()
                    statement_result_set.add_column_to_result_set('TEXT', 2097152, 0, 0, 'string')
                    text_col_obj = statement_result_set.columns.get('TEXT')
                    text_col_obj.add_column_value(row - 1, sql_text)
                    CommonNav.nav_screen_back(nav.ptg2_em, self.output_directory)
                    statement_field_obj = statement_field_obj.next()
                else:
                    statement_field_obj = statement_field_obj.next()
                    select_row_rc = False

            if sql_text_rc:
                if not select_row_rc:
                    sql_text_rc = select_row_rc

        return sql_text_rc, statement_result_set

    def compare_sql_text(self, statement_result_set):
        """
        Compares the SQl Text extracted from the Detector SQL Call Text Display for a statement to the user's supplied list
        of SQL executed for the program specified in the JSON file.

        :param statement_result_set: :py :Class Results representing all the statements from an SQL Display
        :return: True - A match was found in the users specified text list and the text matched exactly.
        """

        overall_compare_rc = True
        user_keys_to_remove = []
        statement_info_obj = statement_result_set.columns.get('SQL_CALL')
        # for row, call_type in statement_info_obj.data.items():
        #     display_text = statement_result_set.get_row_data('TEXT', row)
        #     for key, user_text in self.user_supplied_text_dict.items():
        #         if user_text.strip() == display_text:
        #             compare_rc = True
        #             del self.user_text_not_matched_dict[key]
        #             statement_result_set.add_column_to_result_set('MATCHED USER TEXT', 2097152, 0, 0, 'string')
        #             matched_text_col = statement_result_set.columns.get('MATCHED USER TEXT')
        #             matched_text_col.add_column_value(row - 1, user_text.strip())
        #         else:
        #             compare_rc = False

        for userkey, user_text in self.user_supplied_text_dict.items():
            for row, call_type in statement_info_obj.data.items():
                display_text = statement_result_set.get_row_data('TEXT', row)
                if user_text.strip() == display_text:
                    compare_rc = True
                    # If this key doesn't already exist in the list then add it so we can remove the matching entries
                    # from list of not matched.
                    if userkey not in user_keys_to_remove:
                        user_keys_to_remove.append(userkey)
                    statement_result_set.add_column_to_result_set('MATCHED USER TEXT', 2097152, 0, 0, 'string')
                    matched_text_col = statement_result_set.columns.get('MATCHED USER TEXT')
                    matched_text_col.add_column_value(row - 1, user_text.strip())
                else:
                    compare_rc = False

        # Run through the list of SQL Text the user supplied that we found a match and remove them from the dictionary
        # leaving just the ones we didn't.
        for key in user_keys_to_remove:
            del self.user_text_not_matched_dict[key]

        if overall_compare_rc:
            if not compare_rc:
                overall_compare_rc = compare_rc

        return overall_compare_rc

    def text_not_found_report(self):
        """
        Prints a report showing the pair of key/text from the user provided text_list object in the JSON file that a
        match was not found for.

        :return:
        """
        not_found_report_title = '                     SQL Text Not Found Report'
        Results.display_compare_report_header(None, None, title_override=not_found_report_title, file_name=self.output_directory)
        max_col_len = 8
        max_val_len = 50
        try:
            for k, v in self.user_text_not_matched_dict.items():
                if len(k) > max_col_len:
                    max_col_len = len(k)
                if len(v) > max_val_len:
                    max_val_len = len(v)
        except AttributeError:
            pass
        not_found_report_col = "{} {}"
        not_found_report_col = not_found_report_col.format('USER KEY'.ljust(max_col_len), 'USER TEXT'.ljust(max_val_len))
        not_found_sep = "{} {}"
        not_found_sep = not_found_sep.format('-'.ljust(max_col_len, '-'), '-'.ljust(max_val_len, '-'))
        CommonNav.println(not_found_report_col, self.output_directory)
        CommonNav.println(not_found_sep, self.output_directory)
        for user_key, user_text in self.user_text_not_matched_dict.items():
            not_found_report_line = "{} {}"
            not_found_report_line = not_found_report_line.format(user_key.ljust(max_col_len), user_text.ljust(max_val_len))
            CommonNav.println(not_found_report_line, self.output_directory)
