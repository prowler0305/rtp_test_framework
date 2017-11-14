from core.BaseTest import *
from core.InputParms import InputParms


class History(BaseTest):
    """

    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        BaseTest.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.dict_parms = test_parms_dict
        self.connection = connection_instance
        self.command_line_overrides = input_arg_dict
        self.current_datastore = None
        self.current_interval_date = None
        self.current_interval_time = None
        self.current_interval_date_2 = None
        self.current_interval_time_2 = None
        self.current_vcat = None
        self.specific_column_to_compare = None
        self.common_history_expected_parms_list = ['current_datastore', 'current_interval_date', 'current_interval_time',
                                                   'current_vcat']
        self.common_history_optional_parms_list = ['column', 'current_interval_date_2', 'current_interval_time_2']

    def build_test(self):
        """
        Check and set all expected and optional parameters that are for tests that use the products Historical Displays
        :return:
        """

        super(History, self).build_test()
        self.set_common_expected_parms()
        self.set_common_optional_parms()

    def set_common_expected_parms(self):
        """
        Set the value for a list of common expected parameters that are required for all subclasses of History.
        :return: Nothing
        """

        for parm in self.common_history_expected_parms_list:
            if parm == 'current_interval_time' and self.current_interval_date == '1':
                continue
            else:
                rc, value = self.get_parm_value(parm)
                if rc:
                    if parm == 'current_datastore':
                        self.current_datastore = value.upper()
                        self.expected_parms_dict[parm] = value
                    elif parm == 'current_interval_date':
                        self.current_interval_date = value
                        self.expected_parms_dict[parm] = value
                    elif parm == 'current_interval_time':
                        self.current_interval_time = value
                        self.expected_parms_dict[parm] = value
                    elif parm == 'current_vcat':
                        self.current_vcat = value
                        self.expected_parms_dict[parm] = value
                    else:
                        continue
                else:
                    InputParms.no_required_parameter(parm)

    def set_common_optional_parms(self):
        """
        Set the value for a list of common optional parameters that can be used for a subclass of History.
        :return: Nothing
        """

        for parm in self.common_history_optional_parms_list:
            rc, value = self.get_parm_value(parm)
            if parm == 'column':
                if rc:
                    self.specific_column_to_compare = value
                    self.optional_parms_dict[parm] = value
            elif parm == 'current_interval_date_2':
                if rc:
                    self.current_interval_date_2 = value
                    self.optional_parms_dict[parm] = value
            elif parm == 'current_interval_time_2':
                if rc:
                    self.current_interval_time_2 = value
                    self.optional_parms_dict[parm] = value
            else:
                continue
