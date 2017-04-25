var termText = "";
var modemState = null;
update = function(){
	var objDiv = document.getElementById("term");
	// console.log(objDiv.scrollTop, objDiv.scrollHeight)
	document.getElementById("term").innerHTML = termText;
	objDiv.scrollTop = objDiv.scrollHeight;	

}

print = function(str){
	date = new Date().toLocaleString();
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open( "POST", "http://localhost:8888/log&log=" + str, false ); // false for synchronous request
	xmlHttp.send( null );

	termText = termText + str;
	update();
}

println = function(str){
	date = new Date().toLocaleString();
	var xmlHttp = new XMLHttpRequest();
	newline = date + " " + str + "<br>";
	xmlHttp.open( "POST", "http://localhost:8888/log&log=" + newline, false ); // false for synchronous request
	xmlHttp.send( null );
	termText =  termText + newline	
	update();
}

on = function(){
	if(modemState === "on"){
		println("[INFO] Modem is on");
		return;
	} else {
		println("[INFO] Powering on modem");
		stateSetter("on");
		
	}
	
}

off = function(){
	if(modemState === "off"){
		println("[INFO] Modem is off");
		return;
	} else {
		println("[INFO] Powering off modem");
		stateSetter("off");
		
	}
}

reboot = function(){
	if(modemState === "reboot"){
		println("[INFO] Modem is rebooting");
		return;
	} else {
		println("[INFO] Rebooting modem");
		stateSetter("reboot");
	}
}

boot = function(){
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "http://localhost:8888/log", false ); // false for synchronous request
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
		date = new Date().toLocaleString();

		print(date + " [PING] ")
	    var xmlHttp = new XMLHttpRequest();
	    xmlHttp.open( "GET", "http://localhost:8888/ping", false ); // false for synchronous request
    	xmlHttp.send( null );
    	if((xmlHttp.responseText > 1000) || (xmlHttp.responseText === -1)){
    		println("[ERR] Delay too high. Reboot may be needed.")
    	} else {
    		latency = xmlHttp.responseText + "ms"
    		println(latency);
    	}
}

stateSetter = function(str){
	if((str !== "on") || (str !== "off") || ((str !== "reboot"))){
		return;
	} else {
		modemState = str;
	}
}
