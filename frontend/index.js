//var detached = $('#link_page_body').detach();
//$('body').append(detached);


function go_to_upload_page() {
	document.getElementById("upload_menu_button").classList.add("active_main_menu_button");
	document.getElementById("link_menu_button").classList.remove("active_main_menu_button");
	document.getElementById("record_menu_button").classList.remove("active_main_menu_button");

	document.getElementById("upload_page_body").style.display = "flex"
	document.getElementById("link_page_body").style.display = "none"
	//document.getElementById("link_page_body").style.display = "none"
}
function go_to_link_page() {
	document.getElementById("upload_menu_button").classList.remove("active_main_menu_button");
	document.getElementById("link_menu_button").classList.add("active_main_menu_button");
	document.getElementById("record_menu_button").classList.remove("active_main_menu_button");

	document.getElementById("upload_page_body").style.display = "none"
	document.getElementById("link_page_body").style.display = "flex"
	//document.getElementById("link_page_body").style.display = "none"
}
function go_to_record_page() {
	document.getElementById("upload_menu_button").classList.remove("active_main_menu_button");
	document.getElementById("link_menu_button").classList.remove("active_main_menu_button");
	document.getElementById("record_menu_button").classList.add("active_main_menu_button");

	document.getElementById("upload_page_body").style.display = "none"
	document.getElementById("link_page_body").style.display = "none"
	//document.getElementById("link_page_body").style.display = "flex"
}
