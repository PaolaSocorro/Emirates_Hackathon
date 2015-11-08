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
	$("#persona").append("<h2>You are a <b>Venturer</b></h2>");
	$("#persona").append("<p>Leisure travel occupies a central place in your life. If you are a typical Venturer, you go to more places, more often and participate in more unique experiences than anyone else. That’s why I call you a Venturer-someone who ventures forth very eagerly and excitedly. You fit in a small group. Only about 4% of all travelers share your extreme love of going to out of the way places and constantly seeking out of the ordinary adventures.</p>");

}

function showPioneers(){
	$("#persona").append("<h2>You are a <b>Pioneer</b></h2>");
	$("#persona").append("<p>As a Pioneer, your personality fits between venturers and those more in the center of the personality spectrum (“Centrics”). You share a number of characteristics in common with pure Venturers. You like to travel, especially to foreign destinations and you seek new experiences and new destinations for almost all trips you take. You are also physically active at home and on trips. But, unlike your pure Venturer friends, you don’t want to take such extreme vacations and are more likely to plan your trips-set an itinerary of places you want to visit and schedules when you will be there. You also have more company. About 17% of the population has a personality that matches yours, vs. only 4% for pure Venturers.</p>");
}


function showVoyagers(){
	$("#persona").append("<h2>You are a <b>Voyager</b></h2>");
	$("#persona").append("<p>By definition, you fit between Venturer and Traditional but with a leaning towards the Venturer side. Compared to other groups, you have lots of company. Three out of ten travelers (30%) place in your group, making you one of the largest segments of travelers. As a result, the majority of travel providers-airlines, resorts, rental car companies, tour operators, cruise lines, and others- place you at the top of their list of persons they want to reach and motivate to travel.</p>");

}

function showTraditionals(){
	$("#persona").append("<h2>You are a <b>Traditional</b></h2>");
	$("#persona").append("<p>If you examine the description of Venturers, you will find a personality quite the opposite of yours. You prefer a life that is more structured, stable and predictable. You would rather follow some set patterns or routines in your life so that you are more likely to know what will happen during each day and, therefore, can plan or prepare for it much better.</p>");

}




function getFareResults(persona){


	// sending GET request to get form values
	var url = "/airfaresearch.json?origin=" + $("#airportcodes").val() + 
				"&persona=" + persona;
	console.log(url)


	// calling for geoJSON
	$.get(url, function (data) {
		var geojsonFeature = JSON.parse(data);
		console.log(geojsonFeature);

		if (geojsonFeature.features.length === 0) {
			searchCampsites();
		} else {
			processFareResults(geojsonFeature);
		}
		window.location = "#linktomap";

	})
}



