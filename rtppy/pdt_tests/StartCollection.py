from core.BaseTest import BaseTest
from core.Factories import Factory
from core.InputParms import InputParms
from core.common import CommonNav


class StartStopCollection(BaseTest):
    """
    Document this class
    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        BaseTest.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.collections_options = None
        self.test_type = None

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """
        expected_parms = ['options']
        coll_override_list = ['collection_profile', 'high_level', 'current_datastore', 'itime', 't_limit', 'samp']

        super(StartStopCollection, self).build_test()

        type_found, self.test_type = InputParms.check_json_parm(self.dict_parms, connection_instance=None, parameter_name='test_type')
        if self.test_type == 'start collection':
            for parm in expected_parms:
                rc, value = self.get_parm_value(parm)
                if rc:
                    if parm == 'options':
                        self.collections_options = value
                        self.expected_parms_dict[parm] = value
                        for start_override in coll_override_list:
                            if start_override in self.command_line_overrides:
                                coll_rc, override_value = InputParms.check_override_parm(self.command_line_overrides, start_override)
                                if coll_rc:
                                    self.collections_options[start_override] = override_value
                            else:
                                continue
                    else:
                        continue
                else:
                    InputParms.no_required_parameter(parm)

    def execute_test(self):
        """
        Starts a product collection.

        :return: True - Collection was started successfully
                 False - Collection not started successfully
        """

        self.check_if_output_file_needed('start_collection')
        CommonNav.print_test_start_end('Start/Stop Collection', file_name=self.output_directory)
        self.parameter_summary()

        navigation = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                              ssid=self.connection.get_ssid(), userid=self.connection.get_userid(),
                                              debug_mode=self.debug_mode, output_directory=self.output_directory)

        navigation.start_product(release_environment=self.product_release)

        if self.test_type == 'start collection':
            collection_rc = navigation.start_collection(self.collections_options)
        else:
            if self.product_code == 'PDT':
                collection_rc = navigation.pdt_terminate_collection()
            else:
                collection_rc = navigation.psa_terminate_collection()

        navigation.stop_emulator()

        CommonNav.print_test_start_end('Start/Stop Collection', output_type='end',
                                       file_name=self.output_directory)
        if collection_rc:
            BaseTest.countdown_timer(15)
            return True, self.output_directory
        else:
            return False, self.output_directory
