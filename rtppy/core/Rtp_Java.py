import os
import subprocess
import platform
import errno


class RtpJava(object):

    @staticmethod
    def execute_rtpj(test, userid=None, ssid=None, log=None, library=None, sync=True):
        """
        Executes a specific RTPJ test file.
        :param test: The RTPJ test name.  The test must be present in the RTPJ jar file.
        :param userid: A userid test override.
        :param ssid: A DB2 subsystem test override.
        :param log: The log level override.
        :param library: The json test file override location.
        :param sync: Determines if the process should be synchronous or asynchronous
        :return: RTPJ return code. (0 - success, -1 - error)
        """

        # Setup the required environment variables
        env = dict(os.environ)

        if 'RTP_HOME' in env:
            home = env['RTP_HOME']
        else:
            raise ValueError("The RTP_HOME environment variable is not set.")

        if 'JDBC_DRIVERS' in env:
            jdbc = env['JDBC_DRIVERS']
        else:
            raise ValueError("The JDBC_DRIVERS environment variable is not set.")

        # Check and set the java classpath
        rtpj = home + os.sep + 'rtpj' + os.sep + 'target' + os.sep + 'rtpj-1.0-SNAPSHOT.jar'
        if os.path.isfile(rtpj):
            env['CLASSPATH'] = jdbc + os.sep + '*' + os.pathsep + rtpj + os.pathsep
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), rtpj)

        # Initialize basic arguments
        args = ['java', 'com.ca.rtp.core.JsonTestRunner', test]

        # Append specific program arguments
        if userid is not None:
            args.append('--USERID=' + userid)

        if ssid is not None:
            args.append('--SSID=' + ssid)

        if log is not None:
            args.append('--LOG=' + log)

        if library is not None:
            args.append('--LIBRARY=' + library)

        # Save current directory
        current_dir = os.getcwd()
        # Change into target jar directory
        os.chdir(home + os.sep + 'rtpj' + os.sep + 'target')

        # Execute the java program

        if sync:
            rc = subprocess.call(args, env=env, shell=False)
            os.chdir(current_dir)

            # Convert the rc to a signed int
            try:
                rc = RtpJava.int32(rc)
            except OverflowError:
                rc = -1
        else:
            rc = subprocess.Popen(args, env=env, shell=False)

        return rc

    @staticmethod
    def int32(x):
        """
        Convert "unsigned" int value to a signed int.
        :param x: value to be converted
        :return: the signed integer value
        """
        if x > 0xFFFFFFFF:
            raise OverflowError
        if x > 0x7FFFFFFF:
            x = int(0x100000000-x)
            if x < 2147483648:
                return -x
            else:
                return -2147483648
        return x
