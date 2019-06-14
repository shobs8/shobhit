jQuery(document).ready(function($) {
	jQuery(".myBtn").click(function(){
		// console.log('ok');
		jQuery(this).parent().find(".modal").fadeIn();
	});
	jQuery(".close").click(function(){
		$(".modal").hide();
	});
	// jQuery(".thread-create-form #title").on('keypress', function () {
	// 	if($(this).val().length>30){
	// 		$(this).parent().parent().append(
	// 			"<div class='form-group col-md-10 float-right'><p style='color: red;'>The Title max length is 30.</p></div>"
	// 		)
	// 		return false;
	// 	}
	// });
	jQuery(".collapse1-content-item").click(function(){
		var thread = $(this).parent().data("thread")
		var endpoint = '/social/thread'
		var data = {'uid': thread}
		ajaxCaller(data, endpoint, (res) => {
			var res = JSON.parse(res)
            if (res.uid) {
                threadDrawer(res, jQuery(this));
            }
        })
	});
	jQuery(".respond-to-topic-modal form a").click(function() {
		var form = $(this).parent().parent().parent()
		var data = new FormData(form[0]);
		data.append('type', 1)
		var endpoint = `/social/message/${data.get('thread')}`

		fileUploadAjaxCaller(data, endpoint, (res) => {
			$(this).closest(".respond-to-topic-modal").hide();
        })
	})

	jQuery(".respond-to-author-form a").click(function() {
		var form = $(this).parent().parent().parent();
		var data = new FormData(form[0]);
		data.append('type', 2)
		var endpoint = `/social/message/${data.get('thread')}`
		console.log(endpoint, data.get('thread'), data.get('type'))
		fileUploadAjaxCaller(data, endpoint, (res) => {
			$(this).closest("form").find("textarea").val("");
        })
	})

	jQuery('.collapse1-content-item-pop').on('click', '.follow-thread', function() {
		var thread = $(this).closest(".collapse1-content-item-pop").data("thread");
		var endpoint = '/social/thread/follow';
		var data = {
			'thread': thread,
		}
		ajaxCaller(data, endpoint, (res) => {
			parent = $(this).parent()
			$(this).remove();
			parent.append(
				`<a class="myBtn btn btn btn-primary unfollow-thread" style="margin-left: 0px; width:100px;">UnFollow</a>`
			)
        })
	})

	jQuery('.collapse1-content-item-pop').on('click', '.unfollow-thread', function() {
		var thread = $(this).closest(".collapse1-content-item-pop").data("thread");
		var endpoint = '/social/thread/unfollow';
		var data = {
			'thread': thread,
		}
		ajaxCaller(data, endpoint, (res) => {
			parent = $(this).parent()
			$(this).remove();
			parent.append(
				`<a class="myBtn btn btn btn-primary follow-thread" style="margin-left: 0px; width:100px;">Follow</a>`
			)
        })
	})

	jQuery(".over_threads").click(function(){
		// jQuery(".collapse1-content-item-pop").fadeOut( "slow" ).css({height:"0"});
		// $('.over_threads').fadeOut();
	});
	jQuery(".close-pop").click(function(){
		// $('.over_threads').fadeOut();
		jQuery(".collapse1-content-item-pop").fadeOut( "slow" ).css({height:"0"});

	});

	jQuery(".close-pop-category").click(function(){
		jQuery(".collapse1-content-category-pop").fadeOut( "slow" );
	});

	jQuery(".collapse-main-Boards h5").click(function(){
		var page = 1;
		var category = jQuery(this).data("category");
		var endpoint = '/social/category';
		var data = {
			"uid": category,
			'page': page
		};
		var target = $(this).siblings(".collapse1-content-category-pop").children('.table-main');
		var tbody = target.children("table").children("tbody");
		tbody.children().remove();

		ajaxCaller(data, endpoint, (res) => {
			res = JSON.parse(res);
			threads = res.threads;
			page = res.next_page;
			drawCategoryThreadsTableBody(threads, tbody)
		})
		jQuery(this).parent().find(".collapse1-content-category-pop").fadeIn("slow")
			.css({top:0,position:'absolute'})
			.animate({top:0}, 500, function() {
		});
		target.off('scroll');
		target.scroll(function() {
			if(target.scrollTop() + target.innerHeight() >= target[0].scrollHeight && page !== null) {
				data.page = page;
				$('.spinner').show();
				ajaxCaller(data, endpoint, (res) => {
					res = JSON.parse(res);
					threads = res.threads;
					page = res.next_page;
					drawCategoryThreadsTableBody(threads, tbody)
					$('.spinner').hide();
				})
			}
		});
	});

	jQuery(".collapse-main-Boards table").on("click", "tbody tr", function(){
		var thread = jQuery(this).data("thread")
		var endpoint = '/social/thread'
		var data = {'uid': thread}
		ajaxCaller(data, endpoint, (res) => {
			var res = JSON.parse(res)
            if (res.uid) {
                allThreadPopupDrawer(res);
            }
        })
	});

	$('html').click(function() {
		// $('.over_threads').fadeOut();
		// $(".modal").hide();
		// jQuery(".collapse1-content-item-pop").fadeOut( "slow" ).css({height:"0"});
		// jQuery(".collapse1-content-category-pop").fadeOut( "slow" );
	});
	$('.modal-content').click(function(event){
		event.stopPropagation();
	});
	$('.myBtn').click(function(event){
		event.stopPropagation();
	});

	//category
	$('.collapse1-content-item-pop').click(function(event){
		event.stopPropagation();
	});
	$('.collapse-main-Boards h5').click(function(event){
		event.stopPropagation();
	});

	//thread
	$('.collapse1-content-category-pop').click(function(event){
		event.stopPropagation();
	});
	$('.collapse1-content-item').click(function(event){
		event.stopPropagation();
	});

	  // We can attach the `fileselect` event to all file inputs on the page
	$(document).on('change', ':file', function() {
		var input = $(this),
			numFiles = input.get(0).files ? input.get(0).files.length : 1,
			label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
		input.trigger('fileselect', [numFiles, label]);
	});

	  // We can watch for our custom `fileselect` event like this
	$(document).ready( function() {
		$(':file').on('fileselect', function(event, numFiles, label) {

			var input = $(this).parents('.input-group').find(':text'),
				log = numFiles > 1 ? numFiles + ' files selected' : label;
			if( input.length ) {
				input.val(log);
			} else {
				// if( log ) alert(log);
			}

		});
	});
	$( ".collapse1-content-item-img a.rr-value1" ).click(function(event) {
		event.preventDefault();
		/* console.log($(this).offset());
		$('.collapse1-content-item-right-new.collapse1-content-item-right-toggle').position({ top: $(this).offset().top, left: $(this).offset().left});
		// $(".collapse1-content-item-right-new.collapse1-content-item-right-toggle div:last-child").focus();
		$('.collapse1-content-item-right-new.collapse1-content-item-right-toggle').toggle("slow"); */
		var toggle = $('.collapse1-content-item-right-new.collapse1-content-item-right-toggle')
		var thread = $(this).closest(".thread-holder").data("thread");
		var endpoint = '/social/thread/message';
		var data = {
			'thread': thread,
		}
		ajaxCaller(data, endpoint, (res) => {
			var res = JSON.parse(res)
			toggle.children().remove();
			for (i = 0; i < res.length; i++) {
				toggle.append(
					`<div class="collapse1-content-item-right-row">
						<div class="collapse1-content-item-right">
							<span><img src="${res[i].user.avatar}">Username</span>
							<p>${res[i].content}</p>
						</div>
					</div>`
				)
			}
		})
		$('.collapse1-content-item-right-new.collapse1-content-item-right-toggle').hide("fast");
		$(this).parent().parent().find(".collapse1-content-item-right-new.collapse1-content-item-right-toggle").toggle("slow");
		return false;
	});
	$( "body" ).click(function(event) {
		// $('.collapse1-content-item-right-new.collapse1-content-item-right-toggle').hide("fast");
		var container = $('.collapse1-content-item-right-new.collapse1-content-item-right-toggle');
		if (!container.is(event.target) && container.has(event.target).length === 0) {
			container.hide();
		}
	});
});

