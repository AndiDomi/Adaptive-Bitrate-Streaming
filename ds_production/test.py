from Tcp import TcpProt
import time




test_tcp_server = TcpProt('191.168.11.42', 5060, 1024)
test_tcp_server.start(1)

def run():
    time.sleep(1)
    print(test_tcp_server.get_msg())
    run()
run()