#!/usr/bin/env python3
import os
import socket
import time
import logging
import gi
from flask import Flask, Response, abort

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
from gi.repository import GLib
# scheduler library for the application
from apscheduler.schedulers.blocking import BlockingScheduler
# scrap packages to count them library
from scapy.all import *
# fetch O-time class
from Fetchtime import SyncTime
# required for the scheduler
logging.basicConfig()
GObject.threads_init()
Gst.init(None)
























