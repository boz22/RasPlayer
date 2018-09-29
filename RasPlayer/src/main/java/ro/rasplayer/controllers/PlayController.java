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

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.view.RedirectView;

import com.sun.media.protocol.http.DataSource;

import jdk.internal.jline.internal.Log;

@Controller
public class PlayController {

	@Autowired
	private RestTemplate restTemplate;
	
    @GetMapping("/home")
    public RedirectView greeting() {
    	return new RedirectView("/web/index.html");
    }
    
    @GetMapping("/index")
    public String index() {
        return "index";
    }    

    @GetMapping("/radio/{audioLocation}/{radioName}/play")
    public ResponseEntity<String> playRadio( @PathVariable String audioLocation, @PathVariable String radioName ) {
    	if( audioLocation == null || radioName == null ){
    		System.out.println("Wrong parameters");
    		return new ResponseEntity<String>("NOT_OK", HttpStatus.BAD_REQUEST);
    	}
    	System.out.println("Playing radio: " + radioName + " at location: " + audioLocation);
    	
        HttpHeaders headers = new HttpHeaders();
        HttpEntity<Object> entity = new HttpEntity<Object>(headers);
    	ResponseEntity<String> out = restTemplate.exchange("http://localhost:8081/radio/play?radio_name=" + radioName + "&location=" + audioLocation, HttpMethod.GET, entity, String.class);
    	
    	return new ResponseEntity<String>(out.getBody(), out.getStatusCode()); 
    }    

    @GetMapping("/radio/{audioLocation}/{radioName}/stop")
    public ResponseEntity<String> stopRadio( @PathVariable String audioLocation, @PathVariable String radioName ) {
    	if( audioLocation == null || radioName == null ){
    		System.out.println("Wrong parameters");
    		return new ResponseEntity<String>("NOT_OK", HttpStatus.BAD_REQUEST);
    	}
    	System.out.println("Stoping radio: " + radioName + " at location: " + audioLocation);
    	
        HttpHeaders headers = new HttpHeaders();
        HttpEntity<Object> entity = new HttpEntity<Object>(headers);
    	ResponseEntity<String> out = restTemplate.exchange("http://localhost:8081/radio/stop?radio_name=" + radioName + "&location=" + audioLocation, HttpMethod.GET, entity, String.class);
    	
    	return new ResponseEntity<String>(out.getBody(), out.getStatusCode()); 
    }
    
    @GetMapping("/radio/{audioLocation}/{radioName}/set/volume")
    public ResponseEntity<String> setVolume( @PathVariable String audioLocation, @PathVariable String radioName, @RequestParam String value ) {
    	System.out.println("Setting radio volume...");
    	if( audioLocation == null || radioName == null || value == null ){
    		System.out.println("Wrong parameters");
    		return new ResponseEntity<String>("NOT_OK", HttpStatus.BAD_REQUEST);
    	}
    	System.out.println("Setting volume for radio: " + radioName + " at location: " + audioLocation + " to value: " + value);
    	
        HttpHeaders headers = new HttpHeaders();
        HttpEntity<Object> entity = new HttpEntity<Object>(headers);
    	ResponseEntity<String> out = restTemplate.exchange("http://localhost:8081/radio/set/volume?radio_name=" + radioName + "&location=" + audioLocation + "&volume=" + value, HttpMethod.GET, entity, String.class);
    	
    	return new ResponseEntity<String>(out.getBody(), out.getStatusCode()); 
    }    
    
    @GetMapping("/radio/{audioLocation}/{radioName}/volume")
    public ResponseEntity<String> getVolume( @PathVariable String audioLocation, @PathVariable String radioName) {
    	if( audioLocation == null || radioName == null ){
    		System.out.println("Wrong parameters");
    		return new ResponseEntity<String>("NOT_OK", HttpStatus.BAD_REQUEST);
    	}
    	System.out.println("Getting volume for radio: " + radioName + " at location: " + audioLocation);
    	
        HttpHeaders headers = new HttpHeaders();
        HttpEntity<Object> entity = new HttpEntity<Object>(headers);
    	ResponseEntity<String> out = restTemplate.exchange("http://localhost:8081/radio/volume?radio_name=" + radioName + "&location=" + audioLocation, HttpMethod.GET, entity, String.class);
    	
    	return new ResponseEntity<String>(out.getBody(), out.getStatusCode()); 
    }        
    
    @GetMapping("/radio/{audioLocation}/{radioName}/status")
    public ResponseEntity<String> statusRadio( @PathVariable String audioLocation, @PathVariable String radioName ) {
        HttpHeaders headers = new HttpHeaders();
        HttpEntity<Object> entity = new HttpEntity<Object>(headers);
        ResponseEntity<String> out = restTemplate.exchange("http://localhost:8081/radio/status?radio_name=" + radioName + "&location=" + audioLocation, HttpMethod.GET, entity, String.class);
    	return new ResponseEntity<String>(out.getBody(), out.getStatusCode()); 
    }        
    

}