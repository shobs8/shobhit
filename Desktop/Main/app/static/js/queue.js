$(document).ready( function() {
    $('#btnQueueIndv').on('click', () => {
        $('.queue-buttons').hide();
        $('.preloader-queue').show();

        var queueType = 0;
        var indvSelGame = $('#indvSelGame').val();
        var indvSelLeag = $('#indvSelLeag').val();
        var indvSelWagerAmount = $('#indvSelWagerAmount').val();
        var indvTxtUser = $('#indvTxtUser').val();

        var queueData = {
            'type': queueType,
            'game': indvSelGame,
            'league': indvSelLeag,
            'wager': indvSelWagerAmount,
            'user': indvTxtUser,
        };

        $.ajax({
            url: "/newQueue",
            type: "post",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(queueData),
        })
        .done(function(res) {
            $('.queue-buttons').show();
            $('.preloader-queue').hide();
            alert(res.message);
        })
        .fail(function() {
            console.log("Sorry. Server unavailable. ");
        });

    });
});