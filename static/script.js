function addRows(){
	var table = document.getElementById('inTable');
	var rowCount = table.rows.length;
	var cellCount = table.rows[0].cells.length;
	var row = table.insertRow(rowCount);
	var cell = 'cell'+0;
	cell = row.insertCell(0);
	cell.innerHTML = rowCount;
	for(var i = 1; i < cellCount; i++){
		var cell = 'cell'+i;
		cell = row.insertCell(i);
		var copycel = document.getElementById('col'+i).innerHTML;
		cell.innerHTML=copycel;
	}
}


function deleteRows(){
	var table = document.getElementById('inTable');
	var rowCount = table.rows.length;
	if(rowCount > '2'){
		var row = table.deleteRow(rowCount-1);
		rowCount--;
	}
	else{
		alert('There should be atleast one row');
	}
}

function convert(valNum) {
	valNum = parseFloat(valNum);
	document.getElementById("watts").innerHTML= valNum * 746;
  }