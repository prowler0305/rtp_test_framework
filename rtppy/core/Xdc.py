from core.common import CommonNav


class Xdc(object):
    """

    """
    def __init__(self, nav_instance, output_file=None):
        """

        :param nav_instance: instance of :py:class 'RTPNav' that represents the current product navigation.
        :param output_file: Optional - Indicate where screen captures should be written to. Either directory/file
        location specified. Defaults to None which indicates to the console.
        """
        self.nav = nav_instance
        self.output_loc = output_file

    def enter_xdc(self, authorized=True):
        """
        Enters XDC either authorized or non authorized via TSO command. Uses program IEFBR14 for entering.

        :param authorized: Enters xdc non authorized if set to False. Defaults to True
        :return: If successful returns otherwise PTG2 will throw an exception.
        """
        if authorized:
            xdc_tso_command = 'TSO XDCCALLA IEFBR14'
        else:
            xdc_tso_command = 'TSO XDCCALL IEFBR14'

        CommonNav.tso_command(self.nav.ptg2_em, xdc_tso_command, text_to_wait_for='DBC854I z/XDC for z/OS',
                              out_file=self.output_loc)
        return True

    def xdc_find_instruction_set(self, instruction_set, start_search_address):
        """
        Issues the XDC find command for some hex string (i.e. instruction(s)) starting from the address given.

        :param instruction_set:
        :param start_search_address:
        :return: True - number of matches is 1
                 False - number of matches is 0
                 None - problem with find command in general (i.e. syntax errors, etc...)
        """
        self.nav.ptg2_em.screen['xdc'] = 'FIND %s %s' % (instruction_set, start_search_address)
        CommonNav.nav_screen_capture(self.nav.ptg2_em, file_name=self.output_loc)
        self.nav.ptg2_em.app.ispf_submit()
        CommonNav.nav_screen_capture(self.nav.ptg2_em, file_name=self.output_loc)

        if self.nav.ptg2_em.screen.contains('NUMBER OF MATCHES:             1'):
            return True
        elif self.nav.ptg2_em.screen.contains('NUMBER OF MATCHES:             0'):
            return False
        else:
            return None

    def xdc_set_asid(self, asid_identifier):
        """
        Issues the XDC SET ASID command to switch the address space XDC is acting upon. Requires XDC was entered APF Authorized.

        :param asid_identifier: address space id identifier. Can be hex value or jobname (i.e. 02AD or PTXRUN19)
        :return: True or False if SET ASID command was successful
        """
        self.nav.ptg2_em.screen['xdc'] = 'SET ASID %s' % asid_identifier
        self.nav.ptg2_em.submit_screen(wait_for_text='DBC878I ASID SET TO')
        CommonNav.nav_screen_capture(self.nav.ptg2_em, file_name=self.output_loc)
        if self.nav.ptg2_em.screen.contains('DBC878I ASID SET TO'):
            return True
        else:
            return False

    def xdc_zap_on(self, instr_addr_to_zap, zap_value):
        """
        Zap the instruction at the address given with the value given.

        :param instr_addr_to_zap: Address of the byte to zap
        :param zap_value: Hex value to zap the instruction with
        :return: Zap command used if successful or None if failed.
        """
        zap_command = 'ZAP %s=%s' % (instr_addr_to_zap, zap_value)
        self.nav.ptg2_em.screen['xdc'] = zap_command
        CommonNav.nav_screen_capture(self.nav.ptg2_em, file_name=self.output_loc)
        self.nav.ptg2_em.app.ispf_submit()

        if not self.nav.ptg2_em.screen.contains('ZAP %s=' % instr_addr_to_zap):
            return zap_command
        else:
            return None

    def xdc_zap_off(self, instr_addr_to_zap, zap_back_to_byte):
        """
        Zaps the byte given back into the instruction address given.

        :param instr_addr_to_zap: Address of the byte to zap back to the byte value given
        :param zap_back_to_byte: Single byte in hex to zap in.
        :return: Zap off command used if successful or None if failed.
        """
        zap_off_command = 'ZAP %s=%s' %(instr_addr_to_zap, zap_back_to_byte)
        self.nav.ptg2_em.screen['xdc'] = zap_off_command
        CommonNav.nav_screen_capture(self.nav.ptg2_em, file_name=self.output_loc)
        self.nav.ptg2_em.app.ispf_submit()

        if not self.nav.ptg2_em.screen.contains('ZAP %s=' % instr_addr_to_zap):
            return zap_off_command
        else:
            return None

    def xdc_map_command(self, module_name, loadlib):
        """
        Issues the XDC map given the module name and loadlib

        :param module_name: Name of the load module to map
        :param loadlib: Loadlib dataset the module is in.
        :return:
        """
        self.nav.ptg2_em.screen['xdc'] = 'MAP %s,%s' % (module_name, loadlib)
        CommonNav.nav_screen_capture(self.nav.ptg2_em, file_name=self.output_loc)
        self.nav.ptg2_em.submit_screen()
        CommonNav.nav_screen_capture(self.nav.ptg2_em, file_name=self.output_loc)
        if self.nav.ptg2_em.screen.contains('The following maps have been built:'):
            return True
        else:
            return False
