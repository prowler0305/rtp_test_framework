from core.AggregateBase import AggregateBase
from core.InputParms import InputParms
from core.common import CommonNav


class AggregateKeys(AggregateBase):
    """

    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict, level):
        AggregateBase.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.level = str(level.upper())
        self.key_value = None
        self.key_option = 'U'
        self.line_command = 'P'

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """

        expected_parms = ['key_value']
        optional_parms = ['key_option', 'line_command']
        self.expected_parms_dict['level'] = self.level
        super(AggregateKeys, self).build_test()

        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'key_value':
                    self.key_value = str(value)
                    self.expected_parms_dict['key_value'] = value
                else:
                    continue
            else:
                InputParms.no_required_parameter(parm)

        for opt_parm in optional_parms:
            rc, value = self.get_parm_value(opt_parm)
            if opt_parm == 'key_option':
                if rc:
                    self.key_option = value
                    self.optional_parms_dict['key_option'] = value
                else:
                    InputParms.no_optional_parameter(opt_parm, self.key_option)
                    self.optional_parms_dict['key_option'] = self.key_option
            elif opt_parm == 'line_command':
                if rc:
                    self.line_command = value
                    self.optional_parms_dict['line_command'] = value
                else:
                    InputParms.no_optional_parameter(opt_parm, self.line_command)
                    self.optional_parms_dict['line_command'] = self.line_command

    def execute_test(self):
        """

        :return:
        """
        agg_failed = True
        navigation_instance = super(AggregateKeys, self).execute_test()
        navigation_instance.view_by('k')
        if navigation_instance.view_key(self.key_option):
            key_result_set = navigation_instance.build_display_table()
            if self.key_value != 'ALL':
                agg_failed = self.aggregate_single_key_level(navigation_instance, key_result_set)
            else:
                agg_failed = self.aggregate_all_keys_level(navigation_instance, key_result_set)
        else:
            CommonNav.println("%s. Most likely due to the key related to option %s was set to 'N' in the collection profile used."
                              % (navigation_instance.ptg2_em.screen.messages["DT665E"].value, self.key_option), self.output_directory)

        CommonNav.print_test_start_end('Aggregate Compare', output_type='end', file_name=self.output_directory)

        navigation_instance.stop_emulator()

        if agg_failed:
            return False, self.output_directory
        else:
            return True, self.output_directory

    def aggregate_single_key_level(self, nav_instance, key_result_set):
        """

        :param nav_instance:
        :param key_result_set:
        :return:
        """

        if nav_instance.select_row(self.key_value, line_command=self.line_command):
            lower_result_set = nav_instance.build_display_table(build_primary_key_dict='N')
            row_found = key_result_set.find_key_from_value('KEY', self.key_value)
            if row_found is not None:
                agg_failed = self.call_aggregate_compare(self.level, lower_result_set, key_result_set, row_found,
                                                         self.key_value, specific_column=self.specific_column_to_compare,
                                                         line_command=self.line_command, output_file=self.output_directory)
                return agg_failed
            else:
                CommonNav.println("Key '%s' not found in higher level result set." % self.key_value, file_path=self.output_directory)
                agg_failed = True
                return agg_failed
        else:
            # TODO: Temporary code for line command P on key display for connect type with key *NULL*
            if self.line_command == 'P' and self.key_value == '*NULL*':
                raise Exception("Navigation for line command '%s' for key '%s' not possible." %
                                (self.line_command, self.key_value))

            else:
                raise Exception("Key '%s' either not found or not selectable with line_command '%s'." %
                                (self.key_value, self.line_command))

    def aggregate_all_keys_level(self, nav_instance, key_result_set):
        """

        :param nav_instance:
        :param key_result_set:
        :return:
        """

        overall_agg_failed = False

        key_info_obj = key_result_set.columns.get('KEY')
        for row in key_info_obj.data.keys():
            key_value = key_result_set.get_row_data('KEY', row)
            if nav_instance.select_row(key_value, line_command=self.line_command):
                lower_result_set = nav_instance.build_display_table(build_primary_key_dict='N')
                row_found = key_result_set.find_key_from_value('KEY', key_value)
                if row_found is not None:
                    indv_agg_failed = self.call_aggregate_compare(self.level, lower_result_set, key_result_set,
                                                                  row_found, key_value, specific_column=self.specific_column_to_compare,
                                                                  line_command=self.line_command, output_file=self.output_directory)
                    if indv_agg_failed:
                        overall_agg_failed = indv_agg_failed
                else:
                    CommonNav.println("Key '%s' not found in higher level result set." % key_value, file_path=self.output_directory)
                    overall_agg_failed = True

                CommonNav.nav_screen_back(nav_instance.ptg2_em, out_file=self.output_directory)
            else:
                # TODO: Temporary code for line command P on key display for connect type with key *NULL*
                if key_value == '*NULL*' and self.line_command == 'P':
                    CommonNav.println("Navigation for line command '%s' for key '%s' not possible." % (self.line_command, key_value), file_path=self.output_directory)
                else:
                    CommonNav.println("Key '%s' either not found or not selectable with line_command '%s'." % (key_value, self.line_command), file_path=self.output_directory)
        return overall_agg_failed
