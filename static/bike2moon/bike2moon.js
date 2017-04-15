var canvas, c;
var w, h;
var space, moon, earth, bike;

document.addEventListener("DOMContentLoaded", function() {
    space = document.getElementById("space");
    moon = document.getElementById("moon");
    earth = document.getElementById("earth");
    bike = document.getElementById("bike");

    canvas = document.getElementById("spaaaace");
    draw();
});

window.addEventListener("resize", draw);

function spaceClip() {
    let mh, imw, sx, sy;
    if(1886/1067 > w/h) { // clip image horizontally
        imh = 1067;
        imw = 1886*h / 1067;
        sx = (1886 - imw) / 2;
        sy = 0;
    } else { // clip image vertically
        imh = 1886*h/w;
        imw = 1886;
        sx = 0;
        sy = (1067 - imh) / 2;
    }

    return [sx, sy, imw, imh];
}

function draw() {
    console.log("draw!");
    w = 2*window.innerWidth;
    h = 2*window.innerHeight*0.7;
    canvas.width = w;
    canvas.height = h;
    canvas.style.width = w/2;
    canvas.style.height = h/2;
    c = canvas.getContext('2d');

    let clip = spaceClip();
    c.drawImage(space, clip[0], clip[1], clip[2], clip[3], 0, 0, w, h);

    c.strokeStyle = "#0F0";
    c.lineWidth = 8;
    c.beginPath();
    c.moveTo(0.15*w, 0.8*h);
    c.quadraticCurveTo(w, h, 0.75*w, 0.25*h);
    c.stroke();

    c.drawImage(moon, 0.75*w-w/12, 0.25*h-w/12, w/6, w/6);
    c.drawImage(earth, 0.15*w-w/12, 0.8*h-w/12, w/6, w/6);
    let r = bikePos(0.62);
    console.log(r);
    c.drawImage(bike, r[0]-w/12, r[1]-w/6, w/6, w/6);
    c.translate(0.5, 0.5);
}

function bikePos(t) {
    let x1 = 0.15*w;
    let y1 = 0.8*h;
    let x2 = w;
    let y2 = h;
    let x3 = 0.75*w;
    let y3 = 0.25*h;

    let x = 2*(1-t)*t*x2 + (1-t)*(1-t)*x1 + t*t*x3;
    let y = 2*(1-t)*t*y2 + (1-t)*(1-t)*y1 + t*t*y3;

    //let x = (x2 - (1-t)*(1-t)*x1 - t*t*x3) / (2*(1-t)*t);
    //let y = (y2 - (1-t)*(1-t)*y1 - t*t*y3) / (2*(1-t)*t);
    return [x,y];
}
