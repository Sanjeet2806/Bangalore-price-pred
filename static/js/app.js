//returns the no of bathrooms clicked by user
function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for(var i in uiBathrooms) {
      if(uiBathrooms[i].checked) {
          return parseInt(i)+1;   //returns the index+1 of clicked radio button index
      }
    }
    return -1; // Invalid Value
  }
  
  //returns the BHK value clicked by user
  function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for(var i in uiBHK) {
      if(uiBHK[i].checked) {
          return parseInt(i)+1; //returns the index+1 of clicked bhk button index
      }
    }
    return -1; // Invalid Value
  }
  
  //function to estiate price and display it
  function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    //getting the user entered values
    var sqft = document.getElementById("uiSqft");
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var location = document.getElementById("uiLocations");
    var estPrice = document.getElementById("uiEstimatedPrice");
  
    var url = "http://127.0.0.1:5000/predict_home_price"; //posting to server endpoint which will estimate the price for us
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
    //var url = "http://"
  
    $.post(url, {  
        total_sqft: parseFloat(sqft.value),  //sending user inputs to server in  form-data format
        bhk: bhk,
        bath: bathrooms,
        location: location.value
    },function(data, status) {        //on getting the estimated price as response from server displaying it on client side
        console.log(data.estimated_price);
        estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
        console.log(status);
    });
  }
  
  function onPageLoad() {
    console.log( "document loaded" );
    var url = "http://127.0.0.1:5000/get_location_names"; //fetching the location data from server endpoint which supplies us with the location names on requesting it
    // var url = "/api/get_location_names"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
    $.get(url,function(data, status) {
        console.log("got response for get_location_names request");
        if(data) {
            var locations = data.locations; //locations are stored in locations attribute of the object and storing to a list
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            // appending to the dropdown element for each element in the locations list
            for(var i in locations) {
                var opt = new Option(locations[i]);
                $('#uiLocations').append(opt);
            }
        }
    });
  }
  
  window.onload = onPageLoad; //fetching the location names from server on page load