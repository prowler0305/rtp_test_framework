from core.InputParms import InputParms
from core.BaseTest import BaseTest
from core.Rtp_Java import RtpJava
from core.common import CommonNav


class RTPJExec(BaseTest):
    """
    Test type class that can be used to execute distributed SQL via RTPJ framework.
    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        BaseTest.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.rtpj_file = None
        self.rtpj_library = None
        self.rtpj_sync = True
        self.rtpj_log_level = 'DEFAULT'

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """

        expected_parms = ['rtpj_file']
        optional_parms = ['rtpj_library', 'rtpj_sync', 'rtpj_log_level']

        super(RTPJExec, self).build_test()

        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'rtpj_file':
                    self.rtpj_file = value
                    self.expected_parms_dict[parm] = value
                else:
                    continue
            else:
                InputParms.no_required_parameter(parm)

        for opt_parm in optional_parms:
            rc, value = self.get_parm_value(opt_parm)
            if opt_parm == 'rtpj_library':
                if rc:
                    self.rtpj_library = value
                    self.optional_parms_dict[opt_parm] = self.rtpj_library
            elif opt_parm == 'rtpj_sync':
                if rc and value.lower() != 'true':
                    if value.lower() != 'false':
                        InputParms.parameter_value_not_valid(opt_parm, value, "True or False")
                    else:
                        self.rtpj_sync = False
                        self.optional_parms_dict[opt_parm] = self.rtpj_sync
                else:
                    self.default_parms_dict[opt_parm] = self.rtpj_sync
            elif opt_parm == 'rtpj_log_level':
                if rc and value.upper() != 'DEFAULT':
                    self.rtpj_log_level = value.upper()
                    self.optional_parms_dict[opt_parm] = self.rtpj_log_level
                else:
                    self.default_parms_dict[opt_parm] = self.rtpj_log_level
            else:
                continue

    def execute_test(self):
        """
        Allows execution of distributed SQL with RTPPY via integration with RTPJ.
        :return: True(success) or False(Failure)
        """

        rtpj_exec_rc = False
        self.check_if_output_file_needed('rtpj_activity')
        CommonNav.print_test_start_end('Distributed SQL Activity', file_name=self.output_directory)
        self.parameter_summary()

        if self.rtpj_log_level == 'DEFAULT':
            if self.rtpj_sync:
                if RtpJava.execute_rtpj(self.rtpj_file, ssid=self.connection.get_ssid(), userid=self.connection.get_userid(),
                                        library=self.rtpj_library, sync=self.rtpj_sync) == 0:
                    rtpj_exec_rc = True
            else:
                if RtpJava.execute_rtpj(self.rtpj_file, ssid=self.connection.get_ssid(), userid=self.connection.get_userid(),
                                        log='ERROR', library=self.rtpj_library, sync=self.rtpj_sync) is not None:
                    rtpj_exec_rc = True
        else:
            call_rc = RtpJava.execute_rtpj(self.rtpj_file, ssid=self.connection.get_ssid(), userid=self.connection.get_userid(),
                                           log=self.rtpj_log_level, library=self.rtpj_library, sync=self.rtpj_sync)
            if call_rc == 0 or call_rc is not None:
                rtpj_exec_rc = True

        CommonNav.print_test_start_end('Distributed SQL Activity', output_type='end', file_name=self.output_directory)

        if rtpj_exec_rc:
            return True, self.output_directory
        else:
            return False, self.output_directory
