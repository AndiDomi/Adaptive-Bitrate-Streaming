#!/usr/bin/env python3
import datetime
import os
import socket
import time
import logging
import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
from gi.repository import GLib
# scheduler library for the application
from apscheduler.schedulers.blocking import BlockingScheduler
# scrap packages to count them library
from scapy.all import *
# fetch O-time class
from FetchTime import *
from Tcp import TcpProt

# required for the scheduler
logging.basicConfig()
GObject.threads_init()
Gst.init(None)


class Bandwidth_base():
    SERVER_OR_PLAYER = None
    SNIFF_IP = None
    SNIFF_PORT = None
    SNIFF_TIME = None
    TIME_START = None

    # start tcp sockets for server

    def time_start(self):
        pass

    def set_up_socket(self, test_tcp):
        pass

    def after_counting_algo(self):
        pass

    def __init__(self, server_or_player, sniff_IP, sniff_PORT, sniff_TIME, tcp_send_ip):
        self.SERVER_OR_PLAYER = server_or_player
        self.SNIFF_IP = sniff_IP
        self.SNIFF_PORT = sniff_PORT
        self.SNIFF_TIME = sniff_TIME
        self.TCP_SEND_IP = tcp_send_ip

    def start(self):
        # initialize the socket to sent and receive messages
        test_tcp = self.set_up_socket()

        # get the time to start the application
        self.TIME_START = self.time_start(test_tcp)
        print(self.TIME_START)

        # count the packages to the specific ip and port for the set amount of time
        def count_udp():
            global count
            count = 0

            def pkt_callback(pakets):
                global count
                count += 1

            packets = sniff(lfilter=pkt_callback,
                            filter='udp and host ' + self.SNIFF_IP + ' and port ' + self.SNIFF_PORT, store=0, timeout=1)

            # main brain of the function
            self.after_counting_algo(count, test_tcp)

            # start everything
            schedule_run.add_job(count_udp)

        schedule_run = BlockingScheduler()

        def start_sched(datetime):
            print("Program started in 3 seconds!")
            schedule_run.add_job(count_udp)

        time_start = self.TIME_START
        schedule_run.add_job(start_sched, 'date', run_date=time_start, args=[time_start])
        schedule_run.start()

        def on_error(self, bus, msg):
            print('on_error():', msg.parse_error())
