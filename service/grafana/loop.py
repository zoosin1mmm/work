import time
import random
import socket
from common import *

def main():
    grafanaHead = "kv.tracking"
    env = str(raw_input("ENV? ( staging / staging-preview ) ") or "staging")
    domain = "{}.{}.".format(grafanaHead, str(env))
    targets = [
        "delete_data",
        "clear_data",
        "get_data",
        "info_data",
        "set_data"
    ]
    start = 0
    end = int(raw_input("Count? ") or 1)
    value_start = int(raw_input("Value Range(?~)? ") or 1)
    value_end = int(raw_input("Value Range(~?)? ") or 1)

    # calculate timestamp
    now = int(time.time())
    def_timestamp = now - 3600
    timestamp = int(raw_input("timestamp : ") or def_timestamp)
    interval = abs(now - timestamp)
    interval = int(interval / end)

    for x in xrange(start, end):
        timestamp = timestamp + interval
        print "-------------------"
        print "Count: {} Time: {}".format(x, timestamp)
        print "-------------------"
        for target in targets:
            value = random.randint(value_start, value_end)
            graphiteLog(domain + target, value, timestamp)
            print "    Send To \"{}\" Data: {} ".format(domain + target, value)


def graphiteLog(operation, value, timestamp):
    graphitePort = 2003
    graphiteServer = 'tsdb-sink.exosite.com'
    command = "nc {} {} -w 2 -v".format(graphiteServer, graphitePort)
    data = "{} {} {}\n".format(operation, value, timestamp)
    try:
        nc = Popen(command, shell=True, stdin=PIPE,
                   stderr=PIPE, close_fds=True, cwd=".")
        nc.stdin.write(data)
        line = nc.stderr.readline()
        nc.stdin.close()
        nc.wait()
        output = {
            "output": line.strip()
        }
    except IOError as e:
        raise "Grafana Send Data error: {}".format(e)


if __name__ == '__main__':
    main()
