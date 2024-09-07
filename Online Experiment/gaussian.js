document.body.style.backgroundColor = "#777777"; 
    // initialize jsPsych
    var jsPsych = initJsPsych({
      on_finish: function() {
        jsPsych.data.displayData();
      }
    });

    // list of all the stimuli
    const stimuli = ['gaussianBlockOneH_111318.png', 'gaussianBlockOneH_114966.png', 'gaussianBlockOneH_120086.png', 'gaussianBlockOneH_122734.png', 'gaussianBlockOneH_123788.png', 'gaussianBlockOneH_130500.png', 'gaussianBlockOneH_130594.png', 'gaussianBlockOneH_133531.png', 'gaussianBlockOneH_136696.png', 'gaussianBlockOneH_144105.png', 'gaussianBlockOneH_172503.png', 'gaussianBlockOneH_179488.png', 'gaussianBlockOneH_199417.png', 'gaussianBlockOneH_208086.png', 'gaussianBlockOneH_20942.png', 'gaussianBlockOneH_227255.png', 'gaussianBlockOneH_231519.png', 'gaussianBlockOneH_245015.png', 'gaussianBlockOneH_246074.png', 'gaussianBlockOneH_253249.png', 'gaussianBlockOneH_279532.png', 'gaussianBlockOneH_282389.png', 'gaussianBlockOneH_283672.png', 'gaussianBlockOneH_291260.png', 'gaussianBlockOneH_310070.png', 'gaussianBlockOneH_31720.png', 'gaussianBlockOneH_321612.png', 'gaussianBlockOneH_328536.png', 'gaussianBlockOneH_337639.png', 'gaussianBlockOneH_340214.png', 'gaussianBlockOneH_365394.png', 'gaussianBlockOneH_368344.png', 'gaussianBlockOneH_409638.png', 'gaussianBlockOneH_416672.png', 'gaussianBlockOneH_428391.png', 'gaussianBlockOneH_430219.png', 'gaussianBlockOneH_431654.png', 'gaussianBlockOneH_444271.png', 'gaussianBlockOneH_458616.png', 'gaussianBlockOneH_475472.png', 'gaussianBlockOneH_476547.png', 'gaussianBlockOneH_478774.png', 'gaussianBlockOneH_481546.png', 'gaussianBlockOneH_487256.png', 'gaussianBlockOneH_487824.png', 'gaussianBlockOneH_506250.png', 'gaussianBlockOneH_509170.png', 'gaussianBlockOneH_512964.png', 'gaussianBlockOneH_527311.png', 'gaussianBlockOneH_529800.png', 'gaussianBlockOneH_54054.png', 'gaussianBlockOneH_542990.png', 'gaussianBlockOneH_554450.png', 'gaussianBlockOneH_555494.png', 'gaussianBlockOneH_559481.png', 'gaussianBlockOneH_561211.png', 'gaussianBlockOneH_562191.png', 'gaussianBlockOneH_568991.png', 'gaussianBlockOneH_582529.png', 'gaussianBlockOneH_590459.png', 'gaussianBlockOneH_604743.png', 'gaussianBlockOneH_618823.png', 'gaussianBlockOneH_623606.png', 'gaussianBlockOneH_625671.png', 'gaussianBlockOneH_629548.png', 'gaussianBlockOneH_636274.png', 'gaussianBlockOneH_653292.png', 'gaussianBlockOneH_66687.png', 'gaussianBlockOneH_670118.png', 'gaussianBlockOneH_673815.png', 'gaussianBlockOneH_678941.png', 'gaussianBlockOneH_680176.png', 'gaussianBlockOneH_694769.png', 'gaussianBlockOneH_698886.png', 'gaussianBlockOneH_715496.png', 'gaussianBlockOneH_732943.png', 'gaussianBlockOneH_736863.png', 'gaussianBlockOneH_74485.png', 'gaussianBlockOneH_750188.png', 'gaussianBlockOneH_792581.png', 'gaussianBlockOneH_794414.png', 'gaussianBlockOneH_830265.png', 'gaussianBlockOneH_83326.png', 'gaussianBlockOneH_842488.png', 'gaussianBlockOneH_849418.png', 'gaussianBlockOneH_850164.png', 'gaussianBlockOneH_855167.png', 'gaussianBlockOneH_870482.png', 'gaussianBlockOneH_892276.png', 'gaussianBlockOneH_895842.png', 'gaussianBlockOneH_913395.png', 'gaussianBlockOneH_929047.png', 'gaussianBlockOneH_936013.png', 'gaussianBlockOneH_941779.png', 'gaussianBlockOneH_947117.png', 'gaussianBlockOneH_955961.png', 'gaussianBlockOneH_970682.png', 'gaussianBlockOneH_980031.png', 'gaussianBlockOneH_986841.png', 'gaussianBlockOneH_999301.png', 'gaussianBlockTwoH_114653.png', 'gaussianBlockTwoH_123963.png', 'gaussianBlockTwoH_130229.png', 'gaussianBlockTwoH_13591.png', 'gaussianBlockTwoH_151426.png', 'gaussianBlockTwoH_157.png', 'gaussianBlockTwoH_160212.png', 'gaussianBlockTwoH_160690.png', 'gaussianBlockTwoH_161567.png', 'gaussianBlockTwoH_161608.png', 'gaussianBlockTwoH_168027.png', 'gaussianBlockTwoH_174803.png', 'gaussianBlockTwoH_175692.png', 'gaussianBlockTwoH_18137.png', 'gaussianBlockTwoH_184604.png', 'gaussianBlockTwoH_195884.png', 'gaussianBlockTwoH_204676.png', 'gaussianBlockTwoH_205189.png', 'gaussianBlockTwoH_208182.png', 'gaussianBlockTwoH_222366.png', 'gaussianBlockTwoH_225242.png', 'gaussianBlockTwoH_227835.png', 'gaussianBlockTwoH_228272.png', 'gaussianBlockTwoH_240760.png', 'gaussianBlockTwoH_245311.png', 'gaussianBlockTwoH_245803.png', 'gaussianBlockTwoH_24682.png', 'gaussianBlockTwoH_248207.png', 'gaussianBlockTwoH_251127.png', 'gaussianBlockTwoH_263684.png', 'gaussianBlockTwoH_264081.png', 'gaussianBlockTwoH_268455.png', 'gaussianBlockTwoH_273917.png', 'gaussianBlockTwoH_274638.png', 'gaussianBlockTwoH_280524.png', 'gaussianBlockTwoH_28703.png', 'gaussianBlockTwoH_311213.png', 'gaussianBlockTwoH_312352.png', 'gaussianBlockTwoH_315864.png', 'gaussianBlockTwoH_338150.png', 'gaussianBlockTwoH_35141.png', 'gaussianBlockTwoH_36442.png', 'gaussianBlockTwoH_370372.png', 'gaussianBlockTwoH_387503.png', 'gaussianBlockTwoH_39129.png', 'gaussianBlockTwoH_394605.png', 'gaussianBlockTwoH_431331.png', 'gaussianBlockTwoH_440177.png', 'gaussianBlockTwoH_450536.png', 'gaussianBlockTwoH_451692.png', 'gaussianBlockTwoH_454257.png', 'gaussianBlockTwoH_45933.png', 'gaussianBlockTwoH_470833.png', 'gaussianBlockTwoH_471019.png', 'gaussianBlockTwoH_485316.png', 'gaussianBlockTwoH_494101.png', 'gaussianBlockTwoH_509368.png', 'gaussianBlockTwoH_515861.png', 'gaussianBlockTwoH_519066.png', 'gaussianBlockTwoH_524864.png', 'gaussianBlockTwoH_531579.png', 'gaussianBlockTwoH_534149.png', 'gaussianBlockTwoH_545852.png', 'gaussianBlockTwoH_548864.png', 'gaussianBlockTwoH_556216.png', 'gaussianBlockTwoH_559347.png', 'gaussianBlockTwoH_597423.png', 'gaussianBlockTwoH_624987.png', 'gaussianBlockTwoH_62625.png', 'gaussianBlockTwoH_656893.png', 'gaussianBlockTwoH_657235.png', 'gaussianBlockTwoH_6587.png', 'gaussianBlockTwoH_66063.png', 'gaussianBlockTwoH_672140.png', 'gaussianBlockTwoH_690715.png', 'gaussianBlockTwoH_691566.png', 'gaussianBlockTwoH_695807.png', 'gaussianBlockTwoH_739749.png', 'gaussianBlockTwoH_762109.png', 'gaussianBlockTwoH_781819.png', 'gaussianBlockTwoH_792212.png', 'gaussianBlockTwoH_798846.png', 'gaussianBlockTwoH_800190.png', 'gaussianBlockTwoH_800523.png', 'gaussianBlockTwoH_836800.png', 'gaussianBlockTwoH_848643.png', 'gaussianBlockTwoH_852172.png', 'gaussianBlockTwoH_854096.png', 'gaussianBlockTwoH_857003.png', 'gaussianBlockTwoH_889969.png', 'gaussianBlockTwoH_906823.png', 'gaussianBlockTwoH_917598.png', 'gaussianBlockTwoH_918388.png', 'gaussianBlockTwoH_950115.png', 'gaussianBlockTwoH_95044.png', 'gaussianBlockTwoH_966287.png', 'gaussianBlockTwoH_969243.png', 'gaussianBlockTwoH_982584.png', 'gaussianBlockTwoH_986406.png', 'gaussianBlockTwoH_986988.png', 'gaussianI_104148.png', 'gaussianI_128010.png', 'gaussianI_129355.png', 'gaussianI_14942.png', 'gaussianI_16184.png', 'gaussianI_167067.png', 'gaussianI_181555.png', 'gaussianI_188485.png', 'gaussianI_191487.png', 'gaussianI_19530.png', 'gaussianI_199793.png', 'gaussianI_202480.png', 'gaussianI_217622.png', 'gaussianI_219437.png', 'gaussianI_22033.png', 'gaussianI_227702.png', 'gaussianI_23.png', 'gaussianI_249612.png', 'gaussianI_269164.png', 'gaussianI_288900.png', 'gaussianI_295463.png', 'gaussianI_309934.png', 'gaussianI_312949.png', 'gaussianI_319389.png', 'gaussianI_320433.png', 'gaussianI_330636.png', 'gaussianI_342223.png', 'gaussianI_346690.png', 'gaussianI_347910.png', 'gaussianI_349161.png', 'gaussianI_349963.png', 'gaussianI_355324.png', 'gaussianI_360182.png', 'gaussianI_374121.png', 'gaussianI_376237.png', 'gaussianI_386465.png', 'gaussianI_390881.png', 'gaussianI_415379.png', 'gaussianI_440516.png', 'gaussianI_441797.png', 'gaussianI_46288.png', 'gaussianI_463424.png', 'gaussianI_469476.png', 'gaussianI_482041.png', 'gaussianI_48229.png', 'gaussianI_492486.png', 'gaussianI_49542.png', 'gaussianI_498877.png', 'gaussianI_510614.png', 'gaussianI_511698.png', 'gaussianI_516563.png', 'gaussianI_518620.png', 'gaussianI_518633.png', 'gaussianI_530507.png', 'gaussianI_539598.png', 'gaussianI_549759.png', 'gaussianI_571253.png', 'gaussianI_573343.png', 'gaussianI_579933.png', 'gaussianI_581798.png', 'gaussianI_595539.png', 'gaussianI_595811.png', 'gaussianI_599645.png', 'gaussianI_619887.png', 'gaussianI_622415.png', 'gaussianI_623377.png', 'gaussianI_627264.png', 'gaussianI_64154.png', 'gaussianI_641751.png', 'gaussianI_656387.png', 'gaussianI_669660.png', 'gaussianI_679094.png', 'gaussianI_684606.png', 'gaussianI_690756.png', 'gaussianI_7045.png', 'gaussianI_705714.png', 'gaussianI_711696.png', 'gaussianI_716824.png', 'gaussianI_733574.png', 'gaussianI_790794.png', 'gaussianI_792064.png', 'gaussianI_800280.png', 'gaussianI_80623.png', 'gaussianI_832682.png', 'gaussianI_834701.png', 'gaussianI_838383.png', 'gaussianI_859424.png', 'gaussianI_871542.png', 'gaussianI_878955.png', 'gaussianI_879688.png', 'gaussianI_881982.png', 'gaussianI_884150.png', 'gaussianI_888242.png', 'gaussianI_888782.png', 'gaussianI_889388.png', 'gaussianI_894870.png', 'gaussianI_92024.png', 'gaussianI_957396.png', 'gaussianI_957879.png', 'gaussianI_987018.png', 'gaussianUncorrelated_124241.png', 'gaussianUncorrelated_126628.png', 'gaussianUncorrelated_129029.png', 'gaussianUncorrelated_131068.png', 'gaussianUncorrelated_132274.png', 'gaussianUncorrelated_150770.png', 'gaussianUncorrelated_183110.png', 'gaussianUncorrelated_203236.png', 'gaussianUncorrelated_208406.png', 'gaussianUncorrelated_21380.png', 'gaussianUncorrelated_273638.png', 'gaussianUncorrelated_277919.png', 'gaussianUncorrelated_292743.png', 'gaussianUncorrelated_303010.png', 'gaussianUncorrelated_304313.png', 'gaussianUncorrelated_315991.png', 'gaussianUncorrelated_319700.png', 'gaussianUncorrelated_321156.png', 'gaussianUncorrelated_330265.png', 'gaussianUncorrelated_332722.png', 'gaussianUncorrelated_338294.png', 'gaussianUncorrelated_357333.png', 'gaussianUncorrelated_373890.png', 'gaussianUncorrelated_38339.png', 'gaussianUncorrelated_384234.png', 'gaussianUncorrelated_384419.png', 'gaussianUncorrelated_389920.png', 'gaussianUncorrelated_396224.png', 'gaussianUncorrelated_407875.png', 'gaussianUncorrelated_409486.png', 'gaussianUncorrelated_410045.png', 'gaussianUncorrelated_412346.png', 'gaussianUncorrelated_413993.png', 'gaussianUncorrelated_428896.png', 'gaussianUncorrelated_448587.png', 'gaussianUncorrelated_45141.png', 'gaussianUncorrelated_458062.png', 'gaussianUncorrelated_497861.png', 'gaussianUncorrelated_502103.png', 'gaussianUncorrelated_506670.png', 'gaussianUncorrelated_512547.png', 'gaussianUncorrelated_518473.png', 'gaussianUncorrelated_519655.png', 'gaussianUncorrelated_523130.png', 'gaussianUncorrelated_52497.png', 'gaussianUncorrelated_546265.png', 'gaussianUncorrelated_558038.png', 'gaussianUncorrelated_559083.png', 'gaussianUncorrelated_561878.png', 'gaussianUncorrelated_563111.png', 'gaussianUncorrelated_576050.png', 'gaussianUncorrelated_57984.png', 'gaussianUncorrelated_580386.png', 'gaussianUncorrelated_590593.png', 'gaussianUncorrelated_595317.png', 'gaussianUncorrelated_620219.png', 'gaussianUncorrelated_621845.png', 'gaussianUncorrelated_641709.png', 'gaussianUncorrelated_646904.png', 'gaussianUncorrelated_659163.png', 'gaussianUncorrelated_691564.png', 'gaussianUncorrelated_692411.png', 'gaussianUncorrelated_69338.png', 'gaussianUncorrelated_694708.png', 'gaussianUncorrelated_696819.png', 'gaussianUncorrelated_705280.png', 'gaussianUncorrelated_712334.png', 'gaussianUncorrelated_721397.png', 'gaussianUncorrelated_722521.png', 'gaussianUncorrelated_736306.png', 'gaussianUncorrelated_745940.png', 'gaussianUncorrelated_763123.png', 'gaussianUncorrelated_774941.png', 'gaussianUncorrelated_7863.png', 'gaussianUncorrelated_78838.png', 'gaussianUncorrelated_802104.png', 'gaussianUncorrelated_816903.png', 'gaussianUncorrelated_81923.png', 'gaussianUncorrelated_820339.png', 'gaussianUncorrelated_831881.png', 'gaussianUncorrelated_834010.png', 'gaussianUncorrelated_841963.png', 'gaussianUncorrelated_842420.png', 'gaussianUncorrelated_853818.png', 'gaussianUncorrelated_857561.png', 'gaussianUncorrelated_865995.png', 'gaussianUncorrelated_869222.png', 'gaussianUncorrelated_876218.png', 'gaussianUncorrelated_895824.png', 'gaussianUncorrelated_900652.png', 'gaussianUncorrelated_902635.png', 'gaussianUncorrelated_918426.png', 'gaussianUncorrelated_923074.png', 'gaussianUncorrelated_923544.png', 'gaussianUncorrelated_923598.png', 'gaussianUncorrelated_939626.png', 'gaussianUncorrelated_944711.png', 'gaussianUncorrelated_958392.png', 'gaussianUncorrelated_985116.png', 'gaussianUncorrelated_993277.png'];
    
    // create timeline 
    var timeline = [];
    
    // Define the checkbox screen
    let sourceOfSubject = {
      type: jsPsychSurveyMultiChoice,
      questions: [
        {
          prompt: "Through what website did you access this study?",
          options: ["Prolific", "Sona", "Other"],
          required: true  // Ensures the user selects at least one option
        }
      ],
      data: {
        trial_name: 'source_of_subject'
      },
      on_finish: function(data) {
        // Store the checkbox response globally to access later in conditional trial
        jsPsych.data.addProperties({ selectedSource: data.response.Q0 });
      }
    };
    
    // Define a conditional trial to dynamically adjust the prompt for text entry
    let textEntryTrial = {
      type: jsPsychSurveyText,
      questions: function() {
        // Get the previously selected option
        let selectedOptions = jsPsych.data.get().last(1).values()[0].selectedSource;
        
        // Define the prompt and placeholder based on the response
        let textPrompt;
        let placeholder;
        
        if (selectedOptions.includes("Prolific")) {
          textPrompt = "Please enter your unique Prolific Identifier";
          placeholder = 'Prolfic ID';
        } else if (selectedOptions.includes("Sona")) {
          textPrompt = "Please enter your Sona ID";
          placeholder = 'Sona ID';
        } else {
          textPrompt = "Please enter your email address";
          placeholder = "(e.g. johnDoe123@gmail.com)";
        }
        
        // Return the dynamic question
        return [{
          prompt: textPrompt,
          placeholder: placeholder,
          rows: 1,
          columns: 40
        }];
      },
      on_finish: function(data) {
        // Log the response for debugging
         jsPsych.data.addProperties({ userID: data.response.Q0 });
      }
    };
    
    // Add both trials to the timeline
    timeline.push(sourceOfSubject);
    timeline.push(textEntryTrial);
    
    
        // Define the consent screen
    let consentTrial = {
      type: jsPsychSurveyMultiChoice,
      questions: [
        {
          prompt: "Please read the consent form and indicate your choice below:",
          options: ["I consent", "I do not consent"],
          required: true,  // Make sure the user must select an option
          horizontal: false // Vertical alignment of the checkboxes
        }
      ],
      preamble: `
        <h3>Consent Form</h3>
        <p>Please read the following:</p>
        <p>This study involves a series of tasks that require you to respond to various stimuli...</p>
        <p>If you consent to participate, please indicate by selecting "I consent" below.</p>
      `,
      on_finish: function(data) {
        // Get the user's response
        let consentResponse = data.response.Q0;
        
        // If the user does not consent, end the experiment
        if (consentResponse === "I do not consent") {
          jsPsych.endExperiment("You chose not to consent. The experiment will now end.");
        }
      }
    };
    
    // Add the consent trial to the timeline
    timeline.push(consentTrial);


    
    
    // Experiment Instructions
    const instructions = {
        type: jsPsychHtmlKeyboardResponse,
        stimulus: `
            <p>In this task you will be shown a series of squares which contain a pattern of black and white pixels. </p>
            <p>In half of the trials, a black <b>H</b> will be present in the pattern. You will be asked to determine whether or not the <b>H</b> is in the image.
            It will be very difficult to make this determination, but trust your intuition. The <b>H</b> will not be obvious, but it is always centered, and you will be shown an image of the <b>H</b> for reference before you begin.</p>
            
            <p>For each image, please press <b>Y</b> if you see the <b>H</b> and press <b>N</b> if you do not see the <b>H</b>.</p>
            
            <p>Remember, you will be better at this task than you think.</p> 
                
            <p>Thank you for participating.</p>
            
            <p>Press the spacebar to continue.</p>
            `,
        choices: " ",
        post_trial_gap: 2000
    };
    timeline.push(instructions);
    
    // Experiment Instructions 2
    const instructions2 = {
        type: jsPsychHtmlKeyboardResponse,
        stimulus: `
            <p>Remember to press <b>Y</b> if you believe that you see an <b>H</b>.</p>
            
            <p>Remember to press <b>N</b> if you do not believe that you see an <b>H</b>.</p>
            
            <p>You will now be shown the template <b>H</b> that will be in half of the stimuli.</p>
            
            <p>You will have 10 seconds to view the template <b>H</b>.</p>
            
            <p>After those 10 seconds, the first image will automatically appear and you will begin making your selections.</p>

            <p>Press the spacebar to continue when you are ready.</p>
            `,
        choices: " ",
        post_trial_gap: 2000
    };
    timeline.push(instructions2);
    
    // display the template H for 10 seconds
    var displayTemplate = {
        type: jsPsychImageKeyboardResponse,
        stimulus: 'H.png',
        choices: "NO_KEYS",  // Do not allow any keypresses
        trial_duration: 10000 // 10000 milliseconds = 10 seconds
    };
    timeline.push(displayTemplate);
    
    // Block one code
    // CONDITION == 1 for H/Uncorrelated
    // CONDITION == 2 for H/I
    // filter the stimuli to get this block's stimuli
    let blockOneStimuli;
    if (CONDITION == 1) {
      blockOneStimuli = stimuli.filter(stimulus => stimulus.includes('BlockOneH') || stimulus.includes('Uncorrelated'));
    }
    else {
      blockOneStimuli = stimuli.filter(stimulus => stimulus.includes('BlockOneH') || stimulus.includes('gaussianI'));
    }
    
    // randomly shuffle the stimuli
    blockOneStimuli = jsPsych.randomization.shuffle(blockOneStimuli);
    
    // push trials to the timeline
    let trialNumber = 1;
    for (let stimulus of blockOneStimuli) {
      
      let curStimulus = stimulus;
      let trial = {
        type: jsPsychImageKeyboardResponse,
        stimulus: curStimulus,
        choices: ["y", "n"],
        data: {
          stimulusName: curStimulus,  // Record the stimulus name
          trialNumber: trialNumber,   // Record the trial number
          stimulusType: curStimulus.includes('BlockOneH') ? 'target' : 'distractor'
          }, 
        post_trial_gap: 2000,
        on_finish: function(data) {
          
          // Map 'y' and 'n' responses to target/distractor labels
          data.responseType = data.response === 'y' ? 'target' : 'distractor';
          data.responseTime = data.rt;
          data.blockType = CONDITION == 1 ? 'Uncorrelated': 'I-Correlated';
          data.weightingScheme = 'gaussian';
          data.blockOrder = CONDITION == 1 ? 'Uncorrelated First': 'I-Correlated First';
        }
      };
      
      // push trial to timeline
      timeline.push(trial);
      
      // increment the trial counter
      trialNumber++;
    }

    // break screen 
    var breakScreen = {
      type: jsPsychHtmlKeyboardResponse,
      stimulus: `
      <p>You have completed half of the trials.</p>
      
      <p>When you are ready, you will be shown the template <b>H</b> again and you will resume the task.</p>
      
      <p>Remember, press <b>Y</b> if you see the <b>H</b> and press <b>N</b> if you do not see the <b>H</b>.</p>
    
      <p>This task feels difficult, but keep following your intuition and you will do great.</p>
      
      <p>Press the spacebar to continue</p>
      `,
      choices: " ",
      post_trial_gap: 2000
    };
    timeline.push(breakScreen);
    timeline.push(displayTemplate); // display the template once more
    
    
    
    // code for block 2 here
    // CONDITION == 1 for H/I
    // CONDITION == 2 for H/Uncorrelated
    // filter the stimuli to get this block's stimuli
    let blockTwoStimuli;
    if (CONDITION == 1) {
      blockTwoStimuli = stimuli.filter(stimulus => stimulus.includes('BlockTwoH') || stimulus.includes('gaussianI'));
    }
    else {
      blockTwoStimuli = stimuli.filter(stimulus => stimulus.includes('BlockTwoH') || stimulus.includes('Uncorrelated'));
    }
    
    // randomly shuffle the stimuli
    blockTwoStimuli = jsPsych.randomization.shuffle(blockTwoStimuli);
    
    // push trials to the timeline
    trialNumber = 1;
    for (let stimulus of blockTwoStimuli) {
      
      let curStimulus = stimulus;
      let trial = {
        type: jsPsychImageKeyboardResponse,
        stimulus: curStimulus,
        choices: ["y", "n"],
        data: {
          stimulusName: curStimulus,  // Record the stimulus name
          trialNumber: trialNumber,   // Record the trial number
          stimulusType: curStimulus.includes('BlockTwoH') ? 'target' : 'distractor'
          }, 
        post_trial_gap: 2000,
        on_finish: function(data) {
          // Map 'y' and 'n' responses to target/distractor labels
          data.responseType = data.response === 'y' ? 'target' : 'distractor';
          data.responseTime = data.rt;
          data.blockType = CONDITION == 1 ? 'I-Correlated': 'Uncorrelated';
          data.weightingScheme = 'gaussian';
          data.blockOrder = CONDITION == 1 ? 'Uncorrelated First': 'I-Correlated First';
        }
      };
      
      // push trial to timeline
      timeline.push(trial);
      
      // increment the trial counter
      trialNumber++;
    }

  
    // thank user for participating and goodbye
    var goodbyeScreen = {
      type: jsPsychHtmlKeyboardResponse,
      stimulus: `
      <p>You have now completed the experiment.</p>
      
      <p>Press the spacebar to finish the experiment</p>
      `,
      choices: " ",
      on_finish: function(){
        jsPsych.endExperiment("Thank you for participating!");
      }
    };
    timeline.push(goodbyeScreen);
    
    
    jsPsych.run(timeline);