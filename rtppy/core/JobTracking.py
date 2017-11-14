import collections

import time
from ptg2 import zos
from ptg2.context import use_system
from ptg2.zos.jes import Job, find_dd_for_exec_pgm
from ptg2.zos.jesutil import StartedTask
from core.BaseTest import BaseTest


class JobTracking(object):
    """
    Instance class that provides services to interact with started tasks and batch jobs.

    Typical usage:

    .. code-block:: python

    from core.Factories import Factory

        nav_rtptest = Factory.create_nav_class(product_code=self.product_code, lpar=self.connection.get_lpar(),
                                                       ssid=self.connection.get_ssid(), userid=self.connection.get_userid(),
                                                       auto_submit=self.auto_submit, debug_mode=self.debug_mode)

         nav_rtptest.start_test_suite()

        rc, self.jobinfo = self.process_option_6(nav_rtptest)

    """

    def __init__(self, use_lpar, jobid=None, jobname=None):
        """
        
        :param use_lpar: Name of the Lpar. This is typically the same LPAR in which the script is executing on (Required)
        :param jobid: ID of the batch job or started task of which to get an instance for. Can use this or jobname. 
        :param jobname: Name of the batch job or started task of which to get an instance for. Can use this or jobid.
        """
        self.use_lpar = use_lpar
        self.jobid = jobid
        self.jobname = jobname
        self.job_handle = None
        self.jobfile = None
        self.jcl_log = None
        self.started_task = None

        self.__set_job_handle()

    def __set_job_handle(self):
        """
        Set the job_handle needed for when other methods in this class are used. 
        :return: 
        """
        # if instance was created with no jobid, then we must be dealing with a started task so we need to get the jobid
        if self.jobid is None:
            self.started_task = StartedTask(self.jobname, system=self.use_lpar)
            if self.started_task.is_running():
                self.jobid = self.started_task.jobid
            else:
                raise Exception("Started Task by name '%s' is not running on indicated lpar '%s' "
                                % (self.jobname, self.use_lpar))

        with use_system(self.use_lpar):
            self.job_handle = Job.get(str(self.jobid))

    def wait_till_job_complete(self):
        """
        Waits for a job to complete before returning. Messages are issued by PTG2 not this method.
        :return: Nothing
        """
        self.job_handle.wait_for_job()

    def update_job_status(self):
        """

        :return:
        """
        self.job_handle.update()

    def get_job_step_return_codes(self, list_o_steps):
        """
        Takes a list of step names in order of execution and obtains their return codes and returns them in an
        ordered dictionary to ensure dictionary represents step execution order.
        :param list_o_steps:
        :return: dictionary of step names and return codes
        """
        stepname_rc_dict = collections.OrderedDict()

        for step_name in list_o_steps:
            stepname_rc_dict[step_name] = self.job_handle.step_result(step=step_name)
        return stepname_rc_dict

    def get_job_message_log(self, update=False):
        """
        If not an "update" request gets the initial contents of the job spool file at the time of the call. If an update
        request is being made then gets the information added to the log since the last time this method was called.
        
        :return: Sets the class instance variable for access to the information.  
        """
        if update:
            return self.jobfile.added_lines()
        else:
            self.jobfile = self.job_handle.get_spool_file("JES2.JESMSGLG")

    def get_job_jcl_log(self):
            """
            Gets the entire contents of the jobs JESJCL log

            :return: Sets the class instance variable for access to the information.
            """
            self.jcl_log = self.job_handle.get_spool_file("JES2.JESJCL")

    def print_message_log(self, log_to_print=None):
        """
        Prints the contents of the log requested or defaults to printing the the whole updated message log from the job
        at the time this method is called.

        :param log_to_print: 
        :return: 
        """
        if log_to_print is None:
            if self.jobfile is None:
                self.get_job_message_log()

            for line in self.jobfile:
                print(line)
        else:
            for line in log_to_print:
                print(line)

    def search_whole_message_log(self, what_to_find):
        """
        Searches for a string in the whole output file obtained. Be careful of usage as this method can return TRUE
        if string looking for is not unique and repeats as searches the contents of the log when called from the 
        beginning.
        :param what_to_find: the string to find in the message log. 
        :return: True if found or False if not.
        """

        if self.jobfile.contains(what_to_find):
            return True
        else:
            return False

    def find_print_found_message_from_log(self, what, use_log=None, print_message=True):
        """
        Finds the string(i.e. what) given in a log file and if found prints the matching string from the log file given.
        
        This method can be useful to validate a message exists and print its contents for visualization in a whole log 
        file or just the updated part since the last time the log was accessed.
        
        Example:
        
        
        
        :param what: string to be found
        :param use_log: If provided searches the log file object given otherwise searches the whole jobfile object.
        :param print_message: Defaults to True in which if the message and the 'what' matches all or part of the message
                              then its printed. Set to False if no print wanted.
        :return: the matching line in the log or None if not found
        """

        if use_log is None:
            for line in self.jobfile:
                if what in line:
                    if print_message:
                        print(line)
                    return line
            return None
        else:
            for line in use_log:
                if what in line:
                    if print_message:
                        print(line)
                    return line
            return None

    def find_dii_address(self, log_to_search=None):
        """
        Finds the address where PDT DII was loaded after successful PDT collection initialization by finding the
        PDT0182 message and extracting the ADDR= value.

        :param log_to_search: If provided searches the log file object given otherwise searches the whole jobfile object.
        :return:
        """

        if log_to_search is None:
            search_log = self.jobfile
        else:
            search_log = log_to_search

        diiaddr_message = self.find_print_found_message_from_log('PDT0182', use_log=search_log, print_message=False)

        if diiaddr_message is not None:
            addr_start = str(diiaddr_message).find('ADDR=') + 5
            addr_end = str(diiaddr_message).find('FLAG', addr_start)
            dii_address = diiaddr_message[addr_start:addr_end]
            return dii_address
        else:
            return None

    def get_list_dsn_for_dd(self, dd_name, pgm_name):
        """
        Uses PTG2 method to return list of DSN for a DD concatenation.

        :param dd_name: name of the DD to look at (e.g. "STEPLIB", "PTIPLIB", etc...)
        :param pgm_name: name of the program (i.e. PGM=PXMINICC) on the EXEC.
        :return: list of dataset names.
        """
        return find_dd_for_exec_pgm(self.jcl_log.read(), pgm_name, dd_name)

    def search_all_loadlibs_for_mem(self, dd_name, pgm_name, request_member):
        """
        Finds and searches all the datasets in a DD concatenation for the member requested and returns the first loadlib
        DSN it was found in.

        :param dd_name: name of the DD to search. i.e. STEPLIB, PTILIB, etc...
        :param request_member: Member name to search for (e.g. PDTDIUC1, PDTDIIC2, etc...)
        :return: first loadlib DSN where member was found.
        """
        if self.jcl_log is None:
            self.get_job_jcl_log()

        ds_name_list = find_dd_for_exec_pgm(self.jcl_log.read(), pgm_name, dd_name)

        for single_ds_name in ds_name_list:
            for dsn_member in zos.listmembers(single_ds_name):
                if dsn_member == request_member:
                    return single_ds_name

    def find_message_with_timer(self, what, duration, print_timer=True):
        """


        :param what:
        :param duration:
        :param print_timer:
        :return:
        """

        wait_for = 5
        total_wait = 0

        if duration < wait_for:
            wait_for = duration

        while True:
            updated_log = self.get_job_message_log(update=True)
            # self.print_message_log(log_to_print=updated_log)
            if self.find_print_found_message_from_log(what, use_log=updated_log):
                return updated_log
            else:
                BaseTest.countdown_timer(wait_for, watch_timer=print_timer)
                total_wait = wait_for + total_wait
            if total_wait > duration:
                return None
