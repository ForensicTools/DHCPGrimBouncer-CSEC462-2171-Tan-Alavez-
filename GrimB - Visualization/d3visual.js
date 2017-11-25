
var width = 960,
height = 670;
 
d3.select("#bubbleChart").append("svg")
    .attr("width", width)
    .attr("height", height)
	.attr("id", "primarySVG");
 
 function promptFile(){
	 var filePrompt = prompt("Enter file: ", "")
	 var txt;
	 if(filePrompt == null || filePrompt == ""){
		 txt = "User cancelled the prompt."
	 }
	 /* else if(filePrompt[-4:-1] != ".csv"){
		 txt = "Incompatible file."
	 } */ 
	 document.getElementById("prompt")
 
 
 
 
 getFile(filePrompt);
 
	
function getFile(file){
	var exprt = filePrompt;
	if (file === filePrompt){
		var src = exprt;
	} 

 
var src = filePrompt; 
 
d3.csv(filePrompt, function(error, data) {

data.sort(function(a,b) {return b.ratingClassValue - a.ratingClassValue;});
 
 
var svg = d3.select("#primarySVG");
	
 
 
//set bubble padding
var padding = 4;
 
  for (var j = 0; j < data.length; j++) {
    data[j].radius = 10; 
    data[j].x = Math.random() * width;
    data[j].y = Math.random() * height;
  }
 
  var maxRadius = d3.max(_.pluck(data, 'radius'));
 
 
 
  var getCenters = function(vname, size) {
    var centers, map;
    centers = _.uniq(_.pluck(data,vname)).map(function(d) {
      return {
        name: d,
        value: 1
      };
    });
 
	map = d3.layout.pack().size(size);
          map.nodes({children: centers});
 
    return centers;
  };
 
	var nodes = svg.selectAll("circle")
		.data(data);
	
	nodes.enter().append("circle")
   
    .on("mouseover", function(d) {
      showPopover.call(this, d);
    })
    .on("mouseout", function(d) {
      removePopovers();
    })
	; 
 
 
  var force = d3.layout.force();
  
 
  draw('Security');
 
 $("label.ratingBtn").click(function() {
   	draw(this.id);
	});
  
  
 
 function draw(varname) {
 	d3.selectAll("circle").attr("r",10);
	var centers = getCenters(varname, [width, height]);
    force.on("tick", tick(centers, varname));
    labels(centers);
	nodes.attr("class", function(d) {
      return d[varname];
    });
    force.start();
	makeClickable();
  }
 
	
	function tick (centers, varname) {
	  var foci = {};
	  for (var i = 0; i < centers.length; i++) {
		foci[centers[i].name] = centers[i];
	  }
	  return function (e) {
		for (var i = 0; i < data.length; i++) {
		  var o = data[i];
		  var f = foci[o[varname]];
		  o.y += (f.y - o.y) * e.alpha;
		  o.x += (f.x - o.x) * e.alpha;
		 }
		 nodes.each(collide(.2))
		   .attr("cx", function (d) { return d.x; })
		   .attr("cy", function (d) { return d.y; });
	  }
	}
	
		
  function labels(centers) {
    svg.selectAll(".label").remove();
 
    svg.selectAll(".label")
      .data(centers).enter().append("text")
      .attr("class", "label")
      .text(function(d) {
        return d.name;
      })
	.attr("transform", function (d) {
            return "translate(" + (d.x - ((d.name.length)*3)) + ", " + (d.y + 15 - d.r) + ")";
          });     
 
 
  }
 
 // function to hide hover over box 
 
  function removePopovers() {
    $('.popover').each(function() {
      $(this).remove();
    });
  }
 
 
 
 // Hover information
 /////////////////////////////////
 
 
  function showPopover(d) {
    $(this).popover({
      placement: 'auto top',
      container: 'body',
      trigger: 'manual',
      html: true,
      content: function() {
        return ("URL: ").bold() + d.URL + ("</br>Times Visited: ").bold() + d.TimesVisited +
		("</br>Signature Algorithm: ").bold() + d.SigAlgo + ("</br>Issuer Country: ").bold() + d.IssuerC
		+ ("</br>Issuer Organization: ").bold() + d.IssuerO +
		("</br>Issuer OU: ").bold() + d.IssuerOU +
		("</br>Issuer CN: ").bold() + d.IssuerCN +
		("</br>Subject Country: ").bold() + d.SubjectC
		+ ("</br>Subject Organization: ").bold() + d.SubjectO +
		("</br>Subject OU: ").bold() + d.SubjectOU +
		("</br>Subject CN: ").bold() + d.SubjectCN +
		("</br>Issue Date: ").bold() + d.IssueDate +
		("</br>Expiration Date: ").bold() + d.ExpireDate +
		("</br>Security: ").bold() + d.Security;
	  
      }
	  
	});
	

        $(this).popover("show");
  
	
  }
  
  // Causes bubbles to group together
  
  function collide(alpha) {
    var quadtree = d3.geom.quadtree(data);
    return function(d) {
       var r = d.radius + maxRadius + padding,
        nx1 = d.x - r,
        nx2 = d.x + r,
        ny1 = d.y - r,
        ny2 = d.y + r;
      quadtree.visit(function(quad, x1, y1, x2, y2) {
        if (quad.point && (quad.point !== d)) {
          var x = d.x - quad.point.x,
            y = d.y - quad.point.y,
            l = Math.sqrt(x * x + y * y),
            r = d.radius + quad.point.radius + padding;
          if (l < r) {
            l = (l - r) / l * alpha;
            d.x -= x *= l;
            d.y -= y *= l;
            quad.point.x += x;
            quad.point.y += y;
          }
        }
        return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
      });
    };
  }
  
  
 
	function makeClickable () {
		
				
	$("circle").click(function() {
   	console.log(this.id);
	});
	
	var nest = d3.nest()
		.key(function(d){return d.objectName;})
		.entries(data);
		
	
	}
	nodes.exit().remove();
		
	
});
}}