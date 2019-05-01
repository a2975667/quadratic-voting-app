$("#qv_form").submit(function (event) {
	var retVal = confirm("Do you want to continue ?");
		if( retVal == true ) {
			var next_url = the_next_url;
			//console.log(the_next_url)
			//var next_url = '/complete';
			// Cookies.set('next', JSON.stringify(seq));
		
			var formData = JSON.stringify($("#qv_form").serializeArray());
			$.ajax({
				type: "post",
				url: submit_url,
				data: formData,
				success: function (result) {
					window.location.href = next_url;
				},
				dataType: "json",
				contentType: 'application/json'
			});
			window.location.href = next_url;
			event.preventDefault();
		   return true;
		} else {
		   return false;
		}
});

$("#other").click(function () {
	$("#qv_form").submit();
});

$(document).ready(function () {
	var page_url = window.location.pathname;

	if (page_url == '/qv/4'){
		$("#partial").show();
		$('.type').text('Partial Binary Quadratic Voting');
		// $(".qv_vote").map(function () {$(this).attr("value",1);});
		$(".qv_cost").map(function () {$(this).attr("value",1);});
		$(".qv_cost").map(function () {$(this).text(1);
			get_total_cost();
			check_clickable();
		});
	}else if (page_url == '/qv/example'){
		$("#example").show();
		$('#not_example').hide()
		$('.type').text('Binary Quadratic Voting');
	}else{
		$("#binary").show();
		$('.type').text('Binary Quadratic Voting');
	}


	$('#used_votes').text(0);
	$('#total_votes').text(qv_total_voice().toString());
	$('.total_votes').text(qv_total_voice().toString());
	$('#bar').attr('style', 'width: 0%')

	$('select').formSelect();

	$('.plus').click(function () {
		var prev_vote = parseInt($(this).siblings('.qv_vote').val())

		// update vote
		var new_vote = prev_vote + 1
		$(this).siblings('.qv_vote').val(new_vote)

		//update cost
		
		var new_cost = qv_cal(Math.abs(new_vote))
		console.log(new_vote, new_cost)
		$(this).siblings('.qv_cost').attr("value", new_cost)
		$(this).siblings('.qv_cost').text(new_cost.toString())
		get_total_cost()
		check_clickable()

		var replace_icon = ''
		if (new_vote >= 0) {
			for (var i=0; i<new_vote; i++){
				replace_icon = replace_icon + "<i class='far fa-check-circle icon' style='display:inline; color:green; vertical-align: text-bottom;'></i>"
			}
		}else{
			for (var i=0; i<Math.abs(new_vote); i++){
				replace_icon = replace_icon + "<i class='far fa-times-circle icon' style='display:inline; color:red; vertical-align: text-bottom;'></i>"
			}
		}
		
		$(this).siblings('.placeholder').html(replace_icon);
	});

	$('.minus').click(function () {
		var prev_vote = parseInt($(this).siblings('.qv_vote').val())

		// update vote
		var new_vote = prev_vote - 1
		$(this).siblings('.qv_vote').val(new_vote)

		//update cost
		var new_cost = qv_cal(Math.abs(new_vote))
		$(this).siblings('.qv_cost').attr("value", new_cost)
		$(this).siblings('.qv_cost').text(new_cost.toString())
		get_total_cost()
		check_clickable()

		var replace_icon = ''
		if (new_vote >= 0) {
			for (var i=0; i<new_vote; i++){
				replace_icon = replace_icon + "<i class='far fa-check-circle icon' style='display:inline; color:green; vertical-align: text-bottom;'></i>"
			}
		}else{
			for (var i=0; i<Math.abs(new_vote); i++){
				replace_icon = replace_icon + "<i class='far fa-times-circle icon' style='display:inline; color:red; vertical-align: text-bottom;'></i>"
			}
		}
		
		$(this).siblings('.placeholder').html(replace_icon);

	});
});

function add(accumulator, a) {
	return accumulator + a;
}

function get_total_cost() {
	var list_of_cost = $(".qv_cost").map(function () {
		return parseInt($(this).attr("value"));
	}).get();
	var total = list_of_cost.reduce(add)
	$('#used_votes').text(total.toString());
	$('#bar').attr('style', ('width: ' + (total * 100 / qv_total_voice()).toString() + '%'))
	return total;
}

function check_clickable() {
	var total = qv_total_voice()
	var current_total = parseInt($('#used_votes').text())
	$(".qvbtn").each(function (index) {
		var actual_value = parseInt($(this).siblings('.qv_vote').val())
		var current_vote = Math.abs(actual_value)

		// console.log($(this).siblings('.qv_vote').attr('name'), current_vote)
		// console.log(total, current_total, qv_cal(current_vote+1), total < (current_total + qv_cal(current_vote+1)))
		if (total < (current_total - qv_cal(current_vote) + qv_cal(current_vote + 1))) {
			$(this).each(function () {
				if (actual_value > 0) {
					if ($(this).hasClass('plus')) {
						$(this).addClass('disabled');
					}
				} else if (actual_value < 0) {
					if ($(this).hasClass('minus')) {
						$(this).addClass('disabled');
					}
				} else {
					$(this).addClass('disabled');
				}
			})
		} else {
			$(this).removeClass('disabled');
		}
		//console.log( current_vote );
	});
}

function toggle(btn, text) {
	var btn = document.getElementById(btn);
	var text = document.getElementById(text);
	if(btn.innerHTML == "Show") {
    		btn.innerHTML = "Hide";
		text.style.display = "block";
  	}
	else {
		btn.innerHTML = "Show";
		text.style.display = "none";
	}
} 

$(window).on('load', function() {
	get_total_cost();
	check_clickable();
	$(".summary").magnet();
	$("#cover").hide();
});
