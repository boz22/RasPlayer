/**
 * @license
 * Copyright (c) 2014, 2018, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/*
 * Your dashboard ViewModel code goes here
 */
define(['ojs/ojcore', 'knockout', 'jquery', 'ojs/ojfilmstrip', 'ojs/ojknockout', 'ojs/ojprogress', 'ojs/ojbutton', 'ojs/ojlabel'],
 function(oj, ko, $, filmStrip) {
  
    function DashboardViewModel() {
      var self = this;
      var that = this;
      
      this.radioVolume = ko.observable(0);
      this.playingRadio = ko.observable('');
      
      //Radio
      this.showRadioPlay = ko.observable(true);
      this.showRadioLoading = ko.observable(false);
      this.showRadioStop = ko.observable(false);   
      

      self.currentLooping = ko.observable("page");      
      getItemInitialDisplay = function(index)
      {
        return index < 3 ? '' : 'none';
      };            
      this.radios = [
    	  { name: 'Antenne Bayern', id: 'antenne' },
    	  { name: 'Slowly Radio', id: 'slowly' },
    	  { name: 'Radio Cafe', id: 'cafe' }
      ];

      this.selectionIndex = ko.observable(0);  
            
      
      this.getRadiosStatusesRecursive = function( radioIndex ){
    	    $.ajax({
    	    	url: "/radio/analog/" + that.radios[radioIndex].id + "/status", 
    	    	success: function(result){
    	    		console.log("Status: " + result);
    	    		if( "State.Playing" === result ){
    	    			that.selectionIndex(radioIndex);
    	    			that.showRadioStop(true);
    	    			that.showRadioPlay(false);	    			
    	    			that.getVolume( that.radios[i].id, function(volume){
    	    				that.radioVolume(volume);
    	    			} );
    	    			
    	    		} else{
        	    		if( radioIndex < that.radios.length - 1 ){
        	    			that.getRadiosStatusesRecursive(radioIndex + 1);
        	    		}    	    			
    	    		}	    		
    	    	},
    	    	fail: function(){
    	    		if( radioIndex < that.radios.length - 1 ){
    	    			that.getRadiosStatusesRecursive(radioIndex + 1);
    	    		}
    	    	}
      	    });    	  
      }
      
      this.getRadiosStatusesRecursive(0);
      
	  $(document).ready(function(){
    	  $(".oj-filmstrip-arrow.oj-start").click(function(){
    		  if( that.selectionIndex() == 0 ){
    			  that.selectionIndex( that.radios.length - 1 );
    		  } else{
    			  that.selectionIndex( that.selectionIndex() - 1 );
    		  }    		  
    	  });
    	  $(".oj-filmstrip-arrow.oj-end").click(function(){ 
    		  if( that.selectionIndex() == that.radios.length - 1 ){
    			  that.selectionIndex(0);
    		  } else{
    			  that.selectionIndex( that.selectionIndex() + 1 );
    		  }    
    	  });    		  
	  });      
      
   
      
	    
      this.handleRadioAction = function(){    	  
    	  if( this.showRadioPlay() ){
        	  this.showRadioPlay(false);
        	  this.showRadioLoading(true);    
        	  
    		  this.playRadio(that.radios[that.selectionIndex()].id, function(){
    			  that.showRadioLoading(false);
    			  that.showRadioStop(true);
    		  }, function(){
    			  that.showRadioLoading(false);
    			  that.showRadioPlay(true);
    		  });
    	  } else if( this.showRadioStop() ){
    		  this.stopRadio(that.radios[that.selectionIndex()].id, function(){
    			  that.showRadioPlay(true);
    			  that.showRadioStop(false);
    		  }, function(){
    			  that.showRadioStop(true);
    			  that.showRadioPlay(false);
    		  });
    	  }	
      }
      
      this.playRadio = function( radioName, success, fail ){
    	  console.log("Playing radio: " + radioName);    	  
    	    $.ajax({
    	    	url: "/radio/analog/" + radioName + "/play", 
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
	  	    	url: "/radio/analog/" + radioName + "/stop",
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
		    	url: "/radio/analog/" + radioName + "/volume", 
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
		    	url: "/radio/analog/" + radioName + "/set/volume?value=" + value, 
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

      };
    }

    /*
     * Returns a constructor for the ViewModel so that the ViewModel is constructed
     * each time the view is displayed.  Return an instance of the ViewModel if
     * only one instance of the ViewModel is needed.
     */
    return new DashboardViewModel();
  }
);
