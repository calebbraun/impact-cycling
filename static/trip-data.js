function init() 
{
    var pointsString = document.getElementById("myVar").value;
    
    var points = JSON.parse(pointsString);
    console.log(points);
        
    document.getElementById('pointsinfo').innerHTML = points[0] + "<br />";
    document.getElementById('pointsinfo').innerHTML += points[1] + "<br />";
    document.getElementById('pointsinfo').innerHTML += points[2] + "<br />";
    document.getElementById('pointsinfo').innerHTML += points[3] + " grams of co2 saved!";
    
    
}
