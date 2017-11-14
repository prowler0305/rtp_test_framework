import collections
import time


class ColumnInfo(object):
    """
    ColumnInfo represents the information and methods for a column extracted from a dynamic data area
    """
    data_type_dict = {'PLANNAME': 'string', 'COMMIT': 'int', 'ABORT': 'int', 'SQL': 'int', 'TIMEPCT': 'percent',
                      'CPUPCT': 'percent', 'INDB2_TIME': 'time', 'INDB2_CPU': 'time', 'GETPAGE': 'int', 'GETPFAIL': 'int',
                      'SYNCREAD': 'int', 'SPFETCH': 'int', 'LPFETCH': 'int', 'DYNPFETCH': 'int', 'PFPAGES': 'int',
                      'PAGEUPDT': 'int', 'IMWRITE': 'int', 'REOPT': 'int', 'FETCHED': 'int', 'INSERTED': 'int',
                      'UPDATED': 'int', 'DELETED': 'int', 'PSC_MATCH': 'int', 'PSC_NMATCH': 'int', 'PSC_IPREP': 'int',
                      'PSC_KDPREP': 'int', 'DYN_PARSED': 'int', 'DYN_REPLAC': 'int', 'DYN_MATCHE': 'int',
                      'DYN_DUP': 'int', 'RID_USED': 'int', 'RID_FSTG': 'int', 'RID_FLIM': 'int', 'RID_OVRFLW': 'int',
                      'RID_LIMIT': 'int', 'JOIN_SWITC': 'int', 'JOIN_LMTD': 'int', 'IX_SKIPPED': 'int',
                      'DRAINREQ': 'int', 'DRAINFAIL': 'int', 'CLAIMREQ': 'int', 'CLAIMFAIL': 'int', 'DEADLOCK': 'int',
                      'TIMEOUT': 'int', 'ESCALSHR': 'int', 'ESCALEXC': 'int', 'LOCKSUS': 'int', 'LATCHSUS': 'int',
                      'OTHERSUS': 'int', 'LOCKREQ': 'int', 'UNLKREQ': 'int', 'CHANGREQ': 'int', 'QUERYREQ': 'int',
                      'OTHERREQ': 'int', 'GLOCKREQ': 'int', 'GCHNGREQ': 'int', 'GUNLKREQ': 'int', 'GIRLMSUS': 'int',
                      'GXESSUS': 'int', 'FALSESUS': 'int', 'GLOCKFAIL': 'int', 'XESLOCKREQ': 'int', 'XESCHNGREQ': 'int',
                      'XESUNLKREQ': 'int', 'PMAXDEG': 'int', 'PGROUPS': 'int', 'PPLANNED': 'int', 'PREDUCED': 'int',
                      'PFAILCUR': 'int', 'PFAILSRT': 'int', 'PFAILBUF': 'int', 'PFAILENC': 'int', 'SPPLANNED': 'int',
                      'SPFAILBUF': 'int', 'SPFAILCNO': 'int', 'SPFAILRRRS': 'int', 'IO_WTIME': 'time', 'IOWCNT': 'int',
                      'LOCK_WTIME': 'time', 'LOCKWCNT': 'int', 'ORIO_WTIME': 'time', 'ORIOWCNT': 'int',
                      'OWIO_WTIME': 'time', 'OWIOWCNT': 'int', 'SERV_WTIME': 'time', 'SERVWCNT': 'int',
                      'ARCH_WTIME': 'time', 'ARCHWCNT': 'int', 'LATCH_WTIME': 'time', 'LATCHWCNT': 'int',
                      'PLATCH_WTIME': 'time', 'PLATCHWCNT': 'int', 'DRAIN_WTIME': 'time', 'DRAINWCNT': 'int',
                      'CLAIM_WTIME': 'time', 'CLAIMWCNT': 'int', 'ARCRD_WTIME': 'time', 'ARCRDWCNT': 'int',
                      'SMSG_WTIME': 'time', 'SMSGWCNT': 'int', 'GLOCK_WTIME': 'time', 'GLOCKWCNT': 'int',
                      'LOG_WTIME': 'time', 'LOGWCNT': 'int', 'LOB_WTIME': 'time', 'LOBWCNT': 'int', 'OCS_WTIME': 'time',
                      'OCSWCNT': 'int', 'SLS_WTIME': 'time', 'SLSWCNT': 'int', 'DSS_WTIME': 'time', 'DSSWCNT': 'int',
                      'OTS_WTIME': 'time', 'OTSWCNT': 'int', 'PLOCK_WTIME': 'time', 'PLOCKWCNT': 'int',
                      'LLOCK_WTIME': 'time', 'LLOCKWCNT': 'int', 'AT_WTIME': 'time', 'AT_WCNT': 'int',
                      'SP_TOT_CPU': 'time', 'SP_DB2_CPU': 'time', 'SP_TCB_WAIT': 'time', 'SP_TOT_TIME': 'time',
                      'SP_DB2_TIME': 'time', 'SP_CLS1_ZIIP': 'time', 'SP_CLS2_ZIIP': 'time', 'NP_TOT_TIME': 'time',
                      'NP_TOT_CPU': 'time', 'NP_ZIIP_CPU': 'time', 'SP_SQL_CNT': 'int', 'UDF_TOT_CPU': 'time',
                      'UDF_DB2_CPU': 'time', 'UDF_TCB_WAIT': 'time', 'UDF_TOT_TIME': 'time', 'UDF_DB2_TIME': 'time',
                      'UDF_CL1_ZIIP': 'time', 'UDF_CL2_ZIIP': 'time', 'NF_TOT_TIME': 'time', 'NF_TOT_CPU': 'time',
                      'NF_ZIIP_CPU': 'time', 'UDF_SQL_CT': 'int', 'TR_MAIN_TIME': 'time', 'TR_MAIN_CPU': 'time',
                      'TR_MAIN_ZIIP': 'time', 'TR_NEST_TIME': 'time', 'TR_NEST_CPU': 'time', 'TR_NEST_ZIIP': 'time',
                      'UNACC_TIME': 'time', 'ZONCP_CPU': 'time', 'ZIIP_CPU': 'time', 'CL2_ZIIP_CPU': 'time',
                      'XML_MAX_ST': 'int', 'AA_TIME': 'time', 'AA_CNT': 'int', 'PLANCNT': 'int', 'PROGRAM': 'string',
                      'TYPE': 'string', 'CONTOKEN': 'string', 'PLCNT': 'int', 'COLLID': 'string', 'VERSION': 'string',
                      'SQL_CALL': 'string', 'STMT#': 'string', 'SECT#': 'string', 'SQL_TEXT': 'string',
                      'USE_COUNT': 'int', 'KEY': 'string', 'OPID': 'string', 'EXCEPTIONS': 'int', 'CORRID': 'string',
                      'SQLCODE': 'string', 'ERRORCNT': 'int', 'USERS': 'int', 'PROGRAMS': 'string',
                      'LASTDATE': 'string', 'LASTTIME': 'string', '1STDATE': 'string', '1STTIME': 'string',
                      'COUNT': 'int', 'CONNID': 'string', 'TIME': 'string', 'AUTHID': 'string', 'SQLERRD1': 'int',
                      'SQLERRD2': 'int', 'SQLERRD3': 'int', 'SQLERRD4': 'int', 'SQLERRD5': 'int', 'SQLERRD6': 'int',
                      'WARNING': 'string', 'TABLENAME': 'string', 'DBNAME': 'string', 'PCTGP': 'percent',
                      'PCTRIO': 'percent', 'PCTWIO': 'percent', 'PCTFIO': 'percent', 'BUFHIT': 'percent',
                      'SYNC_RIO': 'int', 'ASYN_RIO': 'int', 'ASYN_RPG': 'int', 'ASYN_RPI': 'percent', 'SYNC_WIO': 'int',
                      'ASYN_WIO': 'int', 'ASYN_WPG': 'int', 'ASYN_WPI': 'percent', 'FMT_WIO': 'int',
                      'TS_BUFHIT': 'percent', 'TS_GETPAGE': 'int', 'TS_SYNCRIO': 'int', 'TS_ASYNRIO': 'int',
                      'TS_ASYNRPG': 'int', 'TS_ASYNRPI': 'percent', 'TS_SYNCWIO': 'int', 'TS_ASYNWIO': 'int',
                      'TS_ASYNWPG': 'int', 'TS_ASYNWPI': 'percent', 'TS_FMTWIO': 'int', 'IS_BUFHIT': 'percent',
                      'IS_GETPAGE': 'int', 'IS_SYNCRIO': 'int', 'IS_ASYNRIO': 'int', 'IS_ASYNRPG': 'int',
                      'IS_ASYNRPI': 'percent', 'IS_SYNCWIO': 'int', 'IS_ASYNWIO': 'int', 'IS_ASYNWPG': 'percent',
                      'IS_FMTWIO': 'int', 'TS_CNT': 'int', 'TS_DSN': 'int', 'TS_EXT': 'int', 'TB_CNT': 'int',
                      'IS_CNT': 'int', 'IS_DSN': 'int', 'IS_EXT': 'int', 'SPACENAM': 'string', 'BPID': 'string',
                      'DBID': 'string', 'PSID': 'string', 'TSNAME': 'string', 'TB_GETPAGE': 'int', 'ICT': 'int',
                      'CREATOR': 'string', 'TSID': 'string', 'TBID': 'string', 'TB_SEQU': 'int', 'TB_INDX': 'int',
                      'TB_LINK': 'int', 'SEQPCT': 'percent', 'IDXPCT': 'percent', 'LNKPCT': 'percent',
                      'PCTIGP': 'percent', 'VOLUME': 'string', 'UNIT': 'string', 'PCTDIO': 'percent',
                      'RESPTIM': 'percent', 'TOTAL_IO': 'int', 'DB2_IO': 'int', 'FORMAT_WIO': 'int',
                      'PENDING': 'percent', 'CONNECT': 'percent', 'DISCONN': 'percent', 'IOQUEUE': 'percent',
                      'IOQTIME': 'percent', 'IOQCUR': 'percent', 'IOQAVG': 'percent', 'IOQMAX': 'percent',
                      'VP_ALLOC': 'string', 'GETPAGE_SQ': 'int', 'SYNCRIO_SQ': 'int', 'PF_REQ': 'int', 'PF_IO': 'int',
                      'PF_PGS': 'int', 'PF_PIO': 'int', 'SPF_REQ': 'int', 'SPF_IO': 'int', 'SPF_PGS': 'int',
                      'SPF_PIO': 'percent', 'LPF_REQ': 'int', 'LPF_IO': 'int', 'LPF_PGS': 'int', 'LPF_PIO': 'percent',
                      'DPF_REQ': 'int', 'DPF_IO': 'int', 'DPF_PGS': 'int', 'DPF_PIO': 'percent', 'BUF_UPDATE': 'int',
                      'PAGING_RIO': 'int', 'PAGING_WIO': 'int', 'DMTH': 'int', 'PFDISAB': 'int', 'WIOENGN': 'int',
                      'GPFAIL': 'int', 'EXPFAIL': 'int', 'IOPQCUT': 'int', 'IOPOTHR': 'int', 'HSMTIMO': 'int',
                      'VP_SIZE': 'string', 'VPSEQ': 'int', 'IOPSQ': 'int', 'DWTH': 'int', 'VDWTH': 'int',
                      'VP_TYPE': 'string', 'GBPID': 'string', 'CON': 'string', 'GBPSIZE': 'string', 'SREAD': 'int',
                      'SREAD_DATA': 'int', 'SREAD_NODT': 'int', 'SREAD_XI': 'int', 'SREAD_XIDT': 'int',
                      'SREAD_XINO': 'int', 'RPL_REQ': 'int', 'AREAD_RPL': 'int', 'SWRTE': 'int', 'SWRTE_CHG': 'int',
                      'SWRTE_CLN': 'int', 'AWRTE': 'int', 'AWRTE_CHG': 'int', 'AWRTE_CLN': 'int', 'CASTOUT': 'int',
                      'CAST_PAGES': 'int', 'CAST_AVGPG': 'percent', 'OTHER_REQ': 'int', 'REG_PAGE': 'int',
                      'UNREQ_PAGE': 'int', 'CHKPT': 'int', 'UNLKCAST': 'int', 'READCLAS': 'int', 'READSTAT': 'int',
                      'DELNAME': 'int', 'READDIRI': 'int', 'SEC_DELNAM': 'int', 'SEC_DELNLS': 'int',
                      'SEC_READST': 'int', 'WRTE_NOSTG': 'int', 'SEC_WNOSTG': 'int', 'SEC_WSUSP': 'int',
                      'STRUCTURE': 'string', 'GBPPAGES': 'int', 'DIRENTRY': 'int', 'DIRPAGES': 'int', 'DATPAGES': 'int',
                      'DIRRATIO': 'int', 'GBPCACHE': 'string', 'CLASST': 'int', 'GBPOOLT': 'int', 'GBPCHKPT': 'int',
                      'RATIO': 'int', 'AUTOREC': 'string', 'PND_CACH': 'string', 'PND_RATO': 'int', 'READ': 'int',
                      'READ_HIT': 'int', 'READ_MISS': 'int', 'READ_DIFND': 'int', 'READ_DIADD': 'int',
                      'READ_DISUP': 'int', 'READ_NSTG': 'int', 'WRITE': 'int', 'WRITE_HIT': 'int', 'WRITE_MISS': 'int',
                      'WRITE_CHG': 'int', 'WRITE_CLN': 'int', 'WRITE_UNXI': 'int', 'WRITE_NSTG': 'int',
                      'WRITE_NREG': 'int', 'WRITE_INVS': 'int', 'RECLAIM_DI': 'int', 'RECLAIM_DT': 'int',
                      'XI_RECLAIM': 'int', 'XI_WRITE': 'int', 'XI_NAMINV': 'int', 'XI_COMPINV': 'int',
                      'XI_LOCCACH': 'int', 'CHGPAGES': 'int', 'IS_ASYNWPI': 'percent', 'DSNCNT': 'int', 'EXTCNT': 'int',
                      'TSTY': 'string', 'PCTTGP': 'percent'}

    """ Initializes the Column Info Object"""
    def __init__(self, name, length, column_pos, page, data_type):
        self.name = name
        self.data_type = data_type
        self.length = length
        self.column_pos = column_pos  # relative to first field pos (i.e. '_')
        self.page = page  # starting from 1
        self.data = collections.OrderedDict()

    def display_col_info(self, display_type='print', file_name=None, print_mode='w', new_line=True, output_file_obj=None,
                         column_data=False):
        """
        Either displays to the screen or writes to a file all the information about a column info object.

        :param display_type: Valid data are 'print' or 'write' - Defaults to 'print'
        :param file_name: Name of the file to write to if display_type is 'write' otherwise exception raised
        :param print_mode: How to print to the file (2 choices)
                                'w' - write - Default (existing file with same name will be replaced)
                                'a' - append (add data to the existing file name)
        :param new_line: True(default) - prints the information starting on a new line
                         False         - appends the information to the previous printed line separated by a space " ".
         :param column_data: If True includes column name information when printing or writing.

        Usage example:
        --------------
        Use the get() method on the columns dictionary of the Result class instance to get the column info object
        (value) of the column key "CPUPCT":
                col_obj = result.columns.get('CPUPCT')

        Call the column info object display() method:
                col_obj.display_col_info()

        Result:
                Name: CPUPCT DataType: None Length: 7 Page: 1 ScreenPos: 61
        """
        if display_type not in ('print', 'write'):
            print('Display type %s not a valid option, defaulting to ''print''' % display_type)

        if display_type == 'write':
            if file_name is None and output_file_obj is None:
                raise ValueError("Display type of '%s' requires a file name or file object to be provided." % display_type)
            elif file_name is not None and output_file_obj is not None:
                raise ValueError("Provided either 'file_name' or 'output_file_obj' but not both")

            if output_file_obj is None:
                user_file = open(file_name, print_mode)
            else:
                user_file = output_file_obj

            if new_line:
                if column_data:
                    user_file.write("\nName: %s, DataType: %s, Length: %s, Page: %s, ScreenPos: %s" %
                                    (self.name, self.data_type, self.length, self.page, self.column_pos))
                else:
                    user_file.write("\nName: %s" % self.name)
            else:
                if column_data:
                    user_file.write(" Name: %s, DataType: %s, Length: %s, Page: %s, ScreenPos: %s" %
                                    (self.name, self.data_type, self.length, self.page, self.column_pos))
                else:
                    user_file.write("\nName: %s" % self.name)

            # If output_file_obj wasn't provided then we opened a file so we should close it otherwise its callers
            # responsibility
            if output_file_obj is None:
                user_file.close()
        else:
            if new_line:
                if column_data:
                    print("Name: %s, DataType: %s, Length: %s, Page: %s, ScreenPos: %s" %
                          (self.name, self.data_type, self.length, self.page, self.column_pos))
                else:
                    print("Name: %s" % self.name)
            else:
                if column_data:
                    print("Name: %s, DataType: %s, Length: %s, Page: %s, ScreenPos: %s" %
                          (self.name, self.data_type, self.length, self.page, self.column_pos), end='')
                else:
                    print("Name: %s" % self.name, end='')

    def add_column_value(self, row_num, value):
        """
        Adds the row number (key) and the data (value) to the column info objects data{} dictionary.

        :param row_num: Row number on the display the data is on (should be passed as 0 based number)
        :param value: data for that row
        """
        row_num += 1
        self.data[row_num] = value

    def total_number_of_rows(self):
        """
        Returns the total number of data rows for a column info object
        """
        return len(self.data)

    def get_row_value(self, row_num):
        """
        Gets the data (value) for a given row (key) from the column info object dictionary.
        :param row_num: Row number (1 based) to retrieve data for.
        :return: columns row value (i.e data) in the appropriate format (i.e. string, integer, etc..)
        """
        if self.get_column_data_type() == 'int':
            return int(self.data.get(row_num))
        else:
            return str(self.data.get(row_num))

    def get_row_number(self, value_to_find):
        """
        Returns the row number (key) from the column info object data dictionary for a specific value.
        :param value_to_find: Value to find the row number for.
        :return: Row number (i.e key).
        """
        for key, value in self.data.items():
            if value == value_to_find:
                return key

    def get_all_col_info(self):
        """
        Returns the column information for a specific column name in a tuple

        :return: tuple of columns information (name, length, position, page, data type)
        """
        info_tuple = (self.name, self.length, self.column_pos, self.page, self.data_type)
        return info_tuple

    def get_column_name(self):
        """
        Returns the name of a column

        really not sure needed since knowing the column name is needed to get info unless can be used
        to retrieve a name of a column using an index number could be useful. e.g. col_info_object.keys()[1]

        :return: column name
        """
        return self.name

    def get_column_length(self):
        """
        Returns the length of a column

        :return: length of column
        """
        return self.length

    def get_column_pos(self):
        """
        Returns the position of the column name
            Note: the position is relative to the first input field in the dynamic display row

        :return: position of column name
        """
        return self.column_pos

    def get_column_page(self):
        """
        Returns the page number the column is on

        :return: page number
        """
        return self.page

    def get_column_data_type(self):
        """
        Returns the columns data type
        :return: data type (e.g. 'string', 'int', etc)
        """
        return self.data_type

    def display_row_data(self, row, display_type='print', file_name=None, print_mode='w', new_line=True, output_file_obj=None):
        """
        Prints the requested column info objects row data.

        :param row: row of data to print (1 based)
        :param display_type: Valid data are 'print' or 'write' - Defaults to 'print'
        :param file_name: Name of the file to write to if display_type is 'write' otherwise exception raised
        :param print_mode: How to print to the file (2 choices)
                                'w' - write - Default (existing file with same name will be replaced)
                                'a' - append (add data to the existing file name)
        :param new_line: True(default) - prints the information starting on a new line
                         False         - appends the information to the previous printed line separated by a space " ".
        :return: prints the requested column info objects row data
        """
        if display_type not in ('print', 'write'):
            print("Display type %s is not a valid option, defaulting to 'print'" % display_type)

        if display_type == 'write':
            if file_name is None and output_file_obj is None:
                raise ValueError("Display type of '%s' requires a file name or a file object to be provided." % display_type)
            elif file_name is not None and output_file_obj is not None:
                raise ValueError("Provided either 'file_name' or 'output_file_obj' but not both")

            if output_file_obj is None:
                user_file = open(file_name, print_mode)
            else:
                user_file = output_file_obj

            if new_line:
                user_file.write('\nRow: %s  Data: %s' % (row, self.get_row_value(row)))
            else:
                user_file.write(' Row: %s  Data: %s' % (row, self.get_row_value(row)))

            # If output_file_obj wasn't provided then we opened a file so we should close it otherwise its callers
            # responsibility
            if output_file_obj is None:
                user_file.close()

        else:
            if new_line:
                print('Row: %s  Data: %s' % (row, self.get_row_value(row)))
            else:
                print(' Row: %s  Data: %s' % (row, self.get_row_value(row)), end=''),

    def aggregate_data(self, other_col_info_obj=None, data_to_cause_aggregate_skip=None):
        """

        :param other_col_info_obj: Optional, can pass another columns column info object if needed. This is useful if while
                                    aggregating data certain rows need to be skipped based on the data in another column of
                                    the result set.

        :param data_to_cause_aggregate_skip: Required if other_col_info_obj parameter used. List of 1 or more values from
                                             the other_col_info_obj to match on to cause the current row to be skipped and
                                             not added in the aggregation.

        :return: returns the aggregated sum or zero.
        """

        """
        - Initialize the aggregate_sum variable to either a int or float depending on the columns data type.
        - for every row in the data dictionary (i.e. for all the rows of data for that column)
            - get the data for that row key.
            - if columns data type is 'time'
                - convert the possible up to DD:HH:MM:SS.ssssss value into total seconds
                - add the time value into the aggregate_sum variable
            - if the columns data type is 'percent'
                - split the percent data on the percent sign (%) so we have just a float.
                - add the float value into the aggregate_sum variable.
            - else we have an integer value which is a straight summation into the aggregate_sum variable

        """

        if self.data_type is 'time':
            aggregate_sum = 0.000000
        elif self.data_type is 'percent':
            aggregate_sum = 0.00
        else:
            aggregate_sum = 0

        for row in self.data:
            skip_row = False
            if other_col_info_obj is not None:
                for skip_value in data_to_cause_aggregate_skip:
                    if other_col_info_obj.get_row_value(row) == skip_value:
                        skip_row = True
                        break
            if skip_row:
                continue
            data = self.get_row_value(row)
            if self.data_type is 'string':
                return data  # Caller is nuts for calling a aggregate method with a string, just return the string.
            elif self.data_type is 'time':
                # convert the time value to total seconds and add into sum
                total_seconds = self.convert_time_string(data)
                aggregate_sum += total_seconds
            elif self.data_type is 'percent':
                percent_split_list = data.split('%')
                aggregate_sum += float(percent_split_list[0])
            else:  # data type is straight integer type
                aggregate_sum += data

        return aggregate_sum

    def compare_values(self, other_col_obj, row, other_row, range_pct=0):
        """
        Compares two pieces of data of types integer, time, or string for the current result set and a passed in
        baseline result set.

        :param other_col_obj: instance of :py:class ColumnInfo representing the other metric data
        :param row: current result set row being processed
        :param other_row: row in the other result set that matches.
        :param range_pct: Default behavior, indicated by default of 0, indicates comparison of two data should be
                          exactly equal.

                          Can override default with a percentage number to use to calculate the plus or minus range
                          (i.e. 10) the current value is allowed to be within of the baseline value.

        :return:    True - current value is within percentage range
                    False - current value is not within percentage range
        """
        if self.get_column_data_type() is 'int':
            baseline_val = other_col_obj.get_row_value(other_row)
            if self.get_row_value(row) == baseline_val:
                return True

            if range_pct == 0:
                if self.get_row_value(row) == baseline_val:
                    return True
                else:
                    return False
            else:
                floor = ColumnInfo.l_bound(baseline_val, range_pct)
                ceil = ColumnInfo.u_bound(baseline_val, range_pct)

                if floor < self.get_row_value(row) < ceil:
                    return True
                else:
                    return False

        elif self.get_column_data_type() is 'time':
            # Get both column info objects row time data as strings
            current_time_data = self.get_row_value(row)
            baseline_time_data = other_col_obj.get_row_value(other_row)

            # convert the times to total number of seconds for comparison
            baseline_total_seconds = self.convert_time_string(baseline_time_data)
            current_total_seconds = self.convert_time_string(current_time_data)

            if current_total_seconds == baseline_total_seconds:
                return True

            if range_pct == 0:
                if current_total_seconds == baseline_total_seconds:
                    return True
                else:
                    return False
            else:
                # calculate the low and high boundary range
                floor = ColumnInfo.l_bound(baseline_total_seconds, range_pct)
                ceil = ColumnInfo.u_bound(baseline_total_seconds, range_pct)

                # See if the other columns time data is within range
                if floor < current_total_seconds < ceil:
                    return True
                else:
                    return False

        elif self.get_column_data_type() is 'string':
            if self.get_row_value(row) == other_col_obj.get_row_value(other_row):
                return True
            else:
                return False

        elif self.get_column_data_type() is 'percent':
            # Get the row data replacing the % sign with ' ' and extract the data without any spaces into a list
            temp_current_list = str.split(str.replace(self.get_row_value(row), '%', ' '))
            temp_baseline_list = str.split(str.replace(other_col_obj.get_row_value(other_row), '%', ' '))
            # Convert data from list to float
            current_percent_data = float(temp_current_list[0])
            baseline_percent_data = float(temp_baseline_list[0])
            if current_percent_data == baseline_percent_data:
                return True

            if range_pct == 0:
                if current_percent_data == baseline_percent_data:
                    return True
                else:
                    return False
            else:
                # calculate the low and high boundary range
                floor = ColumnInfo.l_bound(baseline_percent_data, range_pct)
                ceil = ColumnInfo.u_bound(baseline_percent_data, range_pct)

                if floor < current_percent_data < ceil:
                    return True
                else:
                    return False
        else:
            print('\nData type - "%s" for column name - %s is not a known data type ' % (self.get_column_data_type(),
                  self.get_column_name()))
            return None

    def convert_time_string(self, time_string):
        """
        Converts a time data string in the format up to DD:HH:MM:SS.ssssss into a float
        e.g.(total seconds.fractional seconds)
        :param time_string: a string in a time format up to DD:HH:MM:SS.ssssss
        :return: converted time string as float - total seconds.fractional seconds
        """

        # split time on the '.' for later (e.g. 12:34:56.123456)
        time_data_split = str.split(time_string, '.')
        # Convert the left side of the '.' to total number of seconds (i.e. time string up to DD:HH:MM:SS)
        total_seconds = self.convert_time_to_total_seconds(time_data_split[0])
        # Put the total seconds and fraction seconds back together as 1 string.
        total_seconds = '{0}.{1}'.format(str(total_seconds), time_data_split[1])
        # return total seconds as a float
        return float(total_seconds)

    @staticmethod
    def convert_time_to_total_seconds(time_data):
        """
        Converts a time to total number of seconds.

        :param time_data: a time value in the format in the range DD:HH:MM:SS to MM:SS
        :return: time value in total number of seconds
        """

        # Determine if the time string has HH:MM:SS or just MM:SS. Then split the string into a struct_time tuple
        # (HH, MM, SS) or (MM, SS) so we can do the appropriate math to convert the time into total number of seconds
        if len(str.split(time_data, ':')) == 2:
            time_tuple = time.strptime(time_data, '%M:%S')
            total_seconds = (time_tuple.tm_min * 60) + time_tuple.tm_sec
        else:
            time_tuple = time.strptime(time_data, '%H:%M:%S')
            total_seconds = (time_tuple.tm_hour * 60) + (time_tuple.tm_min * 60) + time_tuple.tm_sec
        # TODO: add in possibility for time value to be DD:HH:MM:SS
        return total_seconds

    @staticmethod
    def l_bound(value, range_pct):
        """
        Calculates the low end of the range percentage

        :param value: baseline data to use
        :param range_pct: range percentage to use
        :return: low end range value
        """
        return value - ColumnInfo.base(value, range_pct)

    @staticmethod
    def u_bound(value, range_pct):
        """
        Calculates the upper end of the range percentage

        :param value: baseline data to use
        :param range_pct: range percentage to use
        :return: upper end range value
        """
        return value + ColumnInfo.base(value, range_pct)

    @staticmethod
    def base(val, pct):
        """
        Calculates the percentage of a number

        :param val: number to calculate percentage of
        :param pct: percentage to calculated
        :return: calculated percent
        """
        return (val * pct) / 100
