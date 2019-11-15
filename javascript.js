function following() {
  document.getElementById('setFollow').innerHTML="Following PixelPlanets";
 }

var addButton = document.querySelector("#add");
var editButton = document.querySelector("#edit");
var addUser = document.querySelector("#addUser");
var checkUser = document.querySelector("#checkUser");
//var deleteButton = document.querySelector("#delete");

var message = document.getElementById("newMessage");


var signUpForm = document.getElementById("signUpForm");
				signUpForm.onclick = function () {
					var signUpFormView = document.getElementById("hidden-1");
					var signInFormView = document.getElementById("display-1");
						signUpFormView.style.display="block";
					signInFormView.style.display="none";
				};


function showData() {
	fetch('http://localhost:8080/posts', {credentials: "include"}).then
	(function(response){
		console.log(response)
		if (response.status == 401 || response.status == 422){
			document.getElementById('modalOverlay').style.display = "block";
		}
		else if (response.status == 200){
			document.getElementById('modalOverlay').style.display = "none";
			console.log("ModalOverlayHidden")
		response.json().then(function(data){
			//newShow(data);
			message.innerHTML ="";
			data.forEach(function(element){
				
				var feed = document.createElement("li");

				var titleName = document.createElement("h5");
				titleName.innerHTML = element.name
				feed.appendChild(titleName);
				titleName.style.paddingLeft ="50px";

				var titlepTitle = document.createElement("p");
				titlepTitle.innerHTML = element.pTitle
				feed.appendChild(titlepTitle);
				titlepTitle.style.fontSize ="12px";
				titlepTitle.style.color ="black";
				titlepTitle.style.paddingLeft ="10px";
				titlepTitle.style.float ="Left";
			


				var titleDate = document.createElement("p");
				titleDate.innerHTML = element.date
				feed.appendChild(titleDate);
				titleDate.style.fontSize ="12px";
				titleDate.style.color ="gray";
				titleDate.style.paddingLeft ="20px";
				titleDate.style.float ="Left";
				

				var titleLocation = document.createElement("p");
				titleLocation.innerHTML = element.location
				feed.appendChild(titleLocation);
				titleLocation.style.fontSize ="12px";
				titleLocation.style.color ="gray";
				titleLocation.style.paddingTop ="12px";
				titleLocation.style.paddingLeft ="220px";
				titleDate.style.float ="Left";
				

				var titlepBody = document.createElement("p");
				titlepBody.innerHTML = element.pBody
				feed.appendChild(titlepBody);
				titlepBody.style.clear ="both";
				titlepBody.style.paddingLeft ="10px";

				var deleteButton = document.createElement("button");
				deleteButton.innerHTML = "delete";
				deleteButton.onclick = function () {
					//alert("Are you sure you want to delete this?");
					if (confirm("Are you sure you want to delete this?")){
						deleteEvent(element.id);
						console.log("Delete Clicked:", feed.id);
					}
					//deleteRestaurant(restaurant.id);
					//send an alert;
				};
				var editButton = document.createElement("button");

				editButton.innerHTML = "edit";
				editButton.onclick = function () {
					var editForm = document.getElementById("hidden");
					editForm.style.display="block";
					var editSubmit = document.getElementById("submitEditButton");
					console.log(element);
					var editedName = document.getElementById("name-edit");
					var editedDate = document.getElementById("date-edit");
					var editedLocation = document.getElementById("location-edit");
					var editedpTitle = document.getElementById("pTitle-edit");
					var editedpBody = document.getElementById("pBody-edit");
					editedName.value = element["name"];
					editedDate.value = element["date"];
					editedLocation.value = element["location"];
					editedpTitle.value = element["pTitle"];
					editedpBody.value = element["pBody"];
					console.log("Edited", feed.id);
					//deleteRestaurant(restaurant.id);
					//send an alert;

					submitEditButton.onclick = function () {
						editEvent(element.id, editedName.value, editedDate.value, editedLocation.value, editedpTitle.value, editedpBody.value);
					}

				};


				feed.appendChild(deleteButton);
				feed.appendChild(editButton);

				message.appendChild(feed);

				//var message2 = document.createElement("p");
				//message2.innerHTML= element["name"] + element["date"]
				//+ element["location"] + element["pTitle"]+ element["pBody"];
				/*console.log (element["name"]);*/
				//console.log (element["name"]);
				//message.appendChild(message2);
			});
		});
	}});

};

