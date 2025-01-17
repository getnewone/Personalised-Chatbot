$(document).ready(function () {
    $('#toggleIcon').click(function () {
        $('#chatContainer').toggle();
    });

    $('#chatForm').submit(function (event) {
        event.preventDefault();
        var userInput = $('#user_input').val();
        $('#chatMessages').append('<div class="message user-message">' + userInput + '</div>');

        $.ajax({
            type: 'POST',
            url: '/chat',
            data: JSON.stringify({ user_input: userInput }),
            contentType: 'application/json',
            success: function (response) {
                $('#chatMessages').append('<div class="message bot-message">' + response + '</div>');
                $('#user_input').val('');
            },
            error: function () {
                alert('Error occurred');
            }
        });
    });
});
