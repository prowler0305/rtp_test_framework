from core.BaseTest import BaseTest
from core.Factories import Factory
from core.Rtp_Java import RtpJava
from core.common import CommonNav
# from pdt_tests.StartCollection import StartStopCollection
# from rtpj_tests.RTPJExec import RTPJExec


class PdtExceptions(BaseTest):
    """
    Test type class that can be used to start a collection and access PDT Exception displays.
    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        BaseTest.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.start_collection_instance = None
        self.rtpj_exec_instance = None

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """

        # Set the test_type json parameter to be 'start collection' in order to create a start collection instance
        # so the calling of the build and execute methods will work correctly
        super(PdtExceptions, self).build_test()
        # self.dict_parms['test_type'] = 'start collection'
        # self.start_collection_instance = StartCollection(self.dict_parms, self.connection, self.command_line_overrides)
        # self.start_collection_instance.build_test()
        # self.rtpj_exec_instance = RTPJExec(self.dict_parms, self.connection, self.command_line_overrides)
        # self.rtpj_exec_instance.build_test()

    def execute_test(self):
        """
        Starts a PDT collection then submits SQL via integration with RTPJ executing file Select_Count_Test.JSON and
        then waits for the SQL to finish. Then access the Current Interval Exception display looking for exceptions data
        to be displayed to indicate success or failure. The success or failure depends on the collection profile that
        was used when starting the collection.

        :return: True(success) or False(Failure)
        """

        exceptions_rc = False
        self.check_if_output_file_needed('pdt_exceptions')
        CommonNav.print_test_start_end('Exceptions', file_name=self.output_directory)
        self.parameter_summary()

        # self.start_collection_instance.execute_test()

        nav_instance = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                                ssid=self.connection.get_ssid(),
                                                userid=self.connection.get_userid(),
                                                debug_mode=self.debug_mode, output_directory=self.output_directory)

        nav_instance.start_product(release_environment=self.product_release)

        if RtpJava.execute_rtpj('Select_Count_Test.JSON', ssid=self.connection.get_ssid(),
                                userid=self.connection.get_userid(), library="C:\\Users\\spean03\\Desktop\\JSON\\PDT1497") == 0:
            nav_instance.main_menu_option('1', panelid='PDTO0002')
            CommonNav.nav_screen_capture(nav_instance.ptg2_em, file_name=self.output_directory)
            BaseTest.countdown_timer(10)
            try:
                nav_instance.pdt_view_type('X', current_interval=True)
                exception_display_results = nav_instance.build_display_table()
                # TODO: Should enhance this to make the row_num parameter dynamic so user can specify.
                number_of_sql_exceptions = exception_display_results.get_row_data(self.specific_column_to_compare, 1)
                if number_of_sql_exceptions > 1:
                    exceptions_rc = True
                else:
                    exceptions_rc = False

            except Exception as view_exception:
                CommonNav.nav_screen_capture(nav_instance.ptg2_em, file_name=self.output_directory)
                CommonNav.printlns(view_exception, file_path=self.output_directory)

        CommonNav.print_test_start_end('Exceptions', output_type='end', file_name=self.output_directory)

        if exceptions_rc:
            return True, self.output_directory
        else:
            return False, self.output_directory
