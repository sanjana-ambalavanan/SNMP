import netsnmp
import sys
import argparse


def main():
	snmpgetbulk= snmp()
	status=True
	if [i for i in snmpgetbulk if "None" in i] or not snmpgetbulk:
		status=False
	if status:
		print "\n======================================= TEST CASE RESULT : PASS ====================================="
	else:
		print snmpgetbulk
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
	parser.add_argument("-m","--max_repetitions",help="max repetitions",type=int)
	parser.add_argument("-n","--non_repeaters",help="count of non-repeaters",type=int)
	parser.add_argument("-o","--oid",help="oid to get")

	try:
		args = parser.parse_args()
	except Exception:
		print "error in arguments passed"
	vars = netsnmp.VarList(netsnmp.Varbind(args.oid))
	snmpgetbulk=[]
	if args.version==2 or args.version==1:
		session=netsnmp.Session(Version=args.version, DestHost=args.ip,Community=args.community)
		session.getbulk(args.non_repeaters,args.max_repetitions,vars)
		for i in vars:
			print('{}.{} : {}'.format(i.tag, i.iid, i.val))	
			snmpgetbulk.append('{}.{} : {}'.format(i.tag, i.iid, i.val))
		
	if args.version==3:
		session=netsnmp.Session(Version=args.version, DestHost=args.ip, SecLevel=args.level,AuthProto=args.authprotocol, AuthPass=args.authpassword, PrivProto=args.privprotocol,PrivPass=args.privpassword, SecName=args.v3_uname)
		session.getbulk(args.non_repeaters,args.max_repetitions,vars)
		for i in vars:
			print('{}.{} : {}'.format(i.tag, i.iid, i.val))	
			snmpgetbulk.append('{}.{} : {}'.format(i.tag, i.iid, i.val))
	return snmpgetbulk


if __name__ == "__main__":
    main()
