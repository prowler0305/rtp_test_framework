import datetime
# import sys
from ptg2.context import use_system
from core.BaseTest import BaseTest
from core.Factories import Factory
from core.HexConversion import add_two_hex_strings
from core.InputParms import InputParms
from core.JobTracking import JobTracking
from core.Rtp_Java import RtpJava
from core.common import CommonNav
from pdt_tests.StartCollection import StartStopCollection


class AbendRestart(BaseTest):
    """
    Document this class
    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        BaseTest.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.start_collection_instance = None
        self.stop_collection_instance = None
        self.nav_instance = None
        self.xman_name = None
        self.wait_time_after_init = 6
        self.wait_time_after_abend_restart = 61
        self.num_abend_restarts = 2
        self.abend_in = None
        self.zapped_dii_instr_addr = None
        self.zapped_diu_instr_addr = None
        self.loadlib = None
        self.xman_job = None
        self.init_complete = None
        self.init_progress = None
        self.term_complete = None
        self.term_progress = None

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """
        expected_parms = ['xman', 'abend_in']
        optional_parms = ['wait_time_after_coll_init', 'wait_time_after_abend_restart', 'number_of_abend_restarts']

        super(AbendRestart, self).build_test()
        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'xman':
                    self.xman_name = value.upper()
                    self.expected_parms_dict[parm] = self.xman_name
                if parm == 'abend_in':
                    self.abend_in = value.upper()
                    self.expected_parms_dict[parm] = self.abend_in
            else:
                InputParms.no_required_parameter(parm)

        for opt_parm in optional_parms:
            rc, value = self.get_parm_value(opt_parm)
            if opt_parm == 'wait_time_after_coll_init':
                if rc:
                    self.wait_time_after_init = value
                    self.optional_parms_dict[opt_parm] = self.wait_time_after_init
                else:
                    self.default_parms_dict[opt_parm] = self.wait_time_after_init
            elif opt_parm == 'wait_time_after_abend_restart':
                if rc:
                    self.wait_time_after_abend_restart = value
                    self.optional_parms_dict[opt_parm] = self.wait_time_after_abend_restart
                else:
                    self.default_parms_dict[opt_parm] = self.wait_time_after_abend_restart
            elif opt_parm == 'number_of_abend_restarts':
                if rc:
                    self.num_abend_restarts = value
                    self.optional_parms_dict[opt_parm] = self.num_abend_restarts
                else:
                    self.default_parms_dict[opt_parm] = self.num_abend_restarts
            else:
                continue

        # Set the test_type json parameter to be 'start collection' in order to create a start collection instance
        # so the calling of the build and execute methods will work correctly
        self.dict_parms['test_type'] = 'start collection'
        self.start_collection_instance = StartStopCollection(self.dict_parms, self.connection, self.command_line_overrides)
        self.start_collection_instance.build_test()
        # Set the test_type json parameter to be 'stop collection' in order to create a stop collection instance
        # so the calling of the build and execute methods will work correctly
        self.dict_parms['test_type'] = 'stop collection'
        self.stop_collection_instance = StartStopCollection(self.dict_parms, self.connection, self.command_line_overrides)
        self.stop_collection_instance.build_test()

    def execute_test(self):
        """
        Tests the products Abend restart functionality by doing the following:
        
            --Note: See "Main Restart Logic" section that follows for reference to "restart logic"
         
         1. Starts a collection and continues if start successful
         2. If testing abend restart within 5 minutes of collections start:
             a. Execute restart logic
                i. If restart fails
                    1. Test successful
                ii. Else
                    1. Test failed - we shouldn't have restarted the collection automatically
         3. Else if testing abend restart between 5 minutes and 59 minutes:
            a. Sleep for users specified amount of time via paramter or a default time
            b. Execute restart logic
                i. If successful
                    1. test successful
                ii. Else
                    1. test failed we should have restarted automatically
         4. Else testing abend restart after 60 minutes
            a. Sleep for 60 minutes
            b. Execute restart logic
                i. If successful
                    1. Test successful
                ii.  Else
                    1. Test failed we should have restarted automatically
        
        -------------------
        Main Restart Logic
        -------------------
        I. Execute XDC ZAP scripts to force abends to occur in collection engine code.
        II. Execute SQL activity via RTPJ and/or RTPTEST to drive abends in collection code.
        III. Look for collection termination/initialization and/or abend restart message in Xmanlog
            a. If collection restart/initialization messages found:
                1. Return True
            b. Else
                1. Return False

        :return: True
                 False
        """

        abend_restart_rc = False
        self.check_if_output_file_needed('abend_restart')
        CommonNav.print_test_start_end('Abend Restart', file_name=self.output_directory)
        self.parameter_summary()
        # self.parameter_summary(self.expected_parms_dict, output_file=self.output_directory)
        # self.parameter_summary(self.optional_parms_dict, parameter_type='optional', output_file=self.output_directory)
        # self.parameter_summary(self.default_parms_dict, parameter_type='default', output_file=self.output_directory)

        self.nav_instance = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                                     ssid=self.connection.get_ssid(),
                                                     userid=self.connection.get_userid(),
                                                     debug_mode=self.debug_mode, output_directory=self.output_directory)

    # Build our expected collection initialization and termination message we expect to see.
        self.init_progress, self.init_complete = self.nav_instance.build_collection_init_term_messages()
        self.term_progress, self.term_complete = self.nav_instance.build_collection_init_term_messages(message_type='term')

        # Edit the xman job name, module/csect name based on DB2 Version in the needed XDC commands pds members.
        db2_ver = CommonNav.db2_version(self.nav_instance.u_ssid.upper())
        if db2_ver is None:
            raise ValueError('DB2 Version for SSID %s could not be found.' % self.nav_instance.u_ssid.upper())

        # Get the initial view of the xmanager before we start the collection.
        self.xman_job = JobTracking(use_lpar=self.connection.get_lpar(), jobname=self.xman_name)
        self.xman_job.get_job_message_log()  # Get the initial xman log output before we start the collection

        #  Just for good measure lets check to see that the xmanager fully initialized successfully
        if self.xman_job.find_print_found_message_from_log('PXM0101') is not None:
            print("Xmanager Initialized")

        if self.start_collection_instance.execute_test():
            update_job_log = self.xman_job.find_message_with_timer(self.init_progress, 30)
            # Search for collection init complete message to make sure collection is running.
            if update_job_log is not None:
                self.xman_job.find_print_found_message_from_log(self.init_complete, use_log=update_job_log)
                print("Collection start successful")

                collection_mod_address = self.xman_job.find_dii_address(update_job_log)
                if collection_mod_address is not None:
                    # Initial sleep time after initial collection start
                    print("Continue after wait_time_after_coll_init value expires in %d minute(s)." % self.wait_time_after_init)
                    BaseTest.countdown_timer(self.wait_time_after_init * 60)
                    for repeat in range(0, self.num_abend_restarts):
                        print("\nForce abend restart - %s" % datetime.datetime.now())
                        if self.abend_in == 'DII':
                            force_abend_rc = self.zap_dii(self.xman_name, collection_mod_address)
                        else:
                            force_abend_rc = self.zap_diu(self.xman_name, db2_ver)

                        if force_abend_rc:
                            if self.abend_in == 'DII':
                                RtpJava.execute_rtpj('Abend_Restart_10_Test.JSON',
                                                     ssid=self.connection.get_ssid(),
                                                     userid=self.connection.get_userid(),
                                                     sync=False)
                            else:
                                RtpJava.execute_rtpj('Abend_Restart_100_Test.JSON',
                                                     ssid=self.connection.get_ssid(),
                                                     userid=self.connection.get_userid(),
                                                     sync=False)

                            while self.xman_job.find_print_found_message_from_log(self.term_progress, use_log=update_job_log) is None:
                                print("Collection not terminating yet. Checking again in "),
                                BaseTest.countdown_timer(6)
                                update_job_log = self.xman_job.get_job_message_log(update=True)

                            if self.abend_in == 'DIU':
                                if not self.zap_diu(self.xman_name, db2_ver, zap='off'):
                                    print("Can't continue testing due to previous error zapping DIU back to normal. "
                                          "Stopping %s collection. Stopping Xmanager." % self.product_code)
                                    self.xman_job.started_task.stop()

                            # if repeat == 0 and self.wait_time_after_init < 5:
                            #     if self.check_no_abend_restart():
                            #         return True
                            #     else:
                            #         return False
                            # elif repeat == 0 and self.wait_time_after_init > 5:
                            #     if self.check_abend_restart():
                            #         abend_restart_rc = True
                            #     else:
                            #         return False
                            # elif repeat > 0 and self.wait_time_after_abend_restart < 60:
                            #     if self.check_no_abend_restart():
                            #         return True
                            #     else:
                            #         return False
                            # elif repeat > 0 and self.wait_time_after_abend_restart > 60:
                            #     if self.check_abend_restart():
                            #         abend_restart_rc = True
                            #     else:
                            #         return False
                            # else:
                            #     pass  # This might need to be some sort of error message possibly.
                            print("Wait for all abend restart related events to occur.")
                            BaseTest.countdown_timer(60)

                            if self.num_abend_restarts > 1:
                                print("Continue after wait_time_after_abend_restart value expires in %d minute(s)." % self.wait_time_after_abend_restart)
                                BaseTest.countdown_timer(self.wait_time_after_abend_restart * 60)
                        else:
                            print("Can't continue testing due to previous error. Stopping %s collection." % self.product_code)
                            self.stop_collection_instance.execute_test()
                else:
                    print("Couldn't obtain address where %s collection engine module address was loaded. Terminating"
                          " collection." % self.product_code)

                if self.stop_collection_instance.execute_test():  # Stop the collection if we successfully started it.
                    update_job_log = self.xman_job.get_job_message_log(update=True)

                    if self.xman_job.find_print_found_message_from_log(self.term_progress, use_log=update_job_log) and \
                            self.xman_job.find_print_found_message_from_log(self.term_complete, use_log=update_job_log):
                        print("Collection terminate successful")

        """Todo: Temporarily to help with initial Abend Restart QA testing get the whole log at the end and print it. This is useful
        for now as QA runs each test case the Xman log will be recorded here which has all the messages in and around abend
        restart testing. They can then restart the xmanager being used between each test and still get a record of each
        xman log for each test to validate abend restart success or failure."""
        BaseTest.countdown_timer(10, watch_timer=False)
        self.xman_job.get_job_message_log()
        self.xman_job.print_message_log()
        abend_restart_rc = True

        CommonNav.print_test_start_end('Abend Restart', output_type='end', file_name=self.output_directory)

        if abend_restart_rc:
            return True, self.output_directory
        else:
            return False, self.output_directory

    def zap_dii(self, xman_name, dii_address, zap='on'):
        """


        :param xman_name:
        :param dii_address:
        :param zap:
        :return:
        """

        not_zapped_search_instruction_set = 'C4E35BC4C9C9E2D8EBECD0080024'
        zapped_search_instruction_set = 'C4E35BC4C9C9E2D800ECD0080024'
        zap_off_byte = not_zapped_search_instruction_set[16] + not_zapped_search_instruction_set[17]
        zap_dii_rc = False
        xdc_tso_command = 'TSO XDCCALLA IEFBR14'

        # Enter XDC authorized
        CommonNav.tso_command(self.nav_instance.ptg2_em, xdc_tso_command, text_to_wait_for='DBC854I z/XDC for z/OS',
                              out_file=self.output_directory)

        if self.xdc_set_asid(xman_name):
            if zap == 'on':
                xdc_find_rc = self.xdc_find_instruction_set(zapped_search_instruction_set, dii_address)
                if xdc_find_rc is False:
                    if self.xdc_find_instruction_set(not_zapped_search_instruction_set, dii_address):
                        field = self.nav_instance.ptg2_em.screen.get_field_for_key(1)
                        addr_start = field.following_text.find('_') + 1
                        addr_end = field.following_text.find('(') - 3
                        self.zapped_dii_instr_addr = field.following_text[addr_start:addr_end]
                        self.zapped_dii_instr_addr = add_two_hex_strings(self.zapped_dii_instr_addr, '8')
                        zap_command = self.xdc_zap_on(self.zapped_dii_instr_addr)
                        if zap_command is not None:
                            self.nav_instance.ptg2_em.screen['xdc'] = 'D +0'
                            self.nav_instance.ptg2_em.app.ispf_submit()
                            CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
                            zap_dii_rc = True
                        else:
                            error_msg = '\nZap command - %s - failed.\n' % zap_command
                    else:
                        error_msg = '\nFind command did not find instruction to zap in DII.\n'
                elif xdc_find_rc:
                    zap_dii_rc = True
                else:
                    error_msg = "\nProblem issuing xdc 'FIND' command. Possibly a syntax error.\n"
            else:
                zap_off_command = self.xdc_zap_off(self.zapped_dii_instr_addr, zap_off_byte)
                if zap_off_command is not None:
                    self.nav_instance.ptg2_em.screen['xdc'] = 'D %s' % self.zapped_dii_instr_addr
                    self.nav_instance.ptg2_em.app.ispf_submit()
                    CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
                    zap_dii_rc = True
                else:
                    error_msg = '\nZap off command - %s - failed.\n' % zap_off_command
        else:
            error_msg = '\nSET command failed for Xman - %s\n' % xman_name

        # Get out of XDC and return emulator back to wherever xdc was called from.
        self.nav_instance.ptg2_em.app.ispf_submit(action='pf4')
        CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)

        if zap_dii_rc:
            return True
        else:
            print(error_msg)
            return False

    def zap_diu(self, xman_name, ssid_version, zap='on'):
        """

        :param xman_name:
        :param ssid_version:
        :param zap:
        :return:
        """
        assert isinstance(self.xman_job, JobTracking)
        not_zapped_search_instruction_set = '07FF9140CA33A7840011'
        zapped_search_instruction_set = '07FF0040CA33A7840011'
        zap_off_byte = not_zapped_search_instruction_set[4] + not_zapped_search_instruction_set[5]
        zap_diu_rc = False
        xdc_tso_command = 'TSO XDCCALLA IEFBR14'
        module_name = 'PDTDIUC' + ssid_version[1]
        csect_name = 'DT$DIUC' + ssid_version[1]

        # Get the XMANAGER JESJCL log and find the DSN where PDTDIUCx exists.
        if zap == 'on':
            self.xman_job.get_job_jcl_log()
            diu_in_loadlib = self.xman_job.search_all_loadlibs_for_mem('STEPLIB', 'PXMINICC', module_name)

        # Enter XDC authorized
        CommonNav.tso_command(self.nav_instance.ptg2_em, xdc_tso_command, text_to_wait_for='DBC854I z/XDC for z/OS',
                              out_file=self.output_directory)

        if self.xdc_set_asid(xman_name):
            if zap == 'on':
                if self.xdc_map_command(module_name, diu_in_loadlib):
                    xdc_find_rc = self.xdc_find_instruction_set(zapped_search_instruction_set, module_name + '.' + csect_name)
                    if xdc_find_rc is False:
                        if self.xdc_find_instruction_set(not_zapped_search_instruction_set, module_name + '.' + csect_name):
                            field = self.nav_instance.ptg2_em.screen.get_field_for_key(1)
                            addr_start = field.following_text.find('_') + 1
                            addr_end = field.following_text.find('(') - 3
                            self.zapped_diu_instr_addr = field.following_text[addr_start:addr_end]
                            self.zapped_diu_instr_addr = add_two_hex_strings(self.zapped_diu_instr_addr, '2')
                            zap_command = self.xdc_zap_on(self.zapped_diu_instr_addr)
                            if zap_command is not None:
                                self.nav_instance.ptg2_em.screen['xdc'] = 'D +0'
                                self.nav_instance.ptg2_em.app.ispf_submit()
                                CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
                                zap_diu_rc = True
                            else:
                                error_msg = '\nZap command - %s - failed.\n' % zap_command
                        else:
                            error_msg = '\nFind command did not find a match.\n'
                    elif xdc_find_rc:
                        zap_diu_rc = True
                    else:
                        error_msg = "\nProblem issuing xdc 'Find' command. Possibly a syntax error.\n"
                else:
                    error_msg = '\nMap command failed for Xman - %s\n' % xman_name
            else:
                zap_off_command = self.xdc_zap_off(self.zapped_diu_instr_addr, zap_off_byte)
                if zap_off_command is not None:
                    self.nav_instance.ptg2_em.screen['xdc'] = 'D %s' % self.zapped_diu_instr_addr
                    self.nav_instance.ptg2_em.app.ispf_submit()
                    CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
                    zap_diu_rc = True
                else:
                    error_msg = '\nZap off command - %s - failed.\n' % zap_off_command
        else:
            error_msg = '\nSET command failed for Xman - %s\n' % xman_name

        # Get out of XDC and return emulator back to wherever xdc was called from.
        self.nav_instance.ptg2_em.app.ispf_submit(action='pf4')
        CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)

        if zap_diu_rc:
            return True
        else:
            print(error_msg)
            return False

    def xdc_find_instruction_set(self, instruction_set, start_search_address):
        """


        :param instruction_set:
        :param start_search_address:
        :return: True - number of matches is 1
                 False - number of matches is 0
                 None - problem with find command in general (i.e. syntax errors, etc...)
        """
        self.nav_instance.ptg2_em.screen['xdc'] = 'FIND %s %s' % (instruction_set, start_search_address)
        CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
        self.nav_instance.ptg2_em.app.ispf_submit()
        CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)

        if self.nav_instance.ptg2_em.screen.contains('NUMBER OF MATCHES:             1'):
            return True
        elif self.nav_instance.ptg2_em.screen.contains('NUMBER OF MATCHES:             0'):
            return False
        else:
            return None

    def xdc_set_asid(self, asid_identifier):
        """
        Issues the XDC SET ASID command to. Requires XDC was entered APF Authorized.

        :param asid_identifier: address space id identifier. Can be hex value or jobname (i.e. 02AD or PTXRUN19)
        :return: True or False if SET ASID command was successful
        """
        self.nav_instance.ptg2_em.screen['xdc'] = 'SET ASID %s' % asid_identifier
        self.nav_instance.ptg2_em.submit_screen(wait_for_text='DBC878I ASID SET TO')
        CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
        if self.nav_instance.ptg2_em.screen.contains('DBC878I ASID SET TO'):
            return True
        else:
            return False

    def xdc_zap_on(self, instr_addr_to_zap):
        """
        Zap the instruction at the address given with a x'00' to force a S0C1 abend.

        :param instr_addr_to_zap: address of the byte to zap
        :return: Zap command used if successful or None if failed.
        """
        zap_command = 'ZAP %s=00' % instr_addr_to_zap
        self.nav_instance.ptg2_em.screen['xdc'] = zap_command
        CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
        self.nav_instance.ptg2_em.app.ispf_submit()

        if not self.nav_instance.ptg2_em.screen.contains('ZAP %s=' % instr_addr_to_zap):
            return zap_command
        else:
            return None

    def xdc_zap_off(self, instr_addr_to_zap, zap_back_to_byte):
        """
        Zaps the byte given back into the instruction address given.

        :param instr_addr_to_zap: address of the byte to zap back to the byte value given
        :param zap_back_to_byte: single byte in hex to zap in.
        :return: Zap off command used if successful or None if failed.
        """
        zap_off_command = 'ZAP %s=%s' %(instr_addr_to_zap, zap_back_to_byte)
        self.nav_instance.ptg2_em.screen['xdc'] = zap_off_command
        CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
        self.nav_instance.ptg2_em.app.ispf_submit()

        if not self.nav_instance.ptg2_em.screen.contains('ZAP %s=' % instr_addr_to_zap):
            return zap_off_command
        else:
            return None

    def xdc_map_command(self, module_name, loadlib):
        """
        Issues the XDC map givent he module name and loadlib

        :param module_name: name of the load module to map
        :param loadlib: loadlib dataset the module is in.
        :return:
        """
        self.nav_instance.ptg2_em.screen['xdc'] = 'MAP %s,%s' % (module_name, loadlib)
        CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
        self.nav_instance.ptg2_em.submit_screen()
        CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
        if self.nav_instance.ptg2_em.screen.contains('The following maps have been built:'):
            return True
        else:
            return False

    def check_no_abend_restart(self):
        """

        :return:
        """
        print("Looking for no abend restart message. Timeout after %d seconds" % 60)
        update_job_log = self.xman_job.find_message_with_timer('PDT0134', 60, print_timer=False)
        if update_job_log is not None:
            self.xman_job.find_print_found_message_from_log(self.term_complete, use_log=update_job_log)
        if self.xman_job.find_print_found_message_from_log(self.init_progress, use_log=update_job_log) is None:
            update_job_log = self.xman_job.find_message_with_timer(self.init_progress, 10)
            if update_job_log is None:
                return True
            else:
                return False

    def check_abend_restart(self):
        """

        :return:
        """
        print("Looking for no abend restart message. Timeout after %d seconds" % 90)
        update_job_log = self.xman_job.find_message_with_timer('PDT0132', 90, print_timer=False)
        if update_job_log is not None:
            if self.xman_job.find_print_found_message_from_log(self.init_progress, use_log=update_job_log) is not None:
                self.xman_job.find_print_found_message_from_log(self.init_complete, use_log=update_job_log)
                return True
            else:
                return False
