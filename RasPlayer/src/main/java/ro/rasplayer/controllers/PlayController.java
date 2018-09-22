package ro.rasplayer.controllers;

import java.io.File;
import java.io.IOException;
import java.net.URL;

import javax.media.CannotRealizeException;
import javax.media.Format;
import javax.media.Manager;
import javax.media.MediaLocator;
import javax.media.NoDataSourceException;
import javax.media.NoPlayerException;
import javax.media.Player;
import javax.media.PlugInManager;
import javax.media.format.AudioFormat;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.servlet.view.RedirectView;

import com.sun.media.protocol.http.DataSource;

@Controller
public class PlayController {

    @GetMapping("/test")
    public String test() {
    	System.out.println("*** Playing radio");
    	System.setProperty("java.awt.headless", "false");
    	System.out.println("*** Set headless mode for AWT");
    	//File file = new File("/home/bogdan/Downloads/JavaSoundDemo/audio/1-welcome.wav");    	
    	//File file = new File("/home/bogdan/Downloads/probz.mp3");
    	try {
    		System.out.println("*** Loading plugin");
    	       Format input1 = new AudioFormat(AudioFormat.MPEGLAYER3);
    	        Format input2 = new AudioFormat(AudioFormat.MPEG);
    	        Format output = new AudioFormat(AudioFormat.LINEAR);
    	        PlugInManager.addPlugIn(
    	            "com.sun.media.codec.audio.mp3.JavaDecoder",
    	            new Format[]{input1, input2},
    	            new Format[]{output},
    	            PlugInManager.CODEC
    	        );    	

    	        System.out.println("*** Loaded plugin");
    	        
    		URL url = new URL("http://live.radiocafe.ro:8048/live.aac");
    		MediaLocator media = new MediaLocator(url);
    		DataSource dataSource = (DataSource) Manager.createDataSource(url);
    		System.out.println("*** " + dataSource.getContentType());

    		System.out.println("*** Creating player");
			Player player = Manager.createRealizedPlayer(url);
			System.out.println("*** Created player");
			System.out.println("*** Starting player");
			player.start();
			System.out.println("*** Started player");
			Thread.currentThread().sleep(5000);
			System.out.println("*****" + player.getGainControl().getLevel());
			//player.getGainControl().setMute(true);
			player.getGainControl().setLevel(Float.valueOf("0.1"));
		} catch (NoPlayerException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}  catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (CannotRealizeException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (NoDataSourceException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    	return "OK";
    }
	
    @GetMapping("/home")
    public RedirectView greeting() {
    	return new RedirectView("/web/index.html");
    }
    
    @GetMapping("/index")
    public String index() {
        return "index";
    }    

    @GetMapping("/radio/{radioName}/play")
    public String playRadio( @PathVariable String radioName ) {
    	String radioUrl = null;
    	switch ( radioName ) {
    	case "radioCafe":
    		radioUrl = "http://live.radiocafe.ro:8048/live.aac";
    		break;
    	case "slowlyRadio":
    		radioUrl = "http://94.23.222.12:8021/stream";
    		break;
    	case "antenneBayern":
    		radioUrl = "https://mp3channels.webradio.de/antenne?&amsparams=playerid:AntenneBayernWebPlayer";
    		break;
    	}
    	if( radioUrl != null ) {
    		System.out.println("Radio URL to play: " + radioUrl);
    	}
    	Runtime rt = Runtime.getRuntime();
    	try {
    		Process pr = rt.exec("vlc " + radioUrl);
    	} catch (Exception e) {
    		System.out.println("Exception thrown while opening the player");
    	}    	
    	return "OK"; 
    }    

    @GetMapping("/radio/{radioName}/stop")
    public String stopRadio( @PathVariable String radioName ) {
    	Runtime rt = Runtime.getRuntime();
    	try {
    		Process pr = rt.exec("pkill vlc");
    	} catch (Exception e) {
    		System.out.println("Exception thrown while opening the player");
    	}    	
    	return "OK"; 
    }    
    

}