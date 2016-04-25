echo "*******CPU INFORMATION*******"
echo "mapper_1 1 minute CPU load"
snmpget -v 1 -c public 10.0.0.1 .1.3.6.1.4.1.2021.10.1.3.1 
echo "mapper_1 percentage of user CPU time"
snmpget -v 1 -c public 10.0.0.1 .1.3.6.1.4.1.2021.11.9.0 
echo "mapper_1 raw user cpu time"
snmpget -v 1 -c public 10.0.0.1 .1.3.6.1.4.1.2021.11.50.0 
echo "mapper_1 percentages of system CPU time"
snmpget -v 1 -c public 10.0.0.1 .1.3.6.1.4.1.2021.11.10.0 
echo "mapper_1 raw system CPU time"
snmpget -v 1 -c public 10.0.0.1 .1.3.6.1.4.1.2021.11.52.0 
echo "mapper_1 percentage of idle CPU time"
snmpget -v 1 -c public 10.0.0.1 .1.3.6.1.4.1.2021.11.11.0
echo "*******MEMORY INFORMATION*******"
echo "mapper_1 available swap space"
snmpget -v 1 -c public 10.0.0.1 .1.3.6.1.4.1.2021.4.4.0
echo "mapper_1 toal RAM used"
snmpget -v 1 -c public 10.0.0.1 .1.3.6.1.4.1.2021.4.6.0
echo "mapper_1 total RAM buffered"
snmpget -v 1 -c public 10.0.0.1 .1.3.6.1.4.1.2021.4.14.0
echo "mapper_1 total cached memory"
snmpget -v 1 -c public 10.0.0.1 .1.3.6.1.4.1.2021.4.15.0



