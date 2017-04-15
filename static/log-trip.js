function initAutocomplete()
{
    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('start_input')),
        {types: ['geocode']});
    
    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('end_input')),
        {types: ['geocode']});
}

function getInputs()
{   
    var startAddress = document.getElementById("start_input").value;
    
    var endAddress = document.getElementById("end_input").value;
    
    var url = 'tripdata/';
    
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);
    
    xmlHttpRequest.onreadystatechange = function()
    {
        if (xmlHttpRequest.readyState == 4 && xmlHttpRequest == 200)
            {
                getInputsCallback(xmlHttpRequest.responseText);
            }
    };
    xmlHttpRequest.send();
    
    return inputs;
}