// API function
const ajaxCaller = (data, endpoint, success, failure) => {
    $.ajax({
        url: `${endpoint}/${data.uid}`,
				method: "post",
				data: JSON.stringify(data),
				contentType: "application/json",
        success: (res) => {
            if (typeof success === "function") {
                success(res)
            } else {
                console.log(res)
            }
        },
        error: (res) => {
            if (typeof failure === "function") {
                failure(res)
            } else {
                console.log(res)
            }
        }
    })
}

const fileUploadAjaxCaller = (data, endpoint, success, failure) => {
    $.ajax({
        url: `${endpoint}`,
		type: "POST",
		xhr: function() {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                myXhr.upload.addEventListener('progress',progressHandlingFunction, false);
            } else {
                console.log("Upload progress is not supported!");
            }
            return myXhr;
		},
		data: data,
		cache: false,
		processData: false,
		contentType: false,
        success: (res) => {
            if (typeof success === "function") {
                success(res)
            } else {
                console.log(res)
            }
        },
        error: (res) => {
            if (typeof failure === "function") {
                failure(res)
            } else {
                console.log(res)
            }
        }
    })
}

const progressHandlingFunction = (e) => {
    if (e.lengthComputable) {
        console.log("hai progress!");
        console.log(e.loaded);
        console.log(e.total);
        $("progress").attr({value: e.loaded, max: e.total});
    }
}

