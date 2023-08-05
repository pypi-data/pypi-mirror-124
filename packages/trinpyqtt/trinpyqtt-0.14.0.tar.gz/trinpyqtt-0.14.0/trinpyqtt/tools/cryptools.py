from Cryptodome.Hash import SHA1
from binascii import unhexlify
import base64
import struct
import time
import datetime
import os
import errno
import json
# noinspection PyCompatibility
from http.client import HTTPSConnection
from base64 import b64encode


def get_now_timestamp():
    d = datetime.datetime.now()
    return int(time.mktime(d.timetuple()))


def to_little_endian(i):
    return struct.pack('<I', i)


def get_salt():
    sys_ts = int(get_now_timestamp())
    return to_little_endian(sys_ts)


def hash_password(password):
    salt = get_salt()
    sha1 = SHA1.new()
    sha1.update(salt + password)
    s1 = salt + sha1.digest()
    hash_pw = base64.b64encode(s1)
    return hash_pw.decode('utf-8')


def _gen_unit_key(key, cid, uid, msg):

    loc = '/opt/trinity/trinqtt'
    dir_name = os.path.dirname(loc)
    try:
        os.makedirs(dir_name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    if not os.path.exists(loc):
        os.mknod(loc)

    # Write the password
    password = unhexlify(key)
    with open(loc, 'bw+') as f:
        f.write(password)
    f.close()
    os.chmod(loc, 0o644)

    # Write the Customer ID
    cid_loc = loc + '.cid'
    with open(cid_loc, 'w+') as cid_f:
        cid_f.write(cid)
    cid_f.close()
    os.chmod(loc, 0o644)

    print(f"""
Done.
Your Customer ID is: {cid} 
Your UID(Device Unique ID) is: {uid} 
{msg}""")


def _zte_reg(uid, auth, reg_endpoint):
    conn = HTTPSConnection("connect.trintel.co.za")
    payload = ''
    headers = {
        'Authorization': f'Basic {auth}',
    }
    conn.request("GET", f"/api/v3/devices/zte/{uid}/{reg_endpoint}/", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode('utf-8'))
    return data


def _zte_ack(key, cid, uid, auth):
    conn = HTTPSConnection("connect.trintel.co.za")
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    conn.request("PUT", f"/api/v3/devices/zte/{uid}/{key}/", json.dumps({"cid": cid}), headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode('utf-8'))
    return data


def zero_touch_enrollment(uid, auth, reg_endpoint):

    if uid:
        print('UID={u}'.format(u=uid))
        rep = None
        try:
            rep = _zte_reg(uid=uid, auth=auth, reg_endpoint=reg_endpoint)
            if rep:

                # {
                #     "cid": "12345678",
                #     "key": "xxxxxxxxxxxxxxxxxxxxxx",
                #     "kai": 165,
                #     "pdr": 290,
                #     "detail": "Enrolment OK. Please confirm key."
                # }

                err = rep.get('err', None)
                if err:
                    print(err)
                else:
                    cid = rep.get('cid', None)
                    key = rep.get('key', None)
                    kai = rep.get('kai', None)
                    pdr = rep.get('pdr', None)
                    detail = rep.get('detail', None)
                    if cid and key and uid:
                        _gen_unit_key(key, cid, uid, detail)
                        _zte_ack(key, cid, uid, auth)
                    else:
                        print(detail)
        except Exception as x:
            print('Could not register and create password: {x}:{rep}'.format(
                x=x, rep=rep))
    else:
        print('Could not find unit UID or Model ID')


def read_password():
    LOC = '/opt/trinity/trinqtt'
    with open(LOC, 'br') as f:
        pw = f.readline().strip()
    f.close()
    return pw


def read_cid():
    LOC = '/opt/trinity/trinqtt.cid'
    with open(LOC, 'r') as f:
        cid = f.readline().strip()
    f.close()
    return cid


def get_password():
    h = hash_password(read_password())
    return h
