var termText = "";
var modemState = null;
update = function(){
	var objDiv = document.getElementById("term");
	// console.log(objDiv.scrollTop, objDiv.scrollHeight)
	document.getElementById("term").innerHTML = termText;
	objDiv.scrollTop = objDiv.scrollHeight;	

}

print = function(str){
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open( "POST", "http://raspberrypi:8888/log&log=" + str, false ); // false for synchronous request
	xmlHttp.send( null );
	termText = termText + str;
	update();
}

println = function(str){
	var xmlHttp = new XMLHttpRequest();
	newline = str + "<br>";
	xmlHttp.open( "POST", "http://raspberrypi:8888/log&log=" + newline, false ); // false for synchronous request
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
	}
}

boot = function(){
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "http://raspberrypi:8888/log", false ); // false for synchronous request
	xmlHttp.send( null );
	termText = xmlHttp.responseText;
	document.getElementById("term").innerHTML = termText;
	document.getElementById("on").onclick = on;
	document.getElementById("off").onclick = off;
	document.getElementById("reboot").onclick = reboot;
	document.getElementById("ping").onclick = ping;
	if(modemState === null){
		// Check modem online
		ping()
	}
	update();
}

ping = function(){
		printDate();
		print(" [PING] ")
	    var xmlHttp = new XMLHttpRequest();
	    xmlHttp.open( "GET", "http://raspberrypi:8888/ping", false ); // false for synchronous request
    	xmlHttp.send( null );
    	avgPing = parseInt(xmlHttp.responseText)
    	if((avgPing > 1000) || (avgPing === -1)){
    		console.log(avgPing)
    		println(" Delay too high. Reboot may be needed.")
    	} else {
    		latency = avgPing + " ms"
    		println(latency);
    		stateSetter("on");
    	}
}

stateSetter = function(str){
	if((str !== "on") || (str !== "off") || ((str !== "reboot"))){
		return;
	} else {
	    var xmlHttp = new XMLHttpRequest();
	    xmlHttp.open( "POST", "http://raspberrypi:8888/state&state=" + str, true ); // false for synchronous request
    	xmlHttp.send( null );
		modemState = str;
	}
}
