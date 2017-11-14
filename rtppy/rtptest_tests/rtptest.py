from ptg2.context import set_system
from ptg2.zos.jes import Job

from core.BaseTest import BaseTest
from core.Factories import Factory
from core.InputParms import InputParms
from core.JobTracking import JobTracking
from core.common import CommonNav


class Rtptest(BaseTest):
    """

    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        BaseTest.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.execute_method = None
        self.auto_submit = 'Y'
        self.action = None
        self.dataset_name = None
        self.multithreading = None
        self.multiple_plan_packages = None
        self.program_name = None
        self.collid = None
        self.include_plan = None
        self.connection_type = None
        self.rtptest_options = None
        self.plan = None
        self.corrid = None
        self.sqlid = None
        self.repeat = None
        self.workstation = None
        self.seed = None
        self.execution_options_dict = {}
        self.rtp_manual_hyperlink_text = 'https://cawiki.ca.com/display/DB2QA/Real+Time+Performance+Testing+Tools'
        self.jobinfo = []
        self.jobid = None
        self.jobname = None
        self.wait_to_complete = True

    def build_test(self):
        """
        Build tests identified in the JSON as - "test_type": "rtptest".
        :return:
        """

        expected_parms = ['execute_method']
        optional_parms = ['auto_submit', 'multithreading', 'multiple_plan_packages', 'include_plan', 'options',
                          'wait_to_complete']

        super(Rtptest, self).build_test()

        """
        Process all the expected parms.
        """
        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'execute_method':
                    self.execute_method = value
                    self.expected_parms_dict[parm] = value
                    if self.execute_method == 'UI':
                        rc, value = self.get_parm_value('action')
                        if rc:
                            self.action = value
                            self.expected_parms_dict['action'] = value
                        else:
                            InputParms.no_required_parameter('action')
                    elif self.execute_method == 'dataset':
                        rc, value = self.get_parm_value('dataset_name')
                        if rc:
                            self.dataset_name = value
                            self.expected_parms_dict['dataset_name'] = value
                        else:
                            InputParms.no_required_parameter('dataset_name')
                    else:
                        InputParms.parameter_value_not_valid('execute_method', self.execute_method, 'UI or dataset')
                else:
                    continue
            else:
                InputParms.no_required_parameter(parm)

        """
        Process all the optional parameters listed in the optional_parms variable
        """
        for opt_parm in optional_parms:
            rc, value = self.get_parm_value(opt_parm)
            if rc:
                if opt_parm == 'auto_submit':
                    if value != 'Y':
                        self.auto_submit = value
                    self.optional_parms_dict[opt_parm] = self.auto_submit
                elif opt_parm == 'multithreading' or opt_parm == 'multiple_plan_packages':
                    if value.upper() != 'N':
                        if value.upper() != 'Y':
                            self.parameter_value_not_y_or_n_error(opt_parm, value)
                        else:
                            if opt_parm == 'multithreading':
                                self.multithreading = value.upper()
                            else:
                                self.multiple_plan_packages = value.upper()
                        self.optional_parms_dict[opt_parm] = value.upper()
                elif opt_parm == 'multiple_plan_packages':
                    if value != 'N':
                        if value != 'Y':
                            self.parameter_value_not_y_or_n_error(opt_parm, value)
                elif opt_parm == 'include_plan':
                    if value.upper() != 'N':
                        if value.upper() != 'Y':
                            self.parameter_value_not_y_or_n_error(opt_parm, value)
                        else:
                            self.include_plan = value.upper()
                            self.optional_parms_dict[opt_parm] = value.upper()
                elif opt_parm == 'options':
                    self.rtptest_options = value
                elif opt_parm == 'wait_to_complete':
                    value = value.lower()
                    if value != "true":
                        if value == "false":
                            self.wait_to_complete = False
                            self.optional_parms_dict[opt_parm] = value
                        else:
                            InputParms.parameter_value_not_valid(opt_parm, value, 'True or False')
                    else:
                        self.optional_parms_dict[opt_parm] = value
            else:
                continue

        """
        If we are driving via the UI certain action options may have additional parameters that can be or should be
        present.
        """
        if self.action is not None:
            # Check for program
            if self.action == '3' or self.action == '5' or self.action == '9' or self.action == '7':
                rc, option_value = self.get_parm_value('program')
                if not rc:
                    option_value = InputParms.get_options_parm_value(self.rtptest_options, 'program')
                if option_value:
                    if self.action == '9' and len(option_value) > 8:
                        self.program_name = option_value[:8].upper()
                    else:
                        self.program_name = option_value.upper()
                    self.expected_parms_dict['program'] = self.program_name
                    self.execution_options_dict['program'] = self.program_name
                else:
                    InputParms.no_required_parameter('program')

            # Check for collection_id
            if self.action == '5' or self.action == '7':
                rc, option_value = self.get_parm_value('collid')
                if not rc:
                    option_value = InputParms.get_options_parm_value(self.rtptest_options, 'collid')
                if option_value:
                    self.collid = option_value
                    self.optional_parms_dict['collid'] = self.collid
                    self.execution_options_dict['collid'] = self.collid

            # Check for connection_type
            if self.action == '3' or self.action == '7':
                rc, option_value = self.get_parm_value('connection_type')
                if not rc:
                    option_value = InputParms.get_options_parm_value(self.rtptest_options, 'connection_type')
                if option_value:
                    self.connection_type = option_value
                    self.expected_parms_dict['connection_type'] = self.connection_type
                    self.execution_options_dict['connection_type'] = self.connection_type
                elif "REG" in self.program_name:
                    # Get the 8th character from the program_name. Since this should be a program that follows the
                    # naming convention it should be either a "C" or an "R" indicating whether we should select the CAF
                    # or RRSAF Connection Type.
                    if self.program_name[7] == 'R' or self.program_name == 'C':
                        self.connection_type = self.program_name[7]
                        self.expected_parms_dict['connection_type'] = self.connection_type
                        self.execution_options_dict['connection_type'] = self.connection_type
                    else:
                        raise ValueError("Attempted to determine proper connection type to select but program '%s' does not follow RTP"
                                         " Test Suite program naming conventions.\nDouble check the name of the program or explicitly"
                                         " code the 'connection_type' parameter in the JSON file. If needed see the 'List"
                                         " of Programs' section\n on the RTP Test Suite page(%s)." %
                                         (self.program_name, self.rtp_manual_hyperlink_text))
                else:
                    try:
                        InputParms.no_required_parameter('connecton_type')
                    except KeyError as error_text_caught:
                        raise ValueError("%s And automatic 'connection_type' determination not possible due to program name."
                                         " Specify parameter explicitly in JSON file." % error_text_caught)

            # Check for planname, corrid, sqlid, repeat, and workstation
            if self.action == '7':
                rc, option_value = self.get_parm_value('plan')
                if not rc:
                    option_value = InputParms.get_options_parm_value(self.rtptest_options, 'plan')
                if option_value:
                    self.plan = option_value
                    self.optional_parms_dict['plan'] = self.plan
                    self.execution_options_dict['plan'] = self.plan

                rc, option_value = self.get_parm_value('corrid')
                if not rc:
                    option_value = InputParms.get_options_parm_value(self.rtptest_options, 'corrid')
                if option_value:
                    self.corrid = option_value
                    self.optional_parms_dict['corrid'] = self.corrid
                    self.execution_options_dict['corrid'] = self.corrid

                rc, option_value = self.get_parm_value('sqlid')
                if not rc:
                    option_value = InputParms.get_options_parm_value(self.rtptest_options, 'sqlid')
                if option_value:
                    self.sqlid = option_value
                    self.optional_parms_dict['sqlid'] = self.sqlid
                    self.execution_options_dict['sqlid'] = self.sqlid

                rc, option_value = self.get_parm_value('repeat')
                if not rc:
                    option_value = InputParms.get_options_parm_value(self.rtptest_options, 'repeat')
                if option_value:
                    self.repeat = option_value
                    self.optional_parms_dict['repeat'] = self.repeat
                    self.execution_options_dict['repeat'] = self.repeat

                rc, option_value = self.get_parm_value('workstation')
                if not rc:
                    option_value = InputParms.get_options_parm_value(self.rtptest_options, 'workstation')
                if option_value:
                    self.workstation = option_value
                    self.optional_parms_dict['workstation'] = self.workstation
                    self.execution_options_dict['workstation'] = self.workstation

                rc, option_value = self.get_parm_value('seed')
                if not rc:
                    option_value = InputParms.get_options_parm_value(self.rtptest_options, 'seed')
                if option_value:
                    self.seed = option_value
                    self.optional_parms_dict['seed'] = self.seed
                    self.execution_options_dict['seed'] = self.seed

    def execute_test(self):
        """
        Execute the built tests identified in the JSON as - "test_type": "rtptest"
        :return: True - requested RTPTEST Action generated and/or submitted the requested Actions JCL job.
        """
        rc = True
        option_rc = False
        job_step_list = []

        self.check_if_output_file_needed('rtptest_execute')

        CommonNav.print_test_start_end('Execute RTPTEST Suite', file_name=self.output_directory)

        self.parameter_summary()

        if self.execute_method == 'dataset':
            set_system(self.connection.get_lpar())
            Job.submit(dsn=self.dataset_name)
            rc = True
        elif self.execute_method == 'UI':
            nav_rtptest = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                                   ssid=self.connection.get_ssid(), userid=self.connection.get_userid(),
                                                   auto_submit=self.auto_submit, debug_mode=self.debug_mode,
                                                   output_directory=self.output_directory)

            nav_rtptest.start_test_suite()
            if self.action == '2':
                rc = self.process_option_2(nav_rtptest)
            elif self.action == '3':
                rc = self.process_option_3(nav_rtptest)
            elif self.action == '4':
                rc = self.process_option_4(nav_rtptest)
            elif self.action == '5':
                rc = self.process_option_5(nav_rtptest)
            elif self.action == '6':
                option_rc, self.jobinfo = self.process_option_6(nav_rtptest)
                job_step_list = ['STRTTRCE', 'RUNIT', 'STCSQLDA', 'CALLSP', 'RRSLOOP', 'DYNHV', 'HVSQLDA', 'ROWIDHV',
                                 'HVTEST', 'RRSRMTE', 'REG011DR', 'REG011SR', 'REG012DR', 'REG012SR','REG021SR',
                                 'REG022DR', 'REG032SR', 'REG033SR', 'REG042SR', 'REG062DR', 'REG062SR', 'REG063DR',
                                 'REG063SR', 'REG064DR', 'REG071SR', 'REG072SR', 'REG080SR', 'REG081SR', 'REG083SR',
                                 'REG121SR', 'REG122SR', 'REG131SR', 'REG132SR', 'REG133DR', 'REG151SR', 'REG152DR',
                                 'REG161BR', 'REG162BR', 'REG163BR', 'REG164BR', 'REG165BR', 'STPTRACE']
            elif self.action == '7':
                rc = self.process_option_7(nav_rtptest)
            elif self.action == '8':
                rc = self.process_option_8(nav_rtptest)
            elif self.action == '9':
                rc, self.jobinfo = self.process_option_9(nav_rtptest)
            elif self.action == '10':
                rc = self.process_option_10(nav_rtptest)
            else:
                raise ValueError("Action option '%s' is not a possible action. Please specify an option from 2 to 10." % self.action)

            nav_rtptest.stop_emulator()  # Need to terminate emulator for ISPF screen driving otherwise WARNING messages appear when job tracking emulator terminates

            if self.debug_mode == 'N':
                if option_rc:
                    self.parse_job_info()
                    job_instance = JobTracking(self.connection.get_lpar(), jobid=self.jobid)
                    if self.wait_to_complete:
                        job_instance.wait_till_job_complete()
                        stepname_result_dict = job_instance.get_job_step_return_codes(job_step_list)
                        for k, v in stepname_result_dict.items():
                            CommonNav.println('%s - %s' % (k, v), file_path=self.output_directory)
                else:
                    rc = False
            else:
                rc = True

        else:
            raise ValueError("Execute_Method parameter value of '%s' invalid. Expected value of 'dataset' or 'UI'." % self.execute_method)

        CommonNav.print_test_start_end('Execute RTPTEST Suite', output_type='end', file_name=self.output_directory)

        if rc:
            return True, self.output_directory
        else:
            return False, self.output_directory

    def process_option_2(self, nav_rtptest):
        """
        Create Objects (Action 2)
        :param nav_rtptest: Instance of NavRtptest
        :return: True or False
        """
        return nav_rtptest.create_objects()

    def process_option_3(self, nav_rtptest):
        """
        Compile Program (Action 3). If the conn_type parameter is provided then the requested Connection Type will be
        selected on the panel. If not provided will attempt to determine the correct connection type to use based on the
        program name if the program name conforms to the RTP Test Suite program naming conventions. If unsuccessful then
        an error exception is raised.

        :param nav_rtptest: Instance of NavRtptest
        :return: True or False
        """

        if self.check_connection_type():
            return nav_rtptest.compile_program(self.program_name, self.connection_type)

    def process_option_4(self, nav_rtptest):
        """
        Bind All Programs (Action 4)
        :param nav_rtptest: Instance of NavRtptest
        :return: True or False
        """
        return nav_rtptest.bind_all_programs(multiple_pp=self.multiple_plan_packages)

    def process_option_5(self, nav_rtptest):
        """
        Bind Single Program (Action 5)
        :param nav_rtptest: Instance of NavRtptest
        :return: True or False
        """

        return nav_rtptest.bind_single_program(self.program_name, collid=self.collid, include_plan=self.include_plan)

    def process_option_6(self, nav_rtptest):
        """
        Process the parameters related to Action "6" of the RTP Test Suite application. Raise an exception if both the
        multithreading and multiple_plan_packages parameters have been set to "Y" as this is not allowable. Otherwise
        execute the Action.
        :param: nav_rtptest: Instance of NavRtptest
        :return: True or False
        """
        if self.multithreading == 'Y' and self.multiple_plan_packages == 'Y':
            raise ValueError("Both 'Multi Threading' and 'Multiple Plan/Packages' options can not be selected. Please"
                             " specify only one execute option.")
        else:
            return nav_rtptest.execute_all(multithreading=self.multithreading, multiple_pp=self.multiple_plan_packages)

    def process_option_7(self, nav_rtptest):
        """
        Execute Single Program (Action 7)
        :param nav_rtptest: Instance of NavRtptest
        :return: True or False
        """
        if self.check_connection_type():
            return nav_rtptest.execute_single(self.execution_options_dict, multithreading=self.multithreading)

    def process_option_8(self, nav_rtptest):
        """
        Free All PKGE/PLAN
        :param nav_rtptest: Instance of NavRtptest
        :return: True or False
        """

        return nav_rtptest.free_all_programs(multiple_pp=self.multiple_plan_packages)

    def process_option_9(self, nav_rtptest):
        """
        Free Single Package
        :param nav_rtptest: Instance of NavRtptest
        :return: True or False
        """

        return nav_rtptest.free_single_program(self.program_name)

    def process_option_10(self, nav_rtptest):
        """
        Cleanup
        :param nav_rtptest: Instance of NavRtptest
        :return: True or False
        """

        return nav_rtptest.cleanup()

    def check_connection_type(self):
        """
        Checks the value of the connection_type parameter
        :return: True or raises an exception.
        """
        if self.connection_type != 'R' and self.connection_type != 'C':
            raise ValueError("Connection type of '%s' not valid. Expected either 'R' or 'C'." % self.connection_type)
        return True

    def parse_job_info(self):
        """
        Parse the tuple created that contains the (jobname, jobid)
        :return:
        """
        self.jobname = self.jobinfo[0]
        self.jobid = self.jobinfo[1]

    @staticmethod
    def parameter_value_not_y_or_n_error(parameter_name, parameter_value):
        """
        Raises a ValueError exception explaining the expected value of the parameter is "Y" or "N"
        :param parameter_name: Name of the parameter to put in the message
        :param parameter_value: Value the parameter was given instead of the expected value.
        :return: nothing, raises an exception.
        """
        raise ValueError("'%s' parameter value of '%s' not valid. Expected either 'Y' or 'N'." %
                         (parameter_name, parameter_value))