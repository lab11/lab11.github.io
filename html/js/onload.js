
$(".pcb_rev_dropdown").click(function() {
	var button_id = $(this).attr("id");
	var board_class = button_id.replace(/pcb_rev_dropdown_/,"");

	if ($(this).hasClass("showing")) {
		$(".row_old_" + board_class).hide("slow");
		$(this).removeClass("showing");
		$(this).addClass("hiding");
		$(this).children(".hiding").show()
		$(this).children(".showing").hide()
	} else {
		$(".row_old_" + board_class).show("slow");
		$(this).addClass("showing");
		$(this).removeClass("hiding");
		$(this).children(".showing").show()
		$(this).children(".hiding").hide()
	}
});

$(".lightbox_image").click(function(e) {
	var image_id = $(this).attr("id");
	$("#" + image_id + "_full").lightbox_me({
		centered: true,
		});
  //  e.preventDefault();
});

$(".pub_bibtex").click(function() {
	var a_id = $(this).attr("id");
	var div_id = a_id.replace('XXXatag_', '');
	$('#'+div_id).slideToggle( "slow" );
});

$(".pub_abstract").click(function() {
	var a_id = $(this).attr("id");
	var div_id = a_id.replace('XXXatag_', '');
	$('#'+div_id).slideToggle( "slow" );
});

$(".pub_abstract_raw").click(function() {
	var a_id = $(this).attr("id");
	var raw_div_id = a_id.slice(0, -2);
	var html_div_id = a_id.slice(0, -5) + "html";
	$('#'+raw_div_id).hide("slow");
	$('#'+html_div_id).show("slow");
});

$(".pub_abstract_html").click(function() {
	var a_id = $(this).attr("id");
	var html_div_id = a_id.slice(0, -2);
	var raw_div_id = a_id.slice(0, -6) + "raw";
	$('#'+html_div_id).hide("slow");
	$('#'+raw_div_id).show("slow");
});

$(".type_chk").change(function() {
	var chk_val = $(this).attr("value");
	if (this.checked) {
		$('.pub_type_'+chk_val).removeClass('pub-type-not-selected');
	} else {
		$('.pub_type_'+chk_val).addClass('pub-type-not-selected');
	}
});

var pub_author_filter_last_hl = undefined;
$("#pub_filter_author").change(function() {
	var author = $("#pub_filter_author").val();

	$(".author-" + author).each(function() {
		$(this).addClass('author-highlight');
	});
	if (pub_author_filter_last_hl != undefined) {
		$(".author-" + pub_author_filter_last_hl).each(function() {
			$(this).removeClass('author-highlight');
		});
	}
	pub_author_filter_last_hl = author;

	$(".pub_entry").each(function() {
		$(this).parent().removeClass('author-not-selected');
	});

	if (author != "all") {
		$(".pub_entry").each(function() {
			var child = $(this).find(".author-"+author);
			if (child.hasClass("author-"+author)) {
				; //console.log(child);
			} else {
				$(this).parent().addClass('author-not-selected');
			}
		});
	}
});

var pub_filter_venue_last_hl = undefined;
$("#pub_filter_venue").change(function() {
	var venue = $("#pub_filter_venue").val();

	$(".venue-" + venue).each(function() {
		$(this).addClass('venue-highlight');
	});
	if (pub_filter_venue_last_hl != undefined) {
		$('.venue-' + pub_filter_venue_last_hl).each(function() {
			$(this).removeClass('venue-highlight');
		});
	}
	pub_filter_venue_last_hl = venue;

	$(".pub_entry").each(function() {
		$(this).parent().removeClass('venue-not-selected');
	});

	if (venue != "all") {
		$(".pub_entry").each(function() {
			var child = $(this).find(".venue-"+venue);
			if (child.hasClass("venue-"+venue)) {
				; //console.log(child);
			} else {
				$(this).parent().addClass('venue-not-selected');
			}
		});
	}
});

