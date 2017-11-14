import collections

# Python 3 has moved izip to a global function named zip.
try:
    from itertools import izip
except ImportError:
    izip = zip
from itertools import islice
from ptg2.zos.emul import *
from ptg2.ca.db2tools import set_db2tools
from core.common import CommonNav
from core.Rtp_nav import NavRtp


class NavPsa(NavRtp):

    """
    Navigation Class that encapsulates moving around RTP products (PSA/PDT/PTT).
    """

    def __init__(self, u_lpar, u_ssid, userid, datastore_name=None, vcat=None, interval_date=None, interval_time=None,
                 debug_mode='N', output_file=None):
        NavRtp.__init__(self, u_lpar, u_ssid, userid, datastore_name, vcat, interval_date, interval_time, debug_mode, output_file)

        # Create instance of PTG2 emulator.
        self.start_emulator()

    # def start_psa(self, release_environment='R19'):
    def start_product(self, release_environment='R19'):
        """
        Drives to the Subsystem Analyzer main menu for a given release via the DB2 Tools Development Menu.

        :param release_environment: Specifies the runtime environment to enter Detector under. If none given defaults
                                    to R19.

                                    Specify any of the environments listing on the "DB2 Tools Development Menu",
                                    e.g. 'DV190', 'R18', 'R17', etc.

                                    Can also enter the product via the "Extended General Selection Menu" by specifying
                                    the name of an overriding parmlib dataset, e.g. 'SPEAN03.R19.PARMLIB'.
                                    If a suffix other than the default of '00' is needed provide it with the dataset
                                    name in parentheses like a PDS member, i.e 'SPEAN03.R19.PARMLIB(99)'.
        """
        set_db2tools(release_environment)
        self.ptg2_em.start_app('db2tools', db2tools_command='SA', db2tools_expect_panelid='PSAM0001')
        if self.output_file is None:
            CommonNav.nav_screen_capture(self.ptg2_em)
        else:
            CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)

    def product_main(self, change_ssid=False):
        """
        Returns back to the PSA main menu

        :param change_ssid: Indicates that the SSID on the PSA main menu should be changed using its class variable
                            u_ssid.
        """
        self.ptg2_em.app.db2tools_menu()
        self.ptg2_em.app.ispf_command('SA')
        if change_ssid:
            self.ptg2_em.screen['db2ssid'] = self.u_ssid
        if self.output_file is None:
            CommonNav.nav_screen_capture(self.ptg2_em)
        else:
            CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)

    def select_datastore(self):
        """
        Chooses the historical interval data display (option '2') and selects a datastore.

        First uses "ISPF find" commands to speed up the search by looking for the datastore name which will bring the
        row that contains the matching name into view in case it is on a lower display (i.e. page down needed). Then
        locates the vcat with a "find" command as well. If the datastore and vcat requested match then datastore is
        selected. Otherwise the datastore was not moved to the top cause it was on the first screen so traverse all the
        known rows looking for a match. If a match cannot be found an exception is thrown.

        :return: nothing
        """

        self.main_menu_option('2', 'PSAH0001')

        if self.debug_mode is not 'N':
            found_datastore_name = CommonNav.find_command(self.ptg2_em, self.datastore_name, 'PT019I',
                                                          log_find_command=True)
        else:
            found_datastore_name = CommonNav.find_command(self.ptg2_em, self.datastore_name, 'PT019I')

        if not found_datastore_name:
            CommonNav.nav_screen_capture(self.ptg2_em)
            raise ValueError("Datastore '%s' not found." % self.datastore_name)

        if self.debug_mode is not 'N':
            found_vcat = CommonNav.find_command(self.ptg2_em, self.vcat, 'PT019I', column_name='HIGHLEVEL',
                                                log_find_command=True)
        else:
            found_vcat = CommonNav.find_command(self.ptg2_em, self.vcat, 'PT019I', column_name='HIGHLEVEL')

        # if after find command no matching vcat(i.e. Highlevel) found then raise exception
        if not found_vcat:
            CommonNav.nav_screen_capture(self.ptg2_em)
            raise ValueError("No VCAT - %s, found for datastore - %s" % (self.vcat, self.datastore_name))

        # if vcat and datastore name found, get the PTG2 :py:class Field object located on that display row.
        datastore_field_obj_found = self.ptg2_em.screen.field_before(text=self.vcat)

        # Access the field object variable 'following_text' which should contain the entire data row and split on
        # spaces into a list of column data. In which the first element in the list should be the datastore. Check the
        # name to ensure that it matches the users datastore name. This ensures that the vcat and datastore name
        # match each other in the event that the find commands above do not filter out duplicate datastores being
        # moved off the screen.

        while True:
            datastore_data_list = str.split(str(datastore_field_obj_found.following_text))
            if datastore_data_list[0] != self.datastore_name or datastore_data_list[4] != self.vcat:
                datastore_field_obj_found = datastore_field_obj_found.next()
                if datastore_field_obj_found is None:
                    raise EmulatorException("VCAT and Datastore name '%s-%s' not found." %
                                            (self.vcat, self.datastore_name))
            else:
                break

        self.ptg2_em.screen[datastore_field_obj_found.id] = 'S'
        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        self.ptg2_em.app.ispf_submit()

    def select_interval(self, interval_date_override=None, interval_time_override=None, v_type=None, interval_date_2=None, interval_time_2=None):
        """
        Chooses an interval from Interval Summary Display by using find commands to locate the date first then the
        time. Then uses the PTG2 :py:class Screen method field_before to locate the field object (i.e. "_") next to the
        matching date and time. First verifying that the data and time matches by accessing the field object variable
        "following_text" to split and check the first two strings then if verified selects ("S") on that field object
        and submits the panel.

        :param interval_date_override: Combined with the interval_time_override, overrides the use of the :py:class 'NavPdt' instance
                              variable by specifying a date in the format expected by the products
                              "Interval Summary Display". (e.g. YY/MM/DD)
        :param interval_time_override: Combined with the interval_date_override, overrides the use of the :py:class 'NavPdt' instance
                              variable by specifying a time in the format expected by the products
                              "Interval Summary Display". (e.g. HH:MM:SS)
        :param interval_date_2: If provided along with interval_time_2 parameter will select a second interval to
                                provide range interval selection.

        :param interval_time_2: If provided along with interval_date_2 parameter will select a second interval to
                                provide range interval selection.

        :param v_type:  Optional, but if set will change interval Summary by the "View Type" request before selecting
                        the interval(s) requested.
        :return: Nothing
        """

        panel_id_dict = {'O': 'PSAL0202', 'V': 'PSAV0201', 'W': 'PSAS0205'}
        altered_view_type_path = False

        # if user provided override for view type then set that before selecting screen. Interrogate the v_type
        # parameter and transform it to 1 of the three options specified in the panel_id_dict above. This is due to
        # PSA has more than three View Types once you get past the interval summary display but only supports 3 on that
        # display. Otherwise get current value of "View Type =>" on the interval summary display
        if v_type:
            copy_of_v_type = v_type
            if v_type == 'B':
                v_type = 'O'
                altered_view_type_path = True
            elif v_type == 'A':
                v_type = 'V'
                altered_view_type_path = True
            elif v_type == 'S':
                v_type = 'W'
                altered_view_type_path = True

            self.psa_view_type(v_type)
        else:
            v_type = self.ptg2_em.screen['viewtype']  # set v_type to the current value on the screen

        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)

        # if both the interval date and time overrides have been provided set the local variables to those data.
        if interval_date_override is not None and interval_time_override is not None:
            use_interval_date = interval_date_override
            use_interval_time = interval_time_override
        # if interval date override provided but not time raise an exception
        elif interval_date_override is not None and interval_time_override is None:
            raise ValueError("Parameter interval_date also requires interval_time to be provided")
        # if interval time override provided but not date raise an exception
        elif interval_date_override is None and interval_time_override is not None:
            raise ValueError("Parameter interval_time also requires interval_date to be provided")
        # else no overrides provided so set local variables to :py:class NavPdt class variables.
        else:
            use_interval_date = self.interval_date
            use_interval_time = self.interval_time

        if interval_date_2 is not None and interval_time_2 is None:
            raise ValueError("Parameter interval_date_2 also requires interval_time_2 to be provided")
        elif interval_date_2 is None and interval_time_2 is not None:
            raise ValueError("Parameter interval_time_2 also requires interval_date_2 to be provided")

        if interval_date_2 is None:
            interval_selection_order = [use_interval_date, use_interval_time]
        else:
            if self.interval_date > interval_date_2:
                interval_1_greater_interval_2 = True
            elif self.interval_date < interval_date_2:
                interval_1_greater_interval_2 = False
            else:
                if self.interval_time > interval_time_2:
                    interval_1_greater_interval_2 = True
                else:
                    interval_1_greater_interval_2 = False

            if interval_1_greater_interval_2:
                interval_selection_order = [self.interval_date, self.interval_time, interval_date_2, interval_time_2]
            else:
                interval_selection_order = [interval_date_2, interval_time_2, self.interval_date, self.interval_time]

        for interval_date, interval_time in izip(interval_selection_order, islice(interval_selection_order, 1, None)):
            if ':' not in interval_date:
                if interval_date != "1":
                    # Create "find" command with the interval date provided and if :py:class NavPdt class variable debug is
                    # turned on then capture the screen with said command on the command line, issue the find command and if
                    # debug mode activated capture screen positioned to found interval date.
                    if self.debug_mode is not 'N':
                        find_rc = CommonNav.find_command(self.ptg2_em, interval_date, 'PT019I', log_find_command=True)
                    else:
                        find_rc = CommonNav.find_command(self.ptg2_em, interval_date, 'PT019I')

                    # if after find command no interval date found then raise exception
                    if not find_rc:
                        raise Exception("Interval date %s not found." % interval_date)

                    # Create "find" command with the interval time provided specifying the "Time" column. If :py:class NavPdt
                    # class variable debug is turned on then capture the screen with said command on the command line, issue the
                    # find command and if debug mode activated capture screen positioned to found interval time.
                    if self.debug_mode is not 'N':
                        find_rc = CommonNav.find_command(self.ptg2_em, interval_time, 'PT019I', column_name='Time',
                                                         log_find_command=True)
                    else:
                        find_rc = CommonNav.find_command(self.ptg2_em, interval_time, 'PT019I', column_name='Time')

                    # if after find command no interval time found then raise exception
                    if not find_rc:
                        raise Exception("No interval time of, %s, found for interval date - %s" %
                                        (interval_time, interval_date))

                    # if date and time found, get the PTG2 :py:class Field object located on that display row.
                    interval_field_obj_found = self.ptg2_em.screen.field_before(text=interval_time)

                    # Access the field object variable 'following_text' which should contain the entire data row and split on
                    # spaces into a list of column data. In which the first two elements in the list should be the date and
                    # time. Check the date to ensure that it matches the users interval date. This ensures that the date and
                    # time match each other in the event that the find commands above do not filter out a time value for a more
                    # recent date being moved off the screen.

                    interval_data_list = str.split(str(interval_field_obj_found.following_text))
                    if interval_data_list[0] != interval_date:
                        raise EmulatorException("Interval date:time '%s-%s' not found." %
                                                (interval_date, interval_time))
                else:
                    interval_field_obj_found = self.get_first_field(text_before_input_field='-View Interval(s)')
                    interval_data_list = str.split(str(interval_field_obj_found.following_text))
                    self.interval_date = interval_data_list[0]  # override :py:class NavPdt variable interval_date of 1
                    self.interval_time = interval_data_list[1]  # override :py:class NavPdt variable interval_time

                self.ptg2_em.screen[interval_field_obj_found.id] = 'S'
                CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
            else:
                continue

        self.ptg2_em.app.ispf_submit(expect_panelid=panel_id_dict[v_type])
        # If we had to alter the "View Type ==>" used for the interval summary display then we need change the view type
        # to what the user original requested.
        if altered_view_type_path:
            self.psa_view_type(copy_of_v_type)

        # If current interval selection code is not reliable then resurrect the while loop below. Also JSON input
        # will have to change back to a single interval input parameters specified via the PTG2 field id(160627-1)
        # while not self.find_field(self.interval):
        #     if CommonNav.nav_page_down(self.ptg2_em):
        #         continue
        #     else:
        #         break

    def psa_terminate_collection(self):
        """
        Stops a PSA collection using PSA option 5 (Terminate SSID collection) panel)
        :return: True - collection termination request successfully processed.
                 False - termination request unsuccessful due to collection not active.
        """
        self.product_main()  # make sure we start at the PSA main menu

        try:
            self.main_menu_option('5', 'PSAC0002')
        except EmulatorAppException:
            if self.output_file is None:
                CommonNav.nav_screen_capture(self.ptg2_em)
            else:
                CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
            return False
        else:
            if self.output_file is None:
                CommonNav.nav_screen_capture(self.ptg2_em)
            else:
                CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)

        try:
            self.ptg2_em.app.ispf_submit()
            if self.ptg2_em.app.ispf_message == 'SA016 SA016I: Termination request successfully issued':
                return True
            elif self.ptg2_em.app.ispf_message == 'SA017 SA017I: Collection not active for DB2=DB0G':
                return True
            else:
                return False
        except EmulatorAppException:
            print('%s' % self.ptg2_em.app.ispf_message)
            return False

    def psa_view_type(self, type_request):
        """
        Changes the display by the "View Type" option requested.

        :param type_request: valid view type characters A, X, and E
        :return: Raises ValueError if type_request not a valid option.
        """
        list_o_types = ['O', 'V', 'B', 'A', 'S', 'W']
        panel_id_dict = {'B': 'PSAS0221', 'A': 'PSAL0240'}

        if type_request not in list_o_types:
            CommonNav.nav_screen_capture(self.ptg2_em)
            raise ValueError('View Type of %s is not a valid option' % type_request)
        else:
            self.ptg2_em.screen['viewtype'] = type_request
            if type_request == 'O' or type_request == 'V' or type_request == 'W':
                self.ptg2_em.app.ispf_submit()
            else:
                self.ptg2_em.app.ispf_submit(expect_panelid=panel_id_dict[type_request])
            if self.output_file is None:
                CommonNav.nav_screen_capture(self.ptg2_em)
            else:
                CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        if len(self.ptg2_em.screen.messages) != 0:
            return True
        else:
            return False

    def psa_view_option(self, option_request):
        """
        Changes the display by the "View Optn" requested.

        :param option_request: valid view option characters A, B, and C
        :return: Raises ValueError if type_request not a valid option.
        """
        list_o_types = ['A', 'B', 'C']
        panel_id_dict = {'A': 'PSAL0285', 'B': 'PSAL0287', 'C': 'PSAL0288'}

        if option_request not in list_o_types:
            CommonNav.nav_screen_capture(self.ptg2_em)
            raise ValueError("View Option of '%s' is not a valid option" % option_request)
        else:
            self.ptg2_em.screen['viewoptn'] = option_request
            self.ptg2_em.app.ispf_submit(expect_panelid=panel_id_dict[option_request])
            CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        if len(self.ptg2_em.screen.messages) != 0:
            return True
        else:
            return False

    def view_by(self, display_request):
        """
        Changes the display by the "View By" or "View Option" requested.

        :param display_request: valid view by/view option characters
        :return:
        """
        if self.ptg2_em.screen.contains('SS Analyzer Database Activity Display', case_sensitive=True):
            self.ptg2_em.screen['viewby'] = display_request
        else:
            self.ptg2_em.screen['viewoption'] = display_request

        self.ptg2_em.app.ispf_submit()
        if self.output_file is None:
            if self.debug_mode == 'N':
                CommonNav.nav_screen_capture(self.ptg2_em)
            else:
                CommonNav.nav_screen_capture(self.ptg2_em, display_fields=True)
        else:
            if self.debug_mode == 'N':
                CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
            else:
                CommonNav.nav_screen_capture(self.ptg2_em, display_fields=True, file_name=self.output_file)
        if len(self.ptg2_em.screen.messages) != 0:
            raise ValueError("View By '%s' is invalid for View Type '%s'" % (display_request, self.ptg2_em.screen['viewtype']))

    def psa_main_menu_option(self, option, panelid):
        """
        Execute a PSA main menu option.
        :param option:
        :param panelid:
        :return:
        """
        self.ptg2_em.app.ispf_command(option, expect_panelid=panelid)

    def start_collection(self, options):
        """
        Start a PSA collection
        :param options: Collection start options dictionary.
        :return: boolean True if collection was started, False if the start has failed.
        """
        self.product_main()
        self.main_menu_option('4', 'PSAC0001')

        super(NavPsa, self).start_collection(options)
        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        # Try to Navigate to the second PSA collection startup panel
        self.ptg2_em.app.ispf_submit(expect_panelid='PSAC0006')
        # Second collection startup panel options

        col_opts2 = collections.OrderedDict([('Volume and Extent', 'vol_ext'), ('Sampling Rate', 'samp')])

        for option, name in col_opts2.items():
            if option == 'Volume and Extent':
                field, value = self.get_collection_option_value(option, name, 'Y', options)
                field.fill(value)
            elif option == 'Sampling Rate':
                field, value = self.get_collection_option_value(option, name, '100', options)
                field.fill(value)

        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        msg = 'SA011 SA011I: Collection init successful for DB2=%s' % self.u_ssid.upper()
        # Start the collection
        if self.debug_mode != 'Y':
            self.ptg2_em.app.ispf_submit(expect_message=msg)
            CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
            # Wait for 5 seconds
            time.sleep(5)
        # Return to the PSA Main Menu
        self.product_main()
        return True

    def get_collection_option_value(self, option, name, default, options=None):
        """
        Sets a collection options value on the panel.
        :param option:
        :param name:
        :param default:
        :param options:
        :return:
        """
        field = CommonNav.get_first_field(self.ptg2_em, text_before_input_field=option)
        value = ''
        if options is not None:
            value = options.get(name)

        if value is not None:
            return field, value
        else:
            return field, default

    def build_collection_init_term_messages(self, message_type="init", m_user=None, m_ssid=None):
        """
        Returns as a tuple the collection init or collection terminate in progress and complete messages as strings.
        
        i.e. (PDT0100 DETECTOR COLLECTION INIT IN PROGRESS DB2=D11B USER=SPEAN03, PDT0101 DETECTOR COLLECTION INIT COMPLETE FOR DB2=D11B COUNT=0001)
        
        :param message_type: indicates whether initialization or termination messages are built. Defaults to initialization.
        :param m_user: If provided the user id to be used in the USER= parameter of the message string otherwise 
                        class instance variable will be used
        :param m_ssid: If provided the DB2 SSID string that will be used in the DB2= parameter of the message string 
                        otherwise the class instance variable will be used.
        :return: both strings as a tuple (init in prograss, init complete)
        """

        message_user = self.userid.upper()
        message_ssid = self.u_ssid.upper()

        if m_user is not None:
            message_user = m_user.upper()
        if m_ssid is not None:
            message_ssid = m_ssid.upper()

        if message_type == 'init':
            in_progress = "PSA0100 SSANALZE COLLECTION INIT IN PROGRESS DB2=%s USER=%s" % \
                          (message_ssid, message_user)
            complete = "PSA0101 SSANALZE COLLECTION INIT COMPLETE FOR DB2=%s" % message_ssid
        else:
            in_progress = "PSA0103 SSANALZE COLLECTION TERM IN PROGRESS FOR DB2=%s USER=%s" % \
                          (message_ssid, message_user)
            complete = "PSA0104 SSANALZE COLLECTION TERM COMPLETE FOR DB2=%s" % message_ssid

        return str(in_progress), str(complete)


    def test_meth(self, parm2):

        som = 5
        test =2
        return -1




