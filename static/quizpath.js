function showQ2(){
	$("#question2").show();
}

function showQ3(){
	$("#question3").show();
}

function showQ4(){
	$("#question4").show();
}

function showQ5(){
	$("#question5").show();
}

$( document ).ready(function() {
        console.log( "document loaded" );
        $('#load-more-results').hide();
    });


// AUTOCOMPLETE

$(function() {
$("#airportcodes").autocomplete({
	source: function(request, response) {
		$.ajax({
			url: "/autocomplete",
			dataType: "json",
			data: {
				term: request.term
			}
		})
		.done(function(data) {
			response(data.data);
		})
	}
})
});


function showVenturers(){
	$("#persona").html("<h2>You are a <b>Venturer</b></h2><p>Leisure travel occupies a central place in your life. You go to more places, more often and participate in more unique experiences than anyone else. That’s why I call you a Venturer-someone who ventures forth very eagerly and excitedly. You fit in a small group. Only about 4% of all travelers share your extreme love of going to out of the way places and constantly seeking out of the ordinary adventures.</p>");

	getFareResults(); // NEED TO ADD A THEME FOR EACH PERSONA
}

function showPioneers(){
	$("#persona").html("<h2>You are a <b>Pioneer</b></h2><p>You like to travel, especially to foreign destinations and you seek new experiences and new destinations for almost all trips you take. You are also physically active at home and on trips. But, unlike your pure Venturer friends, you don’t want to take such extreme vacations and are more likely to plan your trips-set an itinerary of places you want to visit and schedules when you will be there. You also have more company. About 17% of the population has a personality that matches yours, vs. only 4% for pure Venturers.</p>");
	
	getFareResults();
}


function showVoyagers(){
	$("#question-section").fadeOut(1000);
	$("#persona").hide();
	$(".top-three-results").hide();
	$(".remaining-results").hide();
	$("#persona").html("<h2>You are a <b>Voyager</b></h2><p>Compared to other groups, you have lots of company. Three out of ten travelers (30%) place in your group, making you one of the largest segments of travelers. As a result, the majority of travel providers-airlines, resorts, rental car companies, tour operators, cruise lines, and others- place you at the top of their list of persons they want to reach and motivate to travel.</p>");
	$("#persona").fadeIn(5000);

	getFareResults();
}

function showTraditionals(){
	$("#question-section").fadeOut(1000);
	$("#persona").hide();
	$(".top-three-results").hide();
	$(".remaining-results").hide();
	$("#persona").html("<h2>You are a <b>Traditional</b></h2><p>You prefer a life that is more structured, stable and predictable. You would rather follow some set patterns or routines in your life so that you are more likely to know what will happen during each day and, therefore, can plan or prepare for it much better.</p>");
	$("#persona").fadeIn(5000);

	getFareResults("Romantic");
}




function getRandom(max) {
    return Math.floor(Math.random() * max);
}



