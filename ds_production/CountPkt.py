import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from scapy.all import *
## install pcapy
## install libdnet
from ds_production.FetchTime import *

from Tcp import TcpProt

class CountPackets:

    FILTER_IP = None
    FILTER_PORT = None
    DELAY_SECONDS = None
    SERVER = None
    SCHEDULE = BlockingScheduler()
    TIME_START = None

    def __init__(self, filter_ip, filter_port, delay_seconds, server_port, server_buffer):
        self.FILTER_IP = filter_ip
        self.FILTER_PORT = filter_port
        self.DELAY_SECONDS = delay_seconds
        logging.basicConfig()

        ###################################################
        #server = TcpProt("", server_port, server_buffer)
        #server.connect(1)
        #self.SERVER = server
        ###################################################
    def start_counting_server(self):
        print ("run_counting")

        # todo : change this
        # take the time for synch
        #time_start = self.SERVER.get_msg()
        #self.TIME_START = time_start
        ########################################
        ######
        time_start = SyncTime.get_time_now()
        ######
        print(" The program will start to monitor the packages at: ", self.TIME_START)

        # method to count the packages
        def count_udp():
            print ("count_udp")
            # initialize and reset the count var
            global count
            count = 0

            # function called for every package
            # count how many packages are filtered
            def pkt_callback(pakets):
                global count
                count += 1

            # conf for raspberry pi
            packets = sniff(lfilter=pkt_callback, filter='udp and host '+self.FILTER_IP+' and port'+self.FILTER_PORT, store=0, timeout=self.DELAY_SECONDS)

            # todo: fix this for server or player
            #rec_packages = self.SERVER.get_msg()
            ######################################
            rec_packages = 1

            # if package is 0
            if not rec_packages:
                # wait for a reconnection
                self.SERVER.connect(1)
                self.TIME_START = self.SERVER.get_msg()

                # start everything
                schedule_run.add_job(start_scheduler, 'date', run_date=self.TIME_START, args=[self.TIME_START])
                rec_packages = '0'

            if rec_packages == '0':
                difference_sent_received_packages = 0
            else:
                # the difference between packages sent and received
                difference_sent_received_packages = count - int(rec_packages)

            # test the output
            # TODO remove
            print (str(count) + " - " + str(rec_packages) + " = " + str(difference_sent_received_packages))
            # recursive running of the count_udp method
            schedule_run.add_job(count_udp)

        ##### create schedule object
        schedule_run = BlockingScheduler()

        # function to start for the first time count_udp method
        def start_scheduler(datetime):
            print ("Program started in", datetime)
            schedule_run.add_job(count_udp)

        # start everything
        schedule_run.add_job(start_scheduler, 'date', run_date=self.TIME_START, args=[self.TIME_START])
        schedule_run.start()

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())