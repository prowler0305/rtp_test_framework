from ptg2.common import is_jenkins


class InputParms(object):
    """
    Static class with methods for find and interacting with test input parameters.
    """

    @staticmethod
    def check_override_parm(command_line_overrides, parameter_name):
        """
        Checks to see if the command line contains the requested parameter name indicating an override for a JSON input
        file parameter has been given. Also checks to see that the parameter requested has a value given.
        (i.e. a non "" or None value)
        :param command_line_overrides: dictionary of command line overrides.
        :param parameter_name: name of the parameter to search for in the command line arguments dictionary.
        :return: Returns a tuple:
                    Found and has a value - True, parameters value
                    Not Found or doesn't have a value - False, "" (i.e. empty string cause that is what the value had)
        """
        if parameter_name in command_line_overrides:
            override_value = command_line_overrides.get(parameter_name)
            if override_value != "" and override_value is not None:
                return True, override_value
            else:
                if override_value is not None:
                    InputParms.no_override_value(parameter_name)
                return False, ""
        else:
            return False, ""

    @staticmethod
    def check_json_parm(dict_parms, connection_instance, parameter_name):
        """
        Checks to see if the test parms dictionary from the JSON input file has the requested parameter name indicated.
        Also checks to see that the parameter requested has a value given.
        (i.e. a non "" value)
        :param dict_parms: dictionary of JSON parameters.
        :param connection_instance: instance of the Connection class object.
        :param parameter_name: name of the parameter to search for
        :return: Returns a tuple:
                   Found and has a value - True, parameters value
                   Not Found or doesn't have a value - False, "" (i.e. empty string cause that is what the value had)
        """
        if parameter_name in ('lpar', 'ssid', 'userid', 'ssid2'):
            dictionary_obj = connection_instance.connection
        else:
            dictionary_obj = dict_parms

        if parameter_name in dictionary_obj:
            input_file_value = dictionary_obj.get(parameter_name)
            if input_file_value != "":
                return True, input_file_value
            else:
                return False, ""
        else:
            return False, ""

    @staticmethod
    def no_override_value(parameter_name):
        """
        Prints an informational message for a command line override parameter that was given with no value
        :param parameter_name:
        """
        if is_jenkins():
            return
        else:
            print("Command line override parameter: %s, was giving with no value. Using test level parameter if specified."
                  % parameter_name)

    @staticmethod
    def no_required_parameter(parameter_name):
        """
        Raises a KeyError exception after determining a required parameter has not been found either as an override
        parameter or from the input JSON file.
        :param parameter_name:
        """
        raise KeyError("Input parameter '%s' required but not found in either JSON input file or "
                       "as a command line override." % parameter_name)

    @staticmethod
    def no_optional_parameter(parameter_name, default_value):
        """
        Prints an informational message for a test level optional parameter that was either not specified at all or was
        specified with no value (i.e. " ")
        :param default_value: default value that will be used. (passed in as a string)
        :param parameter_name: Name of the optional parameter
        """
        print("Optional parameter '%s' either not found in JSON input file or provided with no value. Using %s as the "
              "default.\n" % (parameter_name, default_value))

    @staticmethod
    def parameter_value_not_valid(parameter_name, parameter_value, expected_values):
        """

        :param parameter_name:
        :param parameter_value:
        :param expected_values:
        """

        raise ValueError("Value '%s' is not a valid option for parameter '%s'. Valid values are '%s'." %
                         (parameter_value, parameter_name, expected_values))

    @staticmethod
    def get_options_parm_value(options_dictionary, parameter_to_find):
        """
        Finds a parameter inside an additional dictionary JSON object and returns its value.

        Example:

        "tests":
          [
            {
              "test_type": "rtptest",
              "product_code": "RTP",
              "execute_method": "UI",
              "action": "5",
              "auto_submit": "N",
              "include_plan": "Y",
              "options":
              {
                "program": "reg021sr",
                "collid": "mycollidisbigger"
              }
            }
          ]

        The "options" parameter in the JSON is a "tests" parameter that defines another dictionary of additional
        parameters. This routine can return the value for one of the embedded dictionary parameters (i.e. "program"
        or "collid")

        :param options_dictionary: dictionary of JSON parameters and their values.
        :param parameter_to_find: Name of the parameter to find (must be of type string)
        :return: Value of the parameter requested or bool(False)
        """

        return options_dictionary.get(parameter_to_find, False)
