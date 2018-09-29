/**
 * @license
 * Copyright (c) 2014, 2018, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/*
 * Your incidents ViewModel code goes here
 */
define(['ojs/ojcore', 'knockout', 'jquery', 'ojs/ojprogress', 'ojs/ojbutton'],
 function(oj, ko, $) {
  
    function IncidentsViewModel() {
      var self = this;
      var that = this;
      
      this.radioVolume = ko.observable(0);
      this.playingRadio = ko.observable('');
      
      //Antenne
      this.showAntennePlay = ko.observable(true);
      this.showAntenneLoading = ko.observable(false);
      this.showAntenneStop = ko.observable(false);      
      
      //Slowly
      this.showSlowlyPlay = ko.observable(true);
      this.showSlowlyLoading = ko.observable(false);
      this.showSlowlyStop = ko.observable(false);      
      
      //Cafe
      this.showCafePlay = ko.observable(true);
      this.showCafeLoading = ko.observable(false);
      this.showCafeStop = ko.observable(false);
      
	    $.ajax({
	    	url: "/radio/ble/antenne/status", 
	    	success: function(result){
	    		console.log("Status: " + result);
	    		if( "State.Playing" === result ){
	    			that.showAntenneStop(true);
	    			that.showAntennePlay(false);
	    			that.playingRadio('antenne');
	    			that.getVolume( 'antenne', function(volume){
	    				that.radioVolume(volume);
	    			} );
	    		}	    		
	    	}
	    });      
      
	    $.ajax({
	    	url: "/radio/ble/slowly/status", 
	    	success: function(result){
	    		console.log("Status: " + result);
	    		if( "State.Playing" === result ){
	    			that.showSlowlyStop(true);
	    			that.showSlowlyPlay(false);
	    			that.playingRadio('slowly');
	    			that.getVolume( 'antenne', function(volume){
	    				that.radioVolume(volume);
	    			} );	    			
	    		}	    		
	    	}
	    });  	    
	    
	    $.ajax({
	    	url: "/radio/ble/cafe/status", 
	    	success: function(result){
	    		console.log("Status: " + result);
	    		if( "State.Playing" === result ){
	    			that.showCafeStop(true);
	    			that.showCafePlay(false);
	    			that.playingRadio('cafe');
	    			that.getVolume( 'antenne', function(volume){
	    				that.radioVolume(volume);
	    			} );	    			
	    		}	    		
	    	}
	    });  	          	   
	    
      this.handleAntenneAction = function(){
    	  if( this.showAntennePlay() ){
        	  this.showAntennePlay(false);
        	  this.showAntenneLoading(true);    
        	  
    		  this.playRadio('antenne', function(){
    			  that.showAntenneLoading(false);
    			  that.showAntenneStop(true);
    		  }, function(){
    			  that.showAntenneLoading(false);
    			  that.showAntennePlay(true);
    		  });
    	  } else if( this.showAntenneStop() ){
    		  this.stopRadio('antenne', function(){
    			  that.showAntennePlay(true);
    			  that.showAntenneStop(false);
    		  }, function(){
    			  that.showAntenneStop(true);
    			  that.showAntennePlay(false);
    		  });
    	  }	
      }
      
      this.handleSlowlyAction = function(){
    	  if( this.showSlowlyPlay() ){
        	  this.showSlowlyPlay(false);
        	  this.showSlowlyLoading(true);    
        	  
    		  this.playRadio('slowly', function(){
    			  that.showSlowlyLoading(false);
    			  that.showSlowlyStop(true);
    		  }, function(){
    			  that.showSlowlyLoading(false);
    			  that.showSlowlyPlay(true);
    		  });
    	  } else if( this.showSlowlyStop() ){
    		  this.stopRadio('slowly', function(){
    			  that.showSlowlyPlay(true);
    			  that.showSlowlyStop(false);
    		  }, function(){
    			  that.showSlowlyStop(true);
    			  that.showSlowlyPlay(false);
    		  });
    	  }	
      }      
      
      this.handleCafeAction = function(){
    	  if( this.showCafePlay() ){
        	  this.showCafePlay(false);
        	  this.showCafeLoading(true);    
        	  
    		  this.playRadio('cafe', function(){
    			  that.showCafeLoading(false);
    			  that.showCafeStop(true);
    		  }, function(){
    			  that.showCafeLoading(false);
    			  that.showCafePlay(true);
    		  });
    	  } else if( this.showCafeStop() ){
    		  this.stopRadio('cafe', function(){
    			  that.showCafePlay(true);
    			  that.showCafeStop(false);
    		  }, function(){
    			  that.showCafeStop(true);
    			  that.showCafePlay(false);
    		  });
    	  }	
      }      
      
      this.playRadio = function( radioName, success, fail ){
    	  console.log("Playing radio: " + radioName);    	  
    	    $.ajax({
    	    	url: "/radio/ble/" + radioName + "/play", 
    	    	success: function(result){
    	    		console.log("Started radio: " + radioName);
    	    		that.playingRadio(radioName);
	      			that.getVolume(that.playingRadio(), function(data){
	    				that.radioVolume(parseInt(data, 10));
	    	    		if( success ){
	    	    			success();
	    	    		}	    				
	    			} );    	    		
    	    	},
    	    	fail: function(){    	    		
    	    		alert("Error playing radio: " + radioName);
    	    		if( fail ){
    	    			fail();
    	    		}
    	    	}
    	    });
      }
      
      this.stopRadio = function( radioName, success, fail ){
    	  console.log("Stoping radio: " + radioName);
	  	    $.ajax({
	  	    	url: "/radio/ble/" + radioName + "/stop",
		    	success: function(result){
		    		console.log("Stopped radio: " + radioName);
		    		if( success ){
		    			success();
		    		}
		    	},
		    	fail: function(){
		    		alert("Error stopping radio: " + radioName);
		    		if( fail ){
		    			fail();
		    		}
		    	}
		    });    	      	  
      }      
      
      this.incVolume = function(){
    	  var tempVolume;
    	  if( this.radioVolume() <= 90 ){
    		  tempVolume = this.radioVolume() + 10;    		  
    	  } else{
    		  tempVolume = 100;
    	  }
    	  console.log('Trying to set volume to: ' + tempVolume);
    	  console.log('Current volume is ' + this.radioVolume());
		  this.setVolume( that.playingRadio(), tempVolume, function(newVolume){
			  console.log('Setting volume succeded');
			  that.radioVolume(newVolume);
			  console.log('New volume value is ' + that.radioVolume());			  
		  }, function(){
			  console.log('Setting volume failed');
		  } );    	  
      }
      
      this.decVolume = function(){
    	  var tempVolume;
    	  if( this.radioVolume() >= 10 ){
    		  tempVolume = this.radioVolume() - 10;    		  
    	  } else{
    		  tempVolume = 0;
    	  }
    	  console.log('Trying to set (decreasing) volume to: ' + tempVolume);
    	  console.log('Current volume is ' + this.radioVolume());
		  this.setVolume( that.playingRadio(), tempVolume, function(newVolume){
			  console.log('Setting volume succeded');
			  that.radioVolume(newVolume);
			  console.log('New volume value is ' + that.radioVolume());
		  }, function(){
			  console.log('Setting volume failed');
		  } );
      }
      
	  this.getVolume = function( radioName, success, fail ){
	  	    $.ajax({
		    	url: "/radio/ble/" + radioName + "/volume", 
		    	success: function(result){
		    		if( success ){
		    			success( parseInt(result) );
		    		}
		    	},
		    	fail: function(){    	    		
		    		if( fail ){
		    			fail();
		    		}
		    	}
		    });		  
		  }        
	  
	  this.setVolume = function( radioName, value, success, fail ){
	  	    $.ajax({
		    	url: "/radio/ble/" + radioName + "/set/volume?value=" + value, 
		    	success: function(result){
		    		if( success ){
		    			console.log('Raw result after setting volume: ' + result);
		    			console.log('Parsed result after setting volume: ' + parseInt(result));
		    			success( parseInt(result, 10) );
		    		}
		    	},
		    	fail: function(){    	    		
		    		if( fail ){
		    			fail();
		    		}
		    	}
		    });		  
		  }      	  
      
      // Below are a set of the ViewModel methods invoked by the oj-module component.
      // Please reference the oj-module jsDoc for additional information.

      /**
       * Optional ViewModel method invoked after the View is inserted into the
       * document DOM.  The application can put logic that requires the DOM being
       * attached here. 
       * This method might be called multiple times - after the View is created 
       * and inserted into the DOM and after the View is reconnected 
       * after being disconnected.
       */
      self.connected = function() {
        // Implement if needed
      };

      /**
       * Optional ViewModel method invoked after the View is disconnected from the DOM.
       */
      self.disconnected = function() {
        // Implement if needed
      };

      /**
       * Optional ViewModel method invoked after transition to the new View is complete.
       * That includes any possible animation between the old and the new View.
       */
      self.transitionCompleted = function() {
        // Implement if needed
      };
    }

    /*
     * Returns a constructor for the ViewModel so that the ViewModel is constructed
     * each time the view is displayed.  Return an instance of the ViewModel if
     * only one instance of the ViewModel is needed.
     */
    return new IncidentsViewModel();
  }
);
