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



