from bluetooth import bluez
import bluepy
from bluepy.btle import Scanner, DefaultDelegate, Peripheral



class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
            handleConnectedDev(dev)
        elif isNewData:
            print ("Received new data from", dev.addr)

def handleConnectedDev(dev):
 print(dir(dev))
 print(dev.connectable)
 print(dev.addrType)
 print(dev.iface)
 print(dev.scanData)
 print(dev.MANUFACTURER)
 print(dev.PUBLIC_TARGET_ADDRESS)
 print(dev.__dict__) 
 per = Peripheral() 
 per.connect(dev.addr)
 print(dir(per))

#per = Peripheral( "FF:FF:80:03:F9:15" ) 
per = Peripheral()
service = per.getServiceByUUID("00006666-0000-1000-8000-00805f9b34fb")
print(dir(service))

#scanner = Scanner().withDelegate(ScanDelegate())
#devices = scanner.scan(10000.0)
sys.exit(0)
'''
    print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
    for (adtype, desc, value) in dev.getScanData():
        print "  %s = %s" % (desc, value)
'''

'''
#print(dir(bluepy.btle.Scanner))
devices = bluepy.btle.Scanner(0).scan(10000)
for dev in devices:
 print(dir(dev))
 print(dev.addr())
'''
'''
nearby_devices = bluez.discover_devices(lookup_names = True)
for bdaddr in nearby_devices:
 print('Found one device')
 print(bdaddr)
'''

'''
sock=bluez.BluetoothSocket(bluez.L2CAP)
bd_addr = "FF:FF:80:03:F9:15"
#bd_addr = "30:21:63:98:BC:62"
#port = 0x0e01
#port = 0x0e01
port = bluez._get_available_port(protocol=bluez.L2CAP)
print('SOCK')
print(sock.connect((bd_addr,port)))
sock.send("13:ef:21:01:fe:00:00:51:00:10:00:00:00:00:80:00:00:00:80:65")
sock.close()
'''