function getFareResults(persona){


	// sending GET request to get form values
	var url = "/airfaresearch.json?origin=" + $("#airportcodes").val() + 
				"&persona=" + persona;
	console.log(url)


	// calling for geoJSON
	$.get(url, function (data) {
		console.log(data);
		var results = data.data;

		for (var i=0; i<3; i++){
			var r = getRandom(results.length);
			var city=results[r].city;
			var lon=results[r].lon;
			var lat=results[r].lat;
			var fare=results[r].fares;

			var lowestFare = fare[0].lowestFare;
			var lowestFareDep = fare[0].departureDateTime;
			var lowestFareRet = fare[0].returnDateTime;
			 
			var fareArray = [];
			
			for (var f=0; f < fare.length; f++) {
			
				var date = fare[f].departureDateTime.slice(5,10);
				console.log(date);
				var dateLowFare = parseInt(fare[f].lowestFare);
				var dateLowNonStopFare = fare[f].lowestNonStopFare;

				fareArray.push([date, dateLowFare, dateLowNonStopFare]);

				// find the lowest fare
				// see if there's more than one result
				// if so, go through each day and compare with the lowestfare
				// if lower than current lowestfare, update it
				if (isNaN(fare[f].lowestFare) == false){
					if (10 < fare[f].lowestFare && fare[f].lowestFare < lowestFare) {
						lowestFare = fare[f].lowestFare;
						lowestFareDep = fare[f].departureDateTime;
						lowestFareRet = fare[f].returnDateTime;
					}
				}

			}

			results.splice(r, 1);

			console.log("Lowest: ");
			console.log(lowestFare);
			$(".top-three-results").append(
						"<div class='top-result'><h3>" + city +
						"</h3><p>Lowest Fare: $" + parseInt(lowestFare) + 
						"</p><p>Departure Date: " + lowestFareDep.slice(0,10) +
						"</p><p>Return Date: " + lowestFareRet.slice(0,10) +
						"</p><button class='experiences-btn' data-lat='" + lat + "' data-lon='" + lon + "' data-toggle='modal' data-target='#experiences-feed'>Things To Do</button></div>")
			console.log(lowestFareDep);
			console.log(lowestFareRet);

		}

		for (var i=0; i<results.length; i++){
			var city=results[i].city;
			var lon=results[i].lon;
			var lat=results[i].lat;
			var fare=results[i].fares;

			var lowestFare = fare[0].lowestFare;
			var lowestFareDep = fare[0].departureDateTime;
			var lowestFareRet = fare[0].returnDateTime;
			 
			var fareArray = [];
			
			for (var f=0; f < fare.length; f++) {
			
				var date = fare[f].departureDateTime.slice(5,10);
				console.log(date);
				var dateLowFare = parseInt(fare[f].lowestFare);
				var dateLowNonStopFare = fare[f].lowestNonStopFare;

				fareArray.push([date, dateLowFare, dateLowNonStopFare]);

				// find the lowest fare
				// see if there's more than one result
				// if so, go through each day and compare with the lowestfare
				// if lower than current lowestfare, update it
				if (isNaN(fare[f].lowestFare) == false){
					if (10 < fare[f].lowestFare && fare[f].lowestFare < lowestFare) {
						lowestFare = fare[f].lowestFare;
						lowestFareDep = fare[f].departureDateTime;
						lowestFareRet = fare[f].returnDateTime;
					}
				}

			}

			console.log("Lowest: ");
			console.log(lowestFare);
			$(".remaining-results").append(
						"<div class='top-result'><h3>" + city +
						"</h3><p>Lowest Fare: $" + parseInt(lowestFare) + 
						"</p><p>Departure Date: " + lowestFareDep.slice(0,10) +
						"</p><p>Return Date: " + lowestFareRet.slice(0,10) +
						"</p><button class='experiences-btn' data-toggle='modal' data-target='#experiences-feed'>Things To Do</button></div>");
			console.log(lowestFareDep);
			console.log(lowestFareRet);

		}

	})



	$(".top-three-results").fadeIn(7000, function() {
		$("#load-more-results").show();
	});

}


// function showExperiences(){
// 	var lon = $(this).data("lon");
// 	// var lat = $(this).data('coords').lat;

// 	console.log("coords" + lon);
// }


// EVENT LISTENERS

$("#random").on("click", showTraditionals);


$("#load-more-results").on("click", function() {
	$("#load-more-results").hide();
	$(".remaining-results").fadeIn(2000);
});



// FUNCTION TO GET XOLA EXPERIENCES
$(document).on('click', '.experiences-btn', function() {

	var lon = $(this).data("lon");
	var lat = $(this).data("lat");

	console.log("lon: " + lon);
	console.log("lat: " + lat);


	var url = "/experiencesearch.json?lat=" + lat + 
				"&lon=" + lon;
	console.log(url)


	// calling for geoJSON
	$.get(url, function (data) {
		console.log(data);

	})
});



