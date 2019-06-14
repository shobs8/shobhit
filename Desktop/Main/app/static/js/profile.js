$(document).ready(function() {
    $(".close").on("click", function(event){
        $('#matchCreate button.modal-dismiss').click();
    });

    // profile nav
    $('.profile-nav').on('click', '.btn', function(){
        $(this).addClass('btn-primary');
        $(this).siblings().removeClass('btn-primary');
    });

    // profile home
    $('#nav-profile').on("click", function(event) {
        $('#profile-profile').removeClass('hide')
        $('#profile-profile').siblings().addClass('hide');
    })

    // profile messaging
    $('#nav-messaging').on("click", function(event) {
        $('#profile-messaging').removeClass('hide')
        $('#profile-messaging').siblings().addClass('hide');
    });

    // profile settings
    $('#nav-settings').on("click", function(event) {
        $('#profile-settings').removeClass('hide')
        $('#profile-settings').siblings().addClass('hide');
    });

    // profile transactions
    $('#nav-transactions').on("click", function(event) {
        $('#profile-transactions').removeClass('hide')
        $('#profile-transactions').siblings().addClass('hide');
    });

    $('#nav-sponsorship').on("click", function(event) {
        $('#profile-sponsorship').removeClass('hide')
        $('#profile-sponsorship').siblings().addClass('hide');
    });
});

function checkActive(object) {
    if (object.hasClass('active')) {
        return True
    } else {
        return False
    }
}
