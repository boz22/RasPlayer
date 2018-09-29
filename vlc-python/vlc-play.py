import vlc;
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from flask import request


app = Flask(__name__)
api = Api(app)


#Querying output devices
print('Querying output devices')
analog_output = None
bluetooth_output = None

generic_player = vlc.MediaPlayer('')
output_device = generic_player.audio_output_device_enum()
finished = False
while finished is False:
 try:  
  if output_device.contents.device.startswith('alsa_output'):
   analog_output = output_device.contents.device
  elif output_device.contents.device.startswith('bluez_sink'):
   bluetooth_output = output_device.contents.device
  output_device = output_device.contents.next
 except:
  finished = True


if analog_output is not None:
 print('Analog output device is found and initialized')
 print('Analog output device: ' + analog_output)
else:
 print('Analog output device was not found')

if bluetooth_output is not None:
 print('Bluetooth output device is found and initialized')
 print('Bluetooth output device: ' + bluetooth_output)
else:
 print('Bluetooth output device was not found')


#Building players
print('Building players...')
players = {}
if analog_output is not None:
 print('Building analog players')
 players['analog'] = {}
 print('Creating Antenne analog player')
 antenneAnalogPlayer = vlc.MediaPlayer('https://mp3channels.webradio.de/antenne?&amsparams=playerid:AntenneBayernWebPlayer')
 antenneAnalogPlayer.audio_output_device_set( None, analog_output )
 players['analog']['antenne'] = antenneAnalogPlayer

 print('Creating Slowly analog player')
 slowlyAnalogPlayer = vlc.MediaPlayer('http://94.23.222.12:8021/stream')
 slowlyAnalogPlayer.audio_output_device_set( None, analog_output )
 players['analog']['slowly'] = slowlyAnalogPlayer

 print('Creating Radio Cafe analog player')
 cafeAnalogPlayer = vlc.MediaPlayer('http://live.radiocafe.ro:8048/live.aac')
 cafeAnalogPlayer.audio_output_device_set( None, analog_output )
 players['analog']['cafe'] = cafeAnalogPlayer

 print('Creating Magic analog player')
 magicAnalogPlayer = vlc.MediaPlayer('http://80.86.106.143:9128/magicfm.aacp')
 magicAnalogPlayer.audio_output_device_set( None, analog_output )
 players['analog']['magic'] = magicAnalogPlayer

if bluetooth_output is not None:
 print('Building ble players')
 players['ble'] = {}
 print('Creating Antenne ble player')
 antenneBlePlayer = vlc.MediaPlayer('https://mp3channels.webradio.de/antenne?&amsparams=playerid:AntenneBayernWebPlayer')
 antenneBlePlayer.audio_output_device_set( None, bluetooth_output )
 players['ble']['antenne'] = antenneBlePlayer

 print('Creating Slowly ble player')
 slowlyBlePlayer = vlc.MediaPlayer('http://94.23.222.12:8021/stream')
 slowlyBlePlayer.audio_output_device_set( None, bluetooth_output )
 players['ble']['slowly'] = slowlyBlePlayer

 print('Creating Cafe ble player')
 cafeBlePlayer = vlc.MediaPlayer('http://live.radiocafe.ro:8048/live.aac')
 cafeBlePlayer.audio_output_device_set( None, bluetooth_output )
 players['ble']['cafe'] = cafeBlePlayer

 print('Creating Magic ble player')
 magicBlePlayer = vlc.MediaPlayer('http://80.86.106.143:9128/magicfm.aacp')
 magicBlePlayer.audio_output_device_set( None, bluetooth_output )
 players['ble']['magic'] = magicBlePlayer


@app.route('/radio/play', methods=['GET'])
def rest_play_radio():
 print('Playing radio...')
 radio_name=request.args.get('radio_name')
 print('Radio name: ' + radio_name)
 audio_device_location=request.args.get('location')
 print('Audio device location: ' + audio_device_location)
 if audio_device_location not in players.keys():
  print('Key does not exist')
 try:
  print('Playing running radio at: ' + audio_device_location)  
  for key in players[audio_device_location]:
   crt_player = players[audio_device_location][key]
   if crt_player.get_state() == vlc.State.Opening or crt_player.get_state() == vlc.State.Playing or crt_player.get_state() == vlc.State.Paused:
    crt_player.stop()
  print('Playing currently selected radio')
  player = players[audio_device_location][radio_name]; 
  player.play()
  while (player.get_state() == vlc.State.Opening) or (player.get_state() == vlc.State.NothingSpecial):
   print(player.get_state())   
  if player.is_playing() == 0:
   raise Exception("Error Playing the radio")
 except:
  print('Error playing radio name: ' + radio_name + ' and location: ' + audio_device_location)
  #Workaround for throwing exception after stoping and starting the radio
  while player.get_state() != vlc.State.Playing:
   print('Waiting to play...')
  if player.is_playing() == 1:
   return 'OK', 200
  return 'NOT_OK', 500
 return 'OK', 200

@app.route('/radio/set/volume', methods=['GET'])
def rest_radio_set_volume():
 radio_name=request.args.get('radio_name')
 print('Radio name: ' + radio_name)
 audio_device_location=request.args.get('location')
 print('Audio device location: ' + audio_device_location)
 audio_volume=request.args.get('volume') 
 print('Radio volume: ' + audio_volume)
 try:
  players[audio_device_location][radio_name].audio_set_volume(int(audio_volume))
  return audio_volume, 200
 except:
  print('Cannot set volume for a player with radio name: ' + radio_name + ' and location: ' + audio_device_location + ' and volume: ' + audio_volume )
 return 'NOT_OK', 500

@app.route('/radio/volume', methods=['GET'])
def rest_radio_get_volume():
 radio_name=request.args.get('radio_name')
 print('Radio name: ' + radio_name)
 audio_device_location=request.args.get('location')
 print('Audio device location: ' + audio_device_location)
 try:
  return str(players[audio_device_location][radio_name].audio_get_volume()), 200
 except:
  print('Cannot set volume for a player with radio name: ' + radio_name + ' and location: ' + audio_device_location + ' and volume: ' + audio_volume )
 return 'NOT_OK', 500

@app.route('/radio/stop', methods=['GET'])
def rest_stop_radio():
 print('Stoping radio...')
 radio_name=request.args.get('radio_name')
 print('Radio name: ' + radio_name)
 audio_device_location=request.args.get('location')
 print('Audio device location: ' + audio_device_location)
 
 try:
  players[audio_device_location][radio_name].stop()
 except:
  print('Cannot stop player with radio name: ' + radio_name + ' and location: ' + audio_device_location )
 return 'OK'

@app.route('/radio/status', methods=['GET'])
def rest_status_radio():
 radio_name=request.args.get('radio_name')
 audio_device_location=request.args.get('location')
 print('Getting status for radio: ' + radio_name + ' and location: ' + audio_device_location)
 try:
  state = players[audio_device_location][radio_name].get_state()
  return str(state), 200
 except:
  print('Cannot stop player with radio name: ' + radio_name + ' and location: ' + audio_device_location )
  return 'NOT_OK', 500
 return 'OK'

if __name__ == '__main__':
     app.run(port='8081')


#devices=player.audio_output_device_enum()
#print("**************")
#print(devices.contents.device)
#while player.get_state() != vlc.State.Ended:
 #while devices:
  #print(len(devices.contents.device)
  #print(dir(player.audio_output_device_get() ) )

print("Player started");
