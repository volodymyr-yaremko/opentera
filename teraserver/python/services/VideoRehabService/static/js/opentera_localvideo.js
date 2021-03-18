let videoSources = [];
let currentVideoSourceIndex = 0;
let timerHandle = 0;

function init_localview(){
	// Check source
	let urlParams = new URLSearchParams(window.location.search);
	let sourceParam = urlParams.get('source');
	if (sourceParam !== null){
		clientSource = sourceParam;
	}

	if (clientSource === 'openteraplus'){
		// Load QWebChannel library
		include("qrc:///qtwebchannel/qwebchannel.js");

		// Connect shared object
		connectSharedObject(initLocalVideo);

	}else{
		initLocalVideo();
	}
}

function initLocalVideo(){
	navigator.getUserMedia = navigator.mediaDevices.getUserMedia || navigator.getUserMedia ||
		navigator.webkitGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;

	if (navigator.getUserMedia) {
		//navigator.getUserMedia({video: true, audio: false}, handleVideo, videoError);
		navigator.mediaDevices.getUserMedia({video: {facingMode: "user" },
			audio: false}).then(initialHandleVideo).catch(videoError);
	}
}

function initialHandleVideo(stream){
	handleVideo(stream);

	fillVideoSourceList(stream.getVideoTracks()[0].label);

}

function handleVideo(stream) {
	let video = document.getElementById("selfVideo");

	//console.log("Success! Device Name: " + stream.getVideoTracks()[0].label);
	video.srcObject = stream;

}

function videoError(err) {
	// do something
	showError("videoError()",
		str_cant_access_media + ".<br><br>" + str_error_message + ":<br>" + err.name + " - " + err.message, true);
}


function fillVideoSourceList(selected_source=undefined){
	videoSources.length=0;
	let select = document.getElementById('videoSelect');
	select.options.length = 0;
	let count = 0;

	navigator.mediaDevices.enumerateDevices()
	.then(function(devices) {
		devices.forEach(function(device) {
			if (device.kind === "videoinput"){
				if (!device.label.includes(" IR ")) { // Filter "IR" camera, since they won't work.
					videoSources[videoSources.length] = device;
					//select.options[select.options.length] = new Option(device.label.substring(0,device.label.length-12), device.id);
					select.options[select.options.length] = new Option(device.label, device.id);
					count++;
					if (count < 2) {
						hideElement("videoSelect"); // Hide if only one video source
					} else {
						showElement("videoSelect");
					}
				}
			}
			//console.log(device.kind + ": " + device.label + " id = " + device.deviceId);
		});
		if (selected_source !== undefined){
			selectVideoSource(selected_source);
		}else{
			select.selectedIndex = currentVideoSourceIndex;
		}
	})
	.catch(function(err) {
		console.log(err.name + ": " + err.message);
	});
}

function updateVideoSource(){
	let select = document.getElementById('videoSelect');
	if (select.selectedIndex>=0){
		currentVideoSourceIndex = select.selectedIndex;
		let constraints = { deviceId: { exact: videoSources[currentVideoSourceIndex].deviceId } };
		//console.log(constraints);
		navigator.mediaDevices.getUserMedia({video: constraints}).then(handleVideo).catch(videoError);
	}
}

function selectVideoSource(source){
	console.log("Selecting " + source);
	for (let i=0; i<videoSources.length; i++){
		console.log(source + " = " + videoSources[i].label + " ?");
		if (videoSources[i].label.includes(source)){
			let select = document.getElementById('videoSelect');
			select.selectedIndex = i;
			currentVideoSourceIndex = i;
			//updateVideoSource();
			break;
		}
	}
}

function resetInactiveTimer(){

	stopInactiveTimer();

	timerHandle = setTimeout(inactiveTimeout, 3000);
}

function stopInactiveTimer(){
	if (timerHandle != 0){
		clearTimeout(timerHandle);
		timerHandle = 0;
	}
}

function inactiveTimeout(){
	closeButtons('navButtons');
}


function openButtons(id) {
	document.getElementById(id).style.height = "100%";
}

function closeButtons(id) {
	document.getElementById(id).style.height = "0%";
	stopInactiveTimer();
}

function toggleButtons(id) {
	if (isButtonsClosed(id))
		openButtons(id);
	else
		closeButtons(id);

}

function isButtonsClosed(id){
	return document.getElementById(id).style.height === "0%";
}

function setLocalMirror(mirror){
	let video_widget = $('#selfVideo');
	if (video_widget !== undefined){
		(mirror === true) ? video_widget.addClass('videoMirror') : video_widget.removeClass('videoMirror');
	}
}