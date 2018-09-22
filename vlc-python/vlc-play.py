import vlc;
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from flask import request


app = Flask(__name__)
api = Api(app)

antennePlayer = vlc.MediaPlayer('https://mp3channels.webradio.de/antenne?&amsparams=playerid:AntenneBayernWebPlayer')
antennePlayer.audio_output_device_set( None, antennePlayer.audio_output_device_enum().contents.next.contents.device )
antennePlayer.play()



print("**************")
print(dir(antennePlayer.audio_output_device_set))

devices=antennePlayer.audio_output_device_enum()
print(devices.contents.device)
print(devices.contents.next.contents.device)

@app.route('/radio/location', methods=['GET'])
def get_location():
 antennePlayer2 = vlc.MediaPlayer('https://mp3channels.webradio.de/antenne?&amsparams=playerid:AntenneBayernWebPlayer')
 antennePlayer2.audio_output_device_set( None, antennePlayer2.audio_output_device_enum().contents.device )
 antennePlayer2.play()
 return 'OK'

@app.route('/radio/play', methods=['GET'])
def rest_play_radio():
 print('Playing radio...')
 radio_name=request.args.get('radio_name')
 print('Radio name: ' + radio_name)
 audio_device_location=request.args.get('location')
 print('Audio device location: ' + audio_device_location)
 
 if radio_name == 'antenne':
  print('Playing Antenne Bayern')
  antennePlayer.play()

 elif radio_name == 'radio_cafe':
  print('Playing Radio Cafe')
 return 'OK'

@app.route('/radio/stop', methods=['GET'])
def rest_stop_radio():
 print('Stoping radio...')
 radio_name=request.args.get('radio_name')
 print('Radio name: ' + radio_name)
 audio_device_location=request.args.get('location')
 print('Audio device location: ' + audio_device_location)
 
 if radio_name == 'antenne':
  print('Playing Antenne Bayern')
  antennePlayer.stop()

 elif radio_name == 'radio_cafe':
  print('Playing Radio Cafe')
 return 'OK'

if __name__ == '__main__':
     app.run(port='8081')

#print('Playing file');
#player = vlc.MediaPlayer("https://mp3channels.webradio.de/antenne?&amsparams=playerid:AntenneBayernWebPlayer");

#print('Starting player');

#print( dir(player) )
#player.play()


#devices=player.audio_output_device_enum()
#print("**************")
#print(devices.contents.device)
#while player.get_state() != vlc.State.Ended:
 #while devices:
  #print(len(devices.contents.device)
  #print(dir(player.audio_output_device_get() ) )

print("Player started");
