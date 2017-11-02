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
from Tcp import *
# required for the scheduler
logging.basicConfig()
GObject.threads_init()
Gst.init(None)

class Bandwidth_base():
    SERVER_OR_PLAYER = None
    SNIFF_IP = None
    SNIFF_PORT= None
    SNIFF_TIME= None
    TIME_START= None

    def time_start(self):
        return datetime.now()

    def after_counting_algo(self,count):
        print(count)

    def __init__(self):
        print("object created")

    def start(self):
        def count_udp():
            global count
            count = 0
            print("def count_udp")

            def pkt_callback(pakets):
                global count
                count += 1
                print("def callback")

            print("before sniffing")
            packets = sniff(lfilter=pkt_callback, filter='udp and host 192.168.11.40 and port 5000', store=0, timeout=1)
            print("after sniffing")
            # main brain of the function
            self.after_counting_algo()
            schedule_run.add_job(count_udp)

        schedule_run = BlockingScheduler()

        def start_sched(datetime):
            print("Program started in", datetime)
            schedule_run.add_job(count_udp)

        time_start = self.time_start()
        print(time_start)
        schedule_run.add_job(start_sched, 'date', run_date=time_start, args=[time_start])
        schedule_run.start()

        def on_error(self, bus, msg):
            print('on_error():', msg.parse_error())
