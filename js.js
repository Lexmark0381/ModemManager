var termText = "";
var modemState = "on";
var switchOnButton = document.getElementById("on");
var switchOffButton = document.getElementById("off");
var rebootButton = document.getElementById("reboot");
var timeout;
var host = document.location.href.split("http://")[1].split(":")[0]
if(host === "localhost"){
	print("Running in localhost")
	host = "127.0.0.1"
}
console.log(host)

changeFavicon = function(dir){
	document.head = document.head || document.getElementsByTagName('head')[0];
	var link = document.createElement('link'), oldLink = document.getElementById('favicon');
 	link.id = 'favicon';
 	link.rel = 'shortcut icon';
 	link.type = "image/png";
 	link.href = dir;
 	if (oldLink) {
  		document.head.removeChild(oldLink);
 	}
 	document.head.appendChild(link);
}


stateSetter = function(str){
	if((str === "on") || (str === "off") || (str === "reboot")){
	    var xmlHttp = new XMLHttpRequest();
	    var route = "http://" + host + ":8888/state&state=" + str
	    xmlHttp.open( "POST", route, true );
    	xmlHttp.send( null );

		modemState = str;

		if(str === "on"){
			changeFavicon("/img/greenn.png");
			return;
		}
		if(str === "off"){
			changeFavicon("/img/red.png")
			return;
		}
		if (str === "reboot"){
			changeFavicon("/img/grey.png")
			createCountdown(30);
			return;
		}
	}
}

createCountdown = function(count){
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
	document.getElementById("term").innerHTML = termText;
	objDiv.scrollTop = objDiv.scrollHeight;	

}

print = function(str){
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open( "POST", "http://" + host + ":8888/log&log=" + str, false ); // false for synchronous request
	xmlHttp.send();
	termText = termText + str;
	update();
}

println = function(str){
	var xmlHttp = new XMLHttpRequest();
	newline = str + "<br>";
	xmlHttp.open( "POST", "http://" + host + ":8888/log&log=" + newline, false ); // false for synchronous request
	xmlHttp.send( null );
	termText =  termText + newline	
	update();
}

printDate = function(){
	date = new Date().toLocaleString() + " ";
	print(date)
}

on = function(){
	printDate();
	if(modemState === "on"){
		println(" [INFO] Modem is on");
		return;
	} else {
		println(" [INFO] Powering on modem");
		stateSetter("on");
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
	}
}


boot = function(){
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "http://" + host + ":8888/log", false ); // false for synchronous request
	xmlHttp.send( null );
	termText = xmlHttp.responseText;
	document.getElementById("term").innerHTML = termText;
	document.getElementById("on").onclick = on;
	document.getElementById("off").onclick = off;
	document.getElementById("reboot").onclick = reboot;
	document.getElementById("ping").onclick = ping;
	update();
	// adapt();
	shortping();
}

adapt = function(){
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "http://" + host + ":8888/ping", false );
	xmlHttp.send( null );
	avgPing = parseInt(xmlHttp.responseText)
	if (avgPing >= 0){
		modemState = "on";
		stateSetter("on");
		on();
	} else {
		modemState = "off";
		stateSetter("off");
		off();
	}
}

shortping = function(){
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "http://" + host + ":8888/shortping", false );
	xmlHttp.send( null );
	avgPing = parseInt(xmlHttp.responseText)
	if (avgPing >= 0){
		modemState = "on";
		stateSetter("on");
		on();
	} else {
		modemState = "off";
		stateSetter("off");
		off();
	}
}

ping = function(){
		printDate();
		print(" [PING] ")
	    var xmlHttp = new XMLHttpRequest();
	    xmlHttp.open( "GET", "http://" + host + ":8888/ping", false );
    	xmlHttp.send( null );
    	avgPing = parseInt(xmlHttp.responseText)
    	if((avgPing > 1000) || (avgPing === -1)){
    		println(" Delay too high. Reboot may be needed.")
    	} else {
    		latency = avgPing + " ms"
    		println(latency);
    		stateSetter("on");
    	}
}

