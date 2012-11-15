#!/usr/bin/env python
#
# hostinfo.py - Script that takes in a single IP address or file
# of IP addresses and prints out information regarding their
# location on the Internet
#
# USAGE: ./hostinfo.py [IP Address | File of IP Addresses]
#
# All code Copyright (c) 2012, Ben Jackson and Mayhemic Labs -
# bbj@mayhemiclabs.com. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of the author nor the names of contributors may be
# used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys, time, dns, ipaddr, socket
from dns import resolver,reversename

private_nets = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '169.254.0.0/16']

def rdns_query(ip):

	try:
		ipaddr.IPAddress(ip)
	except ValueError, e:
		return 'INVALID'

	try:
		resolver = dns.resolver.Resolver()
		resolver.timeout = 1
		ip_addr = reversename.from_address(ip)
		value = str(resolver.query(ip_addr,"PTR")[0]).rstrip('.')
	except dns.exception.Timeout, e:
		value = 'TIMEOUT'
	except dns.resolver.NXDOMAIN, e:
		value = 'NXDOMAIN'
	except dns.resolver.NoAnswer, e:
		value = 'NOANSWER'
	except e:
		value = 'ERROR'

	return value

def fdns_query(host):

	try:
		resolver = dns.resolver.Resolver()
		resolver.timeout = 1
		value = resolver.query(line)
	except dns.exception.Timeout, e:
		value = ['TIMEOUT']
	except dns.resolver.NXDOMAIN, e:
		value = ['NXDOMAIN']
	except dns.resolver.NoAnswer, e:
		value = ['NOANSWER']
	except e:
		value = ['ERROR']

	return value

def network_lookup(ip):
	try:
		ip_array = ip.split('.')
		ip_rev = ip_array[3] + '.' + ip_array[2] + '.' + ip_array[1] + '.' + ip_array[0]

		resolver = dns.resolver.Resolver()
		resolver.timeout = 1

		as_response = str(resolver.query(ip_rev + '.origin.asn.shadowserver.org','TXT')[0]).replace('"','')
		as_values = as_response.split('|')

		for i in range(len(as_values)):
			as_values[i] = as_values[i].strip()

	except dns.exception.Timeout, e:
		as_values = 'TIMEOUT'
	except dns.resolver.NXDOMAIN, e:
		as_values = 'NXDOMAIN'
	except:
		as_values = 'ERROR'

	return as_values;

def is_internal_network(ip):

	for net in private_nets:
		if ipaddr.IPAddress(ip) in ipaddr.IPNetwork(net):
			return 1
	return 0

def is_ip_address(argument):
	try:
		ipaddr.IPAddress(argument)
		return 1
		
	except ValueError:
		return 0

def is_file(argument):
	try:
		f = open(argument, 'r+')
		return 1
	except IOError:
		return 0

f = []

if is_ip_address(sys.argv[1]):
	f.append(['N/A', sys.argv[1]])

elif is_file(sys.argv[1]):
	file = open(sys.argv[1], 'r+')
	for line in file:
		line = str(line).rstrip()

		if (is_ip_address(line)):
			f.append(['N/A', line])
		else:
			answers = fdns_query(line)
			for data in answers:
				f.append([line, str(data)])
else:
	f.append(['N/A', dns.resolver.query(sys.argv[1])])

print "FQDN|IP_Address|Reverse_DNS|AS_Number|AS_Netblock|AS_Name|Country|Domain|ISP"
for line in f:
	host_ip = str(line[1]).rstrip()

	if host_ip == 'N/A':
		print line[0] + '|' + host_ip 
		continue

	value = rdns_query(host_ip)

	if not is_internal_network(host_ip):
		as_info = network_lookup(host_ip)
	else:
		as_info = 'PRIVATE NETWORK'

	if (value):
		sys.stdout.write(line[0] + '|' + host_ip + '|' + value + '|')
	else: 
		sys.stdout.write(line[0] + '|' + host_ip  + '|ERROR|')

	if(type(as_info) is list):
		print as_info[0] + "|" + as_info[1]  + "|" + as_info[2] + "|" + as_info[3] + "|" + as_info[4] + "|" + as_info[5]
	else:
		print as_info

	time.sleep(.5)
