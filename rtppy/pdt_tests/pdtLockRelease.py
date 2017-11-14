from core.BaseTest import BaseTest
from core.Factories import Factory
from core.HexConversion import add_two_hex_strings
from core.InputParms import InputParms
from core.JobTracking import JobTracking
from core.Xdc import Xdc
from core.common import CommonNav


class LockRelease(BaseTest):
    """
    Document this class
    """

    def __init__(self, test_parms_dict, connection_instance, input_arg_dict):
        BaseTest.__init__(self, test_parms_dict, connection_instance, input_arg_dict)
        self.start_collection_instance = None
        # self.stop_collection_instance = None
        self.nav_instance = None
        self.xman_name = None
        # self.wait_time_after_init = 6
        # self.wait_time_after_abend_restart = 61
        # self.num_abend_restarts = 2
        # self.abend_in = None
        # self.zapped_dii_instr_addr = None
        # self.zapped_diu_instr_addr = None
        self.loadlib = None
        self.xman_job = None
        self.init_complete = None
        self.init_progress = None
        # self.term_complete = None
        # self.term_progress = None

    def build_test(self):
        """
        Ensures and sets all class variables that are required are supplied from either the command line
        override or from the test parameters dictionary from the JSON input file. This ensures that all the minimum
        input parameters needed for the execute routine are provided.
        :return: Nothing
        """
        expected_parms = ['xman']
        # optional_parms = []

        super(LockRelease, self).build_test()
        for parm in expected_parms:
            rc, value = self.get_parm_value(parm)
            if rc:
                if parm == 'xman':
                    self.xman_name = value.upper()
                    self.expected_parms_dict[parm] = self.xman_name
            else:
                InputParms.no_required_parameter(parm)

        # for opt_parm in optional_parms:
        #     rc, value = self.get_parm_value(opt_parm)
        #     if opt_parm == 'wait_time_after_coll_init':
        #         if rc:
        #             self.wait_time_after_init = value
        #             self.optional_parms_dict[opt_parm] = self.wait_time_after_init
        #         else:
        #             self.default_parms_dict[opt_parm] = self.wait_time_after_init
        #     elif opt_parm == 'wait_time_after_abend_restart':
        #         if rc:
        #             self.wait_time_after_abend_restart = value
        #             self.optional_parms_dict[opt_parm] = self.wait_time_after_abend_restart
        #         else:
        #             self.default_parms_dict[opt_parm] = self.wait_time_after_abend_restart
        #     elif opt_parm == 'number_of_abend_restarts':
        #         if rc:
        #             self.num_abend_restarts = value
        #             self.optional_parms_dict[opt_parm] = self.num_abend_restarts
        #         else:
        #             self.default_parms_dict[opt_parm] = self.num_abend_restarts
        #     else:
        #         continue

        # Set the test_type json parameter to be 'start collection' in order to create a start collection instance
        # so the calling of the build and execute methods will work correctly
        # self.dict_parms['test_type'] = 'start collection'
        # self.start_collection_instance = StartCollection(self.dict_parms, self.connection, self.command_line_overrides)
        # self.start_collection_instance.build_test()
        # # Set the test_type json parameter to be 'stop collection' in order to create a stop collection instance
        # so the calling of the build and execute methods will work correctly
        # self.dict_parms['test_type'] = 'stop collection'
        # self.stop_collection_instance = StartCollection(self.dict_parms, self.connection, self.command_line_overrides)
        # self.stop_collection_instance.build_test()

    def execute_test(self):
        """
        Zaps instructions in DT$DIU in order to create a situation where the collection doesn't release a lock which can
        cause DB2 to crash.

        :return: True
                 False
        """

        lock_release_rc = False
        self.check_if_output_file_needed('lock_release')
        CommonNav.print_test_start_end('Lock Release', file_name=self.output_directory)
        self.parameter_summary()

        self.nav_instance = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                                     ssid=self.connection.get_ssid(),
                                                     userid=self.connection.get_userid(),
                                                     debug_mode=self.debug_mode, output_directory=self.output_directory)

        self.nav_instance.start_product(release_environment=self.product_release)
        # Build our expected collection initialization and termination message we expect to see.
        self.init_progress, self.init_complete = self.nav_instance.build_collection_init_term_messages()
        # self.term_progress, self.term_complete = self.nav_instance.build_collection_init_term_messages(message_type='term')

        # Edit the xman job name, module/csect name based on DB2 Version in the needed XDC commands pds members.
        db2_ver = CommonNav.db2_version(self.nav_instance.u_ssid.upper())
        if db2_ver is None:
            raise ValueError('DB2 Version for SSID %s could not be found.' % self.nav_instance.u_ssid.upper())
        else:
            diu_mod_tuple = self.db2_ver_mod_csect_name('PDTDIUC', self.nav_instance.u_ssid.upper(), 'DT$DIUC')
            diu_module_name = diu_mod_tuple[0]
            diu_csect_name = diu_mod_tuple[1]
            dio_mod_tuple = self.db2_ver_mod_csect_name('PDTDIOC', self.nav_instance.u_ssid.upper(), 'DT$DIOC')
            dio_module_name = dio_mod_tuple[0]
            dio_csect_name = dio_mod_tuple[1]

        # Get the initial view of the xmanager before we start the collection.
        self.xman_job = JobTracking(use_lpar=self.connection.get_lpar(), jobname=self.xman_name)
        self.xman_job.get_job_message_log()  # Get the initial xman log output before we start the collection

        #  Just for good measure lets check to see that the xmanager fully initialized successfully
        if self.xman_job.find_print_found_message_from_log('PXM0101') is not None:
            print("Xmanager Initialized")

        # if self.start_collection_instance.execute_test():
        #     update_job_log = self.xman_job.find_message_with_timer(self.init_progress, 30)
        #     # Search for collection init complete message to make sure collection is running.
        #     if update_job_log is not None:
        #         self.xman_job.find_print_found_message_from_log(self.init_complete, use_log=update_job_log)
        #         print("Collection start successful\n")

            if self.zap_two_instructions(self.xman_name, diu_module_name, diu_csect_name,
                                         zapped_instr_set='B90400F7EB0E6010003EA774FFF447000005',
                                         not_zapped_instruction_set='B90400F7EB0E6010003EA774FFF4A7F40005',
                                         first_instr_offset='E', first_zap_value='4700', second_instr_offset='6',
                                         second_zap_value='A7F4'):
                if self.zap_two_instructions(self.xman_name, dio_module_name, dio_csect_name,
                                             zapped_instr_set='B9040018EBE02000003EA774FFF147000005',
                                             not_zapped_instruction_set='B9040018EBE02000003EA774FFF1A7F40005',
                                             first_instr_offset='E', first_zap_value='4700', second_instr_offset='6',
                                             second_zap_value='A7F4'):
                    lock_release_rc = True

        CommonNav.print_test_start_end('Lock Release', output_type='end', file_name=self.output_directory)

        if lock_release_rc:
            return True, self.output_directory
        else:
            return False, self.output_directory

    def zap_two_instructions(self, xman_name, mod_name, csect, zapped_instr_set, not_zapped_instruction_set,
                             first_instr_offset, first_zap_value, second_instr_offset, second_zap_value, zap='on'):
        """
        Zaps jump instruction in DIU to cause the calling of DT$IURLK to be skipped unconditionally so the CML lock is
        not freed.

        :param xman_name: Xman Jobname (i.e. PTXRUN19)
        :param mod_name: Name of the module where the zapping will be done. (i.e PDTDIUCx where 'x' is the DB2 version
                         that will be used by the collection).

        :param csect: Name of the CSECT where the zapping will be done. (i.e DT$DIUCx where 'x' is the DB2 version
                         that will be used by the collection).

        :param not_zapped_instruction_set: Character string of hex bytes that represent the instruction set to use to
                                           find the correct place in the code to ZAP before they have been zapped.

        :param first_instr_offset: Offset, in hex, in the not_zapped_instruction_set character string that the first_zap_value
                                    should go. (0 based)

        :param first_zap_value: character string, in hex, of what the first instruction should be zapped to.

        :param second_instr_offset: Offset, in hex, in the not_zapped_instruction_set character string that the second_zap_value
                                    should go. (0 based)

        :param second_zap_value: character string, in hex, of what the second instruction should be zapped to.

        :param zapped_instr_set: Character string of hex bytes that represent the instruction set after it has been
                                 ZAPPED.


        :param zap: defaults to "on" to zap the code.
        :return: True or False
        """
        assert isinstance(self.xman_job, JobTracking)
        # not_zapped_search_instruction_set = 'B90400F7EB0E6010003EA774FFF4A7F40005'
        # zapped_search_instruction_set = 'B90400F7EB0E6010003EA774FFF447000005'
        zap_diu_rc = False
        error_msg = ""

        xdc_instance = Xdc(self.nav_instance, output_file=self.output_directory)

        # Get the XMANAGER JESJCL log and find the DSN where PDTDIUCx exists.
        if zap == 'on':
            self.xman_job.get_job_jcl_log()
            diu_in_loadlib = self.xman_job.search_all_loadlibs_for_mem('STEPLIB', 'PXMINICC', mod_name)

        # Enter XDC authorized
        if xdc_instance.enter_xdc():
            if xdc_instance.xdc_set_asid(xman_name):
                if zap == 'on':
                    if xdc_instance.xdc_map_command(mod_name, diu_in_loadlib):
                        xdc_find_rc = xdc_instance.xdc_find_instruction_set(zapped_instr_set, mod_name + '.' + csect)
                        if xdc_find_rc is False:
                            if xdc_instance.xdc_find_instruction_set(not_zapped_instruction_set, mod_name + '.' + csect):
                                field = self.nav_instance.ptg2_em.screen.get_field_for_key(1)
                                addr_start = field.following_text.find('_') + 1
                                addr_end = field.following_text.find('(') - 3
                                first_zapped_diu_instr_addr = field.following_text[addr_start:addr_end]
                                first_zapped_diu_instr_addr = add_two_hex_strings(first_zapped_diu_instr_addr, first_instr_offset)
                                first_zap_command = xdc_instance.xdc_zap_on(first_zapped_diu_instr_addr, first_zap_value)
                                if first_zap_command is not None:
                                    self.nav_instance.ptg2_em.screen['xdc'] = 'F +0'
                                    self.nav_instance.ptg2_em.app.ispf_submit()
                                    CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
                                    second_zapped_diu_instr_addr = add_two_hex_strings(first_zapped_diu_instr_addr, second_instr_offset)
                                    second_zap_command = xdc_instance.xdc_zap_on(second_zapped_diu_instr_addr, second_zap_value)
                                    if second_zap_command is not None:
                                        self.nav_instance.ptg2_em.screen['xdc'] = 'F +0'
                                        self.nav_instance.ptg2_em.app.ispf_submit()
                                        CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
                                        zap_diu_rc = True
                                    else:
                                        error_msg = '\nZap command - %s - failed.\n' % second_zap_command
                                else:
                                    error_msg = '\nZap command - %s - failed.\n' % first_zap_command
                            else:
                                error_msg = '\nFind command did not find a match.\n'
                        elif xdc_find_rc:
                            zap_diu_rc = True
                        else:
                            error_msg = "\nProblem issuing xdc 'Find' command. Possibly a syntax error.\n"
                    else:
                        error_msg = '\nMap command failed for Xman - %s\n' % xman_name
                # else:
                #     zap_off_command = Xdc.xdc_zap_off(self.nav_instance, self.zapped_diu_instr_addr, zap_off_byte)
                #     if zap_off_command is not None:
                #         self.nav_instance.ptg2_em.screen['xdc'] = 'D %s' % self.zapped_diu_instr_addr
                #         self.nav_instance.ptg2_em.app.ispf_submit()
                #         CommonNav.nav_screen_capture(self.nav_instance.ptg2_em, file_name=self.output_directory)
                #         zap_diu_rc = True
                #     else:
                #         error_msg = '\nZap off command - %s - failed.\n' % zap_off_command
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
