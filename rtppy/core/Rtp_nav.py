import collections

# PTG2 needed Imports
from ptg2.context import set_system, set_userid
from ptg2.zos.db2 import set_ssid_address
from ptg2.zos.emul import *
from ptg2.ca.db2tools import set_db2tools
from core.InputParms import InputParms
from ptg2.zos.emul_apps import EmulatorAppException

# RTPPY needed imports
from core.Results import Results
from core.RTP_primary_keys import RtpPrimaryKeys
from core.common import CommonNav


class NavRtp(object):

    """
    Navigation Class that encapsulates moving around RTP products (PSA/PDT/PTT).
    """

    def __init__(self, u_lpar, u_ssid, userid, datastore_name=None, vcat=None, interval_date=None, interval_time=None,
                 debug_mode='N', output_file=None):
        self.ptg2_em = None
        self.u_lpar = u_lpar
        self.u_ssid = u_ssid
        self.userid = userid
        self.datastore_name = datastore_name
        self.vcat = vcat
        self.interval_date = interval_date
        self.interval_time = interval_time
        self.screenLen = None
        self.col_name_line = None
        self.persist_column = None
        self.debug_mode = debug_mode
        self.output_file = output_file
        if self.debug_mode == 'Y':
            self.screen_log = True
        else:
            self.screen_log = False
        self.message_container = None

        # Create instance of PTG2 emulator.
        self.start_emulator()

    def start_emulator(self):
        """
        Uses the PTG2 :py:class: 'Emulator' to log on as the user and connect to the specified LPAR. Then sets the
        class variable screen length.

         For more information on the Emulator see the documentation for PTG2
        """
        set_system(self.u_lpar)
        set_userid(self.userid)
        set_ssid_address(self.u_ssid + "@" + self.u_lpar)  # Set which DB2 SSID we will use as a default.
        self.ptg2_em = get_emulator()
        self.screenLen = self.ptg2_em.screen.columns

    def stop_emulator(self):
        """
        Uses the PTG2 :py:class: 'Emulator' to logoff the user and disconnect from the specified LPAR.

         For more information on the Emulator see the documentation for PTG2
        """
        self.ptg2_em.terminate()

    def select_row(self, row_identifier, line_command='S', additional_column_name=None, additional_row_identifier=None,
                   for_product=None):
        """
        Selects a specific row, using the line command requested, in a dynamic data area for any display by the value in
        the first column. An additional column name and value can be provided to identify a row.
        Can override the default line command used by providing a valid line command option.(e.g. 'D', 'Q', 'K', etc.)


        Example:

        Detector Program Display:

              PROGRAM   UNACC_TIME   TYPE SQL        TIMEPCT CPUPCT  INDB2_TIME
              --------  ------------ ---- ---------- ------- ------- ------------
            _ SP#SP3C   00:00.000240 PKGE         15    .00%    .00% 00:00.001615

        :param row_identifier: value that identifies the row to use the line_command on.
        :param line_command: single line command character.
        :param additional_column_name: name of an additional column to use the value to identify the row to select
        :param additional_row_identifier: The value for the additional column parameter.
        :param for_product: 3 character product_code (i.e. PSA). Only required for PSA tests. Not used right now.
        :param message_container: (Optional) If not None is the name of an Ordered Dictionary variable in which any ISPF
                                    panel messages that prevent selecting the row will be returned in. The ordered
                                    dictionary will have the same format as the ptg2 messages dictionary.
                                    See method messages() in ptg2 Py class: Screen in emul.py file.
        :return True - a valid line command character was requested and the emulator instance has been updated with the
                       next display.
                False - raises a ValueError exception if a line command character was requested that is not a valid
                        option. The emulator instance is updated with the display with the products error message on the
                        display.
        """

        id_found = False
        row_identifier = row_identifier.upper()
        if additional_row_identifier is not None:
            additional_row_identifier = additional_row_identifier.upper()

        if additional_column_name is not None and additional_row_identifier is None or additional_column_name is None \
                and additional_row_identifier is not None:
            raise TypeError("Both parameters additional_column_name and additional_row_identifier must be provided"
                            " in order to select a row.")
        else:
            # Make sure we start the search from the top
            CommonNav.nav_max_up(self.ptg2_em, log_screen=self.screen_log, out_file=self.output_file)

            """
            If an additional column has been provided check to see if is already on the current screen. If not then
            do a freeze command to bring it up as the second column. If we can't then return False.
            """
            if additional_column_name is not None:
                if not CommonNav.nav_freeze_unfreeze_column(self.ptg2_em, additional_column_name, command='freeze'):
                    return False
            """
            Find the first dynamic display row and traverse every row until a match of the primary and/or the additional
            columns and values is found and set the found flag.
            """
            while True:
                field_obj = self.get_first_field(text_before_input_field='Interval Date =>')
                number_display_rows = self.num_display_rows()
                for i in range(0, number_display_rows):
                    # get the display row and remove any leading, trailing, and multiple spaces between the data.
                    display_row_text = " ".join(str(field_obj.following_text).split())
                    display_row_text_list = display_row_text.split(' ', 11)
                    if additional_column_name is not None:
                        if display_row_text_list[0] == row_identifier and display_row_text_list[1] == additional_row_identifier:
                            id_found = True
                        else:
                            field_obj = field_obj.next()
                    else:
                        if ' ' in row_identifier:
                            joined_display_text = display_row_text_list[0] + ' ' + display_row_text_list[1]
                            if joined_display_text != row_identifier:
                                field_obj = field_obj.next()
                            else:
                                id_found = True
                        else:
                            use_index = 0
                            # if for_product == 'PSA':
                            #     use_index = 1
                            # else:
                            #     use_index = 0

                            if display_row_text_list[use_index] != row_identifier:
                                field_obj = field_obj.next()
                            else:
                                id_found = True
                    """
                    When a match is found select the row using the line_command and capture the screen
                    """
                    if id_found:
                        self.ptg2_em.screen[field_obj.id] = line_command
                        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)

                        # TODO: Temporary code to throw a more correct exception since PDT does not go to Plan display
                        # TODO: for connection type Key value of *NULL*
                        if row_identifier == '*NULL*' and line_command == 'P' and self.ptg2_em.screen.contains('Key ==> C', case_sensitive=True):
                            try:
                                self.ptg2_em.app.ispf_submit(expect_panelid='PDTV0012')
                            except EmulatorAppException as e:
                                print(e)
                                return False
                        else:
                            self.ptg2_em.app.ispf_submit()

                        CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
                        if len(self.ptg2_em.screen.messages) == 0:
                            return True
                        else:
                            self.message_container = self.ptg2_em.screen.messages
                            if additional_column_name is not None:
                                if not CommonNav.nav_freeze_unfreeze_column(self.ptg2_em, additional_column_name, command='unfreeze'):
                                    CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
                            return False

                if not CommonNav.nav_page_down(self.ptg2_em, log_screen=self.screen_log, out_file=self.output_file):
                    break
            # If an additional column name was provided but we couldn't find a match in all the display rows we need to
            # unfreeze the column to put the display back before we return.
            if additional_column_name is not None:
                CommonNav.nav_freeze_unfreeze_column(self.ptg2_em, additional_column_name, command='unfreeze')

        return False

    def view_key(self, key_request):
        """
        Change the "Key Summary Display" via the "Key" field by the option requested.
        :param key_request: valid key character U, R, C, N, D, I, X, or W
        :return:
        """

        self.ptg2_em.screen['key'] = key_request
        self.ptg2_em.app.ispf_submit()
        if self.debug_mode == 'N':
            CommonNav.nav_screen_capture(self.ptg2_em, file_name=self.output_file)
        else:
            CommonNav.nav_screen_capture(self.ptg2_em, display_fields=True, file_name=self.output_file)
        if 'DT665E' in self.ptg2_em.screen.messages:
            return False
        else:
            return True

    def calc_page_down(self, lines_per_page):
        """
        Calculate the total number of page downs it will take to page through all the data in the dynamic area.

        Uses the total number of lines in the dynamic data area / number of lines per page rounded down.
        (e.g. 68/26 = 2.6 rounded down to 2

        :param lines_per_page: Total number of data rows
        :return: calculated number of page down requests to get to the last page of data.
        """
        # Max sure we are at the beginning
        if self.output_file is None:
            CommonNav.nav_max_up(self.ptg2_em)
        else:
            CommonNav.nav_max_up(self.ptg2_em, out_file=self.output_file)
        # Get the line, pos coordinates of "LINE 1 OF" string in the display
        x, y = self.ptg2_em.screen.find('LINE 1 OF', case_sensitive=True)

        # Get the whole string (i.e. Line 1 of 'some number number')
        line_str = self.ptg2_em.string_get((x + 1), (y + 1), 12)
        # Split the string on spaces into a list of words
        line_of_list = line_str.split()
        # Convert the second number in the string to an integer, this is the total number of display rows in the
        # dynamic data area.
        total_lines = int(line_of_list[3])
        # Divide total number of lines by the number of lines per page. (e.g. 68/26 = 2
        num_pages_down = total_lines / lines_per_page
        # Return the number of page downs needed.
        return num_pages_down

    def num_display_rows(self):
        """
        Calculates the number of dynamic display rows on the display

        :return: total number of rows in the dynamic data area.
        """

        if self.ptg2_em.screen.contains('BOTTOM OF DATA', case_sensitive=True):
            end_marker_string_to_find = 'BOTTOM OF DATA'
        elif self.ptg2_em.screen.contains('F1=HELP', case_sensitive=True):
            end_marker_string_to_find = 'F1=HELP'
        else:
            end_marker_string_to_find = 'PF 1=HELP'

        try:
            first_field = self.get_first_field(text_before_input_field='Time =>')
        except ValueError:
            first_field = self.get_first_field(text_before_input_field='Time ==>')

        (bottom_display_row, bottom_display_column) = self.ptg2_em.screen.find(end_marker_string_to_find,
                                                                               case_sensitive=True)
        num_data_rows = bottom_display_row - (first_field.row - 1)

        return num_data_rows

    def get_first_field(self, text_before_input_field):
        """
        Uses the :py:class:`Emulator` :py:func:`field_after' to obtain the first input field that occurs after the
        requested text string.

        :param text_before_input_field: string that occurs before an input field.
        :return:    Found -  returns the :py:class: 'Field' instance that represents the first field found
                    Not Found - raises an error.
        """
        first = self.ptg2_em.screen.field_after(text=text_before_input_field)
        if first is not None:
            return first
        else:
            raise ValueError('"%s" string not found on panel.' % text_before_input_field)

    def nav_to_page(self, page):
        """
        Navigate to a certain page (i.e. left or right)
        :param page: page number to navigate to (1 based)
        """

        # Make sure we are all the way to the left on page 1.
        if self.output_file is None:
            CommonNav.nav_max_left(self.ptg2_em)
        else:
            CommonNav.nav_max_left(self.ptg2_em, out_file=self.output_file)
        page -= 1  # page number needs to be based on starting from page 1.
        for i in range(page):
            if self.output_file is None:
                CommonNav.nav_shift_right(self.ptg2_em, message_text='PT016W - ALREADY AT RIGHT')
            else:
                CommonNav.nav_shift_right(self.ptg2_em, message_text='PT016W - ALREADY AT RIGHT',
                                          out_file=self.output_file)

    def get_display_columns(self):
        """
        Gets the column names and the dash lines (i.e. lengths) for a display
        :return: both as a string tuple (columns, dashes)
        """

        # Find the first input field in the dynamic data area after 'Interval Date =>' which is unique and appears
        # across all displays
        try:
            field_found = self.get_first_field(text_before_input_field='Time =>')
        except ValueError:
            field_found = self.get_first_field(text_before_input_field='Time ==>')

        # Set initial line, pos, and length for both column names and dash rows on the display
        self.col_name_line = field_found.row - 2
        col_dash_line = field_found.row - 1
        col_pos = field_found.col
        # adjusted_screen_length = self.screenLen - field_found.col
        adjusted_screen_length = self.screenLen - 1

        #  Get the page of column names and dashes.
        col_name_str = self.ptg2_em.string_get(self.col_name_line, col_pos, adjusted_screen_length)
        col_len_str = self.ptg2_em.string_get(col_dash_line, col_pos, adjusted_screen_length)

        return col_name_str, col_len_str

    def build_display_table(self, build_primary_key_dict='Y', build_display_logging=True):
        """
        Builds an entire result set dictionary of column info objects by column name and all the associated rows of data
        for an entire set of displays. (i.e. all rows top to bottom left to right.)

        :param build_primary_key_dict: Indicates whether a primary key dictionary should be built.
        :param build_display_logging: Defaults to True which captures scrolling down and right when capturing the data
                                      for a display. Set to False to skip the logging
        :return: returns an instance of :py:class Results
        """

        page = 0  # initialize page number
        current_panelid = self.ptg2_em.app.ispf_panelid
        primary_key_dict = None

        if build_primary_key_dict == 'Y':
            primary_key_dict = RtpPrimaryKeys.get_primary_key_dict(current_panelid)
        # create instance of Result class object
        result = Results(primary_key_dictionary=primary_key_dict, output_file=self.output_file)

        # Max page left and up to ensure we are starting with first display
        CommonNav.nav_max_left(self.ptg2_em, log_screen=self.screen_log, out_file=self.output_file)
        CommonNav.nav_max_up(self.ptg2_em, log_screen=self.screen_log, out_file=self.output_file)

        # While we can shift to the right get all the columns and their lengths (i.e. dashes)
        while True:
            col_str, len_str = self.get_display_columns()
            page += 1
            result.parse_columns(col_str, len_str, page)
            if not CommonNav.nav_shift_right(self.ptg2_em, log_screen=self.screen_log, message_text='PT016W - ALREADY AT RIGHT',
                                             out_file=self.output_file):
                break
        self.persist_column = list(result.columns)[0]

        CommonNav.nav_max_left(self.ptg2_em, log_screen=build_display_logging, out_file=self.output_file)  # start back on page 1 for the value.

        # While we can page down until we find "*** BOTTOM OF DATA *** get all the columns and all their rows of data
        while True:
            result.parse_values(self, self.num_display_rows(), log_displays=build_display_logging)
            # go all the way back left to column 1
            CommonNav.nav_max_left(self.ptg2_em, log_screen=build_display_logging, out_file=self.output_file)
            if not CommonNav.nav_page_down(self.ptg2_em, log_screen=build_display_logging, out_file=self.output_file):
                break

        return result

    def find_field(self, field_id):
        """
        Finds a PTG2 field_id on the current screen
        :param field_id: field_id to find
        :return: True - found
                 False - not found
        """
        while field_id in self.ptg2_em.screen:
            return True

        return False  # field_id requested not found in current screen

    def refresh(self):
        """
        Refresh the current screen.
        :return: no return
        """
        self.ptg2_em.app.ispf_submit()

    def main_menu_option(self, option, panelid):
        """
        Selects a product main menu option.
        :param option: Product option number
        :param panelid: The panelid expected to see after selecting the main menu option (i.e. PDTC0001)
        :return: nothing
        """
        self.ptg2_em.app.ispf_command(option, expect_panelid=panelid)

    def start_collection(self, collection_options):
        """

        :param collection_options: JSON dictionary of collection options
        :return:
        """
        # First collection start panel options
        col_opts1 = collections.OrderedDict([('DB2 SSID', 'ssid'), ('Interval Time', 'itime'),
                                             ('Round Interval', 'r_interval'),
                                             ('Use Sysplex Interval Time', 'plex_itime'), ('Time Limit', 't_limit'),
                                             ('Externalize', 'extern'), ('High Level', 'high_level'),
                                             ('Datastore Name', 'current_datastore'), ('Auto Start', 'auto')])

        for option, name in col_opts1.items():
            if option == 'DB2 SSID':
                field, value = self.get_collection_option_value(option, name, self.u_ssid.upper(), collection_options)
                field.fill(value)
            elif option == 'Interval Time':
                field, value = self.get_collection_option_value(option, name, '01:00', collection_options)
                values = value.split(':')

                if len(values) is not 2:
                    msg = "The collection start parameter {0} = {1} is not valid."
                    raise ValueError(msg.format(option, join(values)))
                for value in values:
                    field.fill(value)
                    field = field.next()

            elif option == 'Round Interval':
                field, value = self.get_collection_option_value(option, name, 'N', collection_options)
                field.fill(value)
            elif option == 'Use Sysplex Interval Time':
                field, value = self.get_collection_option_value(option, name, 'N', collection_options)
                field.fill(value)
            elif option == 'Time Limit':
                field, value = self.get_collection_option_value(option, name, '00:00', collection_options)
                values = value.split(':')

                if len(values) is not 2:
                    msg = "The collection start parameter {0} = {1} is not valid."
                    raise ValueError(msg.format(option, join(values)))

                for value in values:
                    field.fill(value)
                    field = field.next()
            elif option == 'Externalize':
                field, value = self.get_collection_option_value(option, name, 'N', collection_options)
                field.fill(value)
            elif option == 'High Level':
                field, value = self.get_collection_option_value(option, name, self.vcat, collection_options)
                field.fill(value)
            elif option == 'Datastore Name':
                field, value = self.get_collection_option_value(option, name, self.datastore_name, collection_options)
                field.fill(value)
            elif option == 'Auto Start':
                field, value = self.get_collection_option_value(option, name, 'N', collection_options)
                field.fill(value)

    def get_collection_option_value(self, option, name, default, options=None):
        """
        For a given option on a products "Start Collection" return the PTG2 field object for a given option and either
        the value provided in the options node from the JSON file or a default value.
        :param option: string that identifies which panel option to find. (e.g. "DB2 SSID")
        :param name: the name of the JSON files options dictionary key to get the value for.
        :param default: A value to return as the default to be used to fill in the panel field if a value is not found
                        in the options dictionary
        :param options: The options dictionary extracted from the JSON file.
        :return:
        """

        # If the collection option is Time Limit we need to alter the string we are looking for in order to find the
        # correct field object because PTG2 method does not match on exact case and there is another occurrence of the
        # words 'time limit' before the actual option.
        if option == 'Time Limit':
            option = 'Time Limit         ==>'

        # Call Common service method to find the PTG2 field object for the collection option looking for.
        field = CommonNav.get_first_field(self.ptg2_em, text_before_input_field=option)
        value = ''  # default this
        # if we were given an options dictionary node from the JSON file see if it has an option by the "name" and
        # retrieve its value
        if options is not None:
            value = options.get(name)
        # Return the related PTG2 field object and either the value retrieved or the default value.
        # object.
        if value is not None:
            return field, value
        else:
            return field, default

    def start_product(self, release_environment):
        """
        Base method that is overridden in subclasses NavPdt and NavPsa.
        :return:
        """
        return

    def product_main(self):
        """
        Base method that is overridden in subclasses NavPdt and NavPsa.
        :return:
        """
        return

    def select_datastore(self):
        """
        Base method that is overridden in subclasses NavPdt and NavPsa.
        :return:
        """
        return

    def select_interval(self):
        """
        Base method that is overridden in subclasses NavPdt and NavPsa.
        :return:
        """
        return

    def view_by(self, display_request):
        """
        Base method that is overridden in subclasses NavPdt and NavPsa.

        :param display_request:
        :return:
        """
        return
