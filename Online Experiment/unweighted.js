document.body.style.backgroundColor = "#777777"; 
    // initialize jsPsych
    var jsPsych = initJsPsych({
      on_finish: function() {
        jsPsych.data.displayData();
      }
    });

    // list of all the stimuli
    const stimuli = ['unweightedBlockOneH_12805.png', 'unweightedBlockOneH_145710.png', 'unweightedBlockOneH_151253.png', 'unweightedBlockOneH_164113.png', 'unweightedBlockOneH_175912.png', 'unweightedBlockOneH_217636.png', 'unweightedBlockOneH_250099.png', 'unweightedBlockOneH_253406.png', 'unweightedBlockOneH_253909.png', 'unweightedBlockOneH_254626.png', 'unweightedBlockOneH_256858.png', 'unweightedBlockOneH_267916.png', 'unweightedBlockOneH_275468.png', 'unweightedBlockOneH_286783.png', 'unweightedBlockOneH_289537.png', 'unweightedBlockOneH_300585.png', 'unweightedBlockOneH_30990.png', 'unweightedBlockOneH_33699.png', 'unweightedBlockOneH_363734.png', 'unweightedBlockOneH_37117.png', 'unweightedBlockOneH_373915.png', 'unweightedBlockOneH_378435.png', 'unweightedBlockOneH_381034.png', 'unweightedBlockOneH_383424.png', 'unweightedBlockOneH_407758.png', 'unweightedBlockOneH_412474.png', 'unweightedBlockOneH_43094.png', 'unweightedBlockOneH_44194.png', 'unweightedBlockOneH_442288.png', 'unweightedBlockOneH_443599.png', 'unweightedBlockOneH_448425.png', 'unweightedBlockOneH_452597.png', 'unweightedBlockOneH_45503.png', 'unweightedBlockOneH_455890.png', 'unweightedBlockOneH_465390.png', 'unweightedBlockOneH_467977.png', 'unweightedBlockOneH_469445.png', 'unweightedBlockOneH_473549.png', 'unweightedBlockOneH_477991.png', 'unweightedBlockOneH_480641.png', 'unweightedBlockOneH_482661.png', 'unweightedBlockOneH_482695.png', 'unweightedBlockOneH_483285.png', 'unweightedBlockOneH_489688.png', 'unweightedBlockOneH_521608.png', 'unweightedBlockOneH_532282.png', 'unweightedBlockOneH_538607.png', 'unweightedBlockOneH_539906.png', 'unweightedBlockOneH_557959.png', 'unweightedBlockOneH_559683.png', 'unweightedBlockOneH_562069.png', 'unweightedBlockOneH_56746.png', 'unweightedBlockOneH_599186.png', 'unweightedBlockOneH_61793.png', 'unweightedBlockOneH_638101.png', 'unweightedBlockOneH_651182.png', 'unweightedBlockOneH_653847.png', 'unweightedBlockOneH_655320.png', 'unweightedBlockOneH_656436.png', 'unweightedBlockOneH_670014.png', 'unweightedBlockOneH_686494.png', 'unweightedBlockOneH_695102.png', 'unweightedBlockOneH_696293.png', 'unweightedBlockOneH_734539.png', 'unweightedBlockOneH_752809.png', 'unweightedBlockOneH_770444.png', 'unweightedBlockOneH_775531.png', 'unweightedBlockOneH_785071.png', 'unweightedBlockOneH_789782.png', 'unweightedBlockOneH_8031.png', 'unweightedBlockOneH_810610.png', 'unweightedBlockOneH_81810.png', 'unweightedBlockOneH_821460.png', 'unweightedBlockOneH_831536.png', 'unweightedBlockOneH_8357.png', 'unweightedBlockOneH_837623.png', 'unweightedBlockOneH_850710.png', 'unweightedBlockOneH_851918.png', 'unweightedBlockOneH_856816.png', 'unweightedBlockOneH_857641.png', 'unweightedBlockOneH_864054.png', 'unweightedBlockOneH_873151.png', 'unweightedBlockOneH_882338.png', 'unweightedBlockOneH_883529.png', 'unweightedBlockOneH_896334.png', 'unweightedBlockOneH_896963.png', 'unweightedBlockOneH_905349.png', 'unweightedBlockOneH_911148.png', 'unweightedBlockOneH_938935.png', 'unweightedBlockOneH_950076.png', 'unweightedBlockOneH_960718.png', 'unweightedBlockOneH_963788.png', 'unweightedBlockOneH_967136.png', 'unweightedBlockOneH_971134.png', 'unweightedBlockOneH_972001.png', 'unweightedBlockOneH_973071.png', 'unweightedBlockOneH_975229.png', 'unweightedBlockOneH_993389.png', 'unweightedBlockOneH_998584.png', 'unweightedBlockOneH_999363.png', 'unweightedBlockTwoH_103477.png', 'unweightedBlockTwoH_104416.png', 'unweightedBlockTwoH_151657.png', 'unweightedBlockTwoH_166606.png', 'unweightedBlockTwoH_169043.png', 'unweightedBlockTwoH_187597.png', 'unweightedBlockTwoH_211906.png', 'unweightedBlockTwoH_214258.png', 'unweightedBlockTwoH_215717.png', 'unweightedBlockTwoH_224234.png', 'unweightedBlockTwoH_227547.png', 'unweightedBlockTwoH_22902.png', 'unweightedBlockTwoH_237526.png', 'unweightedBlockTwoH_240470.png', 'unweightedBlockTwoH_251561.png', 'unweightedBlockTwoH_266166.png', 'unweightedBlockTwoH_289636.png', 'unweightedBlockTwoH_301147.png', 'unweightedBlockTwoH_303550.png', 'unweightedBlockTwoH_305060.png', 'unweightedBlockTwoH_308223.png', 'unweightedBlockTwoH_319014.png', 'unweightedBlockTwoH_335323.png', 'unweightedBlockTwoH_349881.png', 'unweightedBlockTwoH_352122.png', 'unweightedBlockTwoH_372841.png', 'unweightedBlockTwoH_374805.png', 'unweightedBlockTwoH_375577.png', 'unweightedBlockTwoH_388675.png', 'unweightedBlockTwoH_394469.png', 'unweightedBlockTwoH_424287.png', 'unweightedBlockTwoH_428649.png', 'unweightedBlockTwoH_434839.png', 'unweightedBlockTwoH_438119.png', 'unweightedBlockTwoH_438847.png', 'unweightedBlockTwoH_470338.png', 'unweightedBlockTwoH_486730.png', 'unweightedBlockTwoH_496119.png', 'unweightedBlockTwoH_511392.png', 'unweightedBlockTwoH_524853.png', 'unweightedBlockTwoH_530855.png', 'unweightedBlockTwoH_546964.png', 'unweightedBlockTwoH_556256.png', 'unweightedBlockTwoH_561451.png', 'unweightedBlockTwoH_564156.png', 'unweightedBlockTwoH_569531.png', 'unweightedBlockTwoH_56963.png', 'unweightedBlockTwoH_570894.png', 'unweightedBlockTwoH_571417.png', 'unweightedBlockTwoH_577881.png', 'unweightedBlockTwoH_601610.png', 'unweightedBlockTwoH_604248.png', 'unweightedBlockTwoH_613889.png', 'unweightedBlockTwoH_635714.png', 'unweightedBlockTwoH_642666.png', 'unweightedBlockTwoH_645520.png', 'unweightedBlockTwoH_653484.png', 'unweightedBlockTwoH_657885.png', 'unweightedBlockTwoH_666466.png', 'unweightedBlockTwoH_68124.png', 'unweightedBlockTwoH_692423.png', 'unweightedBlockTwoH_704385.png', 'unweightedBlockTwoH_708742.png', 'unweightedBlockTwoH_718086.png', 'unweightedBlockTwoH_719366.png', 'unweightedBlockTwoH_721123.png', 'unweightedBlockTwoH_727383.png', 'unweightedBlockTwoH_729704.png', 'unweightedBlockTwoH_739469.png', 'unweightedBlockTwoH_740473.png', 'unweightedBlockTwoH_744141.png', 'unweightedBlockTwoH_755057.png', 'unweightedBlockTwoH_772743.png', 'unweightedBlockTwoH_77362.png', 'unweightedBlockTwoH_774928.png', 'unweightedBlockTwoH_801220.png', 'unweightedBlockTwoH_816027.png', 'unweightedBlockTwoH_818943.png', 'unweightedBlockTwoH_82376.png', 'unweightedBlockTwoH_829784.png', 'unweightedBlockTwoH_832853.png', 'unweightedBlockTwoH_836899.png', 'unweightedBlockTwoH_845373.png', 'unweightedBlockTwoH_845384.png', 'unweightedBlockTwoH_868566.png', 'unweightedBlockTwoH_894601.png', 'unweightedBlockTwoH_895909.png', 'unweightedBlockTwoH_898896.png', 'unweightedBlockTwoH_904973.png', 'unweightedBlockTwoH_909331.png', 'unweightedBlockTwoH_915149.png', 'unweightedBlockTwoH_919966.png', 'unweightedBlockTwoH_934639.png', 'unweightedBlockTwoH_956010.png', 'unweightedBlockTwoH_97038.png', 'unweightedBlockTwoH_978523.png', 'unweightedBlockTwoH_978630.png', 'unweightedBlockTwoH_984958.png', 'unweightedBlockTwoH_993736.png', 'unweightedBlockTwoH_99535.png', 'unweightedI_101338.png', 'unweightedI_126909.png', 'unweightedI_131858.png', 'unweightedI_133946.png', 'unweightedI_13475.png', 'unweightedI_137504.png', 'unweightedI_138245.png', 'unweightedI_180982.png', 'unweightedI_187508.png', 'unweightedI_188349.png', 'unweightedI_21534.png', 'unweightedI_216760.png', 'unweightedI_239674.png', 'unweightedI_247110.png', 'unweightedI_248824.png', 'unweightedI_274035.png', 'unweightedI_300258.png', 'unweightedI_30849.png', 'unweightedI_311203.png', 'unweightedI_316505.png', 'unweightedI_334347.png', 'unweightedI_337975.png', 'unweightedI_353556.png', 'unweightedI_364633.png', 'unweightedI_368130.png', 'unweightedI_37564.png', 'unweightedI_376685.png', 'unweightedI_378334.png', 'unweightedI_380467.png', 'unweightedI_384970.png', 'unweightedI_389194.png', 'unweightedI_389195.png', 'unweightedI_406415.png', 'unweightedI_410883.png', 'unweightedI_434222.png', 'unweightedI_444791.png', 'unweightedI_452312.png', 'unweightedI_453134.png', 'unweightedI_455150.png', 'unweightedI_456779.png', 'unweightedI_457675.png', 'unweightedI_458307.png', 'unweightedI_458457.png', 'unweightedI_459133.png', 'unweightedI_470546.png', 'unweightedI_476244.png', 'unweightedI_495327.png', 'unweightedI_514642.png', 'unweightedI_522463.png', 'unweightedI_54619.png', 'unweightedI_578793.png', 'unweightedI_58054.png', 'unweightedI_58219.png', 'unweightedI_620823.png', 'unweightedI_625391.png', 'unweightedI_630962.png', 'unweightedI_638020.png', 'unweightedI_646713.png', 'unweightedI_646854.png', 'unweightedI_6543.png', 'unweightedI_657825.png', 'unweightedI_658302.png', 'unweightedI_680686.png', 'unweightedI_682242.png', 'unweightedI_68975.png', 'unweightedI_690214.png', 'unweightedI_717574.png', 'unweightedI_723074.png', 'unweightedI_728483.png', 'unweightedI_73820.png', 'unweightedI_752027.png', 'unweightedI_75397.png', 'unweightedI_760211.png', 'unweightedI_768552.png', 'unweightedI_778970.png', 'unweightedI_780323.png', 'unweightedI_783826.png', 'unweightedI_794523.png', 'unweightedI_803984.png', 'unweightedI_813126.png', 'unweightedI_826295.png', 'unweightedI_828640.png', 'unweightedI_862838.png', 'unweightedI_865696.png', 'unweightedI_86584.png', 'unweightedI_867507.png', 'unweightedI_868896.png', 'unweightedI_87043.png', 'unweightedI_878854.png', 'unweightedI_887950.png', 'unweightedI_890635.png', 'unweightedI_89542.png', 'unweightedI_904357.png', 'unweightedI_905375.png', 'unweightedI_908631.png', 'unweightedI_966503.png', 'unweightedI_985594.png', 'unweightedI_988450.png', 'unweightedI_988818.png', 'unweightedI_992086.png', 'unweightedUncorrelated_109821.png', 'unweightedUncorrelated_121645.png', 'unweightedUncorrelated_128170.png', 'unweightedUncorrelated_129443.png', 'unweightedUncorrelated_13651.png', 'unweightedUncorrelated_146922.png', 'unweightedUncorrelated_157352.png', 'unweightedUncorrelated_158224.png', 'unweightedUncorrelated_162639.png', 'unweightedUncorrelated_165722.png', 'unweightedUncorrelated_183343.png', 'unweightedUncorrelated_188716.png', 'unweightedUncorrelated_19836.png', 'unweightedUncorrelated_198395.png', 'unweightedUncorrelated_198988.png', 'unweightedUncorrelated_215183.png', 'unweightedUncorrelated_219955.png', 'unweightedUncorrelated_23330.png', 'unweightedUncorrelated_235871.png', 'unweightedUncorrelated_239350.png', 'unweightedUncorrelated_249130.png', 'unweightedUncorrelated_255309.png', 'unweightedUncorrelated_256445.png', 'unweightedUncorrelated_26358.png', 'unweightedUncorrelated_276195.png', 'unweightedUncorrelated_283189.png', 'unweightedUncorrelated_289269.png', 'unweightedUncorrelated_304933.png', 'unweightedUncorrelated_324296.png', 'unweightedUncorrelated_332723.png', 'unweightedUncorrelated_342542.png', 'unweightedUncorrelated_368284.png', 'unweightedUncorrelated_37389.png', 'unweightedUncorrelated_39112.png', 'unweightedUncorrelated_393916.png', 'unweightedUncorrelated_405814.png', 'unweightedUncorrelated_422747.png', 'unweightedUncorrelated_42582.png', 'unweightedUncorrelated_428021.png', 'unweightedUncorrelated_433140.png', 'unweightedUncorrelated_439875.png', 'unweightedUncorrelated_450795.png', 'unweightedUncorrelated_462081.png', 'unweightedUncorrelated_463568.png', 'unweightedUncorrelated_463649.png', 'unweightedUncorrelated_477272.png', 'unweightedUncorrelated_484863.png', 'unweightedUncorrelated_497407.png', 'unweightedUncorrelated_509430.png', 'unweightedUncorrelated_518857.png', 'unweightedUncorrelated_524849.png', 'unweightedUncorrelated_542015.png', 'unweightedUncorrelated_543059.png', 'unweightedUncorrelated_545608.png', 'unweightedUncorrelated_548364.png', 'unweightedUncorrelated_552001.png', 'unweightedUncorrelated_569574.png', 'unweightedUncorrelated_582171.png', 'unweightedUncorrelated_589815.png', 'unweightedUncorrelated_597570.png', 'unweightedUncorrelated_597758.png', 'unweightedUncorrelated_637780.png', 'unweightedUncorrelated_639292.png', 'unweightedUncorrelated_642939.png', 'unweightedUncorrelated_653412.png', 'unweightedUncorrelated_655639.png', 'unweightedUncorrelated_663075.png', 'unweightedUncorrelated_663811.png', 'unweightedUncorrelated_675035.png', 'unweightedUncorrelated_690056.png', 'unweightedUncorrelated_69495.png', 'unweightedUncorrelated_72179.png', 'unweightedUncorrelated_729699.png', 'unweightedUncorrelated_735406.png', 'unweightedUncorrelated_73606.png', 'unweightedUncorrelated_743442.png', 'unweightedUncorrelated_753273.png', 'unweightedUncorrelated_753633.png', 'unweightedUncorrelated_754620.png', 'unweightedUncorrelated_765706.png', 'unweightedUncorrelated_772787.png', 'unweightedUncorrelated_78065.png', 'unweightedUncorrelated_788715.png', 'unweightedUncorrelated_790745.png', 'unweightedUncorrelated_792472.png', 'unweightedUncorrelated_840345.png', 'unweightedUncorrelated_849034.png', 'unweightedUncorrelated_850634.png', 'unweightedUncorrelated_852216.png', 'unweightedUncorrelated_8663.png', 'unweightedUncorrelated_873657.png', 'unweightedUncorrelated_88389.png', 'unweightedUncorrelated_884744.png', 'unweightedUncorrelated_897115.png', 'unweightedUncorrelated_913332.png', 'unweightedUncorrelated_949336.png', 'unweightedUncorrelated_951843.png', 'unweightedUncorrelated_968064.png', 'unweightedUncorrelated_973540.png', 'unweightedUncorrelated_982578.png'];
    
    // create timeline 
    var timeline = [];
    
    // Define the checkbox screen
    let sourceOfSubject = {
      type: jsPsychSurveyMultiChoice,
      questions: [
        {
          prompt: "Through what website did you access this study?",
          options: ["Prolific", "Sona", "Other"],
          required: true  
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
          placeholder = "e.g. johnDoe123@gmail.com";
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
          required: true,  
          horizontal: false 
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
      blockOneStimuli = stimuli.filter(stimulus => stimulus.includes('BlockOneH') || stimulus.includes('unweightedI'));
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
          data.weightingScheme = 'unweighted';
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
      blockTwoStimuli = stimuli.filter(stimulus => stimulus.includes('BlockTwoH') || stimulus.includes('unweightedI'));
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
          data.weightingScheme = 'unweighted';
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