from core.Factories import Factory
from core.History import History
from core.common import CommonNav


class AggregateBase(History):
    """
    The parent class that is inherited by aggregate_compare test types of which provides common functionality needed by
    all child aggregate compare test scripts.
    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        History.__init__(self, test_parms_dict, connection_instance, input_arg_dict)

    def build_test(self):
        """
        Parent method called by all child aggregate compare tests to ensures and set all class variables that are common
        to all aggregate compare test that are required are supplied from either the command line override or from the
        test parameters dictionary from the JSON input file. This ensures that all the minimum input parameters needed
        for the execute routines are provided.

        This method should be called via super() after inheriting this class.
        Example:

        super(aggregate_compare_class_name, self).build_test()

        :return: Nothing
        """

        super(AggregateBase, self).build_test()
        self.set_common_expected_parms()
        self.set_common_optional_parms()

    def execute_test(self):
        """
        Can be called via super() by aggregate compare children to execute the common functionality needed by all
        aggregate compare tests which includes:

        1. Checking of the output file is needed and creating if so
        2. printing the summary of parameters in use
        3. creating the correct product navigation class needed
        4. entering the appropriate product
        5. selecting the datastore needed
        6. selecting the needed interval(s)

        :return: product navigation class instance created to be used further by the childs execute_test method
        """
        self.check_if_output_file_needed('aggregate_compare')
        CommonNav.print_test_start_end('Aggregate Compare', file_name=self.output_directory)
        self.parameter_summary()
        aggregate_nav = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                                 ssid=self.connection.get_ssid(),
                                                 userid=self.connection.get_userid(),
                                                 current_interval_date=self.current_interval_date,
                                                 current_datastore=self.current_datastore,
                                                 current_interval_time=self.current_interval_time,
                                                 current_vcat=self.current_vcat,
                                                 output_directory=self.output_directory,
                                                 debug_mode=self.debug_mode)

        aggregate_nav.start_product(release_environment=self.product_release)

        aggregate_nav.select_datastore()

        aggregate_nav.select_interval(interval_date_2=self.current_interval_date_2, interval_time_2=self.current_interval_time_2)
        return aggregate_nav

    @staticmethod
    def call_aggregate_compare(level, lower_result_set, higher_result_set, high_level_identified_row,
                               high_level_identifier, specific_column=None, line_command=None, output_file=None, prog_type_unkn=False):
        """
        Calls the :py:Results.py:aggregate_compare method.

        :param prog_type_unkn:
        :param line_command:
        :param level:
        :param lower_result_set:
        :param higher_result_set:
        :param high_level_identified_row:
        :param high_level_identifier:
        :param specific_column:
        :param output_file:
        :return: Return code from py:Results:aggregate_compare method.
        """
        return(lower_result_set.aggregate_compare(level, higher_result_set, high_level_identified_row,
                                                  high_level_identifier, specific_column_name=specific_column,
                                                  l_command=line_command, file_name=output_file, ptype_unkn=prog_type_unkn))
