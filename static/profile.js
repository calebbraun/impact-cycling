function init() 
{
    var dataString = document.getElementById("myVar").value;
    
    var userData = JSON.parse(dataString);
    console.log(userData);
        
    document.getElementById('welcome').innerHTML = "Welcome, " + userData[0] + "!";
    document.getElementById('subwelcome').innerHTML = "Check below to see how many miles you've biked, how much money you've saved, and how much you've reduced your CO2 emissions.";
    
    document.getElementById('milescaption').innerHTML = "You have biked a total of " + "X" + " miles.";
    document.getElementById('moneycaption').innerHTML = "You have saved a total of " + "X" + " dollars.";
    document.getElementById('co2caption').innerHTML = "You have reduced your CO2 emissions by " + "X" + " grams.";
    
}
