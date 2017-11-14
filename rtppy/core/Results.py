import collections
import datetime
from core.columnInfo import ColumnInfo
from core.common import CommonNav


class Results(object):
    def __init__(self, primary_key_dictionary=None, output_file=None):
        self.columns = collections.OrderedDict()
        self.output_file = output_file

        if primary_key_dictionary is None:
            self.primary_key_dictionary = collections.OrderedDict()
        else:
            self.primary_key_dictionary = collections.OrderedDict(primary_key_dictionary)

    def parse_columns(self, col_name_str, col_len_str, page):
        """
        Parses a string of space delimited column names and their associated dashes from a display.

        Then creates a dictionary (columns) using the list of columns as the key. The value being a ColumnInfo object
        that contains the columns name, length(derived from the length of each associated dash string under the column),
        its horizontal pos on the display, the page number the column appears on, and its data type.

        :param col_name_str: Space delimited string of column names.
        :param col_len_str: Space delimited string of symbols (e.g. dashes) that will be used to determine the length
                            of the column.
        :param page: Page number that the column is on.
        """
        col_names = col_name_str.split()
        col_len = col_len_str.split()
        prev_col_offset = 0

        for column, col_length in zip(col_names, col_len):
            length = len(col_length)
            data_type = ColumnInfo.data_type_dict.get(column)
            try:
                if prev_col_offset > 0:
                    pos = col_name_str.index(column, prev_col_offset, len(col_name_str))
                    prev_col_offset = length + pos
                else:
                    pos = col_name_str.index(column, prev_col_offset, len(col_name_str))
                    prev_col_offset = length + pos
            except Exception as index_error:
                print('Current string being processed:\n %s' % col_name_str)
                print('\nCurrent column name looking for is: %s' % column)
                raise index_error

            if column not in self.columns:
                column_obj = ColumnInfo(column, length, pos, page, data_type)
                self.columns[column] = column_obj

            # Todo: below prints are test code
            """
            col_info_obj = self.columns.get(column)
            print('Column name is %s' % col_info_obj.name)
            print('Column length is %s ' % col_info_obj.length)
            print('Column position is %s' % col_info_obj.column_pos)
            print('Column is on page %s\n' % col_info_obj.page)
            """

    def parse_values(self, nav_pdt, num_data_rows, log_displays=True):
        """
        Creates a dictionary of (row, value) pairs and adds all the data for a given ColumnInfo object

        :param nav_pdt: instance of :py:class NavPdt
        :param num_data_rows: total number of data rows to process.
        :param log_displays: Defaults to True which captures scrolling down and right when capturing the data for a
        display. Set to False to skip the logging
        """

        try:
            field_found = nav_pdt.get_first_field(text_before_input_field='Time =>')
        except ValueError:
            field_found = nav_pdt.get_first_field(text_before_input_field='Time ==>')

        current_page = 1
        for column_name, col_info in self.columns.items():
            if current_page != self.get_column_info(column_name, 'page'):
                CommonNav.nav_shift_right(nav_pdt.ptg2_em, message_text='PT016W - ALREADY AT RIGHT', log_screen=log_displays,
                                          out_file=self.output_file)
                current_page += 1

            for i in range(0, num_data_rows):
                data_str = nav_pdt.ptg2_em.string_get(field_found.row + i, field_found.col +
                                                      col_info.column_pos, col_info.length)
                row_num = len(col_info.data.keys())
                col_info.add_column_value(row_num, data_str.strip())

    def get_column_info(self, col_name, info_request='all'):
        """
        Gets information about a column (i.e. length, position, page)

        :param col_name: name of the column to get
        :param info_request:
                    all - returns all the information in a tuple
                    length - returns the columns length
                    position - returns the columns horizontal position
                    page - returns the page number (starting from 1) that the column is on.
                    data type - returns the columns data type as a string (e.g. 'integer')
        :return: based on the request. See the parameters documented above.
        """
        #  Find the column info object for the given column name
        col_info_obj = self.columns.get(col_name)
        if info_request == 'all':
            return col_info_obj.get_all_col_info()

        elif info_request == 'name':
            return col_info_obj.get_column_name()

        elif info_request == 'length':
            return col_info_obj.get_column_length()

        elif info_request == 'position':
            return col_info_obj.get_column_pos()

        elif info_request == 'page':
            return col_info_obj.get_column_page()

        elif info_request == 'data type':
            return col_info_obj.get_column_data_type()
        else:
            raise ValueError('Column info request of %s is not a valid request type' % info_request)

    def get_row_data(self, column_name, row_num):
        """
        Gets the row data for a column info object by the column name. If there the column is not in the columns
        dictionary then 'None' is returned.

        :param column_name: name of the column to get the data for.
        :param row_num: Row number of the data to get (1 based)
        :return: Data for the requested row or None if the column name is not in the result columns dictionary
        """
        col_obj = self.columns.get(column_name)
        if col_obj is None:
            return None
        return col_obj.get_row_value(row_num)

    def display_all_rows(self, display_type='print', file_name=None, print_mode='w'):
        """
        Either displays to the screen or writes to a file all the columns and their rows of data.

        :param display_type: Valid data are 'print' or 'write' - Defaults to 'print'
        :param file_name: Name of the file to write to if display_type is 'write' otherwise exception raised
        :param print_mode: How to print to the file (2 choices)
                                'w' - write - Default (existing file with same name will be erased)
                                'a' - append (add data to the existing file name)
        """
        if display_type not in ('print', 'write'):
            print('Display type %s not a valid option, defaulting to ''print''' % display_type)

        if display_type == 'write':
            if file_name is None:
                raise ValueError('Display type of %s requires a file name for parameter file_name' % display_type)
            else:
                user_file = open(file_name, print_mode)

        for column, d_col_obj in self.columns.items():
            if display_type == 'write':
                user_file.write('Column: %s\n' % column)
            else:
                print('\nColumn: %s' % column)
            for row, data in d_col_obj.data.items():
                if display_type == 'write':
                    user_file.write('Row: %s  Data: %s\n' % (row, data))
                else:
                    print('Row: %s  Data: %s' % (row, data))

        if display_type == 'write':
            user_file.close()

    def init_rows_not_found(self):
        """
        Create and initialize a Not_found dictionary, whose key/value pairs are all the row numbers from the result sets
        total number of rows.
        :return: ordered dictionary
        """
        column_obj = list(self.columns.values())[0]
        initial_row_not_found_dict = collections.OrderedDict()
        for i in range(0, column_obj.total_number_of_rows()):
            initial_row_not_found_dict[i + 1] = i + 1

        return initial_row_not_found_dict

    def update_primary_keys_dict(self, row):
        """
        Updates the result instances primary_key_dictionary
        :param row: The row in which to get the data for the primary key.
        :return: Nothing, primary key dictionary will be updated. If a primary key (i.e. column name) is not in the
                 result set columns dictionary a
        """
        for key in self.primary_key_dictionary:
            self.primary_key_dictionary[key] = self.get_row_data(key, row)

    def find_key_row(self, row_search_dict, key_dictionary):
        """
        Uses a dictionary of row numbers to search the result set for a matching row. Finds and compares the data
        in the result set row against the column name and data in the key_dictionary which should contain the
        column names and their data as key,value pairs.

        :param row_search_dict: dictionary of rows to search.
        :param key_dictionary: dictionary of column names with the data to match on.
        :return: True - matching row found
                 False - no match found
        """
        for row in row_search_dict:
            row_found = 0
            for column_key, key_value in key_dictionary.items():
                if key_value != self.get_row_data(column_key, row):
                    row_found = -1
                    break
            if row_found != -1:
                return row
        return -1

    def find_key_from_value(self, primary_column_name, primary_value, secondary_column_name=None, secondary_value=None):
        """
        Returns the row number (i.e. key) in the result sets data dictionary a value exists given a column name.
        Additionally a second column and value can be provided if the primary value can exist more than once.

        :param primary_column_name: Primary column to find a matching row for
        :param primary_value: The value that indicates a match is found
        :param secondary_column_name: Additional column name to identify a matching row if the primary column could
                                      contain duplicate values.
        :param secondary_value: The additional value to identify the matching row against.
        :return: the row number in the result set data dictionary that matches, else returns None.
        """

        for col, col_obj in self.columns.items():
            if col == primary_column_name:
                for p_row, p_value in col_obj.data.items():
                    if p_value == primary_value and secondary_column_name is not None:
                        s_value = self.get_row_data(secondary_column_name, p_row)
                        if s_value == secondary_value:
                            return p_row
                    elif p_value == primary_value and secondary_column_name is None:
                        return p_row
                    else:
                        continue
        return None

    def compare_results(self, other_result_set, range_pct, specific_column_name=None, file_name=None):
        """
        Compares all the data from two result sets and prints a report.

        :param other_result_set: other instance of :py:class Results (a.k.a the baseline run of the data)
        :param range_pct: The allowable plus or minus range percentage the comparison can be between.
        :param specific_column_name: Optional - Compares the data only for the column name indicated.
        :param file_name: Optional - specify the name of a file to have the comparison report written to it.
        :return: A tuple that contains in this order:
                    1. the comparison return code.
                    2. a dictionary of the row numbers found between the two results sets that match each other.
                    3. dictionary of the rows in the result set that were not in the other result.
                    4. dictionary of rows in the other result set that were not in this result set.
        """
        compare_return_code = True
        global print_compare_header
        print_compare_header = True
        # Ensure that range percentage number passed in is integer type otherwise TypeError will occur during range calc
        range_pct = int(range_pct)
        # get the current result set (a.k. self) first column info object in the column info dictionary
        cur_temp_obj = list(self.columns.values())[0]

        """
        Initialize two Not_found dictionaries, one for both result sets.
        These dictionaries will then be reduced down to contain only the row numbers for which a matching row could not
        be found.
        """
        cur_result_set_row_not_found = self.init_rows_not_found()
        base_result_set_row_not_found = other_result_set.init_rows_not_found()
        result_sets_row_mapping = collections.OrderedDict()

        """
        For all the rows in the result set:
            1) Call the update_primary_keys_dict method with the row number to populate the primary keys dictionary
               keys with the appropriate rows data in order to identify the matching row in the other result set.
        """
        for row in cur_temp_obj.data:
            self.update_primary_keys_dict(row)
            # If the row is found in the other result set remove this row number from the row_not_found dictionary
            # then compare all the data between the two result sets for that row.
            base_row_found = other_result_set.find_key_row(base_result_set_row_not_found, self.primary_key_dictionary)
            if base_row_found != -1:
                del base_result_set_row_not_found[base_row_found]
                del cur_result_set_row_not_found[row]
                # Add both row and base_row_found to dictionary of mapped found rows
                result_sets_row_mapping[row] = base_row_found
                if not self.compare_row(other_result_set, row, base_row_found, range_pct, specific_column_name, file_name):
                    compare_return_code = False

        if len(base_result_set_row_not_found) > 0 or len(cur_result_set_row_not_found) > 0:
            compare_return_code = False

        return compare_return_code, result_sets_row_mapping, cur_result_set_row_not_found, base_result_set_row_not_found

    def compare_row(self, other_result_set, row, matching_row, range_pct, specific_column_name, file_name=None):
        """
        Compares all the columns of data for a row between two result set instances. If comparison fails, prints info
        to identify the two results columns and data, to the comparison report.

        :param other_result_set: the other result set of which to compare the data two
        :param row: current result set row being processed.
        :param matching_row: row in the other result set that matches.
        :param range_pct: The allowable plus or minus range percentage the comparison can be between.
        :param specific_column_name: Optional - Compares the data only for the column name indicated.
        :param file_name: Optional - specify the name of a file to have the comparison report written to it.
        :return: True - All data compared successfully and no comparison report generated.
                 False - At least 1 set of data didn't not fit comparison expectations and a report was produced.
        """
        compare_successful = True

        if file_name is not None:
            user_file = open(file_name, mode='a')

        for column_key, col_obj in self.columns.items():
            if specific_column_name is not None:
                if column_key != specific_column_name:
                    continue

            baseline_col_obj = other_result_set.columns.get(column_key)
            if not col_obj.compare_values(baseline_col_obj, row, matching_row, range_pct):
                global print_compare_header
                if print_compare_header:
                    Results.display_compare_report_header(range_pct, col_obj.total_number_of_rows(), file_name=file_name,
                                                          title_override='Interval Comparison Report')
                    if specific_column_name is not None:
                        if file_name is None:
                            print('\nSpecific column comparison requested: %s' % specific_column_name)
                        else:
                            user_file.write('\nSpecific column comparison requested: %s' % specific_column_name)
                    print_compare_header = False
                if file_name is None:
                    print('\nBaseline Column - ', end='')
                    baseline_col_obj.display_col_info()
                    baseline_col_obj.display_row_data(matching_row)
                    print('Current Column - ', end='')
                    col_obj.display_col_info()
                    col_obj.display_row_data(row)
                    compare_successful = False
                else:
                    user_file.write('\nBaseline Column - ')
                    baseline_col_obj.display_col_info(display_type='write', print_mode='a', new_line=False,
                                                      output_file_obj=user_file)

                    baseline_col_obj.display_row_data(matching_row, display_type='write', output_file_obj=user_file,
                                                      print_mode='a', new_line=False)
                    user_file.flush()
                    user_file.write('\nCurrent Column - ')
                    col_obj.display_col_info(display_type='write', output_file_obj=user_file, print_mode='a', new_line=False)
                    col_obj.display_row_data(row, display_type='write', output_file_obj=user_file, print_mode='a',
                                             new_line=False)
                    user_file.write('\n')
                    user_file.flush()
                    compare_successful = False
        if file_name is not None:
            user_file.close()
        return compare_successful

    def aggregate_compare(self, level, other_result_set, high_lvl_identifier_row, high_lvl_identifier_value,
                          specific_column_name=None, l_command=None, file_name=None, ptype_unkn=False):
        """
        Does an aggregate compare of two results sets. The other_result_set being the higher level result set to compare
        the data to after adding up all the rows of data for a given column.

        e.g. Add up at the statement level all the SQL counts for all the statements for a given program and compare it
        to that programs SQL column at higher program display level.

        :param level: keyword that indicates whether the other_result_set is a 'plan' or 'program' result set.
        :param other_result_set: other instance of :py:class Results (a.k.a the higher level result set)
        :param high_lvl_identifier_row: Identifies the row number in the higher level result sets data dictionary that
                                        should be aggregated and compare.
        :param high_lvl_identifier_value: Value that identifies the row at the higher level, indicated by the 'level'
                                          parameter, to compare the aggregate sum to. (e.g. program name or plan name)
        :param specific_column_name: Optional - Compares the data only for the column name indicated.
        :param file_name: Optional - specify the name of a file to have the comparison report written to it.
        :return: True - At least 1 set of data didn't not fit comparison expectations and a report was produced.
                 False - All data compared successfully and no comparison report generated.

        """

        global print_aggregate_compare_header
        print_aggregate_compare_header = True
        overall_compare_failed = False
        """
        Psuedocode
        First part - Summing up the data at the lower level
            - For every column in the lower level results(self) columns dict, get the column name and column info object
                - for that column gets it data type
                - if column we are processing is not a primary key then we can go further otherwise move on to the next
                    because the primary keys are usually columns we see as strings and don't need to be summed up.
                    - if the columns data type is percent or string then continue on and skip aggregating cause the
                        percentages at the lower level do not correlate to the high level percent column and aggregating
                        string data isn't appropriate.
                    - call the column info object aggregate_data method to sum up all the rows for this column.

            Second part - Find and access the higher level matching column data and compare it against the aggregate_sum
                - Get the appropriate column names column info object based on the value of the 'level' parameter.
                    * e.g. if 'level' was program then get the column info object for column name PROGRAM out of the
                        high level result set.
                - for every row in the higher level column info objects data dictionary
                    - Get that column info objects data value for the row
                        * e.g. if it is a program column info object get the program name for that row
                    - if the row value for that column info object is the same as the high level identifier value passed
                        - get the higher level data for that row that matches the lower level column we are
                            processing
                            - if None is returned by the get method then continue since it means that the higher level
                                result set does not have a column by that name.
                        - if the column data type is 'percent' or 'string' then skip comparison cause we didn't
                            aggregate the data.
                        - if the column data type is 'time'
                            - convert the possible up to DD:HH:MM:SS.ssssss value into total seconds
                            - call the static ColumnInfo upper and lower bound methods to find the min/max range of the
                                higher level time within 1%. This is needed of time data because the aggregate_sum of
                                the lower level time will never equal the higher level time because of the way the data
                                is aggregated in the collection engine. Except in case of zero value.
                            - if the aggregate_sum fits between the min/max range or the aggregate_sum is exactly equal
                                to the high level total seconds (i.e. both values are zero) then go to the next.
                            - else comparison failed so
                                - convert the aggregate_sum(i.e. total seconds) into a time object
                                - format the value into a human readable time value (i.e. HH:MM:SS.ssssss)
                                - turn on the individual compared value flag
                        - else the column data type is time
                            - if the higher level integer data is not equal to the aggregate_sum
                                - turn on the individual compared value flag
                        - if the individual compare flag is false
                            - if the comparison report header hasn't been printed yet
                                - call the print header function
                                - indicate the 'Aggregate Level' was the value of the 'level' parameter.
                                - indicate now the report header has been printed
                            - get the higher level result sets column info object for the column we were processing
                            - print into the report what the higher level column name was and its data for the row we
                                are processing by calling the display_col_info and display_row_data methods.
                            - print into the report the aggregate sum of the lower level data.
                            - set the overall compare to indicate failure

            - return indicating overall aggregate compare pass or fail
        """

        if file_name is not None:
            user_file = open(file_name, mode='a')
        if ptype_unkn:
            unkn_warning_message = "WARNING!!! Program was found with a 'TYPE' of 'UNKN'"
        else:
            unkn_warning_message = None

        for column, col_obj in self.columns.items():
            assert isinstance(col_obj, ColumnInfo)
            if specific_column_name is not None:
                if column != specific_column_name:
                    continue
            columns_data_type = col_obj.get_column_data_type()

            if column not in self.primary_key_dictionary:
                if columns_data_type is 'percent' or columns_data_type is 'string':
                    continue
                if level.lower() == 'plan' or (level.lower() == 'keys' and l_command == 'G'):
                    if column == 'INDB2_CPU' or column == 'GETPAGE' or column == 'SQL':
                        aggregate_sum = col_obj.aggregate_data()
                    else:
                        aggregate_sum = col_obj.aggregate_data(other_col_info_obj=self.columns.get('TYPE'), data_to_cause_aggregate_skip=('PROC', 'UDF', 'TRIG'))
                else:
                    aggregate_sum = col_obj.aggregate_data()

                if level == 'PLAN' or level == 'plan':
                    other_col_info_obj = other_result_set.columns.get('PLANNAME')
                elif level == 'PROGRAM' or level == 'program':
                    other_col_info_obj = other_result_set.columns.get('PROGRAM')
                elif level == 'DBASE':
                    other_col_info_obj = other_result_set.columns.get('DBNAME')
                else:
                    other_col_info_obj = other_result_set.columns.get('KEY')

                for row in other_col_info_obj.data:
                    indv_compare_failed = False
                    higher_level_value = other_col_info_obj.get_row_value(row)
                    if higher_level_value == high_lvl_identifier_value and row == high_lvl_identifier_row:
                        higher_level_data = other_result_set.get_row_data(column, row)
                        if higher_level_data is None:
                            continue

                        if columns_data_type is 'percent' or columns_data_type is 'string':
                            continue

                        elif columns_data_type is 'time':
                            higher_level_total_seconds = other_col_info_obj.convert_time_string(higher_level_data)
                            # calculate the low and high boundary range
                            floor = ColumnInfo.l_bound(higher_level_total_seconds, 0.01)
                            ceil = ColumnInfo.u_bound(higher_level_total_seconds, 0.01)
                            # See if the other columns time data is within range
                            if floor < aggregate_sum < ceil or aggregate_sum == higher_level_total_seconds:
                                continue
                            else:
                                # convert aggregate time sum to datetime obj for printing in time string format
                                time_obj = datetime.datetime.utcfromtimestamp(aggregate_sum)
                                aggregate_sum = time_obj.strftime('%H:%M:%S.%f')
                                indv_compare_failed = True
                        else:
                            if higher_level_data != aggregate_sum:
                                indv_compare_failed = True

                        if indv_compare_failed:
                            if print_aggregate_compare_header:
                                Results.display_compare_report_header(1, col_obj.total_number_of_rows(),
                                                                      title_override='Aggregate Comparison Report ',
                                                                      file_name=file_name)

                                CommonNav.println('\nAggregate Level: %s' % str.upper(level), file_path=file_name, timestamp=False)
                                CommonNav.println('Higher Level Value - %s' % str.upper(high_lvl_identifier_value), file_path=file_name, timestamp=False)
                                if unkn_warning_message is not None:
                                    CommonNav.println(unkn_warning_message, color_state='warning', file_path=file_name, timestamp=False)
                                # if file_name is None:
                                #     print('\nAggregate Level: %s' % str.upper(level))
                                #     print('Higher Level Value - %s' % str.upper(high_lvl_identifier_value))
                                # else:
                                #     user_file.write('\nAggregate Level: %s\n' % str.upper(level))
                                #     user_file.write('\nHigher Level Value - %s' % str.upper(high_lvl_identifier_value))
                                if specific_column_name is not None:
                                    CommonNav.println('Specific column comparison requested: %s' % specific_column_name, timestamp=False)
                                    # if file_name is None:
                                    #     print('Specific column comparison requested: %s' % specific_column_name)
                                    # else:
                                    #     user_file.write('\nSpecific column comparison requested %s' % specific_column_name)
                                    #     user_file.flush()
                                print_aggregate_compare_header = False

                            print_other_col_info_obj = other_result_set.columns.get(column)
                            if file_name is None:
                                print('\nHigher Level Column - ', end='')
                                print_other_col_info_obj.display_col_info()
                                print_other_col_info_obj.display_row_data(row)
                                print('Lower Level Aggregated Sum - %s' % aggregate_sum)
                            else:
                                user_file.write('\nHigher Level Column - '),
                                print_other_col_info_obj.display_col_info(display_type='write', output_file_obj=user_file,
                                                                          print_mode='a', new_line=False)
                                user_file.flush()
                                print_other_col_info_obj.display_row_data(row, display_type='write', output_file_obj=user_file,
                                                                          print_mode='a')
                                user_file.write('\nLower Level Aggregated Sum - %s' % aggregate_sum)
                                user_file.write('\n')
                                user_file.flush()
                            overall_compare_failed = True
        if not overall_compare_failed:
            if ptype_unkn:
                if print_aggregate_compare_header:
                    Results.display_compare_report_header(1, col_obj.total_number_of_rows(),
                                                          title_override='Aggregate Comparison Report ',
                                                          file_name=file_name)

                    CommonNav.println('\nAggregate Level: %s' % str.upper(level), file_path=file_name, timestamp=False)
                    CommonNav.println('Higher Level Value - %s' % str.upper(high_lvl_identifier_value), file_path=file_name, timestamp=False)
                    CommonNav.println(unkn_warning_message, color_state='warning', file_path=file_name, timestamp=False)
                    CommonNav.println("All Data aggregated successfully", color_state='success', file_path=file_name, timestamp=False)
                    print_aggregate_compare_header = False
                overall_compare_failed = True
        if file_name is not None:
            user_file.close()
        return overall_compare_failed

    @staticmethod
    def rows_not_found_report(row_not_found_dict, datastore_name=None, interval_date=None, interval_time=None, file_name=None):
        """
        Prints the Rows Not found report for a dictionary of row number keys. Additionally prints out the datastore
        name, interval_date, and/or interval time if requested.
        :param row_not_found_dict: Required - a dictionary of key/value pairs where the keys are row numbers.
        :param datastore_name: Optional - if specified will print a line identifying what datastore the rows not found
        :param interval_date: Optional - if specified will print a line identifying the interval date
        :param interval_time: Optional - if specified will print a line identifying the interval time
        :param file_name: location and name of where to write the report header to.
        :return: Nothing
        """
        list_of_rows = ""
        current_date_time_object = datetime.datetime.now()
        report_title = current_date_time_object.strftime('%Y-%m-%d')
        report_title += '          Rows Not Found Report          '
        report_title += current_date_time_object.strftime('%H:%M:%S')
        title_len = len(report_title)
        dashes = '-' * title_len

        if file_name is None:
            print('\n%s' % dashes)
            print(report_title)
            if datastore_name is not None:
                print('\nDatastore Name: %s' % datastore_name)
            if interval_date is not None:
                print('\nInterval Date: %s' % interval_date)
            if interval_time is not None:
                print('\nInterval Time: %s' % interval_time)

            for key in row_not_found_dict:
                list_of_rows = list_of_rows + str(key) + ', '

            print(list_of_rows)
        else:
            with open(file_name, mode='a') as user_file:
                user_file.write('\n%s' % dashes)
                user_file.write('\n' + report_title)
                if datastore_name is not None:
                    user_file.write('\nDatastore Name: %s' % datastore_name)
                if interval_date is not None:
                    user_file.write('\nInterval Date: %s' % interval_date)
                if interval_time is not None:
                    user_file.write('\nInterval Time: %s' % interval_time)

                for key in row_not_found_dict:
                    list_of_rows = list_of_rows + str(key) + ', '

                user_file.write('\n' + list_of_rows)

    @staticmethod
    def display_compare_report_header(range_pct, total_rows_compared, title_override=None, file_name=None, special_message=None):
        """
        Prints the header information and title for the data comparison report

        :param special_message: Can contain a special line of output that should be writing out after the standard header
        information.
        :param range_pct: print range percentage used in the comparison.
        :param total_rows_compared: total number of rows that were compared.
        :param title_override: Overrides the default report title used.
        :param file_name: location and name of where to write the report header to.
        """
        current_date_time_object = datetime.datetime.now()
        report_title = current_date_time_object.strftime('%Y-%m-%d')
        if title_override is not None:
            report_title += '          ' + title_override + '          '
        else:
            report_title += '          Data Comparison Report          '
        report_title += current_date_time_object.strftime('%H:%M:%S')
        title_len = len(report_title)
        dashes = '-' * title_len
        CommonNav.println(dashes, file_path=file_name, timestamp=False)
        CommonNav.println(report_title, file_path=file_name, timestamp=False)
        if special_message is not None:
            CommonNav.println(special_message, file_path=file_name, color_state='warning', timestamp=False)
        if range_pct is not None:
            CommonNav.println('\nRange Percentage used with integer and/or time data types: %s%%' % range_pct, file_path=file_name, timestamp=False)
            if 'Aggregate' in report_title:
                CommonNav.println('Total number of rows aggregated: %s' % total_rows_compared, file_path=file_name, timestamp=False)
            else:
                CommonNav.println('Total number of rows compared from current_interval data: %s' % total_rows_compared, file_path=file_name, timestamp=False)
        # if file_name is None:
        #     print('\n%s' % dashes)
        #     print(report_title)
        #     if range_pct is not None:
        #         print('\nRange Percentage used with integer and/or time data types: %s%%' % range_pct)
        #         print('Total number of rows compared: %s' % total_rows_compared)
        # else:
        #     with open(file_name, mode='a') as user_file:
        #         user_file.write('\n%s' % dashes)
        #         user_file.write('\n' + report_title)
        #         if range_pct is not None:
        #             user_file.write('\n\nRange Percentage used with integer and time data types: %s%%' % range_pct)
        #             user_file.write('\nTotal number of rows compared: %s\n' % total_rows_compared)

    def add_column_to_result_set(self, new_column_name, length, pos, page, data_type):
        """
        Adds a new column and column info object to the current result sets columns dictionary

        :param new_column_name: Name of the column to be used as the dictionary key
        :param length: integer that is the max length of the data that can be contained in the column
        :param pos: position on the screen where the column data started on the Product screen
        :param page: number of scroll right actions to bring that column up on the product display
        :param data_type: what kind of data is in the column represented as a string (i.e. 'int', 'string', 'percent', or 'time')
        :return: True - new column key and its Column Info object has been added.
                 False - A key already exists in the columns dict with the new column name given.
        """

        if new_column_name not in self.columns:
            column_obj = ColumnInfo(new_column_name, length, pos, page, data_type)
            self.columns[new_column_name] = column_obj
            return True
        else:
            return False

    def sql_text_report_header(self,  for_plan=None, for_program=None, user_text_supplied=False, report_type='static'):
        """
        Prints the Header for the SQL Text report.
        :param for_plan: If supplied adds the 'Plan:' report line with the plan name supplied.
        :param for_program: If supplied adds the 'Program:' report line with the program name supplied.
        :param user_text_supplied: Indicate True or False to have the 'User Supplied Text' column added to the report.
        :return: True - Result set being used to call this method is definitely a statement level result set so the
                        header was successfully printed.
                False - The result set instance used to call this method is not a statement level result set.
        """
        if self.check_result_set_type('statement'):
            sql_call_obj = self.columns.get('SQL_CALL')
            assert isinstance(sql_call_obj, ColumnInfo)
            if report_type == 'static':
                sql_text_title = '                     Static SQL Text Captured Report'
            else:
                sql_text_title = '                     Dynamic SQL Text Captured Report'
            Results.display_compare_report_header(None, sql_call_obj.total_number_of_rows(), title_override=sql_text_title, file_name=self.output_file)
            if for_plan is not None:
                add_plan_line = "{}:  {}\n"
                add_plan_line = add_plan_line.format('PLAN', for_plan.ljust(8))
                CommonNav.println(add_plan_line, file_path=self.output_file)
            if for_program is not None:
                add_prog_line = "{}:  {}\n"
                add_prog_line = add_prog_line.format('PROGRAM', for_program.ljust(8))
                CommonNav.println(add_prog_line, file_path=self.output_file)

            max_len = 25
            try:
                for text in self.columns.get('TEXT').data.values():
                    if len(text) > max_len:
                        max_len = len(text)
            except AttributeError:
                pass

            if not user_text_supplied:
                report_col_line = "{} {} {} {}"
                report_col_line = report_col_line.format('SQL_CALL'.ljust(8), 'STMT#'.ljust(8), 'SECT#'.ljust(8), 'TEXT CAPTURED BY PRODUCT'.ljust(8))
                report_col_sep = "{} {} {} {}"
                report_col_sep = report_col_sep.format('-'.ljust(8, '-'), '-'.ljust(8, '-'), '-'.ljust(8, '-'), '-'.ljust(max_len, '-'))
            else:
                report_col_line = "{} {} {} {} {}"
                report_col_line = report_col_line.format('SQL_CALL'.ljust(8), 'STMT#'.ljust(8), 'SECT#'.ljust(8),
                                                         'TEXT CAPTURED BY PRODUCT'.ljust(max_len), 'MATCHED USER SUPPLIED TEXT'.ljust(max_len))
                report_col_sep = "{} {} {} {} {}"
                report_col_sep = report_col_sep.format('-'.ljust(8, '-'), '-'.ljust(8, '-'), '-'.ljust(8, '-'),
                                                       '-'.ljust(max_len, '-'), '-'.ljust(max_len, '-'))

            CommonNav.println(report_col_line, self.output_file)
            CommonNav.println(report_col_sep, self.output_file)
            return True
        else:
            error_message = 'ERROR - This method can only be used on a statements level result set.'
            CommonNav.println(error_message, self.output_file)
            return False

    def sql_text_report(self, statement_result_set_check=True):
        """
        Creates a report of SQL text for a statement so to see what Text was obtained for each row of a statement result
        set.
        :param statement_result_set_check: Specify False to skip the check that ensures dealing with a statement result
        set type. If check is skipped its possible a Traceback Exception can occur. Suggestion only skipping when this
        method call directly follows the :py :class Results :method sql_text_report_header call.
        :return:
        """
        if statement_result_set_check:
            check_rc = self.check_result_set_type('statement')
            if not check_rc:
                error_message = 'ERROR - This method can only be used on a statements level result set.'
                CommonNav.println(error_message, self.output_file)
                return
        else:
            check_rc = True

        if check_rc:
            sql_call_obj = self.columns.get('SQL_CALL')
            assert isinstance(sql_call_obj, ColumnInfo)
            for row, sql_call_val in sql_call_obj.data.items():
                user_text = " ".ljust(1)
                if 'MATCHED USER TEXT' in self.columns and self.get_row_data('MATCHED USER TEXT', row) != 'None':
                    report_line = "{} {} {} {} {}"
                    user_text = self.get_row_data('MATCHED USER TEXT', row).ljust(len(self.get_row_data('MATCHED USER TEXT', row)))
                else:
                    report_line = "{} {} {} {}"

                if 'TEXT' in self.columns:
                    max_len = 25
                    for text in self.columns.get('TEXT').data.values():
                        if len(text) > max_len:
                            max_len = len(text)
                    statement_text = self.get_row_data('TEXT', row).ljust(max_len)
                else:
                    statement_text = " ".ljust(1)

                report_line = report_line.format(sql_call_val.ljust(8), self.get_row_data('STMT#', row).ljust(8),
                                                 self.get_row_data('SECT#', row).ljust(8), statement_text, user_text)
                CommonNav.println(report_line, self.output_file)
            return True

    def check_result_set_type(self, result_type):
        """

        :return:
        """

        result_set_type_dict = {'plan': 'PLANNAME', 'program': 'PROGRAM', 'statement': 'SQL_CALL', 'database': 'DBNAME',
                                'spacename': 'SPACENAM', 'table': 'TABLENAME'}
        if result_type in result_set_type_dict:
            column_name = result_set_type_dict.get(result_type)
            if column_name in self.columns:
                return True
            else:
                return False
        else:
            error_message = "Result type request of '%s' is not a none result set type. Choose from either 'plan', " \
                            "'program', 'statement', database, spacename, or table." % result_type
            CommonNav.println(error_message, file_path=self.output_file)
            return False
