// initialize jsPsych
var jsPsych = initJsPsych({
    on_finish: function() {
      jsPsych.data.displayData();
    }
  });

  // create timeline
  var timeline = [];
  
  
  // Random redirection after welcome screen
  // CONDITION == 1 is for unweighted
  // CONDITION == 2 is for gaussian
  const randomRedirect = {
    type: jsPsychCallFunction,
    func: function() {
      // Redirect based on the selected condition
      if (CONDITION == 1) {
        window.location.href = 'https://4jhr4eeejw.cognition.run/';
      } else {
        window.location.href = 'https://vugdhxakle.cognition.run/';
        
      }
    }
  };
  
  // Add the random redirection function to the timeline
  timeline.push(randomRedirect);
  
  
  // Start the experiment
  jsPsych.run(timeline);