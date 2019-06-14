jQuery(document).ready(function($) {
	jQuery(".myBtn").click(function(){
		// console.log('ok');
		jQuery(this).parent().find(".modal").fadeIn();
	});
	jQuery(".close").click(function(){
		$(".modal").hide();
	});

	jQuery(".collapse1-content-item").click(function(){
		// $('.over_threads').fadeIn();
		jQuery(this).parent().find(".collapse1-content-item-pop").fadeIn("slow")
			.animate({height:"100%"}, 300, function() {
		});
		$("body, html").animate({
			scrollTop: $(".collapse-custom .collapse-main").position().top - 40
		});
	});

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
		jQuery(this).parent().find(".collapse1-content-category-pop").fadeIn("slow")
			.css({top:0,position:'absolute'})
			.animate({top:0}, 500, function() {
		});
	});
	jQuery(".collapse-main-Boards table tbody tr").click(function(){
		var thread = jQuery(this).data("thread")
		getThread(thread, (res) => {
			var res = JSON.parse(res)[0]
            if (res.uid) {
                drawThread(res);
            }
        })
		// $("body, html").animate({
		// 	scrollTop: $(".collapse-custom .collapse-main").position().top - 40
		// });
		// // $('.over_threads').fadeIn();
		// var data_thread = jQuery(this).attr('data-thread');
		// $('#data-thread-' + data_thread).fadeIn("slow")
		// 	.animate({height:"100%"}, 200, function() {
		// });

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
				  if( log ) alert(log);
			  }

		  });
	});
});

// API function
const getThread = (uid, success, failure) => {
    $.ajax({
        url: `/thread/${uid}`,
        method: "post",
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

// DRAW function
const drawThread = (res) => {
	$("body, html").animate({
		scrollTop: $(".collapse-custom .collapse-main").position().top - 40
	});
	// $('.over_threads').fadeIn();
	jQuery('.all-thread-popup .collapse1-content-item-pop').attr("id", `data-thread-${res.uid}`);
	jQuery('.all-thread-popup .collapse1-content-item-pop img').attr("src", res.image);
	jQuery('.all-thread-popup .collapse1-content-item-pop .rr-value1').text(res.link);
	jQuery('.all-thread-popup .collapse1-content-item-pop .rr-value2').text(res.hashtag);
	jQuery('.all-thread-popup .collapse1-content-item-pop h6').text(res.description);
	messages = jQuery('.messages')
	messages.children().remove()

	for (i=0; i < res.messages.length; i++){
		console.log(res.messages[i])
		messages.append(
			`<div class="collapse1-content-item-right-row">
				<div class=" collapse1-content-item-right-top col-lg-12 p-0 float-left">
					<span>${res.messages[i].id}</span> <i class="fa fa-bicycle" aria-hidden="true"></i>
				</div>
				${ res.messages[i].content.substring(40) }...
				<div class="box-hover-clear">
					<h5>${ res.messages[i].content }</h5>
				</div>
				<div class="close-popup">
					<div class="close-popup_box">x</div>
				</div>
			</div>`
		)
	}
	$(".close-popup").click(function(){
        $(this).closest(".collapse1-content-item-right-row").remove();
	});

	$('#data-thread-' + res.uid).fadeIn("slow")
		.animate({height:"100%"}, 200, function() {
	});
}
