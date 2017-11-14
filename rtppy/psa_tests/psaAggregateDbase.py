from core.AggregateBase import AggregateBase
from core.InputParms import InputParms
from core.common import CommonNav


class AggregateDbase(AggregateBase):
    """
    Document this class
    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict, level):
        AggregateBase.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.dbname = None
        self.level = str(level.upper())

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """

        expected_parms = ['dbname']
        super(AggregateDbase, self).build_test()
        self.expected_parms_dict['level'] = self.level

        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'dbname':
                    self.dbname = str(value)
                    self.expected_parms_dict['dbname'] = value
                else:
                    continue
            else:
                InputParms.no_required_parameter(parm)

    def execute_test(self):
        """

        :return:
        """
        navigation_instance = super(AggregateDbase, self).execute_test()
        dbase_result_set = navigation_instance.build_display_table()

        if self.dbname != 'ALL':
            agg_failed = self.aggregate_single_dbase_level(navigation_instance, dbase_result_set)
        else:
            agg_failed = self.aggregate_all_dbase_level(navigation_instance, dbase_result_set)

        CommonNav.print_test_start_end('Aggregate Compare', output_type='end', file_name=self.output_directory)

        navigation_instance.stop_emulator()

        if agg_failed:
            return False, self.output_directory
        else:
            return True, self.output_directory

    def aggregate_single_dbase_level(self, nav_instance, dbase_result_set):
        """
        Selects a single Database and aggregates the DB Table Activity display data and compares it against the Database
        data.
        :param nav_instance: instance
        :param dbase_result_set:
        :return: True - aggregation failed
                 False - aggregation passed.
        """

        if nav_instance.select_row(self.dbname, for_product=self.product_code):
            table_result_set = nav_instance.build_display_table()
            row_found = dbase_result_set.find_key_from_value('DBNAME', self.dbname)
            if row_found is not None:
                agg_failed = self.call_aggregate_compare(self.level, table_result_set, dbase_result_set, row_found,
                                                         self.dbname, specific_column=self.specific_column_to_compare,
                                                         output_file=AggregateBase.output_directory)
                return agg_failed
            else:
                print("DBNAME '%s' not found in higher level result set." % self.dbname)
                agg_failed = True
                return agg_failed
        else:
            error_string = 'Database name ' + self.dbname + ' not found.'
            self.raise_row_not_found_exception(nav_instance, error_string)

    def aggregate_all_dbase_level(self, nav_instance, dbase_result_set):
        """
        Aggregates the DB Table Activity data and compares it against the Database data for ALL the Databases
        in a result set.
        :param nav_instance:
        :param dbase_result_set:
        :return: True - aggregation failed
                 False - aggregation passed.
        """

        overall_agg_failed = False

        col_info_obj = dbase_result_set.columns.get('DBNAME')
        for row in col_info_obj.data.keys():
            dbase_name = dbase_result_set.get_row_data('DBNAME', row)
            if nav_instance.select_row(dbase_name, for_product=self.product_code):
                table_result_set = nav_instance.build_display_table()
                row_found = dbase_result_set.find_key_from_value('DBNAME', dbase_name)
                if row_found is not None:
                    indv_agg_failed = self.call_aggregate_compare(self.level, table_result_set, dbase_result_set, row_found,
                                                                  dbase_name, specific_column=self.specific_column_to_compare,
                                                                  output_file=self.output_directory)
                    # if the aggregate compare failed (i.e. its TRUE that aggregate compare failed) then set
                    # overall failure flag.
                    if indv_agg_failed:
                        overall_agg_failed = indv_agg_failed
                else:
                    print("DBNAME '%s' not found in higher level result set." % dbase_name)
                    overall_agg_failed = True

                CommonNav.nav_screen_back(nav_instance.ptg2_em, out_file=self.output_directory)
            else:
                print("Database name '%s' not found." % dbase_name)
        return overall_agg_failed
