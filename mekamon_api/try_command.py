import logging
import sys
import socket
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
import sys
import time

import config
from utils import unhexlify
from motion_controller import MotionController


ble = BLERadio()



logging_format = '%(asctime)s : %(filename)s : %(levelname)s : %(message)s'
logging_level = logging.INFO
logging.basicConfig(format=logging_format, level=logging_level)
logging.info("Running %s", " ".join(sys.argv))

# logging.info('Initializing Mekamon UDP listener on %s:%s' % (config.UDP_IP_ADDRESS,
#         config.UDP_PORT_NO))
# serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# serverSock.bind((config.UDP_IP_ADDRESS, config.UDP_PORT_NO))

def get_connection(ble):
  uart_connection = None
  for adv in ble.start_scan(timeout = 20):
    print("found something")
    print(adv.complete_name)
    if "Meka" in adv.complete_name:
      uart_connection = ble.connect(adv)
      break
  ble.stop_scan()
  return uart_connection

def try_command(command):
  uart_connection = None
  while True:
    if not uart_connection: 
      print("Trying to connect...")
      uart_connection = get_connection(ble)


    if uart_connection and uart_connection.connected:
      mekamon_uart = uart_connection[UARTService]

      motion_controller = MotionController(mekamon_uart)
      motion_controller.pwn_mekamon()
      motion_controller.set_height("height,%d" % (config.default_height))
      time.sleep(2)
      mekamon_uart.write(unhexlify(command))
      break

if __name__ == "__main__":
  try_command(sys.argv[1])