// DRAW function
const allThreadPopupDrawer = (res) => {
	$("body, html").animate({
		scrollTop: $(".collapse-custom .collapse-main").position().top - 40
	});
	// $('.over_threads').fadeIn();
	jQuery('.all-thread-popup .collapse1-content-item-top label').text(`${res.user.firstname} ${res.user.lastname}`);
	jQuery('.all-thread-popup .collapse1-content-item-pop').attr("id", `data-thread-${res.uid}`);
	jQuery('.all-thread-popup .collapse1-content-item-pop img').attr("src", res.image);
	jQuery('.all-thread-popup .collapse1-content-item-pop .rr-value1').text(res.link);
	jQuery('.all-thread-popup .collapse1-content-item-pop .rr-value2').text(res.hashtag);
	jQuery('.all-thread-popup .collapse1-content-item-pop h6').text(res.description);
	jQuery('.all-thread-popup .respond-to-author-form input[name=thread]').val(res.uid)
	jQuery('.all-thread-popup .respond-to-topic-modal input[name=thread]').val(res.uid)


	follow_btn = jQuery('.all-thread-popup .follow-btn');
	follow_btn.children().remove()

	if (res.following) {
		follow_btn.append(
			`<a class="myBtn btn btn btn-primary unfollow-thread" style="margin-left: 0px; width:100px;">UnFollow</a>`
		)
	} else {
		follow_btn.append(
			`<a class="myBtn btn btn btn-primary follow-thread" style="margin-left: 0px; width:100px;">Follow</a>`
		)
	}

	messages = jQuery('.messages')
	messages.children().remove()

	if (res.messages) {
		for (i=0; i < res.messages.length; i++){
			if (res.messages[i].image){
				imageTag = `<div><img src="${res.messages[i].image}" class="message-image"></div>`;
			} else {
				imageTag = "";
			};
			messages.append(
				`<div class="collapse1-content-item-right-row">
					<div class=" collapse1-content-item-right-top col-lg-12 p-0 float-left">
						<span>${res.messages[i].user.firstname} ${res.messages[i].user.lastname}</span> <img src="${res.messages[i].user.avatar}">
					</div>
					${ res.messages[i].content.substring(0, 40) }...
					${imageTag}
					<div class="box-hover-clear">
						<h5>${ res.messages[i].content }</h5>
					</div>
					<div class="close-popup">
						<div class="close-popup_box">x</div>
					</div>
				</div>`
			)
		}
	};
	$(".close-popup").click(function(){
        $(this).closest(".collapse1-content-item-right-row").remove();
	});

	$('#data-thread-' + res.uid).fadeIn("slow")
		.animate({height:"100%"}, 200, function() {
	});
}

