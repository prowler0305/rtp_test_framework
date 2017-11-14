import sys
from core.Builder import Builder
from core.common import CommonNav


def main(args):
    """
    :param args: input arguments passed in from the command line.
    """

    test_rc = True
    # create Parse input class instance
    input_arg_dict = Builder.parse_input_parameters()
    if "file" in input_arg_dict:
        connection_node, tests_node = Builder.parse_json_input(input_arg_dict.get('file'))
        if input_arg_dict.get('p') is not None:
            Builder.description_output(tests_node, input_arg_dict)
            test_rc = True
        else:
            connection_obj = Builder.build_connection(connection_node, input_arg_dict)

            list_o_tests = Builder.build_tests(tests_node, input_arg_dict, connection_obj)
            for this_test in list_o_tests:
                status_str = str(type(this_test).__name__)
                test_status, output_file = this_test.execute_test()
                if test_status:
                    status_str += " - Passed"
                    CommonNav.println(status_str, file_path=output_file, color_state='success')
                else:
                    status_str += " - Failed"
                    CommonNav.println(status_str, file_path=output_file, color_state='error')
                    test_rc = False

    if not test_rc:
        return False


if __name__ == '__main__':
    rc = main(sys.argv[1:])
    sys.exit(rc)
