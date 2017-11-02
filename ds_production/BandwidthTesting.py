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

    def after_counting_algo(self):
        pass

    def set_up_socket(self,test_tcp):
        pass

    def __init__(self, server_or_player, sniff_IP, sniff_PORT, sniff_TIME):
        self.SERVER_OR_PLAYER = server_or_player
        self.SNIFF_IP= sniff_IP
        self.SNIFF_PORT= sniff_PORT
        self.SNIFF_TIME= sniff_TIME


    def start(self):

        # initialize the socket to sent and receive messages
        test_tcp = self.set_up_socket()

        # get the time to start the application
        self.TIME_START=self.time_start(test_tcp)
        print(self.TIME_START)

        # count the packages to the specific ip and port for the set amount of time
        def count_udp():
            global count
            count = 0
            def pkt_callback(pakets):
                global count
                count += 1
            packets = sniff(lfilter=pkt_callback, filter='udp and host '+self.SNIFF_IP+' and port '+self.SNIFF_PORT, store=0, timeout=1)



            # main brain of the function
            self.after_counting_algo(count,test_tcp)

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



class Bandwidth (Bandwidth_base):
    def __init__(self, server_or_player, sniff_IP, sniff_PORT, sniff_TIME):
        Bandwidth_base.__init__(self, server_or_player, sniff_IP, sniff_PORT, sniff_TIME)


    def start(self):
        Bandwidth_base.start(self)

    def time_start(self,test_tcp):
        if(self.SERVER_OR_PLAYER=="1"):
            time_start = test_tcp.get_msg()
            return time_start

        elif(self.SERVER_OR_PLAYER=="0"):
            time = SyncTime.get_time_now()
            test_tcp.send_msg(time)
            return time

    def set_up_socket(self):
        if(self.SERVER_OR_PLAYER=="1"):
            test_tcp_server = TcpProt('', 3345, 1024)
            test_tcp_server.start(1)
            return test_tcp_server

        else:
            test_tcp_client = TcpProt('', 3345, 1024)
            test_tcp_client.start(0)
            return test_tcp_client








    def after_counting_algo(self,count, test_tcp):
        if(self.SERVER_OR_PLAYER=="1"):
            try:
                test_tcp.get_msg()
                if(test_tcp.get_msg==''):
                    print("no messages")
                else:
                    print("The client producet ",test_tcp.get_msg())
            except :
                print("No packages from Client, waiting...")
                test_tcp.get_msg()

        elif(self.SERVER_OR_PLAYER=="0"):
            try:
                print("Packages sent to the Server", count)
                test_tcp.send_msg(count)
            except :
                print("Cannot send packages, retrying...")
                test_tcp.send_msg(count)





    def on_error(self, bus, msg):
        Bandwidth_base.on_error(self)









