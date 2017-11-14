from ptg2.zos.emul_apps import App
from core.common import CommonNav
from core.Rtp_nav import NavRtp


class NavRtptest(NavRtp):
    """
    Instance class that provides services to interact with the RTP Activity Suite mainframe application options. This
    allows SQL activity actions be included in automation JSON test files.

    Typical usage:

    .. code-block:: python

    from core.Factories import Factory

        nav_rtptest = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                                       ssid=self.connection.get_ssid(), userid=self.connection.get_userid(),
                                                       auto_submit=self.auto_submit, debug_mode=self.debug_mode)

         nav_rtptest.start_test_suite()

        rc, self.jobinfo = self.process_option_6(nav_rtptest)

    """

    def __init__(self, u_lpar, u_ssid, userid, auto_submit=None, debug_mode='N', output_file=None):
        NavRtp.__init__(self, u_lpar, u_ssid, userid, debug_mode=debug_mode, output_file=output_file)
        self.auto_submit = auto_submit

        # Create instance of PTG2 emulator.
        self.start_emulator()

    def start_test_suite(self):
        """
        Starts the RTPTEST suite application
        :return:
        """

        if self.ptg2_em.app.name != 'db2tools':
            self.ptg2_em.app.tso_ispf()

        self.ptg2_em.app.ispf_command('TSO RTPTEST')

        if self.ptg2_em.screen.contains("MSGX013"):
            self.ptg2_em.app.ispf_submit()
            if self.debug_mode != 'N':
                CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
            self.ptg2_em.app.ispf_command('MSG OFF')
        self.ptg2_em.screen['localssid'] = self.u_ssid
        self.ptg2_em.screen['autosubmit'] = self.auto_submit
        # for line in self.ptg2_em.screen.lines:
        #     print(line)
        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        return

    def create_objects(self):
        """
        Drives the RTPTEST Action option "2" Create Objects
        :return: - True or False indicating success of job generation and/or automatic submission
        """

        self.ptg2_em.screen['actions'] = '2'
        return self.rtp_test_submit_screen()

    def compile_program(self, program_name, conn_type):
        """
        Drives the RTPTEST Action option "3" Compile Program for the program name and connection type provided.

        :param program_name: Name of an RTPTEST suite program to compile.
        :param conn_type: The connection type to use specified as a single character, "C" for CAF and "R" for RRSAF.
        :return: - True or False indicating success of job generation and/or automatic submission
        """

        if conn_type == 'R':
            self.ptg2_em.screen['rrsaf'] = 'S'
        else:
            self.ptg2_em.screen['caf'] = 'S'

        self.ptg2_em.screen['actions'] = '3'
        self.fill_rtptest_field('Compile Program', program_name)
        return self.rtp_test_submit_screen()

    def bind_all_programs(self, multiple_pp=None):
        """
        Drives the RTPTEST Action option "4" Bind All Programs.
        :param multiple_pp:  Multi Plan/Package option of "Y" or "N"
        :return: - True or False indicating success of job generation and/or automatic submission
        """

        self.ptg2_em.screen['actions'] = '4'
        if multiple_pp is not None:
            self.ptg2_em.screen['multiplanpackage'] = multiple_pp
        return self.rtp_test_submit_screen()

    def bind_single_program(self, program_name, collid=None, include_plan=None):
        """
        Drives the RTPTEST Action option "4" Bind All Programs.
        :param program_name: (Required) - Name of the program to bind the package for.
        :param collid: (optional) - What collection ID to put in the Collection ID field if not the test suites default
        :param include_plan:  (optional) - Value of "Y" indicates to set the "Include Plan" parameter.
        :return: - True or False indicating success of job generation and/or automatic submission
        """

        self.ptg2_em.screen['actions'] = '5'
        self.fill_rtptest_field('Bind Single Program', program_name)

        if collid is not None:
            if len(collid) > 8:
                self.ptg2_em.screen['command'] = 'expand'
                if self.debug_mode == 'Y':
                    CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
                collid_field_obj = CommonNav.get_first_field(self.ptg2_em, 'Collection ID')
                collid_field_obj.focus()
                self.ptg2_em.app.ispf_submit()
                if self.debug_mode == 'Y':
                    CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
                self.ptg2_em.send_string(collid)
                CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
                CommonNav.nav_screen_back(self.ptg2_em, out_file=self.output_file)
            else:
                self.ptg2_em.screen['collectionid'] = collid

        if include_plan is not None:
            self.ptg2_em.screen['includeplan'] = include_plan

        return self.rtp_test_submit_screen()

    def execute_all(self, multithreading=None, multiple_pp=None):
        """
        Drives the RTPTEST Action option "6" Execute ALL.
        :param multithreading: "Multi Threading" option of "Y" or "N"
        :param multiple_pp:  Multi Threading with Multiple Plan/Packages option of "Y" or "N"
        :return: - True or False indicating success of job generation and/or automatic submission
        """

        CommonNav.nav_page_down(self.ptg2_em, out_file=self.output_file)
        self.ptg2_em.screen['actions'] = '6'
        if multithreading is not None:
            self.ptg2_em.screen['multithreading'] = multithreading
        if multiple_pp is not None:
            self.ptg2_em.screen['multipleplanpackages'] = multiple_pp
        return self.rtp_test_submit_screen()

    def execute_single(self, execute_options, multithreading=None):
        """
        Drives the RTPTEST Action option "7" Execute Programs(s).
        :param execute_options:  Execution options dictionary
        :param multithreading: "Multi Tasks" option of "Y" or "N"
        :return: - True or False indicating success of job generation and/or automatic submission
        """

        CommonNav.nav_page_down(self.ptg2_em, out_file=self.output_file)
        self.ptg2_em.screen['actions'] = '7'
        if multithreading is not None:
            self.ptg2_em.screen['multipletasks'] = multithreading

        # See what the connection_type parameter and set either CAF or RRSAF on the panel
        conn_type = execute_options['connection_type']
        if conn_type == 'R':
            self.ptg2_em.screen['rrsaf'] = 'S'
        else:
            self.ptg2_em.screen['caf'] = 'S'

        # Hit enter to get the next panel
        self.ptg2_em.app.ispf_submit()

        # Set the app
        for eoption, evalue in execute_options.items():
            if eoption == 'plan':
                self.fill_rtptest_field('PLAN', evalue)
            elif eoption == 'sqlid' and conn_type == 'R':
                self.fill_rtptest_field('SQLID', evalue)
            elif eoption == 'repeat' and conn_type == 'R':
                self.fill_rtptest_field('REPEAT', evalue)
            elif eoption == 'workstation' and conn_type == 'R':
                self.fill_rtptest_field('WORKSTATION', evalue)
            elif eoption == 'program':
                if len(evalue) > 8:
                    CommonNav.expand_and_fill_field(self.ptg2_em, 'program', evalue)
                else:
                    self.ptg2_em.screen['program'] = evalue
            elif eoption == 'corrid':
                if len(evalue) > 8:
                    CommonNav.expand_and_fill_field(self.ptg2_em, 'corrid', evalue)
                else:
                    self.ptg2_em.screen['corrid'] = evalue
            elif eoption == 'collid':
                if len(evalue) > 8:
                    CommonNav.expand_and_fill_field(self.ptg2_em, 'collid', evalue)
                else:
                    self.ptg2_em.screen['collid'] = evalue
            elif eoption == 'seed' and multithreading is not None:
                if len(evalue) > 8:
                    CommonNav.expand_and_fill_field(self.ptg2_em, 'seed', evalue)
                else:
                    self.ptg2_em.screen['seed'] = evalue
            else:
                continue

        return self.rtp_test_submit_screen()

    def free_all_programs(self, multiple_pp=None):
        """
        Drives the RTPTEST Action option "8" Free All Programs.
        :param multiple_pp:  Multi Plan/Package option of "Y" or "N"
        :return: - True or False indicating success of job generation and/or automatic submission
        """

        CommonNav.nav_page_down(self.ptg2_em, out_file=self.output_file)
        self.ptg2_em.screen['actions'] = '8'
        if multiple_pp is not None:
            self.ptg2_em.screen['multiplanpackage'] = multiple_pp
        return self.rtp_test_submit_screen()

    def free_single_program(self, program_name):
        """
        Drives the RTPTEST Action option "9" Free Single Program.
        :param program_name: (Required) - Name of the program to bind the package for.
        :return: - True or False indicating success of job generation and/or automatic submission
        """

        CommonNav.nav_page_down(self.ptg2_em, out_file=self.output_file)
        self.ptg2_em.screen['actions'] = '9'
        self.fill_rtptest_field('Free Single Package', program_name)
        return self.rtp_test_submit_screen()

    def cleanup(self):
        """
        Drives the RTPTEST Action option "10" Cleanup.

        :return: - True or False indicating success of job generation and/or automatic submission
        """

        CommonNav.nav_page_down(self.ptg2_em, out_file=self.output_file)
        # Cleanup action can't do auto submission so we will do it for it.
        if self.auto_submit == 'Y':
            self.ptg2_em.screen['autosubmit'] = 'N'
        self.ptg2_em.screen['actions'] = '10'
        if self.rtp_test_submit_screen():
            self.ptg2_em.screen['command'] = 'submit'
            if self.debug_mode == 'N':
                self.ptg2_em.app.ispf_submit()
            else:
                CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
            return True
        else:
            return False

    def rtp_test_submit_screen(self):
        """
        Common routine to submit and capture the current RTPTEST suite panel which generates and/or automatically
        submits the generated JCL job.
        :return: Successful - return tuple - True, list containing (jobname, jobid)
                 Unsuccessful - False
        """
        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        if self.debug_mode == 'N':
            self.ptg2_em.app.ispf_submit()
            self.ptg2_em.read_screen()
            if self.ptg2_em.screen.contains("SUBMITTED") or self.ptg2_em.app.ispf_panelid == 'ISREDDE2':
                submitted_job_list = str.split(str(self.ptg2_em.screen.lines[0]))
                submitted_job_list = str.split(str(submitted_job_list[2]), '(')
                submitted_job_list = [str.strip(item, ')') for item in submitted_job_list]
                return True, submitted_job_list
            else:
                CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
                return False
        else:
            return True, None

    def fill_rtptest_field(self, text_to_find, field_value):
        """
        Uses the CommonNav get_first_field method to find the input field object that occurs after some text and fill it
        in with the value supplied.
        :param text_to_find: Text to use to find the input field that occurs after it.
        :param field_value: Value to fill in the field with.
        :return: Will return if the field was found and the value filled in otherwise an exception is raised.
        """

        input_field = CommonNav.get_first_field(self.ptg2_em, text_before_input_field=text_to_find)
        input_field.fill(field_value)
