/* Add here all your JS customizations */

var socket;

$(document).ready(function() {
    $(".collapse1-content-item-right-row").hover(function() {
        $(this).closest('.collapse1-content-item-right-row').toggleClass("collapse_close_box");
    });
    $(".close-popup").click(function() {
        $(this).closest(".collapse1-content-item-right-row").remove();
    });

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

    $('a[href="#matchCreate"]').click(function() {
        getMyMatchInfo();
    });

    $('#reportMatchBtn').on("click", function(event) {
        var cnsl = $('#cmmConsole div[class="rr-one-item radio-trigger selected"] span.rr-value').attr('data-value');
        var game = $('#cmmGamesList div[class="one-game-entry radio-trigger a-radio xbox-game selected"] span[class*="rr-value"]').attr('data-value');
        var input = $('#cmmCrossplay div[class*=" selected"] span[class*="rr-value"]').attr('data-value');
        var wager = $('#cmmWagerAmount div[class*=" selected"] span.given-amount').attr('data-value');
        if (wager === undefined) {
            wager = $('#cmmWagerAmount input#cmmAmountField').prop('value');
            if (wager == "") wager = "10";
        }
        var matchlength = $('div[data-name="match_length_rule"] span.realVal').attr('data-val');
        var gametype = $('div[data-name="fn_game_type_rule"] span.realVal').attr('data-val');
        var customrules = $('div#customRulesField textarea#cmmCustomGameRules').prop('value');
        var oddsadvantage = $('div[data-name="fortnite_odds_kills"] span.realVal').attr('data-val');
        if (oddsadvantage === undefined) {
            oddsadvantage = "false";
        }
        var player2 = $('#reportPlayerTwo').val();
        var reportWinner = $('#reportWinner').val();

        var matchdata = {
            'console': cnsl,
            'game': game,
            'input': input,
            'your_wager': wager,
            'game_rules': {
                'match_length': matchlength,
                'game_type': gametype,
                'custom_rules': customrules,
            },
            'odds_advantages': oddsadvantage,
            'player2': player2,
            'winner': reportWinner
        };
        //console.log("---> matchdata: ", matchdata);

        $.ajax({
                url: "/reportusermatch",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(matchdata),
            })
            .done(function(res) {
                if (res.success == '1') {
                    $('#matchCreate button.modal-dismiss').click();
                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });
    });

    $('#createMatchBtn').on("click", function(event) {
        var cnsl = $('#cmmConsole div[class="rr-one-item radio-trigger selected"] span.rr-value').attr('data-value');
        var game = $('#cmmGamesList div[class="one-game-entry radio-trigger a-radio xbox-game selected"] span[class*="rr-value"]').attr('data-value');
        var input = $('#cmmCrossplay div[class*=" selected"] span[class*="rr-value"]').attr('data-value');
        var wager = $('#cmmWagerAmount div[class*=" selected"] span.given-amount').attr('data-value');
        if (wager === undefined) {
            wager = $('#cmmWagerAmount input#cmmAmountField').prop('value');
            if (wager == "") wager = "10";
        }
        var matchlength = $('div[data-name="match_length_rule"] span.realVal').attr('data-val');
        var gametype = $('div[data-name="fn_game_type_rule"] span.realVal').attr('data-val');
        var customrules = $('div#customRulesField textarea#cmmCustomGameRules').prop('value');
        var oddsadvantage = $('div[data-name="fortnite_odds_kills"] span.realVal').attr('data-val');
        if (oddsadvantage === undefined) {
            oddsadvantage = "false";
        }

        var matchdata = {
            'console': cnsl,
            'game': game,
            'input': input,
            'your_wager': wager,
            'game_rules': {
                'match_length': matchlength,
                'game_type': gametype,
                'custom_rules': customrules,
            },
            'odds_advantages': oddsadvantage,
        };
        //console.log("---> matchdata: ", matchdata);

        $.ajax({
                url: "/createusermatch",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(matchdata),
            })
            .done(function(res) {
                if (res.success == '1') {
                    $('#matchCreate button.modal-dismiss').click();

                    var prependStr = '<li class="mailbody-box"><a href=""><div class="row"><div class="col-md-4 column-1 column-text"><input class="star" type="checkbox" title="bookmark page" />';
                    prependStr += '<input type="checkbox" name="cbG02" id="cbG02" class="lock-unlock" /><label for="cbG02" class="lock-label cb0"></label><span class="protected-user"></span>';
                    prependStr += '<p class="m-0 ib mail-content text-white">' + cnsl + '</p></div>';
                    prependStr += '<div class="col-md-2 column-2 column-text"><p class="m-0 text-white">' + game + '</p></div>';
                    prependStr += '<div class="col-md-1 column-3 column-text justify-content-center p-0"><p class="m-0 text-white">' + input + '</p></div>';
                    prependStr += '<div class="col-md-1 p-0 column-4 column-text justify-content-center"><p class="m-0 text-white">$' + wager + '</p></div>';
                    prependStr += '<div class="col-md-1 p-0 column-5 column-text justify-content-center"><p class="m-0 text-white">' + matchlength + '</p></div>';
                    prependStr += '<div class="col-md-1 p-0 column-6 column-text justify-content-center"><p class="m-0 text-white">' + gametype + '</p></div>';
                    prependStr += '<div class="col-md-1 p-0 column-7 text-center column-text justify-content-center"><p class="m-0 text-white">' + oddsadvantage + '</p>';
                    prependStr += '</div></div></a></li>';

                    $('ul#mailbox-visual-scroll').prepend(prependStr);

                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });

    });

    $('#aLeftMenuQueue').click(function() {
        // var queueData = {
        //     'type': "2",
        // };

        // $.ajax({
        //         url: "/getGameGroup",
        //         type: "post",
        //         dataType: "json",
        //         contentType: "application/json",
        //         data: JSON.stringify(queueData),
        //     })
        //     .done(function(res) {
        //         if (res.success == '1') {
        //             var games = res.games;
        //             //console.log("--- games:", games);
        //             var txtHtml = "";
        //             for (var i = 0; i < games.length; i++) {
        //                 txtHtml += '<option value="' + games[i].game_id + '" >' + games[i].title + '</option>';
        //             }
        //             $('#indvSelGame').html(txtHtml);
        //             $('#teamSelGame').html(txtHtml);

        //             var groups = res.groups;
        //             txtHtml = "";
        //             for (var j = 0; j < groups.length; j++) {
        //                 txtHtml += '<option value="' + (j + 1) + '" >' + groups[j] + '</option>';
        //             }
        //             $('#indvSelLeag').html(txtHtml);
        //             $('#teamSelLeag').html(txtHtml);

        //             var regteams = res.regteams;
        //             txtHtml = "";
        //             for (var j = 0; j < regteams.length; j++) {
        //                 txtHtml += '<option value="' + regteams[j] + '" >Team' + (j + 1) + '</option>';
        //             }
        //             $('#teamSelRegi').html(txtHtml);
        //         }
        //     })
        //     .fail(function() {
        //         console.log("Sorry. Server unavailable. ");
        //     });

    });
    $('.sel-playermatch-queue').change(function() {
        //alert("this.id: " + this.id);
        var queueType = $('input[type=radio][name=radioQueueIndvTeam]').val();
        var teamSelGame = $('#teamSelGame').val();
        var teamSelLeag = $('#teamSelLeag').val();
        var queueData = {
            'type': queueType,
            'game': teamSelGame,
            'league': teamSelLeag,
        };

        $.ajax({
                url: "/getGameGroup",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(queueData),
            })
            .done(function(res) {
                if (res.success == '1') {
                    var regteams = res.regteams;
                    var rtHtml = "";
                    for (var j = 0; j < regteams.length; j++) {
                        rtHtml += '<option value="' + regteams[j].team_id + '" >Team ' + j + '</option>';
                    }
                    $('#teamSelRegi').html(rtHtml);

                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });

    });

    $('input[type=radio][name=radioQueueIndvTeam]').change(function() {
        if (this.value == '0') {
            $('#divQueueIndv').css("display", "block");
            $('#divQueueTeam').css("display", "none");
        } else if (this.value == '1') {
            $('#divQueueIndv').css("display", "none");
            $('#divQueueTeam').css("display", "block");
        }
        $("input[name=radioQueueIndvTeam][value='" + this.value + "']").prop("checked", true);
    });

    // Queue Button
    $('#btnQueueIndv').click(function() {
        // var queHtml = '<div class="bounce-loader"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div>';
        // $('.preloader-queue').html(queHtml);

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
                if (res.success == 1) {
                    $('.queue-buttons').show();
                    $('.preloader-queue').hide();
                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });



    });
    $('#btnQueueTeam').click(function() {
        var queueType = 1;
        var teamSelGame = $('#teamSelGame').val();
        var teamSelLeag = $('#teamSelLeag').val();
        var teamSelRegi = $('#teamSelRegi').val();
        var queueData = {
            'type': queueType,
            'game': teamSelGame,
            'league': teamSelLeag,
            'reg_team': teamSelRegi,
        };

        $.ajax({
                url: "/setQueue",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(queueData),
            })
            .done(function(res) {
                if (res.success == '1') {

                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });

    });

    $('#sel_lb_game, #sel_lb_group').change(function() {
        var gmid = $('#sel_lb_game').val();
        var gpid = $('#sel_lb_group').val();
        var lbData = {
            'game_id': gmid,
            'group_id': gpid,
        };

        $.ajax({
                url: "/getLeaderboard",
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(lbData),
            })
            .done(function(res) {
                if (res.success == '1') {
                    //console.log("--- res.leaderboards: " + res.leaderboards);
                    var lbs = res.leaderboards;
                    var lbHtml = '<tr>';
                    for (var j = 0; j < lbs.length; j++) {
                        lbHtml += '<td data-title="Rank" class="pt-3 pb-3">' + String(j + 1) + '</td>';
                        lbHtml += '<td data-title="Score" class="pt-3 pb-3">' + lbs[j].score + '</td>';
                        lbHtml += '<td data-title="Name" class="pt-3 pb-3"><span class="va-middle">' + lbs[j].username + '</span></td>';
                    }
                    lbHtml += '</tr>';
                    $('#tbodyLeaderboard').html(lbHtml);

                }
            })
            .fail(function() {
                console.log("Sorry. Server unavailable. ");
            });

    });


    $('#dvQueuePreloader').click(function() {
        var queHtml = '<div class="bounce-loader"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div>';
        $('#dvQueuePreloader').html(queHtml);

        //Process for queue

    });
    /*
    $('.modal-queue').click(function() {
        var indvRdo = $('input[name=radioQueueIndv]:checked', '#frmQueueIndv').val();
        var indvSelGame = $('#indvSelGame').val();
        var indvSelLeag = $('#indvSelLeag').val();
        var indvTxtUser = $('#indvTxtUser').val();
        var teamRdo = $('input[name=radioQueueTeam]:checked', '#frmQueueTeam').val();
        var teamSelGame = $('#teamSelGame').val();
        var teamSelLeag = $('#teamSelLeag').val();
        var teamSelRegi = $('#teamSelRegi').val();
        //console.log("---> iRdo: ", indvRdo, ',', indvSelGame, ',', indvSelLeag, ',', indvTxtUser);
        //console.log("---> tRdo: ", teamRdo, ',', teamSelGame, ',', teamSelLeag, ',', teamSelRegi);

        $('#queueIT').modal('toggle'); //.modal('hide');
        $('#dvQueuePreloader').css("display", "block");
        $('#dvQueueModal').css("display", "none");

        return false; //Disable Auto Submit of Form
    });
    */

    ///XLZ Leaderboard
    $('#sel_lb_game').on('change', function(e) {
        var optionSelected = $("option:selected", this);
        var valueSelected = this.value;
        var textSelected = this.text;
    });
    $('#sel_lb_group').on('change', function(e) {
        var optionSelected = $("option:selected", this);
        var valueSelected = this.value;
    });

    setupPictureUpload();

    // inventory
    $('#sidebar_a_inventory').click(function() {
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
                                txtHtml += '<img id="img_' + resp['ids'][idx] + 'src=' + "{{ url_for('static', filename='img/inventory/Charm/'" + resp['ids'][idx] + '.png' + ') }}' + "draggable='true' ondragstart='drag(event)' width='50' height='50'>";
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

    //return; //#JKH

    // chat
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

    // $('#datepicker').datetimepicker();
    var t_type = $('#tournament_type').val()
    var bracket_size = $('#bracket_size').val()

    if (t_type === 'single elimination') {
        $('#hold_third_place_match').closest('.form-group').show()

    } else if (t_type === 'round robin') {
        $('#rr_iteration').closest('.form-group').show()
    }

    if (bracket_size === 'names') {
        $('#participants_team').closest('.form-group').show()
    } else {
        $('#number_of_participants').closest('.form-group').show()
    }

    $('#tournament_type').on('change', function() {
        var $val = $(this).val()
        if ($val === 'single elimination') {
            $('#hold_third_place_match').closest('.form-group').show()
            $('#rr_iteration').closest('.form-group').hide()
        } else if ($val === 'double elimination') {
            $('#hold_third_place_match').closest('.form-group').hide()
            $('#rr_iteration').closest('.form-group').hide()
        } else {
            $('#hold_third_place_match').closest('.form-group').hide()
            $('#rr_iteration').closest('.form-group').show()
        }
    });
})

function updateMatchInfo(mid) {
    //alert("updateMatchInfo: " + mid);
    $.ajax({
            url: "/updateusermatch",
            type: "post",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({ 'id': mid }),
        })
        .done(function(res) {
            if (res.success == '1') {
                //console.log("--->res.match: ", res.match);
            }
        })
        .fail(function() {
            console.log("Sorry. Server unavailable. ");
        });

}

function getMyMatchInfo() {
    $.ajax({
            url: "/getusermatch",
            type: "post",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({ 'id': 0 }),
        })
        .done(function(res) {
            if (res.success == '1') {
                //console.log("--->res.match: ", res.match);
                var dicmatch = res.match;

                //Render Create New match Interface
                $('#cmmConsole div[class*=" selected"]').attr('class', 'rr-one-item radio-trigger');
                $('#cmmConsole div[class="rr-one-item radio-trigger"] span[data-value="' + dicmatch['console'] + '"]').closest("div[class='rr-one-item radio-trigger']").attr('class', 'rr-one-item radio-trigger selected');

                $('#cmmGamesList div[class="one-game-entry radio-trigger a-radio xbox-game selected"]').attr('class', 'one-game-entry radio-trigger a-radio xbox-game');
                $('#cmmGamesList div[class="one-game-entry radio-trigger a-radio xbox-game"] span[data-value="' + dicmatch['game'] + '"]').closest("div[class='one-game-entry radio-trigger a-radio xbox-game']").attr('class', 'one-game-entry radio-trigger a-radio xbox-game selected');

                $('#cmmCrossplay div[class*=" selected"]').attr('class', 'rr-one-item radio-trigger');
                $('#cmmCrossplay div[class="rr-one-item radio-trigger"] span[data-value="' + dicmatch['input'] + '"]').closest("div[class='rr-one-item radio-trigger']").attr('class', 'rr-one-item radio-trigger selected');

                var tmpCls = $('#cmmWagerAmount div[class*=" selected"]').attr('class').replace(" selected", "").replace(" default", "");
                $('#cmmWagerAmount div[class*="da-select"]').attr('class', tmpCls);
                tmpCls += " selected";
                var dv = $('#cmmWagerAmount div[class*="da-select"] span[data-value="' + dicmatch['your_wager'] + '"]').attr('class');
                if (dv === undefined) {
                    //alert("dv: " + dv + ", tmpCls: " + $('#cmmWagerAmount div[class*="da-select"] form input').closest("div[class*='da-select']").attr('class'));
                    $('#cmmWagerAmount div[class*="da-select"] form input').closest("div[class*='da-select']").attr('class', "da-select custom-box mobile-small selected");
                    $('#cmmWagerAmount div[class*="da-select"] form input').prop('value', dicmatch['your_wager']);
                } else {
                    $('#cmmWagerAmount div[class*="da-select"] span[data-value="' + dicmatch['your_wager'] + '"]').closest("div[class*='da-select']").attr('class', tmpCls);
                }

                tmpCls = $('div[data-name="match_length_rule"] div.ms-options-outer ul li[data-val="' + dicmatch['game_rules']['match_length'] + '"]').html();
                $('div[data-name="match_length_rule"] span.realVal').attr('data-val', dicmatch['game_rules']['match_length']);
                $('div[data-name="match_length_rule"] span.realVal').attr('data-val', dicmatch['game_rules']['match_length']);
                $('div[data-name="match_length_rule"] span.realVal').html(tmpCls);

                tmpCls = $('div[data-name="fn_game_type_rule"] div.ms-options-outer ul li[data-val="' + dicmatch['game_rules']['game_type'] + '"]').html();
                $('div[data-name="fn_game_type_rule"] span.realVal').attr('data-val', dicmatch['game_rules']['game_type']);
                $('div[data-name="fn_game_type_rule"] span.realVal').html(tmpCls);

                $('div#customRulesField textarea#cmmCustomGameRules').prop('value', dicmatch['game_rules']['custom_rules']);

                tmpCls = $('div[data-name="fortnite_odds_kills"] div.ms-options-outer ul li[data-val="' + dicmatch['odds_advantages'] + '"]').html();
                //alert("tmpCls: " + tmpCls);
                $('div[data-name="fortnite_odds_kills"] span.realVal').attr('data-val', dicmatch['odds_advantages']);
                $('div[data-name="fortnite_odds_kills"] span.realVal').html(tmpCls);

                /*
                $('#dvQueuePreloader').css("display", "none");
                $('#dvQueueModal').css("display", "block");
                */
                var queHtml = '<button id="btnGetMatch" type="button" class="btn-size-large btn-full-width-mobile-only site-btn important-btn" style="margin-top:10px;">Queue</button>';
                $('#dvQueuePreloader').html(queHtml);

            }
        })
        .fail(function() {
            console.log("Sorry. Server unavailable. ");
        });
}

$(window).on('beforeunload', function() {
    socket.emit('left', {}, function() {
        socket.disconnect();
    })
    console.log("socket disconnected.");
});

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

/// Inventory functions
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



function get_tournaments() {
    $.ajax({
        url: '/tournaments',
        type: 'GET',
        success: function(data) {
            var tournaments = data.tournaments
            $.each(tournaments, function(index, value) {
                var html_text = ""
                html_text += '<li class="mailbody-box"><a href="/tournament/' + value.tournament_id + '/information">';
                html_text += '<div class="row"><div class="col-md-1 column-1 column-text text-center justify-content-center">';
                html_text += '<img class="discipline" style="max-width: 70px;padding:5px;" src="static/img/tournaments/' + value.logo + '" alt="Fortnite">';
                html_text += '</div><div class="col-md-4 column-2 column-text text-center justify-content-center">';
                html_text += '<p class="m-0 text-white text-uppercase">' + value.name + '</p><small>' + value.organizer + '</small></div>';
                html_text += '<div class="col-md-3 column-3 column-text text-center justify-content-center"><p class="m-0 text-white text-uppercase">' + value.start_date + '</p></div>';
                html_text += '<div class="col-md-2 column-4 column-text text-center justify-content-center"><p class="m-0 text-white text-uppercase">' + value.size + '</p></div>';
                html_text += '<div class="col-md-2 column-5 column-text text-center justify-content-center"><p class="m-0 text-white text-uppercase">Registrations Open</p></div>';
                html_text += '</div></a></li>'
                $('#tournament-visual').append(html_text)
            })
        },
        error: function(err) {
            console.error(err)
        }
    })
}
