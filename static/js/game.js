var questions = {"box1": "I often buy new products before they become popular or come down in price.",
				"box3": "I have much more energy than most persons my age.",
				"box6": "I prefer to go to undiscovered places rather than cities with big hotels. ",
				"box8": "I prefer setting up plans and having a routine rather than spontaneity.",
				"box9": "I am more intellectually curious than most people I know.",
				"box12": "I believe chance has little to do with the successes I've had in my life."
				}

$(document).ready(loadData);

function loadFirstQuestion() {
	$('#box1').show();
	$('#box1').css('background-color','#80ff95');
};

function loadData() {
	loadFirstQuestion();
	for (var i=1; i<=12; i++) {
		if (questions['box'+i]) {
			$('#box'+i).html('<div class="question-data">' + questions['box'+i] + '<br><button class="btn btn-success" id="box' +i+ '-button1" type="button">Yes</button> <button class="btn btn-danger" id="box' +i+ '-button2" type="button">No</button></div>')
		}
		$('#box'+i + ' > .question-data').css('display','none');
		$('#box1  > .question-data').css('display','block');
	}
};

$(document).on('click', '#box1-button1', function() {
	$('#box1').find('button').css('display','none');
	$('#box6 > .question-data').css('display','block');
	$('#box6').css('background-color','#80ff95');
});

$(document).on('click', '#box1-button2', function() {
	$('#box1').find('button').css('display','none');
	$('#box6 > .question-data').css('display','block');
	$('#box6').css('background-color','#80ff95');
});

$(document).on('click', '#box6-button1', function() {
	$('#box6').find('button').css('display','none');
	$('#box9 > .question-data').css('display','block');
	$('#box9').css('background-color','#80ff95');
});

$(document).on('click', '#box6-button2', function() {
	$('#box6').find('button').css('display','none');
	$('#box12 > .question-data').css('display','block');
	$('#box12').css('background-color','#80ff95');
});

$(document).on('click', '#box3-button1', function() {
	//hide page and reveal Pioneers
	alert("You're a pioneer!");
	var persona = {persona: 'pioneer'}
	$.post("/persona", persona, function (result) {
		console.log('result');
	})
	showPioneers();
});

$(document).on('click', '#box3-button2', function() {
	//hide page and reveal Venturers
	alert("You're a Venturer!");
	showVenturers();
});

$(document).on('click', '#box8-button1', function() {
	//hide page and reveal Traditionals
	alert("You're a Traditional!");
	showTraditionals();
});

$(document).on('click', '#box8-button2', function() {
	//hide page and reveal Voyagers
	alert("You're a Voyager!");
	showVoyagers();
});

$(document).on('click', '#box9-button1', function() {
	$('#box9').find('button').css('display','none');
	$('#box3 > .question-data').css('display','block');
	$('#box3').css('background-color','#80ff95');
});

$(document).on('click', '#box9-button2', function() {
	$('#box9').find('button').css('display','none');
	$('#box3 > .question-data').css('display','block');
	$('#box3').css('background-color','#80ff95');
});

$(document).on('click', '#box12-button1', function() {
	$('#box12').find('button').css('display','none');
	$('#box8 > .question-data').css('display','block');
	$('#box8').css('background-color','#80ff95');
});

$(document).on('click', '#box12-button2', function() {
	$('#box12').find('button').css('display','none');
	$('#box8 > .question-data').css('display','block');
	$('#box8').css('background-color','#80ff95');
});

