# /etc/init.d/snmpd start



echo "com2sec read_write default public" > /etc/snmp/snmpd.conf

for e in `env | grep SNMPD`
do
	echo $e | sed 's/SNMPD_//g' | sed 0,/\=/{s/\=/\ /} >> /etc/snmp/snmpd.conf
done

cd /usr/sbin
snmpd start

# snmpget -v 1 -c demopublic test.net-snmp.org system.sysUpTime.0

# mkdir -p /etc/snmp
# cat p_test/configfile>>/etc/snmp/snmpd.conf
# cd /etc/init.d

# snmpd start
# ifconfig
# ps -ef
# rc-service snmpd restart
# show snmp-server
# snmpwalk -v 2c demopublic test.net-snmp.org system
snmpwalk -v1 -c public test.net-snmp.org system.sysUpTime.0
#cd /proj_test
# python p_test/test1.py
