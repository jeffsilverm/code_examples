#! /usr/bin/exec python3
# -*- coding: utf-8 -*-
"""
This program examines packet capture files, looking for IPv4 or IPv6 headers
that have a non-zero value in the DSCP field in the header

Input is a space separated list of pcap filenames
"""
import datetime
import socket
import sys

import dpkt
from dpkt.compat import compat_ord
from typing import Tuple, List


# TC = Traffic Class
# ToS = Type of Service
# DSCP = Differentiated Service Code Point
# The 6 most signigicant bits (MSBs) in byte 1 are DSCP, as defined in RFC 2474
# Note that bit 5 is not used.  This is *not* to be confused with the evil
# bit, RFC 3514
# The 2 LSBs in byte 1 are Explicit Congestion Notification (ECN), as defined
# in RFC 3168

dscp_tab = {0: "best effort",
            8: "priority",
            10: "priority",
            12: "priority",
            14: "priority",
            16: "Immediate",
            18: "Immediate",
            20: "Immediate",
            22: "Immediate",
            24: "Flash voice",
            26: "Flash voice",
            28: "Flash voice",
            30: "Flash voice",
            32: "Flash Override",
            34: "Flash Override",
            36: "Flash Override",
            38: "Flash Override",
            40: "Critical voice RTP",
            46: "Critical voice RTP",
            48: "Internetwork control",
            56: "Network Control"
            }
ecn_tab = {0b00: "Non ECN capable transport",
           0b10: "ECN capable transport 0",
           0b01: "ECN capable transport 1",
           0b11: "Congestion Encountered"
           }


def extract_tos_tc(filename_: str) -> Tuple[List[Tuple], List[Tuple]]:
    """
    :param filename_: The PCAP file to extract the ToS (IPv4) or TC (IPv6) from
    :return: A tuple of lists.  The first list is any IPv4 ToS fields.   The
    second list is any IPv6 TC fields
    """

    # here you can put your code
    fil = open(filename_, "rb")
    git = dpkt.pcap.Reader(fil)

    tos__ipv4 = []
    tc__ipv6 = []
    pkt__ctr = 0

    for timestamp, buf in git:
        pkt__ctr += 1

        print('Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
        # print()
        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)

        # Make sure the Ethernet data contains an IP packet
        ip = eth.data

        # For IPv4
        if isinstance(ip, dpkt.ip.IP):
            tos__ipv4.append((pkt__ctr, ip.tos))
        elif isinstance(ip, dpkt.ip6.IP6):
            tc__ipv6.append((pkt__ctr, ip.fc))
        elif eth.type >= 1536:
            # As of 13-Mar-2019, observed ethertypes include 129 and 3583
            # Per EEE 802.3x-1997, if the ethtype field is 1500 or less, then
            # the ethtype is a length.  If the ethtype field is 1536 or more,
            # then the ethtype field is a type
            print(f"Packet {pkt__ctr} is neither IPv4 nor IPv6. ethtype is: {eth.type}",    # noqa
                file=sys.stderr)
            # See https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml#ieee-802-numbers-1     # noqa
            #

        elif eth.type <= 1500:
            print(f"Packet {pkt__ctr} is using IEEE 802.3 framing",
                  file=sys.stderr)
        else:
            print(f"Packet {pkt__ctr} has an illegal ethtype value: ", eth.type,
                  file=sys.stderr)
    fil.close()
    return tos__ipv4, tc__ipv6


if "__main__" == __name__:
    for filename in sys.argv[1:]:
        print("Working on file " + filename, file=sys.stderr)
        r: Tuple = extract_tos_tc(filename)
        (tos_ipv4, tc_ipv6) = r
        pkt_ctr: int
        for pkt_ctr, pkt_tos in tos_ipv4 + tc_ipv6:
            if pkt_tos != 0:
                # if this ever happens, then I will figure out how to decode
                # the DSCP
                pkt_tos_str = dscp_tab[pkt_tos]
                print(f"Packet {pkt_ctr} in file {filename} has a non-zero ToS or TC!",   # noqa
                    pkt_tos, pkt_tos_str)
        count = len(tos_ipv4) + len(tc_ipv6)
        print(f"Finished with file {filename}, there were {count} packets",
              file=sys.stderr)