showData();

var deleteEvent = function (id){
	console.log (id);
	fetch(`http://localhost:8080/posts/${id}`, {
		method:"DELETE",
		credentials: "include"
	}).then(function(response){
		console.log("Event Deleted");
		showData();
	})
};

var editEvent = function (id, name, date, location, pTitle, pBody){
	console.log (id);
	var bodyStr ="name=" + encodeURI(name);
	bodyStr += "&date=" + encodeURI(date);
	bodyStr += "&location=" + encodeURI(location);
	bodyStr += "&pTitle=" + encodeURI(pTitle);
	bodyStr += "&pBody=" + encodeURI(pBody);
	fetch(`http://localhost:8080/posts/${id}`, {
		body: bodyStr,
		method:"PUT",
		credentials: "include",
		headers: {
			"Content-Type":"application/x-www-form-urlencoded"
		}
	}).then(function(response){
		console.log("Event Updated");
		showData();
		var editForm = document.getElementById("hidden");
		editForm.style.display="none";

	})
};

addButton.onclick = function () {
	var addedName = document.getElementById("name").value;
	var addedDate = document.getElementById("date").value;
	var addedLocation = document.getElementById("location").value;
	var addedpTitle = document.getElementById("pTitle").value;
	var addedpBody = document.getElementById("pBody").value;

	var bodyStr ="name=" + encodeURI(addedName);
	bodyStr += "&date=" + encodeURI(addedDate);
	bodyStr += "&location=" + encodeURI(addedLocation);
	bodyStr += "&pTitle=" + encodeURI(addedpTitle);
	bodyStr += "&pBody=" + encodeURI(addedpBody);

	document.getElementById('name').value='';
	document.getElementById('date').value='';
	document.getElementById('location').value='';
	document.getElementById('pTitle').value='';
	document.getElementById('pBody').value='';

	

	
	fetch("http://localhost:8080/posts", {
		//request response
		method: "POST",
		credentials: "include",
		body: bodyStr,
		headers: {
			"Content-Type":"application/x-www-form-urlencoded"
		}

	}).then(function(response){
		console.log("Server responded!");
		showData();
	});
};

addUser.onclick = function () {
	var addedf_name = document.getElementById("f_name").value;
	var addedl_name = document.getElementById("l_name").value;
	var addedEmail = document.getElementById("email").value;
	var addedPassword = document.getElementById("password").value;

	var bodyStr ="f_name=" + encodeURI(addedf_name);
	bodyStr += "&l_name=" + encodeURI(addedl_name);
	bodyStr += "&email=" + encodeURI(addedEmail);
	bodyStr += "&password=" + encodeURI(addedPassword);

	document.getElementById('f_name').value='';
	document.getElementById('l_name').value='';
	document.getElementById('email').value='';
	document.getElementById('password').value='';

	
	
	fetch("http://localhost:8080/newUsers", {
		//request response
		method: "POST",
		credentials: "include",
		body: bodyStr,
		headers: {
			"Content-Type":"application/x-www-form-urlencoded"
		}

	}).then(function(response){
		console.log("Server responded!");
		//document.getElementById('modalOverlay').style.display = 'block'
		//showData();
		if (response.status == 201) {
			document.getElementById('modalOverlay').style.display = 'none'
			// success
			showData();
		} else if (response.status == 422) {
			alert("That email has been taken, please type in another one.")
		}
	});
	
};
checkUser.onclick = function () {
	var loginEmail = document.getElementById("loginEmail").value;
	var loginPassword = document.getElementById("loginPassword").value;

	var bodyStr = "email=" + encodeURI(loginEmail);
	bodyStr += "&hashed=" + encodeURI(loginPassword);

	document.getElementById('loginEmail').value='';
	document.getElementById('loginPassword').value='';

	
	fetch("http://localhost:8080/sessions", {
		//request response
		method: "POST",
		credentials: "include",
		body: bodyStr,
		headers: {
			"Content-Type":"application/x-www-form-urlencoded"
		}

	}).then(function(response){
		console.log("Server responded!");
		if (response.status == 201){
			document.getElementById('modalOverlay').style.display = 'none'
			showData();
		}
		else{
			//document.getElementById("errorMessage").innerHTML = "Invalid Username or Password. Please try again.";
			alert ("Invalid Username or Password. Please try again.")
			
		}
	});
};