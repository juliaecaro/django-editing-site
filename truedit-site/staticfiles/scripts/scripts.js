// Last edited by: Fredster
// Last edited on: August 11, 2024

// The spinner on loading
document.addEventListener("DOMContentLoaded", function () {
	// Keep the loader visible, hiding the page initially
	document.body.classList.add("loading");
});

window.addEventListener("load", function () {
	// Using requestAnimationFrame to ensure everything is fully rendered
	requestAnimationFrame(function () {
		requestAnimationFrame(function () {
			document.body.classList.remove("loading");
			document.getElementById("loader").style.display = "none";
		});
	});

	// Fallback in case something is still slow to load
	setTimeout(function () {
		document.body.classList.remove("loading");
		document.getElementById("loader").style.display = "none";
	}, 200); // 200ms delay
});

// Re-show the loader when navigating to a new page
document.querySelectorAll("ul.sidebar-nav li a").forEach(function (link) {
	link.addEventListener("click", function () {
		document.getElementById("loader").style.display = "flex";
		document.body.classList.add("loading");
	});
});

// The videos and thumbnails buttons on the pricing page
let videos = document.getElementById("videos")
let thumbnails = document.getElementById("thumbnails")

function videoButton() {
	videos.style.display = "block";
	thumbnails.style.display = "none";

	// Disable the video button and enable the thumbnail button
	document.getElementById("video-button").classList.add("disabled");
	document.getElementById("video-button").disabled = true;

	document.getElementById("thumbnail-button").classList.remove("disabled");
	document.getElementById("thumbnail-button").disabled = false;
}

function thumbnailButton() {
	videos.style.display = "none";
	thumbnails.style.display = "block";

	// Disable the thumbnail button and enable the video button
	document.getElementById("thumbnail-button").classList.add("disabled");
	document.getElementById("thumbnail-button").disabled = true;

	document.getElementById("video-button").classList.remove("disabled");
	document.getElementById("video-button").disabled = false;
}

/* the prices page automatically starts with the video button already clicked upon page load */
document.addEventListener("DOMContentLoaded", function (event) {
	document.getElementById("video-button").click();
});

// Store the previous border style
let previousBorderStyle = "";

// To force focus-visible behavior in either portrait or landscape mode (on mobile)
document.getElementById("presentation-video").addEventListener("focus-visible", function () {
	if (!document.fullscreenElement) {
		this.style.border = "5px solid #E4008A";
	}
});

// To force or remove the transparent border when the home page video is fullscreen or not
// Store the current border style before fullscreen
function handleFullscreenChange() {
	if (document.fullscreenElement) {
		// Store the current border style before changing to fullscreen
		previousBorderStyle = video.style.border;
		// Remove border in fullscreen
		video.style.border = "none";
	} else {
		// Restore the border style after exiting fullscreen
		video.style.border = previousBorderStyle || "5px solid transparent";
	}
}

// Event listener for fullscreen changes
document.addEventListener("fullscreenchange", handleFullscreenChange);
document.addEventListener("webkitfullscreenchange", handleFullscreenChange);
document.addEventListener("mozfullscreenchange", handleFullscreenChange);
document.addEventListener("msfullscreenchange", handleFullscreenChange);