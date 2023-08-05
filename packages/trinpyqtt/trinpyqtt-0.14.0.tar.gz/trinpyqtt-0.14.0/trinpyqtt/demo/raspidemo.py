import os
import glob
import ssl
from trinpyqtt.client import TrinClient
import trinpyqtt.models.raspberrypi as model
import trinpyqtt.tools.constants as MSG_CODES
from time import sleep

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    f.close()
    return lines


def read_temp():
    temp_c = None
    lines = read_temp_raw()
    attempt = 3
    while lines[0].strip()[-3:] != 'YES' and attempt > 0:
        attempt = attempt - 1
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
    return temp_c


# This is used to identify to origin of the messages on the Smart Platform
# It can also called asset id or peripheral id and can be any value, as long as
# it is unique on this particular TrinClient instance. When you want to
# track data and events published from this app, or use Smart to send commands
# to this app, you need to create an 'asset' on Smart with this as
# it's asset id.
APP_ID = 'my_app_id'

# The MQTT broker you are connecting to
HOST = 'mqtt.trintel.co.za'


# A simple sample RPC
# Given some numbers return their sum
def sum_these(*args):
    code = MSG_CODES.SUCCESS
    try:
        reply = sum(list(args))
    except Exception as ex:
        reply = 'NAC {ex}'.format(ex=ex)
        code = MSG_CODES.F_EXCEPTION
    return code, reply


# A map of local valid RPCs
RPC_MAP = {
    'sum_these': sum_these
}


# The TrinClient is the primary receiver of all messages from the broker,
# and filter those to only expose commands related to this app to be sent to
# this app. A command receiver dictionary can be passed in during construction
# that will map the handling function in your app to its id.
# It is guaranteed that the normalised data that arrives here has been vetted
# for correctness. If the nld data key "code" has any value other than
# a 0 (zero), the given message had errors when vetted.
# NLD: {
#       'command': {'sum_these': [123, 345]},
#       'code': 0,
#       'type': 'c',
#       'tct': 'tct',
#       'user_data': None,
#       'ts': 0
# }
def process_msg(client, nld, topic, payload, sender_id,
                sender_aid,
                sender_tct_returned):
    print("""Received message:
    Topic: {topic}
    Payload: {payload}
    NLD: {nld}
    SENDER_ID: {sender}
    SENDER_AID: {sender_aid}
    SENDER_TCT_RETURN {sender_tct_returned}
    """.format(
        topic=topic,
        payload=payload,
        nld=nld,
        sender=sender_id,
        sender_aid=sender_aid,
        sender_tct_returned=sender_tct_returned,
    ))

    # The code will be 0 if the message parse OK
    if nld['code'] >= 0:
        if nld['type'] == 'c':
            tct = nld['tct']
            func = None
            result = None
            code = MSG_CODES.F_NO_RPC
            args = []
            for rpc in RPC_MAP.keys():
                if rpc in nld['command']:
                    func = RPC_MAP[rpc]
                    args = nld['command'][rpc]
                    break

            if func:
                # noinspection PyBroadException
                try:
                    code, result = func(*args)
                except Exception as ex:
                    code = MSG_CODES.F_EXCEPTION

            if tct:
                client.publish_reply(tct, code, result, target=sender_id)

        if nld['type'] == 'x':
            print('We received a reply')


# Instantiate the client
# When 'use_rtc' is set to True the local time on this system will be used
# when publishing. When set to false, the server will use the time it
# receives the message as the canonical timestamp.
daily = 60 * 60 * 24
tc = TrinClient(
    clean_session=False,
    model=model,          # The type of hardware this is running on. Required
    host=HOST,            # One of Trinity's Smart-MQTT broker urls
    port=1883,
    pdr_interval=daily,   # Ditto for 'device' data messages
    ping_interval=60,     # Set the standard MQTT keepalive (PINGREQ) interval
    use_rtc=False,)       # Let the server manage timestamps

# This can be called once for each 'Asset' on this client.
tc.register_command_receiver(APP_ID, process_msg)

# Un-comment this to enable debug logging
tc.enable_logger(logger)

tc.tls_set('./ca3650.crt', tls_version=ssl.PROTOCOL_TLSv1_2)

# Start the client.
tc.run()
sleep(10)

# Simply keep the process running, and publish data ever so often
counter = 0
while True:

    # Once a minute read the temperature
    temp = read_temp()
    temp_payload = {'temp': temp}

    # Once every 15 minutes publish the temperature
    if not divmod(counter, 15)[1]:
        tc.publish_data(temp_payload, pid=APP_ID)
        tc.log('This is published: ', obj=temp_payload)

    counter += 1
    sleep(60)
