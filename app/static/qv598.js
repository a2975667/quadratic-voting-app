function qv_cal(number){	
	return Math.pow(number, 2);
}

function qv_total_voice(){
	var total_votes = $(".qv_cost").length
	return Math.pow(total_votes/2, 2)
}

var submit_url = '/submit_qv598'

var the_next_url = '/qv/5982'