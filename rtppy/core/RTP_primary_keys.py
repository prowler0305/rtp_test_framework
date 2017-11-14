import collections


class RtpPrimaryKeys(object):
    """
    Static class used to build dictionary of primary keys.
    """

    @staticmethod
    def get_primary_key_dict(panel_id):
        """
        Returns the primary key dictionary associated with the panel id. Each panel id contains the primary key(s)
        associated with it in which the value for each key is defaulted to " ".

        :param panel_id: products 8 character panel id
        :return: dictionary of primary keys with their data set to a " "
        """

        if panel_id == 'PDTO0062':
            stmt_level_key_dictionary = collections.OrderedDict([("SQL_CALL", " "), ("PROGRAM", " "), ("STMT#", " "),
                                                               ("COLLID", " "), ("CONTOKEN", " ")])
            return stmt_level_key_dictionary
        elif panel_id == 'PDTO0014':
            stmt_level_key_dictionary = collections.OrderedDict([("SQL_CALL", " "), ("STMT#", " "), ("SECT#", " ")])
            return stmt_level_key_dictionary
        elif panel_id == 'PDTO0015' or panel_id == 'PDTO0013' or panel_id == 'PDTY0013':
            pkge_level_key_dictionary = collections.OrderedDict([("PROGRAM", " "), ("TYPE", " "), ("CONTOKEN", " "),
                                                               ("COLLID", " ")])
            return pkge_level_key_dictionary
        elif panel_id == 'PDTO0012' or panel_id == 'PDTY0014':
            plan_level_key_dictionary = collections.OrderedDict([("PLANNAME", " ")])
            return plan_level_key_dictionary
        elif panel_id == 'PDTV0011':
            key_summary_key_dictionary = collections.OrderedDict([("KEY", " ")])
            return key_summary_key_dictionary
        elif panel_id == 'PDTQ0044' or panel_id == 'PDTQ0047' or panel_id == 'PDTQ0049' or panel_id == 'PDTQ0029':
            dynamic_sql_level_key_dictionary = collections.OrderedDict([("SQL_TEXT", " "), ("SQL_CALL", " "), ("STMT#", " "),
                                                                        ("SECT#", " ")])
            return dynamic_sql_level_key_dictionary
        elif panel_id == 'PDTY0012' or panel_id == 'PDTY0002':
            exception_sql_user_key_dictionary = collections.OrderedDict([("OPID", " ")])
            return exception_sql_user_key_dictionary
        elif panel_id == 'PDTY0015':
            exception_sql_corrid_key_dictionary = collections.OrderedDict([("CORRID", " ")])
            return exception_sql_corrid_key_dictionary
        elif panel_id == 'PDTY0016':
            exception_sql_collid_key_dictionary = collections.OrderedDict([("COLLID", " ")])
            return exception_sql_collid_key_dictionary
        elif panel_id == 'PSAL0202':
            database_activity_summary_key_dictionary = collections.OrderedDict([("DBNAME", " ")])
            return database_activity_summary_key_dictionary
        elif panel_id == 'PSAL0286':
            spacename_activity_summary_key_dictionary = collections.OrderedDict([("SPACENAM", " "), ("DBNAME", " ")])
            return spacename_activity_summary_key_dictionary
        elif panel_id == 'PSAL0085' or panel_id == 'PSAL0285' or panel_id == 'PSAL0287' or panel_id == 'PSAL0288':
            table_activity_summary_key_dictionary = collections.OrderedDict([("DBNAME", " "), ("TSNAME", " "), ("TABLENAME", " ")])
            return table_activity_summary_key_dictionary
        elif panel_id == 'PSAL0280':
            db_table_activity_summary_key_dictionary = collections.OrderedDict([("TSNAME", " "), ("TABLENAME", " ")])
            return db_table_activity_summary_key_dictionary
        else:
            raise TypeError('No primary key dictionary exists for panel ID %s.' % panel_id)
