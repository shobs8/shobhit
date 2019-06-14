var page_number;
var records_number;

$(document).ready(function(){
    var match_table = $('#matchesbody').DataTable();

    // Dropdown sorting
    $('#console-sort').click(function () {match_table.column('0:visible').order('asc').draw();});
    $('#game-sort').click(function () {match_table.column('1:visible').order('asc').draw();});
    $('#result-sort').click(function () {match_table.column('2:visible').order('asc').draw();});
    $('#prize-sort').click(function () {match_table.column('3:visible').order('asc').draw();});
    page_number = {{ pagination.page }};
    records_number = {{ pagination.per_page }};
    getRecordsShown(records_number);
    windowOnScroll(page_number);
});

function getRecordsShown(records_number){
    document.getElementById('records_number').innerHTML = "Showing Results: " + records_number.toString();
}

function windowOnScroll(page_number) {
    $(window).on("scroll", function(e){
        if ($(window).scrollTop() == $(document).height() - $(window).height()){
            if({{ pagination.total }} > page_number * {{pagination.per_page}}) {
                var lastId = $(".post-item:last").attr("id");
                getMoreData({{ pagination.page  1 }});
            }
        }
    });
}

function getMoreData(page_number) {
    $(window).off("scroll");

    $.ajax({
        url: '/sponsorship-infinite/admin?page=' + page_number,
        type: "get",
        beforeSend: function ()
        {
            $('.loading').show();
            console.log("requests sent")
        },
        success: function (data) {
            setTimeout(function() {
                console.log('response received')
                $('.loading').hide();
                data['matches'].forEach(function(match){
                    $("#matchesbody").append(
                        `
                        <tr class="infinite-item">
                    <td>
                        <div class="img">
                            <h1 class="border border-dark stat">${match.winner ==='admin' ? "WIN" : "LOSS"}</h1>
                        </div>
                    </td>
                    <td>
                        <div class="name">
                            <h3>${match.game}</h3>
                        </div>
                    </td>
                    <td>
                        <div class="not-name">
                            <h4>${match.console}</h4>
                        </div>
                    </td>
                    <td>
                        <div class="not-name">
                            <h4>Online</h4>
                        </div>
                    </td>
                    <td>
                        <div class="not-name">
                            <h4>League</h4>
                        </div>
                    </td>
                </tr>
                        `
                    )
                });
                page_number = page_number + 1;
                records_number = records_number  + data['matches'].length;
                getRecordsShown(records_number);
                windowOnScroll();
            }, 1000);
        }
    });
}
