$(document).ready(function () {
    $('#send-btn').click(function () {
        var userMessage = $('#user-input').val().trim();
        if (userMessage === "") return;

        // Display user message
        $('#chat-box').append('<div class="message user-msg">' + userMessage + '</div>');
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);

        // Clear input field
        $('#user-input').val('');

        // Default conversation ID
        var conversationId = 'default_conversation';

        // Send message to Flask backend
        $.ajax({
            url: '/chat/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "message": userMessage,
                "role": "user",
                "conversation_id": conversationId
            }),
            success: function (response) {
                var botResponse = response.response;

                // Display bot response
                $('#chat-box').append('<div class="message bot-msg">' + botResponse + '</div>');
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            },
            error: function (xhr, status, error) {
                $('#chat-box').append('<div class="message bot-msg">Error: ' + error + '</div>');
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            }
        });
    });

    // Allow "Enter" key to send message
    $('#user-input').keypress(function (e) {
        if (e.which === 13) {
            $('#send-btn').click();
        }
    });
});
