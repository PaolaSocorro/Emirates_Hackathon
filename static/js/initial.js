$(document).ready(loadFirstQuestion);

function loadFirstQuestion() {
	$('#box1').css('background-color','#80ff95');
	$('#question').html($('#box1').attr('data-question'));
	$('#box1').html($('#box1').attr('data-question'));
	$('#option1').attr('next', 'q2');
	$('#option2').attr('next', 'q2');
}

$('button').on('click', showNextQuestion);


function showNextQuestion() {
	$('#question').empty();
	console.log($('#option1').attr('next'));
	if ($('#option1').attr('next') == 'q2') {
		$('#question').empty();
		$('#question').html($('#box3').attr('data-question'));
		$('#box6').css('background-color','#80ff95');
		$('#box6').html($('#box6').attr('data-question'));
		$('#option1').attr('next', 'q3');
		$('#option2').attr('next', 'q5');
	}
	$('#option1').on('click', showOption1);
	$('#option2').on('click', showOption2);
}

function showOption1() {
	$('#question').empty();
	if ($('#option1').attr('next') == 'q3') {
		$('#question').empty();
		$('#question').html($('#box6').attr('data-question'));
		$('#box6').css('background-color','#80ff95');
		$('#box6').html($('#box3').attr('data-question'));
		$('#option1').attr('next', 'q4');
		$('#option2').attr('next', 'q4');
	}
	else {
		alert('hi');
	}
	if ($('#option1').attr('next') == 'q4') {
		$('#question').empty();
		$('#question').html($('#box6').attr('data-question'));
		$('#box3').css('background-color','#80ff95');
		$('#box3').html($('#box3').attr('data-question'));
		$('#option1').on('click', function() {
			$('button').hide();
			$('#question').append('<a href="/pioneers.html">See results</a>');
		});
		$('#option2').on('click', function() {
			$('#question').append('<a href="/venturers.html">See results</a>')
		});
	}
	$('button').on('click', showFollowingQuestion);
}

function showOption2() {
	$('#question').empty();
	console.log($('#option2').attr('next'));
	if ($('#option2').attr('next') == 'q5') {
		$('#question').empty();
		$('#question').html($('#box9').attr('data-question'));
		$('#box9').css('background-color','#80ff95');
		$('#box9').html($('#box3').attr('data-question'));
		$('#option1').attr('next', 'q4');
		$('#option2').attr('next', 'q4');
	}
	else {
		alert('hello');
	}
	if ($('#option2').attr('next') == 'q4') {
		$('#question').empty();
		$('#question').html($('#box8').attr('data-question'));
		$('#box8').css('background-color','#80ff95');
		$('#box8').html($('#box3').attr('data-question'));
		$('#option1').on('click', function() {
			$('button').hide();
			$('#question').append('<a href="/pioneers.html">See results</a>');
		});
		$('#option2').on('click', function() {
			$('#question').append('<a href="/venturers.html">See results</a>')
		});
	};
	$('button').on('click', showFollowingQuestion);
}

function showFollowingQuestion() {
	$('#option1').on('click', showOption1);
	$('#option2').on('click', showOption2);
}