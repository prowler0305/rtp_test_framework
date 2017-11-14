from core.Detector_nav import NavPdt
from core.Psa_nav import NavPsa
from core.NavRtptest import NavRtptest


class Factory(object):
    """
    Static class containing different factory methods which are separately documented as to there purpose.
    """

    @staticmethod
    def create_nav_class(product_code, lpar, ssid, userid, auto_submit=None, current_datastore=None, current_interval_date=None, current_interval_time=None,
                         current_vcat=None, output_directory=None, debug_mode='N'):
        """
        Creates and returns the appropriate Navigation class needed by interrogating the product_code parameter from the
        JSON input parameters.

        :param product_code: 3 character product code (i.e. PDT or PSA)
        :param lpar:
        :param ssid:
        :param userid:
        :param auto_submit:
        :param current_datastore:
        :param current_interval_date:
        :param current_interval_time:
        :param current_vcat:
        :param output_directory:
        :param debug_mode:
        :return: specific product navigation class instance or ValueError exception thrown
        """

        product_code = product_code.upper()
        if product_code == 'PDT':
            navigation_instance = NavPdt(lpar, ssid, userid, datastore_name=current_datastore,
                                         interval_date=current_interval_date, interval_time=current_interval_time,
                                         vcat=current_vcat, output_file=output_directory, debug_mode=debug_mode)
            return navigation_instance
        elif product_code == 'PSA':
            navigation_instance = NavPsa(lpar, ssid, userid, datastore_name=current_datastore,
                                         interval_date=current_interval_date, interval_time=current_interval_time,
                                         vcat=current_vcat, output_file=output_directory, debug_mode=debug_mode)
            return navigation_instance
        elif product_code == 'RTP':
            navigation_instance = NavRtptest(lpar, ssid, userid, auto_submit, output_file=output_directory, debug_mode=debug_mode)
            return navigation_instance
        else:
            raise ValueError("Product code '%s' not a valid option. Expected 'PDT' or 'PSA'." % product_code)
