import datetime
import os
from termcolor import colored


class CommonNav(object):
    """
    Common class that encapsulates static methods for non product specific movements and commands in ISPF within
    CA DB2 Tools products using PTG2 APIs.
    """

    @staticmethod
    def nav_screen_capture(emulator, display_fields=False, file_name=None):
        """
        Uses the PTG2 log method to capture and log the current display.

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param display_fields: - Indicate whether output of panel fields is included in the screen capture. Defaults
                                 to False. Set to True if field output is wanted.
        :param file_name: Indicates screen capture should be written to the directory/file location specified.
        """
        if file_name is None:
            emulator.screen.log(fields=display_fields)
        else:
            try:
                with open(file_name, mode='a', encoding='UTF-8') as (user_file):
                    for line in emulator.screen.lines:
                        if not line.isspace():
                            user_file.write(line + '\n')
                    user_file.write('\n')  # put a blank line between screen shots.

            except IOError:
                with open(file_name, mode='w', encoding='UTF-8') as (user_file):
                    for line in emulator.screen.lines:
                        if not line.isspace():
                            user_file.write(line + '\n')
                    user_file.write('\n')  # put a blank line between screen shots.

    @staticmethod
    def nav_screen_back(emulator, log_screen=True, out_file=None):
        """
        Uses the PTG2 ispf_submit method to request a PF3 (end).

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param log_screen: Optional - Log the current screen after the shift occurs - True(default) or False
        :param out_file: Indicates screen capture should be written to the directory/file location specified.
        """
        emulator.app.ispf_submit(action='pf3')
        if log_screen:
            CommonNav.nav_screen_capture(emulator, file_name=out_file)
        return True

    @staticmethod
    def nav_shift_right(emulator, message_text=None, log_screen=True, out_file=None):
        """
        Shifts the display right by 1 PF11 key.

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param message_text: Optional - message text to look for that indicates whether the shift occurred or at the end
        :param log_screen: Optional - Log the current screen after the shift occurs - True(default) or False
        :param out_file: Indicates screen capture should be written to the directory/file location specified.
        :return:    True - shift occurred
                    False - False when shifted as far as can go
        """
        emulator.app.ispf_submit(action='pf11')
        if message_text is not None:
            if not emulator.screen.contains(message_text):
                if log_screen:
                    if out_file is None:
                        CommonNav.nav_screen_capture(emulator)
                    else:
                        CommonNav.nav_screen_capture(emulator, file_name=out_file)
                return True
            else:
                return False
        else:
            if log_screen:
                if out_file is None:
                    CommonNav.nav_screen_capture(emulator)
                else:
                    CommonNav.nav_screen_capture(emulator, file_name=out_file)
            return True

    @staticmethod
    def nav_shift_left(emulator, message_text=None, log_screen=True, out_file=None):
        """
        Shifts the display left by 1 PF10 key.

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param message_text: Optional - message text to look for that indicates whether the shift occurred or at the end
        :param log_screen: Optional - Log the current screen after the shift occurs - True(default) or False
        :param out_file: Indicates screen capture should be written to the directory/file location specified.
        :return:    True - shift occurred
                    False - False when shifted as far as can go if looking for a message.
        """
        emulator.app.ispf_submit(action='pf10')
        if message_text is not None:
            if not emulator.screen.contains(message_text):
                if log_screen:
                    if out_file is None:
                        CommonNav.nav_screen_capture(emulator)
                    else:
                        CommonNav.nav_screen_capture(emulator, file_name=out_file)
                return True
            else:
                return False
        else:
            if log_screen:
                if out_file is None:
                    CommonNav.nav_screen_capture(emulator)
                else:
                    CommonNav.nav_screen_capture(emulator, file_name=out_file)
            return True

    @staticmethod
    def nav_max_left(emulator, log_screen=True, out_file=None):
        """
        Maxes all the way to the left

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param log_screen: Optional - Log the current screen after the shift occurs - True(default) or False
        :param out_file: Indicates screen capture should be written to the directory/file location specified.
        """
        emulator.screen['command'] = 'm'
        emulator.submit_screen(action='pf10')
        if log_screen:
            if out_file is None:
                CommonNav.nav_screen_capture(emulator)
            else:
                CommonNav.nav_screen_capture(emulator, file_name=out_file)

    @staticmethod
    def nav_max_right(emulator, log_screen=True, out_file=None):
        """
        Maxes all the way to the right

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param log_screen: Optional - Log the current screen after the shift occurs - True(default) or False
        :param out_file: Indicates screen capture should be written to the directory/file location specified.
        """
        emulator.screen['command'] = 'm'
        emulator.submit_screen(action='pf11')
        if log_screen:
            if out_file is None:
                CommonNav.nav_screen_capture(emulator)
            else:
                CommonNav.nav_screen_capture(emulator, file_name=out_file)

    @staticmethod
    def nav_max_up(emulator, log_screen=True, out_file=None):
        """
        Pages all the way up

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param log_screen: Optional - Log the current screen after the shift occurs - True(default) or False
        :param out_file: Indicates screen capture should be written to the directory/file location specified.
        :return:
        """
        emulator.screen['command'] = 'm'
        emulator.submit_screen(action='pf7')
        if log_screen:
            if out_file is None:
                CommonNav.nav_screen_capture(emulator)
            else:
                CommonNav.nav_screen_capture(emulator, file_name=out_file)

    @staticmethod
    def nav_max_down(emulator, log_screen=True, out_file=None):
        """
        Pages all the way down

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param log_screen: Optional - Log the current screen after the shift occurs - True(default) or False
        :param out_file: Indicates screen capture should be written to the directory/file location specified.
        :return:
        """
        emulator.screen['command'] = 'm'
        emulator.submit_screen(action='pf8')
        if log_screen:
            if out_file is None:
                CommonNav.nav_screen_capture(emulator)
            else:
                CommonNav.nav_screen_capture(emulator, file_name=out_file)

    @staticmethod
    def nav_page_down(emulator, log_screen=True, out_file=None):
        """
        Pages down by 1 PF8 key if the string "*** BOTTOM OF DATA ***" is not on the screen. This is useful for with a
        scrollable dynamic data area.

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param log_screen: Optional - Log the current screen after the shift occurs - True(default) or False
        :param out_file: Indicates screen capture should be written to the directory/file location specified.
        :return:    True - page down occurred
                    False - no page down when as far as can go
        """

        if not emulator.screen.contains('*** BOTTOM OF DATA ***'):
            emulator.submit_screen(action='pf8')
            if log_screen:
                if out_file is None:
                    CommonNav.nav_screen_capture(emulator)
                else:
                    CommonNav.nav_screen_capture(emulator, file_name=out_file)
            return True
        else:
            return False

    @staticmethod
    def nav_sort_column(emulator, sort_column, sort_order='A'):
        """
        Sorts a display by issuing the ISPF sort command using the column and the order requested.

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param sort_column: Required - column name to sort on (no single quotes required '')
        :param sort_order: Optional - Specify ascending (A) or descending (D) order. Defaults to ascending (A)
        :return: True - sort was successful
                 False - sort unsuccessful
        """

        if sort_order is not 'A' and sort_order is not 'D':
            print("Sort order value of %s is not a valid option. Defaulting to ascending (A)." % sort_order)
            print(sort_order)
            sort_order = 'A'

        emulator.screen['command'] = """sort '""" + sort_column + """' """ + sort_order
        emulator.submit_screen()
        if len(emulator.screen.messages) == 0:
            return True
        else:
            return False

    @staticmethod
    def print_test_start_end(test_name, output_type='start', string_width=80, file_name=None):
        """
        Simple method that takes the name of a automation test (i.e. RTP test class name) and prints either a "start of"
        or "end of" indicator centered across a width. Includes the date and time

        :param test_name: Name of the test of type(str) (i.e. Interval Compare)
        :param output_type: indicates whether to print the start header or the stop footer message. Options are:
                                1) 'start' - Default
                                2) 'end'
        :param string_width: The width of the line to be used. Defaults to 80 bytes.
        :param file_name: Indicates the indicator should be writing to a file and what the location/name is.
        :return: Nothing
        """

        current_date_time_object = datetime.datetime.now()
        current_date = current_date_time_object.strftime('%Y-%m-%d')
        current_time = current_date_time_object.strftime('%H:%M:%S')

        if file_name is None:
            if output_type is 'start':
                output_str = "%s\tStart of %s Test\t%s" % (current_date, test_name, current_time)
                print(output_str.center(string_width))
            elif output_type is 'end':
                output_str = "%s\tEnd of %s Test\t%s" % (current_date, test_name, current_time)
                print(output_str.center(string_width))
            else:
                print("Output type '%s' is not a valid choice" % output_type)
        else:
            if output_type is 'start':
                try:
                    with open(file_name, mode='a') as (user_file):
                        output_str = "%s\tStart of %s Test\t%s\n" % (current_date, test_name, current_time)
                        user_file.write(output_str.center(string_width))
                except IOError:
                    with open(file_name, mode='w') as (user_file):
                        output_str = "%s\tStart of %s Test\t%s\n" % (current_date, test_name, current_time)
                        user_file.write(output_str.center(string_width))
            elif output_type is 'end':
                try:
                    with open(file_name, mode='a') as (user_file):
                        output_str = "%s\tEnd of %s Test\t%s\n" % (current_date, test_name, current_time)
                        user_file.write(output_str.center(string_width))
                except IOError as error:
                    print("IOError exception occurred trying to write end of test statement to file - %s" % file_name)
                    print(error)
            else:
                print("Output type '%s' is not a valid choice" % output_type)

    @staticmethod
    def find_command(emulator, text_to_find, error_message_id, column_name=None, log_find_command=False):
        """
        Issue the ISPF find command for some 'text_to_find'. Additionally can provide a column name to search only
        within a specific column when dealing with a dynamic display area.

        When the string is found the screen is positioned with the column/row within view at the top of the dynamic data
        area and the screen is read so that on return the emulator contains the screen for capturing and further
        processing. If not found the the emulator screen is updated to contain the same screen started on in addition
        to the error message displayed.

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param text_to_find: the text to find
        :param error_message_id: Product message code that should appear if value not found.(i.e. PT019I)
        :param column_name: name of a column in a dynamic display area to only search within
        :param log_find_command: Default is False. Set to True if the capturing of the find command on the command line
                                 and the found text screens is wanted.
        :return: True - text was found and emulator screen updated.
                 False - text not found and emulator screen returned with error message displayed
        """
        if column_name is None:
            emulator.screen['command'] = 'find ' + text_to_find
        else:
            emulator.screen['command'] = 'find ' + text_to_find + ' ' + column_name

        if log_find_command:
            CommonNav.nav_screen_capture(emulator)

        emulator.app.ispf_submit()

        if log_find_command:
            CommonNav.nav_screen_capture(emulator)

        if error_message_id in emulator.screen.messages:
            return False

        return True

    @staticmethod
    def string_to_ptg2_field_id(string_to_transform):
        """
        Transforms a string to a valid PTG2 Field ID. PTG2 framework when setting field ids for a screen strips out any
        non alphanumeric characters which makes it hard to use user data directly. This method will determine if the
        string passed in contains any non alphanumeric characters and if it does will filter out all of them and return
        the transformed string which should now be a valid PTG2 field ID.

        Example - Using a Detector Plan Program Display:

              PROGRAM   UNACC_TIME   TYPE SQL        TIMEPCT CPUPCT  INDB2_TIME
              --------  ------------ ---- ---------- ------- ------- ------------
            _ SP#SP3C   00:00.000240 PKGE         15    .00%    .00% 00:00.001615

            The program name SP#SP3C would be identified by PTG2 as field id - spsp3c. So passing in the string to this
            method as the user would see it (i.e. SP#SP3C) would transform it into spsp3c.


        :param string_to_transform: Text string that may need transforming into a proper PTG2 field id(i.e. SP#SP3C)
        :return: valid PTG2 field id string
        """
        # PTG2 expects field id name to be lower case
        string_to_transform = string_to_transform.lower()
        if string_to_transform.isalnum():
            return string_to_transform
        else:
            string_to_transform = filter(str.isalnum, str(string_to_transform))
            return string_to_transform

    @staticmethod
    def get_first_field(emulator, text_before_input_field):
        """
        Uses the :py:class:`Emulator` :py:func:`field_after' to obtain the first input field that occurs after the
        requested text string.

        :param text_before_input_field: string that occurs before an input field.
        :return:    Found -  returns the :py:class: 'Field' instance that represents the first field found
                    Not Found - raises an error.
        """
        first = emulator.screen.field_after(text=text_before_input_field)
        if first is not None:
            return first
        else:
            raise ValueError('"%s" string not found on panel.' % text_before_input_field)

    @staticmethod
    def printlns(lines, file_path=None):
        """
        Writes any number of lines to a file or stdout. Appends if the file already exists.
        :param file_path: The path of the file.
        :param lines: An array of lines to write.
        :return:
        """

        current_date_time_object = datetime.datetime.now()
        date = current_date_time_object.strftime('%Y-%m-%d')
        time = current_date_time_object.strftime('%H:%M:%S')
        temp = "{}-{}, {}"
        if file_path is None:
            for line in lines:
                print(temp.format(date, time, line))
        else:
            if os.path.isfile(file_path):
                with open(file_path, mode='a') as (user_file):
                    for line in lines:
                        user_file.write(temp.format(date, time, line) + "\n")
            else:
                with open(file_path, mode='w') as (user_file):
                    for line in lines:
                        user_file.write(temp.format(date, time, line) + "\n")

    @staticmethod
    def color_line(line, color_state=None):
        """
        Returns a line of text in a color based on the state requested. See color_state parameter.
        :param line: String to be colored.
        :param color_state: Valid values are:
                            error = red
                            warning = yellow
                            success = green
        :return: Line colored or not.
        """

        if color_state == 'error':
            colored_line = colored(line, 'red')
        elif color_state == 'warning':
            colored_line = colored(line, 'yellow')
        elif color_state == 'success':
            colored_line = colored(line, 'green')
        else:
            colored_line = line

        return colored_line

    @staticmethod
    def println(line, file_path=None, color_state=None, timestamp=True):
        """
        Writes any number of lines to a file or stdout. Appends if the file already exists.
        :param file_path: The path of the file.
        :param line: An array of lines to write.
        :param color_state: Color the line to be printed. Valid values and their corresponding colors are:
                            error = red
                            warning = yellow
                            success = green
        :param timestamp: If set to False prints the line of output without the date and time. Defaults to True.
        :return: Nothing
        """
        if color_state is not None and file_path is None:
            color_state.lower()
            colored_line = CommonNav.color_line(line, color_state=color_state)
        else:
            colored_line = line

        if timestamp:
            current_date_time_object = datetime.datetime.now()
            date = current_date_time_object.strftime('%Y-%m-%d')
            time = current_date_time_object.strftime('%H:%M:%S')
            temp = "{}-{}, {}"
            temp = temp.format(date, time, colored_line)
        else:
            temp = "{}"
            temp = temp.format(colored_line)

        if file_path is None:
                # print(temp.format(date, time, colored_line))
                print(temp)
        else:
            if os.path.isfile(file_path):
                with open(file_path, mode='a') as (user_file):
                        # user_file.write(temp.format(date, time, colored_line) + "\n")
                        user_file.write(temp + "\n")
            else:
                with open(file_path, mode='w') as (user_file):
                    # user_file.write(temp.format(date, time, colored_line) + "\n")
                    user_file.write(temp + "\n")

    @staticmethod
    def create_file_path(path, filename):
        """
        Creates a full file path.
        :param path:
        :param filename:
        :return:
        """
        return path + os.sep + filename

    @staticmethod
    def delete_file(file_path):
        """
        Deletes a file.
        :param path:
        :param file_name:
        :return:
        """
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def create_dir(file_path):
        """
        Create a directory.
        :param file_path:
        :return:
        """
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    @staticmethod
    def nav_freeze_unfreeze_column(emulator, column_name, command='freeze'):
        """

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param column_name: Name of the column to issue the command on.
        :param command: Either the 'freeze' or 'unfreeze' command. Defaults to 'freeze'
        :return: True - successful.
                 False - An ispf error message was displayed after the command was issued.
        """
        if command != 'freeze' and command != 'unfreeze':
            print("Command value of '%s' is not a valid option for nav_freeze_unfreeze_column." % command)
            return False

        emulator.screen['command'] = command + " " + column_name
        emulator.submit_screen()
        if len(emulator.screen.messages) == 0:
            return True
        else:
            for message_key, value_guess_instance in emulator.screen.messages.items():
                if command == 'freeze':
                    if value_guess_instance.value == '- Column is frozen':
                        emulator.submit_screen(action="home")
                        emulator.submit_screen(action="eraseeof")
                        emulator.submit_screen()
                        return True
                    else:
                        return False
                elif command == 'unfreeze':
                    if value_guess_instance.value == '- Column is not frozen':
                        emulator.submit_screen(action="home")
                        emulator.submit_screen(action="eraseeof")
                        emulator.submit_screen()
                        return True
                    else:
                        return False

    @staticmethod
    def expand_and_fill_field(emulator, field_name, value):
        """
        Locates and expands an expandable panel field and fills it in with the value provided.

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param field_name: a PTG2 field name
        :param value: value to fill in
        :return: True or raises an error.
        """

        emulator.screen['command'] = 'expand'
        f_obj = emulator.screen.get_field_for_key(field_name)
        f_obj.focus()
        emulator.app.ispf_submit()
        emulator.send_string(value)
        CommonNav.nav_screen_capture(emulator)
        CommonNav.nav_screen_back(emulator)
        return True

    @staticmethod
    def issue_save_command(emulator, member_name, log_screen=True, out_file=None):
        """
        Issues the 'save' command. Useful in ISPF Edit to save information.

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param member_name: Name of the member being saved.
        :param log_screen: Optional - Log the current screen after - True(default) or False
        :param out_file: Indicates screen capture should be written to the directory/file location specified.
        :return:
        """

        saved_message = "Member %s saved" % member_name
        emulator.app.ispf_command('SAVE', expect_message=saved_message)
        if log_screen:
            CommonNav.nav_screen_capture(emulator, file_name=out_file)

    @staticmethod
    def issue_change_command(emulator, change_from, change_to, change_option=None, log_screen=True, out_file=None):
        """
        Issues an ISPF change command

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param change_from: string value changing from
        :param change_to: string value changing to
        :param change_option: string value of change option to use. E.g. all
        :param log_screen: Optional - Log the current screen after - True(default) or False
        :param out_file:  Indicates screen capture should be written to the directory/file location specified.
        :return:
        """

        if change_option is None:
            change_command = "CHANGE '%s' '%s'" % (change_from, change_to)
        else:
            change_command = "CHANGE '%s' '%s' %s" % (change_from, change_to, change_option)

        change_message = "CHARS '%s' changed" % change_from

        emulator.app.ispf_command(change_command, expect_message=change_message)
        if log_screen:
            CommonNav.nav_screen_capture(emulator, file_name=out_file)

    @staticmethod
    def db2_version(ssid):
        """
        Based on a DB2 SSID returns the known DB2 Version.

        :param ssid: the 4 character ssid string (e.g. D11A, DD0G, etc...)
        :return: version string. E.g. 11, 10, 12, etc..
        """

        db2_version_dict = {'DB0G': '10', 'D10C': '10', 'Q10C': '10', 'DB1G': '10', 'D10E': '10', 'Q10D': '10',
                            'D10A': '10', 'Q10A': '10', 'DB2G': '10', 'D10B': '10', 'Q10B': '10', 'DD0G': '11',
                            'DH0G': '11', 'D11A': '11', 'Q11A': '11', 'DD1G': '11', 'Q11B': '11', 'DH1G': '11',
                            'D11B': '11', 'DD2G': '11', 'DH2G': '11', 'D11E': '11', 'D11C': '11', 'D11D': '11',
                            'DD3G': '11', 'DH3G': '11', 'DB3G': '10', 'D12A': '12', 'DBN1': '12', 'DBN2': '12',
                            'DBN3': '12', 'DT11': '12', 'DT31': '12', 'Q12A': '12'}

        return db2_version_dict.get(ssid)

    @staticmethod
    def tso_command(emulator, command_string, expect_panel=None, text_to_wait_for=None, log_screen=True, out_file=None):
        """
        Issue a TSO command from ISPF.

        :param emulator: Required - instance of :py:class 'Emulator' that represents the current screen.
        :param command_string: tso command to execute.
        :param expect_panel: panelid to be displayed after the TSO command if there is one.
        :param text_to_wait_for: string of text to wait to be displayed before continuing.
        :param log_screen: Optional - Log the current screen after - True( or False(default)
        :param out_file:  Indicates screen capture should be written to the directory/file location specified.
        :return:
        """

        emulator.app.ispf_command(command_string, expect_panelid=expect_panel, wait_for_text=text_to_wait_for)
        if log_screen:
            CommonNav.nav_screen_capture(emulator, file_name=out_file)