$('.pub_prepub').each(function() {
	var id = $(this).attr("id");
	var temp = id.split("XXX");
	var root = temp[0];
	var pub_date = Date.parse(temp[1]);
	var now = new Date();

	if (pub_date > now) {
		var showhide = function() {
			$('#'+id.replace( /(:|\.|\[|\])/g, "\\$1" )).slideToggle("slow");
		};

		var title = $('#' + root.replace("-prepub", "-title"));
		var link = $('#' + root.replace("-prepub", "-link"));
		title.attr('href', '#');
		title.click(showhide);
		link.text('[To Appear]');
		link.attr('href', '#');
		link.click(showhide);
	}
});

$('.github-repo').each(function() {
	var id = $(this).attr("id");
	url_fields = id.split("||")
	var gh_api_repo = "https://api.github.com/repos/" + url_fields[0] + "/" + url_fields[1];
	var gh_api_last_commit = gh_api_repo + "/git/refs/heads/master";
	var a_container = $(this);
	var count = 2;
	$.getJSON(gh_api_repo, {}).done(function (data) {
		//console.log("gh_api_repo done");
		a_container.append('<p class="list-group-item-text" style="display:none;"><small>'+data["description"]+"</small></p>");
		var gh_api_repo = "https://api.github.com/repos/" + url_fields[0] + "/" + url_fields[1];
		show_gh(--count, a_container);
	});
	$.getJSON(gh_api_last_commit, {}).done(function (data) {
		//console.log("gh_api_last_commit done");
		var sha = data['object']['sha'];
		var gh_api_commit = gh_api_repo + "/commits/" + sha;
		$.getJSON(gh_api_commit, {}).done(function (data) {
			//console.log("gh_api_commit done");
			a_container.append('<p class="list-group-item-text text-muted" style="display:none;"><small>Updated '+timeAgo(data['commit']['author']['date'])+' ago by '+data['author']['login']+'</small></p>');
			show_gh(--count, a_container);
		});
	});
});

function show_gh (count, a_container){
	//console.log("count " + count + " container " + a_container);
	if (count == 0) {
		a_container.children("p").slideDown("slow");
	}
}

function timeAgo (time){
	var units = [
		{ name: "second", limit: 60, in_seconds: 1 },
		{ name: "minute", limit: 3600, in_seconds: 60 },
		{ name: "hour", limit: 86400, in_seconds: 3600 },
		{ name: "day", limit: 604800, in_seconds: 86400 },
		{ name: "week", limit: 2629743, in_seconds: 604800 },
		{ name: "month", limit: 31556926, in_seconds: 2629743 },
		{ name: "year", limit: null, in_seconds: 31556926 }
	];
	var diff = (new Date() - new Date(time)) / 1000;
	if (diff < 5) return "now";
	var i = 0;
	while (unit = units[i++]) {
		if (diff < unit.limit || !unit.limit) {
			var diff = Math.floor(diff / unit.in_seconds);
			return diff + " " + unit.name + (diff>1 ? "s" : "");
		}
	};
}

function scroll_if_anchor(href) {
	href = typeof(href) == "string" ? href : $(this).attr("href");

	if (href == undefined) return;

	// You could easily calculate this dynamically if you prefer
	var fromTop = 60;

	// If our Href points to a valid, non-empty anchor, and is on the same page (e.g. #foo)
	// Legacy jQuery and IE7 may have issues: http://stackoverflow.com/q/1593174
	if(href.indexOf("#") == 0) {
		var $target = $(href);

		// Older browser without pushState might flicker here, as they momentarily
		// jump to the wrong position (IE < 10)
		if($target.length) {
			$('html, body').animate({ scrollTop: $target.offset().top - fromTop });
			if(history && "pushState" in history) {
				history.pushState({}, document.title, window.location.pathname + href);
				return false;
			}
		}
	}
}

// When our page loads, check to see if it contains and anchor
scroll_if_anchor(window.location.hash);

// Intercept all anchor clicks
$("body").on("click", "a", scroll_if_anchor);
