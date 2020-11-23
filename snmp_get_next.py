import netsnmp
import sys
import argparse

def main():
	snmpgetnext= snmp()
	status=True
	if [i for i in snmpgetnext if "None" in i] or not snmpgetnext:
		status=False
	if status:
		print "\n======================================= TEST CASE RESULT : PASS ====================================="
	else:
		print snmpgetnext
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
	parser.add_argument("-o","--oid",help="returns oid next to this oid")
	try:
		args = parser.parse_args()		
	except Exception:
		print "error in arguments passed"
	vars = netsnmp.VarList(netsnmp.Varbind(args.oid))
	snmpgetnext=[]
	if args.version==2 or args.version==1:
		session=netsnmp.Session(Version=2, DestHost=args.ip,Community=args.community)
		session.getnext(vars)
		for i in vars:
			print('{}.{} : {}'.format(i.tag, i.iid, i.val))	
			snmpgetnext.append('{}.{} : {}'.format(i.tag, i.iid, i.val))
		
	if args.version==3:
		session=netsnmp.Session(Version=args.version, DestHost=args.ip, SecLevel=args.level,AuthProto=args.authprotocol, AuthPass=args.authpassword, PrivProto=args.privprotocol,PrivPass=args.privpassword, SecName=args.v3_uname)
		session.getnext(vars)
		for i in vars:
			print('{}.{} : {}'.format(i.tag, i.iid, i.val))	
			snmpgetnext.append('{}.{} : {}'.format(i.tag, i.iid, i.val))
	return snmpgetnext


if __name__ == "__main__":
    main()
