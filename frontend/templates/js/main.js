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

        if (numSteps === "") {
            check=false;
            alertMessage += "Number of steps is required\n";
        }

        if (observationDelta === "") {
            check=false;
            alertMessage += "Observation delta is required\n";
        }

        if (videoFps === "") {
            check=false;
            alertMessage += "Video fps is required\n";
        }

        if (check) {
            return "";
        } else {
            return alertMessage;
        }
    };

    /**
     * Upon click of the form button, validate the inputs. If inputs are properly provided, return true and proceed as
     * normal for form submission. Otherwise, raise an alert and return false to indicate form should not be submitted.
     */
    $("#launcher-form").submit(function(event) {
        var environmentName = $('select[name="environmentName"]').val();
        var agentName = $('select[name="agentName"]').val();
        var numSteps = $('.validate-input input[name="numSteps"]').val();
        var observationDelta = $('.validate-input input[name="observationDelta"]').val();
        var videoFps = $('.validate-input input[name="videoFps"]').val();

        var alertMessage = validateInputs(numSteps, observationDelta, videoFps);

        if (alertMessage === "") {
            return true;
        } else {
            alert(alertMessage);
            return false;
        }
    });
})(jQuery);
