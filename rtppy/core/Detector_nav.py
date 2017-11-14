import collections
from itertools import islice

# Python 3 has moved izip to a global function named zip.
try:
    from itertools import izip
except ImportError:
    izip = zip

from ptg2.zos.emul import *
from ptg2.ca.db2tools import set_db2tools
from ptg2.zos.emul_apps import EmulatorAppException
from core.common import CommonNav
from core.Rtp_nav import NavRtp


class NavPdt(NavRtp):
    """
    Navigation Class that encapsulates moving around PDT specifically.
    """

    def __init__(self, u_lpar, u_ssid, userid, datastore_name=None, vcat=None, interval_date=None, interval_time=None,
                 debug_mode='N', output_file=None):
        NavRtp.__init__(self, u_lpar, u_ssid, userid, datastore_name, vcat, interval_date, interval_time, debug_mode, output_file)

        # Create instance of PTG2 emulator.
        self.start_emulator()
        self.select_interval_panel_dict = {'A': 'PDTO0030', 'X': 'PDTY0030', 'E': 'PDTS0040'}
        self.panel_id_dict = {'A': 'PDTO0012', 'X': 'PDTY0012', 'E': 'PDTS0021'}
        self.current_panel_id_dict = {'A': 'PDTO0033', 'X': 'PDTY0002', 'E': 'PDTS0003'}

    # def start_pdt(self, release_environment='R19'):
    def start_product(self, release_environment):
        """
        Drives to the Detector main menu for a given release via the DB2 Tools Development Menu.

        :param release_environment: Specifies the runtime environment to enter Detector under.

                                    Specify any of the environments listing on the "DB2 Tools Development Menu",
                                    e.g. 'DV190', 'R18', 'R17', etc.

                                    Can also enter the product via the "Extended General Selection Menu" by specifying
                                    the name of an overriding parmlib dataset, e.g. 'SPEAN03.R19.PARMLIB'.
                                    If a suffix other than the default of '00' is needed provide it with the dataset
                                    name in parentheses like a PDS member, i.e 'SPEAN03.R19.PARMLIB(99)'.
        """
        set_db2tools(release_environment)
        self.ptg2_em.start_app('db2tools', db2tools_command='DT', db2tools_expect_panelid='PDTM0001')
        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)

    def product_main(self, change_ssid=False):
        """
        Returns back to the PDT main menu

        :param change_ssid: Indicates that the SSID on the PDT main menu should be changed using its class variable
                            u_ssid.
        """
        # if not super(NavPdt, self).product_main():
        self.ptg2_em.app.db2tools_menu()
        self.ptg2_em.app.ispf_command('DT')
        if change_ssid:
            self.ptg2_em.screen['db2ssid'] = self.u_ssid
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

        self.main_menu_option('2', 'PDTD0012')

        if self.debug_mode is not 'N':
            found_datastore_name = CommonNav.find_command(self.ptg2_em, self.datastore_name, 'PT019I',
                                                          log_find_command=True)
        else:
            found_datastore_name = CommonNav.find_command(self.ptg2_em, self.datastore_name, 'PT019I')

        if not found_datastore_name:
            CommonNav.nav_screen_capture(self.ptg2_em)
            raise ValueError("Datastore '%s' not found." % self.datastore_name)

        if self.debug_mode is not 'N':
            found_vcat = CommonNav.find_command(self.ptg2_em, self.vcat, 'PT019I', column_name='VCAT',
                                                log_find_command=True)
        else:
            found_vcat = CommonNav.find_command(self.ptg2_em, self.vcat, 'PT019I', column_name='VCAT')

        # if after find command no matching vcat found then raise exception
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
            if '*ACTIVE*' in str(datastore_field_obj_found.following_text):
                vcat_index = 4
            else:
                vcat_index = 5
            if datastore_data_list[0] != self.datastore_name or datastore_data_list[vcat_index] != self.vcat:
                datastore_field_obj_found = datastore_field_obj_found.next()
                if datastore_field_obj_found is None:
                    raise EmulatorException("VCAT and Datastore name '%s-%s' not found." %
                                            (self.vcat, self.datastore_name))
            else:
                break

        self.ptg2_em.screen[datastore_field_obj_found.id] = 'S'
        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        self.ptg2_em.app.ispf_submit()
        if len(self.ptg2_em.screen.messages) != 0:
            raise EmulatorException(screen=self.ptg2_em.screen)

    def select_interval(self, interval_date_override=None, interval_time_override=None, v_type=None, interval_date_2=None, interval_time_2=None):
        """
        Chooses an interval or a range of intervals from the Interval Summary Display by using find commands to locate
        the date first then the time. Then uses the PTG2 :py:class Screen method field_before to locate the field object
        (i.e. "_") next to the matching date and time. First verifying that the data and time matches by accessing the
        field object variable "following_text" to split and check the first two strings then if verified selects ("S")
        on that field object and submits the panel.

        :param interval_date_override: Combined with the interval_time, overrides the use of the :py:class 'NavPdt'
                                       instance variable by specifying a date in the format expected by the products
                                       "Interval Summary Display". (e.g. YY/MM/DD)

        :param interval_time_override: Combined with the interval_date, overrides the use of the :py:class 'NavPdt'
                                       instance variable by specifying a time in the format expected by the products
                                       "Interval Summary Display". (e.g. HH:MM:SS)

        :param interval_date_2: If provided along with interval_time_2 parameter will select a second interval to
                                provide range interval selection.

        :param interval_time_2: If provided along with interval_date_2 parameter will select a second interval to
                                provide range interval selection.

        :param v_type:  Optional, but if set will change interval Summary by the "View Type" request before selecting
                        the interval(s) requested.
        :return: Nothing
        """

        # if user provided override for view type then set that before selecting screen. Otherwise get current value of
        # View Type =>
        if v_type:
            self.pdt_view_type(v_type, come_from_select_interval=True)
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

        self.ptg2_em.app.ispf_submit(expect_panelid=self.panel_id_dict[v_type])

        # If current interval selection code is not reliable then resurrect the while loop below. Also JSON input
        # will have to change back to a single interval input parameters specified via the PTG2 field id(160627-1)
        # while not self.find_field(self.interval):
        #     if CommonNav.nav_page_down(self.ptg2_em):
        #         continue
        #     else:
        #         break

    def pdt_terminate_collection(self):
        """
        Stops a PDT collection using PDT option 6 (Terminate SSID collection) panel)
        :return: True - collection termination request successfully processed.
                 False - termination request unsuccessful due to collection not active.
        """
        self.product_main()  # make sure we start at the PDT main menu

        try:
            self.main_menu_option('6', 'PDTD0001')  # Select option 6
            # self.ptg2_em.app.ispf_command('6', expect_panelid='PDTD0001')  # Select option 6
        except EmulatorAppException:
            CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
            return False
        else:
            CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)

        try:
            self.ptg2_em.app.ispf_submit(expect_message='DT204 DT204I: Stop request has been successfully processed')
        except EmulatorAppException:
            print('%s' % self.ptg2_em.app.ispf_message)
            return False
        else:
            return True

    def pdt_view_type(self, type_request, current_interval=False, come_from_select_interval=False):
        """
        Changes the display by the "View Type" option requested.

        :param type_request: valid view type characters A, X, and E
        :param current_interval: Indicates whether the current emulator instance is in the product current interval or
                                 historical interval displays.
        :param come_from_select_interval: Indicates if this method is being called by the select_interval method.
        :return: Raises ValueError if type_request not a valid option.
        """
        if type_request != 'A' and type_request != 'X' and type_request != 'E':
            raise ValueError('View Type of %s is not a valid option' % type_request)
        else:
            self.ptg2_em.screen['viewtype'] = type_request
            if current_interval:
                self.ptg2_em.app.ispf_submit(expect_panelid=self.current_panel_id_dict[type_request])
            elif come_from_select_interval:
                self.ptg2_em.app.ispf_submit(expect_panelid=self.select_interval_panel_dict[type_request])
            else:
                self.ptg2_em.app.ispf_submit(expect_panelid=self.panel_id_dict[type_request])
            CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)

    def view_by(self, display_request):
        """
        Changes the display by the "View By" option requested.

        :param display_request: valid view by character P, G, S, Q, F, or K
        :return:
        """
        self.ptg2_em.screen['viewby'] = display_request
        self.ptg2_em.app.ispf_submit()
        if self.debug_mode == 'N':
            CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        else:
            CommonNav.nav_screen_capture(self.ptg2_em, display_fields=True, file_name=self.output_file)

    def view_key(self, key_request):
        """
        Calls the super method in RtpNav to change the Key option.
        :param key_request: valid key character U, R, C, N, D, I, X, or W
        :return:
        """

        return super(NavPdt, self).view_key(key_request)

    def start_collection(self, collection_options):
        """
        Start a PDT collection
        :param collection_options: Collection start options dictionary.
        :return: boolean True if collection was started, False if the start has failed.
        """
        self.product_main()
        self.main_menu_option('5', 'PDTC0001')

        # Fill out the first PDT collection startup panel
        super(NavPdt, self).start_collection(collection_options)
        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        # Try to navigate to the second panel.
        self.ptg2_em.app.ispf_submit(expect_panelid='PDTC0002')
        # Second collection startup panel options
        col_opts2 = collections.OrderedDict([('Triggered SQL', 'trig_sql'), ('Plan Excl/Incl List', 'exclude_list'),
                                             ('Standard Activity', 'standard'), ('Dynamic SQL Stats', 'dynam_stats'),
                                             ('View By Keys', 'view_keys'), ('Dynamic Exceptions', 'dynam_excp'),
                                             ('Static Exceptions', 'static_excp'), ('SQL Errors', 'sql_errors'),
                                             ('SQL Error Text', 'error_text'), ('Host variables', 'host_vars'),
                                             ('Collection Profile', 'collection_profile'), ('Exception cache', 'excp_cache')])

        for option_text, key in col_opts2.items():
            if option_text == 'Collection Profile':
                field, value = self.get_collection_option_value(option_text, key, ' ', collection_options)
                field.fill(value)
            elif option_text == 'Exception cache':
                field, value = self.get_collection_option_value(option_text, key, '0000', collection_options)
                field.fill(value)
            else:
                field, value = self.get_collection_option_value(option_text, key, 'N', collection_options)
                field.fill(value)

        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)

        success_msg = 'DT202 DT202I: Start request has been successfully processed'

        # Start the collection if debug mode not turned on
        if self.debug_mode != 'Y':
            self.ptg2_em.app.ispf_submit(expect_message=success_msg)
            CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
            # Wait for 5 seconds to ensure collections is started
            time.sleep(5)
        # Return to product main menu
        self.product_main()
        return True

    def build_collection_init_term_messages(self, message_type="init", m_user=None, m_ssid=None):
        """
        Returns as a tuple the collection init or collection terminate in progress and complete messages as strings.
        
        i.e. (PDT0100 DETECTOR COLLECTION INIT IN PROGRESS DB2=D11B USER=SPEAN03, PDT0101 DETECTOR COLLECTION INIT COMPLETE FOR DB2=D11B COUNT=0001)
        
        :param message_type: indicates whether initialization or termination messages are built. Defaults to initialization.
        :param m_user: If provided the user id to be used in the USER= parameter of the message string otherwise 
                        class instance variable will be used
        :param m_ssid: If provided the DB2 SSID string that will be used in the DB2= parameter of the message string 
                        otherwise the class instance variable will be used.
        :return: both strings as a tuple (init in progress, init complete)
        """

        message_user = self.userid.upper()
        message_ssid = self.u_ssid.upper()

        if m_user is not None:
            message_user = m_user.upper()
        if m_ssid is not None:
            message_ssid = m_ssid.upper()

        if message_type == 'init':
            in_progress = "PDT0100 DETECTOR COLLECTION INIT IN PROGRESS DB2=%s USER=%s" % (message_ssid, message_user)
            complete = "PDT0101 DETECTOR COLLECTION INIT COMPLETE FOR DB2=%s" % message_ssid
        else:
            in_progress = "PDT0102 DETECTOR TERM IN PROGRESS FOR DB2=%s USER=%s" % (message_ssid, message_user)
            complete = "PDT0103 DETECTOR TERM COMPLETE FOR DB2=%s" % message_ssid

        return str(in_progress), str(complete)

    def get_sql_text(self):
        """

        :return:
        """

        last_row_with_text = 0
        num_pages_to_bottom_of_text = 0
        if self.ptg2_em.app.ispf_panelid != 'PDTQ0010':
            text_row = 12
            text_col = 2
        else:
            text_row = 9
            text_col = 2
        overall_sql_text = ''
        while True:
            if not self.ptg2_em.screen.contains('BOTTOM OF DATA', case_sensitive=True):
                last_row_with_text = self.ptg2_em.screen.last_line_num - 2
                num_pages_to_bottom_of_text += 1
            if not CommonNav.nav_page_down(self.ptg2_em, log_screen=self.screen_log, out_file=self.output_file):
                break
        if num_pages_to_bottom_of_text != 0:
            CommonNav.nav_max_up(self.ptg2_em, log_screen=self.screen_log, out_file=self.output_file)
            bottom_display_row = last_row_with_text
        else:
            (bottom_display_row, bottom_display_column) = self.ptg2_em.screen.find('BOTTOM OF DATA', case_sensitive=True)

        while True:
            for row_of_text in range(text_row, bottom_display_row + 1):
                # Get the row of SQL text
                part_of_text = self.ptg2_em.string_get(row_of_text, text_col, self.screenLen - 1)
                # Strip leading and trailing blanks
                part_of_text = part_of_text.strip()
                # Add this piece into the overall SQL text string with a space between as long as it is not "BOTTOM OF DATA"
                if "BOTTOM OF DATA" not in part_of_text:
                    overall_sql_text += part_of_text + ' '
            if not CommonNav.nav_page_down(self.ptg2_em, out_file=self.output_file):
                break

        return overall_sql_text.strip()
