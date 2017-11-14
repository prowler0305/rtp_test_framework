import datetime

from core.AggregateBase import AggregateBase
from core.InputParms import InputParms
from core.common import CommonNav
from ptg2.zos.emul_common import EmulatorException


class AggregateProgram(AggregateBase):
    """

    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict, level):
        AggregateBase.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.plan = None
        self.program = None
        self.collid = None
        self.level = str(level.upper())

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """

        expected_parms = ['plan', 'program']
        self.expected_parms_dict['level'] = self.level
        super(AggregateProgram, self).build_test()

        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'plan':
                    self.plan = str(value)
                    self.expected_parms_dict['plan'] = value
                elif parm == 'program':
                    self.program = str(value)
                    self.expected_parms_dict['program'] = value
                    if self.program != 'ALL' and self.plan != 'ALL':
                        rc, value = self.get_parm_value('collid')
                        if rc:
                            self.collid = str(value)
                            self.expected_parms_dict['collid'] = value
                        else:
                            InputParms.no_required_parameter('collid')
                else:
                    continue
            else:
                InputParms.no_required_parameter(parm)

    def execute_test(self):
        """

        :return:
        """

        if self.plan == 'ALL' and self.program != 'ALL':
            raise ValueError("Only value of 'ALL' allowed for 'program' parameter with 'plan' value of '%s' for '%s'"
                             " level compare." % (self.plan, self.level))

        navigation_instance = super(AggregateProgram, self).execute_test()
        if self.plan != 'ALL':
            if navigation_instance.select_row(self.plan):
                program_result_set = navigation_instance.build_display_table()
                if self.program != 'ALL':
                    agg_failed = self.aggregate_single_program_level(navigation_instance, program_result_set)
                else:
                    agg_failed = self.aggregate_all_program_level(navigation_instance, program_result_set)
            else:
                error_string = 'Plan ' + self.plan + ' not found.'
                raise EmulatorException(message=error_string, screen=navigation_instance.ptg2_em.screen)
        else:
            plan_result_set = navigation_instance.build_display_table()
            col_info_obj = plan_result_set.columns.get('PLANNAME')
            for row in col_info_obj.data.keys():
                plan_name = plan_result_set.get_row_data('PLANNAME', row)
                if navigation_instance.select_row(plan_name):
                    program_result_set = navigation_instance.build_display_table()
                    agg_failed = self.aggregate_all_program_level(navigation_instance, program_result_set)

                else:
                    CommonNav.println("Plan '%s' not found." % plan_name, file_path=self.output_directory, color_state='warning')
                    agg_failed = True
                CommonNav.nav_screen_back(navigation_instance.ptg2_em, out_file=self.output_directory)

        CommonNav.print_test_start_end('Aggregate Compare', output_type='end', file_name=self.output_directory)

        navigation_instance.stop_emulator()

        if agg_failed:
            return False, self.output_directory
        else:
            return True, self.output_directory

    def aggregate_single_program_level(self, nav_instance, program_result_set):
        """
        Selects a single program and aggregates the statement display data and compares it against the program data.
        :param nav_instance:
        :param program_result_set:
        :return: True - aggregation failed
                 False - aggregation passed.
        """
        program_type_unkn = False
        program_type_unknown_message = "WARNING!!! Program '%s' program type is 'UNKN'" % self.program
        not_found_error_message = "Program '%s' by COLLID '%s' not found." % (self.program, self.collid)
        # inital try to select the program to get to the statements
        row_sel_rc = nav_instance.select_row(self.program, additional_column_name='COLLID', additional_row_identifier=self.collid)
        # if first select_row comes back false check if its due to the collid is blank due to program type UNKN. If it is then recall select_row setting collid
        # to 'UNKN' so we can continue. If it isn't due to program type UNKN then we have a different problem.
        if not row_sel_rc:
            program_row_number = program_result_set.find_key_from_value('PROGRAM', self.program, secondary_column_name='COLLID', secondary_value='')
            if program_result_set.get_row_data('TYPE', program_row_number) == 'UNKN':
                row_sel_rc = nav_instance.select_row(self.program, additional_column_name='COLLID', additional_row_identifier='UNKN')
                if row_sel_rc:
                    program_type_unkn = True

        if row_sel_rc:
            statement_sum_result_set = nav_instance.build_display_table()
            if not program_type_unkn:
                row_found = program_result_set.find_key_from_value('PROGRAM', self.program, secondary_column_name='COLLID',
                                                                   secondary_value=self.collid)
            else:
                row_found = program_result_set.find_key_from_value('PROGRAM', self.program, secondary_column_name='COLLID',
                                                                   secondary_value='')
            if row_found is not None:
                agg_failed = self.call_aggregate_compare(self.level, statement_sum_result_set, program_result_set,
                                                         row_found, self.program,
                                                         specific_column=self.specific_column_to_compare,
                                                         output_file=self.output_directory, prog_type_unkn=program_type_unkn)
                if program_type_unkn:
                    agg_failed = True
                return agg_failed
            else:
                CommonNav.println("Program '%s' by COLLID '%s' not found in higher level result set." % (self.program, self.collid), file_path=self.output_directory, color_state='warning')
                agg_failed = True
                return agg_failed
        else:
            raise EmulatorException(screen=nav_instance.ptg2_em.screen, message=not_found_error_message)

    def aggregate_all_program_level(self, nav_instance, program_result_set):
        """
        Aggregates the statement data and compares it against the program data for ALL the program in a result set.
        :param nav_instance:
        :param program_result_set:
        :return: True - aggregation failed
                 False - aggregation passed.
        """

        overall_agg_failed = False
        prog_info_obj = program_result_set.columns.get('PROGRAM')
        for row in prog_info_obj.data.keys():
            program_type_unkn = False
            program_name = program_result_set.get_row_data('PROGRAM', row)
            collid = program_result_set.get_row_data('COLLID', row)
            # inital try to select the program to get to the statements
            row_sel_rc = nav_instance.select_row(program_name, additional_column_name='COLLID', additional_row_identifier=collid)
            # if first select_row comes back false check if its due to the collid is blank due to program type UNKN. If it is then recall select_row setting collid
            # to 'UNKN' so we can continue. If it isn't due to program type UNKN then we have a different problem.
            if not row_sel_rc:
                program_row_number = program_result_set.find_key_from_value('PROGRAM', program_name, secondary_column_name='COLLID', secondary_value='')
                if program_result_set.get_row_data('TYPE', program_row_number) == 'UNKN':
                    row_sel_rc = nav_instance.select_row(program_name, additional_column_name='COLLID', additional_row_identifier='UNKN')
                    if row_sel_rc:
                        program_type_unkn = True
            if row_sel_rc:
                statement_sum_result_set = nav_instance.build_display_table()
                row_found = program_result_set.find_key_from_value('PROGRAM', program_name, secondary_column_name='COLLID', secondary_value=collid)
                if row_found is not None:
                    indv_agg_failed = self.call_aggregate_compare(self.level, statement_sum_result_set,
                                                                  program_result_set, row_found, program_name,
                                                                  specific_column=self.specific_column_to_compare,
                                                                  output_file=self.output_directory, prog_type_unkn=program_type_unkn)
                    if program_type_unkn:
                        indv_agg_failed = True
                    if indv_agg_failed:
                        overall_agg_failed = indv_agg_failed
                else:
                    CommonNav.println("Program '%s' by COLLID '%s' not found in higher level result set." % (program_name, collid), file_path=self.output_directory)
                    # print("Program '%s' by COLLID '%s' not found in higher level result set." % (program_name, collid))
                    overall_agg_failed = True

                CommonNav.nav_screen_back(nav_instance.ptg2_em, out_file=self.output_directory, log_screen=False)
            else:
                CommonNav.println("Program '%s' by COLLID '%s' not found." % (program_name, collid), file_path=self.output_directory, color_state='warning')
                # print("Program '%s' by COLLID '%s' not found." % (program_name, collid))
        return overall_agg_failed
