console.log('imported')
var base_form_class = 'form-control'
function check_available(api_url){
	reset_result('custom_url',true)
	var custom = document.getElementById('custom_url');
	var long = document.getElementById('long_url');
	if (custom.value != ''){
		var xhttp = new XMLHttpRequest();	
		xhttp.onreadystatechange = function(){
			if (this.readyState == 4 && this.status == 200){
				console.log('response recived!')
				on_response(this.responseText)
			}
		}
		xhttp.open('POST', api_url, true);
		xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		var post_string = 'custom_url='+custom.value
		xhttp.send(post_string)
		console.log('sent request about :'+custom.value)
	}
	else{
		reset_result('custom_url',false)//if custom is empty, allow submit
	}
}

function on_response(response){ //while getting response from server about url availability.
	response = JSON.parse(response)
	console.log(response)
	custom = document.getElementById('custom_url')
	if (response['is_available'] == true){
		custom.className = base_form_class + ' is-valid'
		submit.disabled = false
	}
	else{
		custom.className = base_form_class + ' is-invalid'
		submit = document.getElementById('submit')
		submit.disabled = true
	}
}

function check_valid_url(){ //if the url is valid, enables custom_url input and submit. else disable submit and custom_url input, while showing feedback.
	console.log('checks if valid url')
	reset_result('long_url', false)
	var long = document.getElementById('long_url')
	var custom = document.getElementById('custom_url')
	if(long.value != ''){ 
		if (is_valid_url(long.value)){
			long.className = base_form_class + ' is-valid'
			submit.disabled = false
			custom = document.getElementById('custom_url')
			custom.disabled = false
			console.log('valid url')
		}
		else{
			reset_result('custom_url', true)
			custom.value = ''
			custom.disabled = true
			long.className = base_form_class + ' is-invalid'
			submit.disabled = true
			console.log('invalid url')
		}
	}
	else{
		reset_result('long_url', false)
		reset_result('custom_url', false)
		custom.value = ''
		custom.disabled = true
	}
}

function is_valid_url(url){// using regex, check if url is valid according to format.
   var pattern = new RegExp('^(https?:\/\/)'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.?)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ //port
    '(\\?[;&amp;a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i');
   return pattern.test(url)
}

function reset_result(id,disabled){ //resets the validity feedback of input and changes the state of submit button.
	console.log('submit disabled: '+ disabled)
	url_element = document.getElementById(id)
	url_element.className = base_form_class
	submit = document.getElementById('submit')
	submit.disabled = disabled
}