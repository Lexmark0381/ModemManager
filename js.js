var termText = "";
var modemState = "on";
var switchOnButton = document.getElementById("on");
var switchOffButton = document.getElementById("off");
var rebootButton = document.getElementById("reboot");
var timeout;
stateSetter = function(str){
	// console.log(modemState, str)
	if((str === "on") || (str === "off") || (str === "reboot")){
		// console.log("Editing state: " + str);
	    var xmlHttp = new XMLHttpRequest();
	    var route = "http://192.168.0.2:8888/state&state=" + str
	    // console.log(route)
	    xmlHttp.open( "POST", route, true ); // false for synchronous request
    	xmlHttp.send( null );
		modemState = str;
		if (str === "reboot"){
			createCountdown(30);
		}
	}
}

function createCountdown(count){
	// console.log(count)
    counter = count ? count : null;
    document.getElementById("reboot").innerHTML = "Reboot (" + counter + ")"
    if(count--){
        timeout  = setTimeout(function(){createCountdown(counter-1);}, 1000);
    } else {
		document.getElementById("reboot").innerHTML = "Reboot";
		stateSetter("on")

    }
}

update = function(){
	var objDiv = document.getElementById("term");
	// console.log(objDiv.scrollTop, objDiv.scrollHeight)
	document.getElementById("term").innerHTML = termText;
	objDiv.scrollTop = objDiv.scrollHeight;	

}

print = function(str){
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open( "POST", "http://192.168.0.2:8888/log&log=" + str, false ); // false for synchronous request
	xmlHttp.send( null );
	termText = termText + str;
	update();
}

println = function(str){
	var xmlHttp = new XMLHttpRequest();
	newline = str + "<br>";
	xmlHttp.open( "POST", "http://192.168.0.2:8888/log&log=" + newline, false ); // false for synchronous request
	xmlHttp.send( null );
	termText =  termText + newline	
	update();
}

printDate = function(){
	date = new Date().toLocaleString() + " ";
	print(date)
}

on = function(){
	if(modemState === "on"){
		printDate();
		println(" [INFO] Modem is on");
		return;
	} else {
		printDate();
		println(" [INFO] Powering on modem");
		stateSetter("on");
		on()
		document.getElementById("reboot").innerHTML = "Reboot";
		clearTimeout(timeout)

	}
	
}

off = function(){
	if(modemState === "off"){
		printDate();
		println(" [INFO] Modem is off");
		return;
	} else {
		printDate();
		println(" [INFO] Powering off modem");
		stateSetter("off");
		off()
		document.getElementById("reboot").innerHTML = "Reboot";
		clearTimeout(timeout)

	}
}

reboot = function(){
	if(modemState === "reboot"){
		printDate();
		println(" [INFO] Modem is rebooting");
		return;
	} else {
		printDate();
		println(" [INFO] Rebooting modem");
		stateSetter("reboot");
		reboot()
	}
}

boot = function(){
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "http://192.168.0.2:8888/log", false ); // false for synchronous request
	xmlHttp.send( null );
	termText = xmlHttp.responseText;
	document.getElementById("term").innerHTML = termText;
	document.getElementById("on").onclick = on;
	document.getElementById("off").onclick = off;
	document.getElementById("reboot").onclick = reboot;
	document.getElementById("ping").onclick = ping;
	update();
}

ping = function(){
		printDate();
		print(" [PING] ")
	    var xmlHttp = new XMLHttpRequest();
	    xmlHttp.open( "GET", "http://192.168.0.2:8888/ping", false ); // false for synchronous request
    	xmlHttp.send( null );
    	avgPing = parseInt(xmlHttp.responseText)
    	if((avgPing > 1000) || (avgPing === -1)){
    		// console.log(avgPing)
    		println(" Delay too high. Reboot may be needed.")
    	} else {
    		latency = avgPing + " ms"
    		println(latency);
    		stateSetter("on");
    	}
}


