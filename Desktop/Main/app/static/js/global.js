$(document).ready(function() {
    // header group
    var headerGroup = document.getElementById("header-group");
    var headerButton = headerGroup.getElementsByClassName("header-button");
    for (var i = 0; i < headerButton.length; i++) {
        headerButton[i].addEventListener("click", function (i) {
            headerButton[i].addClass(" active");
        })
    }

    // sword group
    var navElements = document.getElementsByClassName('nav-link');
    var sword_sound = document.getElementById("sword_sound");
    for(let i = 1; i<navElements.length; i++){
        navElements[i].addEventListener('click', function () {
            sword_sound.play()
        });
    }

    $('#loader').css('display', 'none')

	  $(".collapse1-content-item-right-row").hover(function(){
        $(this).closest('.collapse1-content-item-right-row').toggleClass("collapse_close_box");
	});

	  $(".close-popup").click(function(){
        $(this).closest(".collapse1-content-item-right-row").remove();
	 });

    $(".close").on("click", function(event){
        $('#matchCreate button.modal-dismiss').click();
    });


    //$('div#cmmConsole div[class*="rr-one-item radio-trigger"]').on("click", function(event) {
    $('div[class*="rr-one-item radio-trigger"]').on("click", function(event) {
        var curDiv = event.target;
        if (event.target.tagName.toLowerCase() == "span")
            curDiv = $(event.target).parent()[0]; //event.target.id
        //console.log('curDiv tagName: ', curDiv.tagName);
        //var parentDiv = $(event.target).parent(); //$(parentDiv).children('div').each(function() {
        //$('div#cmmConsole div[class*="rr-one-item radio-trigger"]').each(function() {
        //$(parentDiv).parent().parent().find('div[class*="rr-one-item radio-trigger"]').each(function() {
        //$(parentDiv).parentsUntil("div.row").find('div[class*="rr-one-item radio-trigger"]').each(function() {
        $(curDiv).closest("div[class='row-radios mf-rr']").find('div[class*="rr-one-item radio-trigger"]').each(function() {
            //alert("dd:" + $(this).attr('class'));
            $(this).attr('class', 'rr-one-item radio-trigger');
        });
        $(curDiv).attr('class', 'rr-one-item radio-trigger selected');

    });

    $('div[class*="da-select"]').on("click", function(event) {
        var curDiv = event.target;
        var curTag = event.target.tagName.toLowerCase();
        if (curTag == "span" || curTag == "input")
            curDiv = $(event.target).parent()[0];
        $(curDiv).closest("div.row").find('div[class*="da-select"]').each(function() {
            //alert("dd:" + $(this).attr('class'));
            var deSelAttr = $(this).attr('class').replace('selected', '');
            $(this).attr('class', deSelAttr);
        });
        if ($(curDiv).parent()[0].nodeName.toLowerCase() == "form") {
            curDiv = $(curDiv).closest('div[class*="da-select"]');
        }
        var addAttr = $(curDiv).attr('class') + " selected";
        $(curDiv).attr('class', addAttr);

    });

    $('div.modern-select span[class="form-control bigger"]').on("click", function(event) {
        var curElement = event.target;
        $(curElement).next().toggle(); //css("display", "block");

    });

    $('div.modern-select div.ms-options-outer ul li').on("click", function(event) {
        var curElement = event.target;
        var dataVal = $(curElement).attr('data-val');
        var txtSel = $(curElement).text();

        curElement = $(curElement).closest('div.ms-options-outer');
        var prevSpan = $(curElement).prev().find('span.realVal');
        $(prevSpan).text(txtSel);
        $(prevSpan).attr('data-val', dataVal);

        $(prevSpan).show();
        $(curElement).prev().find('span.placeholder').hide();
        $(curElement).toggle(); //css("display", "block");

    });

    // Player Matches > create a match
    $('#matchSubmit').on("click", function() {
        $('#matchForm').submit();
    });

    $('#matchForm').on("submit", function(event) {
        event.preventDefault();
        var data = $(this).serializeArray();
        print(data)

        $.ajax({
                url: "/createusermatch",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(data),
            })
            .done(function(res) {
                if (res.success == '1') {
                    // reloads match table
                    $("#individual").load(location.href + " #individual");

                    // resets create match form
                    $('#matchForm')[0].reset();
                    var x = document.getElementsByClassName("tab");
                    var c = x.length - 1;
                    while (c >= 0) {
                        $('.step').removeClass('finish');
                        x[c].style.display = "none";
                        c -= 1;
                    }
                    currentTab = 0;
                    showTab(0);
                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });
    });




    // Fake Report to DB
    $("#cacheToDb").on("click", function() {
        $.ajax({
            url: "/cachetodb",
            type: "post",
            dataType: "json",
            contentType: "application/json",
        })
        .done(function(res) {
            if (res.success == '1') {
                // reloads match table
                alert("success");
            }
        })
        .fail(function() {
            console.log("Sorry. Server unavailable. ");
        });
    });

    // Report Match
    $('#fakeReportMatch').on("click", function() {

        event.preventDefault();
        var data = Array(),
            games = ['cod','lol','dota'],
            leagues = ['copper','bronze','silver','gold','platform','illudium','rhodium','diamond'],
            playertwo = 'exam_happy',
            winner = ['exam_happy', 'admin_test'],
            wagers = [5,10,15,25,50],
            rules = 'rules-single',
            type = 'type-1duo';

        for ( var i = 0; i < 10 ; i ++ )
        {
            var number = 1 + Math.floor(Math.random() * 100);

            var contentData = [
                {"name": "game", "value": games[number%3] },
                {"name": "wagers", "value": wagers[number%5] },
                {"name": "rules", "value": rules },
                {"name": "type", "value": type },
                {"name": "league", "value": leagues[number%8] },
                {"name": "playertwo", "value": playertwo},
                {"name": "winner", "value": winner[number%2]},
            ];

            $.ajax({
                url: "/reportusermatch",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(contentData),
            })
            .done(function(res) {
                if (res.success == '1') {
                    // reloads match table
                    $("#individual").load(location.href + " #individual");

                    // resets create match form
                    $('#matchForm')[0].reset();
                    var x = document.getElementsByClassName("tab");
                    var c = x.length - 1;
                    while (c >= 0) {
                        $('.step').removeClass('finish');
                        x[c].style.display = "none";
                        c -= 1;
                    }
                    currentTab = 0;
                    showTab(0);
                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });
        }


    });

    $('#reportMatch').on("click", function() {
        event.preventDefault();
        var data = $('#matchForm').serializeArray();
        console.log(data);

        $.ajax({
                url: "/reportusermatch",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(data),
            })
            .done(function(res) {
                if (res.success == '1') {
                    // reloads match table
                    $("#individual").load(location.href + " #individual");

                    // resets create match form
                    $('#matchForm')[0].reset();
                    var x = document.getElementsByClassName("tab");
                    var c = x.length - 1;
                    while (c >= 0) {
                        $('.step').removeClass('finish');
                        x[c].style.display = "none";
                        c -= 1;
                    }
                    currentTab = 0;
                    showTab(0);
                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });
    });

    // Index > Join Match
    $('#joinMatch').on("click", function(event) {
        event.preventDefault();
        var data = $
        console.log(data)

        $.ajax({
                url: "/joinMatch",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(data),
            })
            .done(function(res) {
                if (res.success == '1') {


                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });
    });

    $('#sidebar_a_inventory').on("click", function(event) {
        $.ajax({
            type: 'GET',
            url: '/getinven',
            data: "",
            contentType: false,
            cache: false,
            processData: false,
            success: function(resp) {
                //console.log(">>>>> resp",resp);
                if (resp['ok']) {
                    var idx = 0;
                    var total = resp['ids'].length;
                    var maxrow = 4;
                    var maxcol = 15;
                    if (total > maxrow * maxcol) {
                        maxcol += parseInt((total - maxrow * maxcol) / maxrow) + 1;
                    }

                    var txtHtml = '<table>';
                    for (var i = 0; i < maxrow; i++) {
                        txtHtml += '<tr>';
                        for (var j = 0; j < maxcol; j++) {
                            idx = j + i * 4;
                            txtHtml += '<td style="padding: 1px;">';
                            if (idx < total) {
                                txtHtml += '<div id="div_' + resp['ids'][idx] + '"  style="border: 1px solid white;border-radius: 4px; width:50px;height:50px;">';
                                txtHtml += '<img id="img_' + resp['ids'][idx] + '" src="' + resp['invens'][idx] + '" draggable="true" ondragstart="drag(event)" width="50" height="50">';
                            } else {
                                txtHtml += '<div style="border: 1px solid white;border-radius: 4px; width:50px;height:50px;">';
                            }
                            txtHtml += '</div>';
                            txtHtml += '</td>';
                        }
                        txtHtml += '</tr>';
                    }
                    txtHtml += '</table>';
                    $("#dvInventory").html(txtHtml);
                    //console.log(">>> txtHtml: ",txtHtml);

                } else {
                    //Set the original picture back
                    picture.attr('src', original_src);
                    //alert(resp['msg']);
                }
            }
        });

    });

    // ondrop="drop(event)" ondragover="allowDrop(event)"
    $("header.card-header,footer.card-footer").on("dragover", function(event) {
        event.preventDefault();
        event.stopPropagation();
        $(this).addClass('dragging');
    });

    $("header.card-header,footer.card-footer").on("drop", function(event) {
        event.preventDefault();
        //event.stopPropagation();

        event.dataTransfer = event.originalEvent.dataTransfer;
        var data = event.dataTransfer.getData("itemID");
        //console.log(" >>> Image Dropped! data: "+data);
        //event.target.appendChild(document.getElementById(data));
        var imgsrc = $("#" + data).attr("src");
        var imgidx = data.split("_")[1];
        //console.log(" >>> Image src: "+imgsrc+", idx: "+imgidx);

        //$("#"+data).parents("div:first").html("");
        $.ajax({
                url: "/getinven",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({ 'id': imgidx }),
            })
            .done(function(res) {
                if (res.success == '1') {
                    $("#" + data).closest("div").html("");

                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });

    });

    setupPictureUpload();
    setupCoverUpload();
    return;

    ///Socket-Related Event Handler
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        console.log("socket connected.");
    });
    socket.on('status', function(data) {
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('message', function(data) {
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    $('#chat-send').click(function(e) {
        text = $('#chat-text').val();
        if (text != '') {
            socket.emit('text', { msg: text });
        }
    });
});

$(window).on('beforeunload', function() {
    var socket;
    socket.emit('left', {}, function() {
        socket.disconnect();
    })
    console.log("socket disconnected.");
});

function setupCoverUpload() {
    //Upload cover code
    $('.user-cover').click(function(event) {
        $('.cover-file').trigger('click');
    });

    $('.cover-file').change(function() {
        var image_size = this.files[0].size;
        if (image_size > 8000000) {
            //Image is too big, must be 8MB or less
            alert('Your picture is too big, please make sure the image is 8 MB or less in size.');
        } else {
            $('.cover-form').submit();
        }
    });

    $('.cover-form').on('submit', function(event) {
        event.preventDefault();

        var picture = $('.user-cover');

        //Grab the current picture src
        var original_src = picture.attr('src');

        //Set the
        picture.attr('src', 'static/images/loading.gif');

        $.ajax({
            type: 'POST',
            url: '/profile',
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
            success: function(resp) {
                if (resp['ok']) {
                    $('.user-cover').attr('src', resp['picture_url']);
                } else {
                    alert(resp['msg']);

                    //Set the original picture back
                    picture.attr('src', original_src);
                }
            }
        });

    });
}

function setupPictureUpload() {
    //Upload picture code
    $('.user-picture').click(function(event) {
        $('.picture-file').trigger('click');
    });

    $('.picture-file').change(function() {
        var image_size = this.files[0].size;
        if (image_size > 8000000) {
            //Image is too big, must be 8MB or less
            alert('Your picture is too big, please make sure the image is 8 MB or less in size.');
        } else {
            $('.picture-form').submit();
        }
    });

    $('.picture-form').on('submit', function(event) {
        event.preventDefault();

        var picture = $('.user-picture');

        //Grab the current picture src
        var original_src = picture.attr('src');

        //Set the
        picture.attr('src', 'static/images/loading.gif');

        $.ajax({
            type: 'POST',
            url: '/profile',
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
            success: function(resp) {
                if (resp['ok']) {
                    $('.user-picture').attr('src', resp['picture_url']);
                    $('.userbox .profile-picture img').attr('src', resp['picture_url']);
                    $('.navmenu .user-top .userpic img').attr('src', resp['picture_url']);
                    $('.nav .user-img img').attr('src', resp['picture_url']);
                } else {
                    alert(resp['msg']);

                    //Set the original picture back
                    picture.attr('src', original_src);
                }
            }
        });

    });
}

// CreateMatch Form functions
var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
    // This function will display the specified tab of the form ...
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    // ... and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").style.display = "none";
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
        document.getElementById("nextBtn").style.display = "inline";
    }
    // ... and run a function that displays the correct step indicator:
    fixStepIndicator(n)
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class to the current step:
    x[n].className += " active";
}



function nextPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // if you have reached the end of the form... :
    if (currentTab >= x.length) {
      //...the form gets submitted:
        document.getElementById("regForm").submit();
        return false;
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");

    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
      // If a field is empty...
        if (y[i].value == "") {
            // add an "invalid" class to the field:
            y[i].className += " invalid";
            // and set the current valid status to false:
            valid = false;
      }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
      document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

// Leaderboard show Popup

function fixLeadStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("leaderboard-step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class to the current step:
    x[n].className += " active";
}

// Leaderboards Part
var currentLeadTab = 0; // Current tab is set to be the first tab (0)

$('#ratingModal .btn-close').click(() => {
    $('#ratingModal').modal('hide');
});

$('#ratingModal').on('hide.bs.modal', function () {
    $('#ratingModal .tab-body main').scrollTop(0);
    $.magnificPopup.close();
})


function getPageId(n) {
    return 'article-page-' + n;
}

function getArticle(data) {
    const article = document.createElement('article');
    article.className = 'article-list__item';

    const formTag = document.createElement('div');
    formTag.className = 'form-row';

    const rankElement=document.createElement('div');
    rankElement.className = 'col-lg-4 text-center';
    var newContent = document.createTextNode(data["recid"]);
    rankElement.appendChild(newContent);

    const ratingElement=document.createElement('div');
    ratingElement.className = 'col-lg-4 text-center';
    var newContent = document.createTextNode(data["rating"]);
    ratingElement.appendChild(newContent);

    const playerElement=document.createElement('div');
    playerElement.className = 'col-lg-4 text-center';
    var newContent = document.createTextNode(data["player"]);
    playerElement.appendChild(newContent);

    formTag.appendChild(rankElement);
    formTag.appendChild(playerElement);
    formTag.appendChild(ratingElement);

    article.appendChild(formTag);

    return article;
}

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function getArticlePage(page, game,group, articlesPerPage = 2) {
    const pageElement = document.createElement('div');
    pageElement.id = getPageId(page);
    pageElement.className = 'article-list__page';

    var contentData = {
        "game": game,
        "group": group,
        "offset": page,
        "limit": articlesPerPage
    };

    $.ajax({
        url: "/searchelorating",
        type: "post",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(contentData)
    })
    .done(function(res) {
        if (res.success == '1') {
            // reloads match table
            for ( var i in res.result ) {
                pageElement.appendChild(getArticle(res.result[i]));
            }
            if (res.result.length > 0)
            {
                articleList.appendChild(pageElement);
                addPaginationPage(page);
            }
        }
    })
    .fail(function() {
        console.log("Sorry. Server unavailable. ");
    });

    return pageElement;
}

function addPaginationPage(page) {
    const pageLink = document.createElement('a');
    pageLink.href = '#' + getPageId(page);
    pageLink.innerHTML = page;

    const listItem = document.createElement('li');
    listItem.className = 'article-list__pagination__item';
    listItem.appendChild(pageLink);

    articleListPagination.appendChild(listItem);

    if (page === 2) {
        articleListPagination.classList.remove('article-list__pagination--inactive');
    }
}

function fetchPage(page, game, group) {
    getArticlePage(page, game, group);
}

function addPage(page, game, group) {
    fetchPage(page, game, group);
}

const articleList = document.getElementById('article-list');
const articleListPagination = document.getElementById('article-list-pagination');
var page = 0;

var removeModal = () => {
    $("#ratingModal .tab-body main").scrollTop( 0 );
    $('#ratingModal .tab-body main .article-list').empty();
    $('#article-list-pagination').empty();
}

$('#ratingModal .tab-body main').on('scroll', function() {

    var group = $("#sel_modal_league").val();
    var game = $("#sel_modal_game").val();

    if($(this).scrollTop() < $(this)[0].scrollHeight - $(this).innerHeight() ) {
        return;
    }
    addPage(++page, game,group);
})


function showLeadTab(n) {
    // This function will display the specified tab of the form ...
    var x = document.getElementsByClassName("rating-tab");
    x[n].style.display = "block";
    // ... and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevLeadBtn").style.display = "none";
        document.getElementById("lead-modal-paginate").style.display = "none";
        x[n+1].style.display="none";
    } else {
        document.getElementById("prevLeadBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        x[n-1].style.display="none";
        document.getElementById("nextLeadBtn").style.display = "none";
        document.getElementById("lead-modal-paginate").style.display = "block";

        var group = $("#sel_modal_league").val();
        var game = $("#sel_modal_game").val();

        removeModal();
        page=0;
        addPage(++page, game, group);

    } else {
        document.getElementById("nextLeadBtn").innerHTML = "Next";
        document.getElementById("nextLeadBtn").style.display = "inline";
    }
    // ... and run a function that displays the correct step indicator:
    fixLeadStepIndicator(n)
}

function nextLeadPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("rating-tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentLeadTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentLeadTab = currentLeadTab + n;
    // if you have reached the end of the form... :
    if (currentLeadTab >= x.length) {
      //...the form gets submitted:
        // document.getElementById("regForm").submit();
        return false;
    }
    // Otherwise, display the correct tab:
    showLeadTab(currentLeadTab);
}

// $('.ratingBy.leaderboard').on("click", function() {
//     var group = $("#sel_lb_league").val();
//     var game = $("#sel_lb_game").val();

//     removeModal();
//     page=0;
//     addPage(++page, game, group);
//     $('#ratingModal').modal('show');

//     currentLeadTab=1;
//     showLeadTab(currentLeadTab);

//     $("#sel_modal_league").val(group);
//     $("#sel_modal_game").val(game);
// });

$('.profile-ratingBy').on("click", function() {
    $('#ratingModal').modal('show');
    currentLeadTab=0;
    showLeadTab(currentLeadTab);
});

// End Leaderboards Part

// Inventory Drag-Drop Related functions
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    console.log("---> target.id: ", ev.target.id);
    ev.dataTransfer.setData("itemID", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("itemID");
    ev.target.appendChild(document.getElementById(data));
}

// Chat functions
function onChatFortnite(fortniteId, fortniteName) {
    socket.emit('left', {}, function() {
        $.ajax({
                url: "/setroom",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({ 'id': fortniteId, 'type': 'fortnite' }),
            })
            .done(function(res) {
                if (res.success == '1') {
                    socket.emit('joined', { 'room': res.room, 'type': 'fortnite' });
                    $("#btn-match").text('Matches');
                    $("#btn-fortnite").text(fortniteName);
                    $("#btn-friend").text('Friends');
                    $.ajax({
                            url: "/getchat",
                            type: "get",
                            dataType: "json",
                            contentType: "application/json",
                        })
                        .done(function(res) {
                            $('#chat').val(res.chat);
                        })
                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });
    });
}

function onChatMatch(matchId, matchName) {
    socket.emit('left', {}, function() {
        $.ajax({
                url: "/setroom",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({ 'id': matchId, 'type': 'match' }),
            })
            .done(function(res) {
                if (res.success == '1') {
                    socket.emit('joined', { 'room': res.room, 'type': 'match' });
                    $("#btn-match").text(matchName);
                    $("#btn-fortnite").text('Fortnite');
                    $("#btn-friend").text('Friends');
                    $.ajax({
                            url: "/getchat",
                            type: "get",
                            dataType: "json",
                            contentType: "application/json",
                        })
                        .done(function(res) {
                            $('#chat').val(res.chat);
                        })
                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });
    });
}

function onChatDirect(friendId, friendName) {
    socket.emit('left', {}, function() {
        $.ajax({
                url: "/setroom",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({ 'id': friendId, 'type': 'friend' }),
            })
            .done(function(res) {
                if (res.success == '1') {
                    socket.emit('joined', { 'room': res.room, 'type': 'friend' });
                    $("#btn-match").text('Matches');
                    $("#btn-fortnite").text('Fortnite');
                    $("#btn-friend").text(friendName);
                    $.ajax({
                            url: "/getchat",
                            type: "get",
                            dataType: "json",
                            contentType: "application/json",
                        })
                        .done(function(res) {
                            $('#chat').val(res.chat);
                        })
                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });
    });
}

function onNewMatch(matchId, matchTitle) {
    $('#modal_title').text(matchTitle);
    $('#modal_id').val(matchId);
    $.ajax({
            url: `/getobservers`,
            type: "get",
            dataType: "json",
            contentType: "application/json"
        })
        .done(function(res) {
            console.log(res);
            if (res.observers.includes(matchId)) {
                socket.emit('left', {}, function() {
                    $.ajax({
                            url: "/setroom",
                            type: "post",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({ 'id': matchId, 'type': 'match' }),
                        })
                        .done(function(res) {
                            if (res.success == '1') {
                                socket.emit('joined', { 'room': res.room, 'type': 'match' });
                                $("#btn-match").text($('#modal_title').text());
                                $("#btn-fortnite").text('Fortnite');
                                $("#btn-friend").text('Friends');
                                $.ajax({
                                        url: "/getchat",
                                        type: "get",
                                        dataType: "json",
                                        contentType: "application/json",
                                    })
                                    .done(function(res) {
                                        $('#chat').val(res.chat);
                                        $('#myModal').modal('hide');
                                    })
                            }
                        })
                        .fail(function() {
                            console.log("Sorry. Server unavailable. ");
                        });
                });
            } else {
                $('#myModal').modal();
            }
        })
}

function onJoin() {
    var matchId = $('#modal_id').val();
    $.ajax({
            url: "/addobserver",
            type: "post",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({ 'match_id': matchId }),
        })
        .done(function() {
            socket.emit('left', {}, function() {
                $.ajax({
                        url: "/setroom",
                        type: "post",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({ 'id': matchId, 'type': 'match' }),
                    })
                    .done(function(res) {
                        if (res.success == '1') {
                            socket.emit('joined', { 'room': res.room, 'type': 'match' });
                            $("#btn-match").text($('#modal_title').text());
                            $("#btn-fortnite").text('Fortnite');
                            $("#btn-friend").text('Friends');
                            $.ajax({
                                    url: "/getchat",
                                    type: "get",
                                    dataType: "json",
                                    contentType: "application/json",
                                })
                                .done(function(res) {
                                    $('#chat').val(res.chat);
                                    $('#myModal').modal('hide');
                                })
                        }
                    })
                    .fail(function() {
                        console.log("Sorry. Server unavailable. ");
                    });
            });
        })
}
