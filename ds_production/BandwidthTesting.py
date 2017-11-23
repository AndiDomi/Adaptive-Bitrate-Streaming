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
from Bandwidth_base import Bandwidth_base
# required for the scheduler
logging.basicConfig()
GObject.threads_init()
Gst.init(None)


class Bandwidth(Bandwidth_base):
    def __init__(self, server_or_player, sniff_ip, sniff_port, sniff_time, tcp_send_ip):
        Bandwidth_base.__init__(self, server_or_player, sniff_ip, sniff_port, sniff_time, tcp_send_ip)

    def start(self):
        Bandwidth_base.start(self)

    def time_start(self, test_tcp):
        if self.SERVER_OR_PLAYER == "SERVER":
            time_start = test_tcp.get_msg()
            return time_start

        elif self.SERVER_OR_PLAYER == "CLIENT":
            time = SyncTime.get_time_now()
            test_tcp.send_msg(time)
            return time

    def set_up_socket(self):
        if self.SERVER_OR_PLAYER == "SERVER":
            test_tcp_server = TcpProt(self.TCP_SEND_IP, 3345, 1024)
            test_tcp_server.start(1)
            return test_tcp_server

        elif self.SERVER_OR_PLAYER == "CLIENT":
            test_tcp_client = TcpProt(self.TCP_SEND_IP, 3345, 1024)
            test_tcp_client.start(0)
            return test_tcp_client



    def after_counting_algo(self, count, test_tcp):
        if self.SERVER_OR_PLAYER == "SERVER":
            print("The client produce ", test_tcp.get_msg())

        elif self.SERVER_OR_PLAYER == "CLIENT":
            print("Packages sent to the Server", count)
            test_tcp.send_msg(count)



    def on_error(self, bus, msg):
        Bandwidth_base.on_error(self)
