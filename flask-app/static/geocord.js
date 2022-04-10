function fillPosition(position_event) {
	var lat_input = document.getElementById("lat-input");
	var lon_input = document.getElementById("lon-input");

	lat_input.value = position_event.coords.latitude;
	lon_input.value = position_event.coords.latitude;
}

function checkLocation() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(fillPosition);
	}	
	else {
		console.log("Unable to grab geolocation.");
	}
}

window.onload = checkLocation;
