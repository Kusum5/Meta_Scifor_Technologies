$(document).ready(function () {

    eel.init()()
    //siriWave configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 640,
        height: 200,
        style: "ios9",
        speed:"0.25",
        amplitude:"1",
        autostart:true,
      });
    //mic button handler
    $("#MicBtn").click(function () {
        eel.playAssistantSound()
        $("#Oval").prop('hidden', true);
        $("#SiriWave").prop('hidden', false);
        eel.allCommands()()
    });
    function doc_keyUp(e){
        if(e.key === 'q' && e.metaKey)
        {
            eel.playAssistantSound()
            $("#Oval").attr("hidden",true);
            $("#SiriWave").attr("hidden",false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup',doc_keyUp,false);
    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }
    //function to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }
    // key up event handler on text box
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message)    
    });
    // send button event handler
    $("#SendBtn").click(function () {   
        let message = $("#chatbox").val()
        PlayAssistant(message)    
    });
    // enter press event handler on chat box
      $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });
});