const threadDrawer = (res, target) => {
	// $('.over_threads').fadeIn();
	var parent = target.parent()
	parent.find(".collapse1-content-item-pop").fadeIn("slow")
		.animate({height:"100%"}, 300, function() {
	});
	$("body, html").animate({
		scrollTop: $(".collapse-custom .collapse-main").position().top - 40
	});

	parent.find('.collapse1-content-item-top label').text(`${res.user.firstname} ${res.user.lastname}`);
	parent.find('.collapse1-content-item-pop').attr("id", `data-thread-${res.uid}`);
	parent.find('.collapse1-content-item-pop img').attr("src", res.image);
	parent.find('.collapse1-content-item-pop .rr-value1').text(res.link);
	parent.find('.collapse1-content-item-pop .rr-value2').text(res.hashtag);
	parent.find('.collapse1-content-item-pop h6').text(res.description);
	follow_btn = parent.find('.collapse1-content-item-pop .follow-btn');
	follow_btn.children().remove()

	if (res.following) {
		follow_btn.append(
			`<a class="myBtn btn btn btn-primary unfollow-thread" style="margin-left: 0px; width:100px;">UnFollow</a>`
		)
	} else {
		follow_btn.append(
			`<a class="myBtn btn btn btn-primary follow-thread" style="margin-left: 0px; width:100px;">Follow</a>`
		)
	}

	messages = parent.find('.messages')
	messages.children().remove()
	if (res.messages) {
		for (i=0; i < res.messages.length; i++){
			if (res.messages[i].image){
				imageTag = `<div><img src="${res.messages[i].image}" class="message-image"></div>`;
			} else {
				imageTag = "";
			};
			messages.append(
				`<div class="collapse1-content-item-right-row">
					<div class=" collapse1-content-item-right-top col-lg-12 p-0 float-left">
						<span>${res.messages[i].user.firstname} ${res.messages[i].user.lastname}</span> <img src="${res.messages[i].user.avatar}">
					</div>
					${ res.messages[i].content.substring(0, 40) }...
					${imageTag}
					<div class="box-hover-clear">
						<h5>${ res.messages[i].content }</h5>
					</div>
					<div class="close-popup">
						<div class="close-popup_box">x</div>
					</div>
				</div>`
			)
		}
	};
	$(".close-popup").click(function(){
        $(this).closest(".collapse1-content-item-right-row").remove();
	});

	$('#data-thread-' + res.uid).fadeIn("slow")
		.animate({height:"100%"}, 200, function() {
	});
}

const drawCategoryThreadsTableBody = (res, tbody) => {
	for (i=0; i < res.length; i++) {
		tbody.append(
			`<tr data-thread="${res[i].uid}">
				<td>
					<i class="fa fa-star" aria-hidden="true"></i>
					<i class="fa fa-lock" aria-hidden="true"></i>
					<i class="fa fa-shield" aria-hidden="true"></i>
					Random Title mode here by Authr
				</td>
				<td>General</td>
				<td>Name</td>
				<td>22</td>
				<td>342</td>
				<td>12m</td>
				<td>
					<div class="progress">
						<div class="progress-bar" role="progressbar" style="width: 75%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
					</div>
				</td>
			</tr>`
		)
	}
}
