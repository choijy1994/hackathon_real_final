$(document).ready(function () {
    
    

//    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    var socket = new WebSocket(
        'ws://' + window.location.host +
        '/ws?session_key=${sessionKey}')

    // chatInput.keypress(function (e) {
    //     if (e.keyCode == 13)
    //         chatButton.click();
    // });

    // chatButton.click(function () {
    //     if (chatInput.val().length > 0) {
    //         sendMessage(currentRecipient, chatInput.val());
    //         chatInput.val('');
    //     }
    // });

    socket.onmessage = function (e) {        
        alert('new message');
    };
});
