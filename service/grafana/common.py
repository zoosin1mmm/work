import os
# import logging
import codecs
import socket
import time
from subprocess import Popen, PIPE, STDOUT
# logger = logging.getLogger(__name__)


class common(object):

    def __init__(self):
        self.graphiteServer = 'tsdb-sink.exosite.com'
        self.graphitePort = 2003

    # Export DQA_NOGRAPHITE_MODE to bypass all actual logging to graphite.
    def graphiteLog(self, macro="ignore.no_name", value=0, log_time=0):
        try:
            if os.environ['DQA_NOGRAPHITE_MODE']:
                logger.info("graphiteLog(bypassed): %s:%s:%s" %
                            (macro, value, log_time))
                return True
        except Exception, e:
            pass

        if log_time == 0:
            log_time = int(time.time())

        command = "echo \"{} {} {}\" | nc {} {}".format(
            macro, value, log_time, self.graphiteServer, self.graphitePort)
        result = self.commandLine(command=command)

        return result['error'] == None

    def commandLine(self, command, path="."):
        # logger.debug("[%s] > %s\n" % (ctime(), command))
        # print command
        p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,
                  stderr=PIPE, close_fds=True, cwd="%s" % path)
        out, error = p.communicate()
        result = {
            "output": out,
            "error": None
        }
        # logger.debug("Output> %s %s" % (out, error))
        if p.returncode != 0:
            # logger.debug("[%s] > %s\n" % (ctime(), command))
            # logger.debug(error)
            result['error'] = error
        return result
