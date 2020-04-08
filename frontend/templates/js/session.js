/**
 * Send a POST request to the /session endpoint which launches a Multivac session. Once the session concludes,
 * redirect back to the main page. If the session was a failure, then also display an alert message.
 */
function sendSessionRequest(environmentName, agentName, numSteps, observationDelta, videoFps) {
    var request = new XMLHttpRequest();

    // Gather input parameters
    var data = new FormData();
    data.append('environmentName', environmentName);
    data.append('agentName', agentName);
    data.append('numSteps', numSteps);
    data.append('observationDelta', observationDelta);
    data.append('videoFps', videoFps);

    request.open('POST', '/session');

    request.onload = function() {
        if (request.status === 200 && request.responseText === 'success') {
            // Session was a success, redirect user.
            window.location = '/';
        } else {
            alert('Multivac session failed - see logs for more information.')
            window.location = '/';
        };
    };

    request.send(data);
};
