import netsnmp
import sys
import argparse


def main():
	snmpget = snmp()
	status=True
	if None in snmpget or 'error' in snmpget or 'timeout' in snmpget or not snmpget:
		status=False
	if status:
		print "\n======================================= TEST CASE RESULT : PASS ====================================="
	else:
		print snmpget
		print "\n======================================= TEST CASE RESULT : FAIL ====================================="
	return status

def snmp():
	parser = argparse.ArgumentParser()
	parser.add_argument("-v","--version",help="version 1 or 2 or 3",choices=[1,2,3],type=int)
	parser.add_argument("-ip","--ip",help="hostname/ip")
	parser.add_argument("-c","--community",help="communit name")
	parser.add_argument("-u","--v3_uname",help="v3 user name")
	parser.add_argument("-x","--privprotocol",help="v3 priv protocol ex:AES")
	parser.add_argument("-X","--privpassword",help="v3 priv password")
	parser.add_argument("-a","--authprotocol",help="v3 auth protocol")
	parser.add_argument("-A","--authpassword",help="v3 auth password")
	parser.add_argument("-l","--level",help="v3 level")
	parser.add_argument("-o","--oid",help="oid to get")
	try:
		args = parser.parse_args()
	except Exception:
		print "error in arguments passed"
	vars = netsnmp.Varbind(args.oid)
	snmpget=[]
	if args.version==2 or args.version==1:
		snmp_get=netsnmp.snmpget(vars, Version=args.version, DestHost=args.ip,Community=args.community)	
	if args.version==3:
		snmp_get=netsnmp.snmpget(vars, Version=args.version, DestHost=args.ip, SecLevel=args.level,AuthProto=args.authprotocol, AuthPass=args.authpassword, PrivProto=args.privprotocol,PrivPass=args.privpassword, SecName=args.v3_uname)
	for j in snmp_get:
		snmpget.append(j)
		print j

	return snmpget


if __name__ == "__main__":
    main()
