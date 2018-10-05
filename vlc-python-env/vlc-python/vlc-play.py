import vlc;
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from flask import request


app = Flask(__name__)
api = Api(app)


#Analog device name: alsa_output.pci-0000_00_1f.3.analog-stereo
#bluetooth: bluez_sink.C0_A2_2E_56_96_26.a2dp_sink

players = {}
players['analog'] = None
players['ble'] = None

outputs = {}
outputs['analog'] = None
outputs['ble'] = None

radio_urls = {}
radio_urls['antenne'] = "https://mp3channels.webradio.de/antenne?&amsparams=playerid:AntenneBayernWebPlayer"
radio_urls['slowly'] = "http://94.23.222.12:8021/stream"
radio_urls['cafe'] = "http://live.radiocafe.ro:8048/live.aac"

def check_audio_outputs():
 print('Querying output devices')
 generic_player = vlc.MediaPlayer('')
 output_device = generic_player.audio_output_device_enum()
 finished = False
 while finished is False:
  try:  
   if output_device.contents.device.startswith('alsa_output'):
    outputs['analog'] = output_device.contents.device
   elif output_device.contents.device.startswith('bluez_sink'):   
    outputs['ble'] = output_device.contents.device
   output_device = output_device.contents.next
  except:
   finished = True
 if outputs['analog'] is not None:
  print('Analog output device is found and initialized')
  print('Analog output device: ' + outputs['analog'])
 else:
  print('Analog output device was not found')
 if outputs['ble'] is not None:
  print('Bluetooth output device is found and initialized')
  print('Bluetooth output device: ' + outputs['ble'])
 else:
  print('Bluetooth output device was not found')


def build_radio_player(output_device, radio_url):
 print('Building radio player for output device: ' + output_device + ' and url: ' + radio_url)

 print('Checking audio outputs')
 check_audio_outputs()
 
 print('Check if there is a device for: ' + output_device)
 if outputs[output_device] is None:
  print('No output device for: ' + output_device + ' was found')
  return None

 print('Check if there is already a player defined at the output: ' + output_device)
 if players[output_device] is not None:
  print('There is already a player defined at output: ' + output_device)
  print('Will stop the player if it is running')
  try:
   players[output_device].stop()
   players[output_device] = None
  except:
   print('Could not stop player running at output device: ' + output_device)

 print('Define the new radio')
 players[output_device] = vlc.MediaPlayer(radio_url)
 players[output_device].audio_output_device_set(None, outputs[output_device])
 return players[output_device]


@app.route('/radio/play', methods=['GET'])
def rest_play_radio():
 print('Playing radio...')
 radio_name=request.args.get('radio_name')
 print('Radio name: ' + radio_name)
 audio_device_location=request.args.get('location') 
 print('Audio device location: ' + audio_device_location)
 radio_url = radio_urls[radio_name]
 print('Radio URL: ' + radio_url)
 try:
  print('Playing running radio: ' + radio_name +' at: ' + audio_device_location)  
  player = build_radio_player(audio_device_location, radio_url) 
  if player is None:
   print('Could not build a proper player')
   return 'Could not build player', 500
  print('Player built. Now trying to play it')
  player.play()
  while (player.get_state() == vlc.State.Opening) or (player.get_state() == vlc.State.NothingSpecial):
   #print(player.get_state())   
   x=1
  if player.is_playing() == 0:
   raise Exception("Error Playing the radio")
 except:
  print('Error playing radio name: ' + radio_name + ' and location: ' + audio_device_location)
  #Workaround for throwing exception after stoping and starting the radio
  while player.get_state() != vlc.State.Playing:
   #print('Waiting to play...')
   x=1
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
  if players[audio_device_location] is None:
   return 'Not audio player found', 500
  players[audio_device_location].audio_set_volume(int(audio_volume))
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
  if players[audio_device_location] is None:
   return 'Not audio player found', 500
  return str(players[audio_device_location].audio_get_volume()), 200
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
  if players[audio_device_location] is None:
   return 'Not audio player found', 500
  players[audio_device_location].stop()
 except:
  print('Cannot stop player with radio name: ' + radio_name + ' and location: ' + audio_device_location )
 return 'OK'

@app.route('/radio/status', methods=['GET'])
def rest_status_radio():
 radio_name=request.args.get('radio_name')
 audio_device_location=request.args.get('location')
 print('Getting status for radio: ' + radio_name + ' and location: ' + audio_device_location)
 try:
  if players[audio_device_location] is None:
   return 'Not audio player found', 500
  state = players[audio_device_location].get_state()
  return str(state), 200
 except:
  print('Cannot stop player with radio name: ' + radio_name + ' and location: ' + audio_device_location )
  return 'NOT_OK', 500
 return 'OK'

if __name__ == '__main__':
     app.run(port='8081')
