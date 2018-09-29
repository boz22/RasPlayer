from bluetooth import *
import subprocess

'''
print "performing inquiry..."
nearby_devices = discover_devices(lookup_names = True)
print "found %d devices" % len(nearby_devices)
for name, addr in nearby_devices:
     print " %s - %s" % (addr, name)
'''

subprocess.call("kill -9 `pidof bluetooth-agent`",shell=True)


client_socket=BluetoothSocket( RFCOMM )
print(dir(client_socket))


client_socket.connect(("c0:a2:2e:56:96:26", 2))
print('Sending')

print(client_socket.__doc__)
print(client_socket.getsockopt(SOL_RFCOMM, 2))
print(client_socket.getsockopt(SOL_RFCOMM, 3))

data = '01fe0000538310000000000050000000'.decode('hex')
client_socket.send(data)	
print('Data sent')
client_socket.close()


