(function ($) {
    "use strict";

    $('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })

    /**
     * Validate inputs from the launcher form.
     * @param numSteps: number of steps parsed from the form
     * @param observationDelta: observation delta parsed from the form
     * @param videoFps: video frames per second parsed from the form
     * @return empty string if parameters are valid; otherwise nonempty string containing an alert message.
     */
    function validateInputs(numSteps, observationDelta, videoFps) {
        var check = true;
        var alertMessage = "Invalid parameters specified:\n";

        var numStepsVal = $(numSteps).val();
        if (numStepsVal === "" || numStepsVal <= 0) {
            check=false;
            alertMessage += "Number of steps must be greater than zero.\n";
        }

        var observationDeltaVal = $(observationDelta).val();
        if (observationDeltaVal === "" || observationDeltaVal < 0) {
            check=false;
            alertMessage += "Observation delta must be greater than zero.\n";
        }

        var videoFpsVal = $(videoFps).val();
        if (videoFpsVal === "" || videoFpsVal < 1) {
            check=false;
            alertMessage += "Video fps must be greater than or equal to 1.\n";
        }

        if (check) {
            return "";
        } else {
            return alertMessage;
        }
    };

    /**
     * Upon click of the form button,
     *   i) Validate inputs
     *   ii) Send a POST request to session endpoint with parameters from the launcher form
     */
    $("#launch-btn").click(function() {
        var environmentName = $('.validate-input input[name="environment_name"]');
        var agentName = $('.validate-input input[name="agent_name"]');
        var numSteps = $('.validate-input input[name="num_steps"]');
        var observationDelta = $('.validate-input input[name="observation_delta"]');
        var videoFps = $('.validate-input input[name="video_fps"]');

        var alertMessage = validateInputs(numSteps, observationDelta, videoFps);

        if (alertMessage === "") {
            // TODO: send POST request
            alert("Correct inputs!");
        } else {
            alert(alertMessage);
        }
    });
})(jQuery);
