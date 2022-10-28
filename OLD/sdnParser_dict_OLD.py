import pktSTR2BYT, printPKTinfo



'''
data = open('data.txt','r').read().replace('-','').replace('\n\n','\n')
data2 = open('data2.txt','w')
data2.write(data)
'''

pkt_str = open('data2.txt','r').readlines()
pkt_str = pkt_str[1]

pkt = pktSTR2BYT.pktSTR2BYT(pkt_str)

pkt_dict = {'Raw Data':pkt}

i = 0

#Extract MAC Addresses
pkt_dict.update({'Source MAC Adress':pkt[i:i+6]})
pkt_dict.update({'Destination MAC Adress':pkt[i+6:i+12]})
i += 12

pkt_dict.update({'EtherTypes':{}})

#Check if tagged traffic
if pkt[i:i+2].hex()=='8100':
    pkt_dict['EtherTypes'].update({'802.1Q':pkt[i:i+2]})
    pkt_dict.update({'VLAN ID':pkt[i+2:i+4]})
    i += 4

#Check if ARP packet
if pkt[i:i+2].hex()=='0806':
    pkt_dict['EtherTypes'].update({'ARP':pkt[i:i+2]})
    i += 2
    pkt_dict.update({'ARP Hardware Type':pkt[i:i+2]})
    i += 2
    pkt_dict.update({'ARP Protocol Type':pkt[i:i+2]})


    i += 2

#Check if IPv4 packet
if pkt[i:i+2].hex()=='0800':
    pkt_dict['EtherTypes'].update({'IPv4':pkt[i:i+2]})
    pkt_dict.update({'IPv4 data':pkt[i+2:i+4]})
    i += 4






printPKTinfo.printPKTinfo(pkt_dict)
