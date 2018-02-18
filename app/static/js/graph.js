var svg = d3.select("svg"),
  width = +svg.attr("width"),
  height = +svg.attr("height");

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
  .force("link", d3.forceLink().id(function (d) { return d.userid; }))
  .force("charge", d3.forceManyBody())
  .force("center", d3.forceCenter(width / 2, height / 2));

(function (data) {

  var link = svg.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(data.links)
    .enter().append("line")
    .attr("stroke-width", function (d) { return Math.sqrt(d.distance); });

  var user = svg.append("g")
    .attr("class", "users")
    .selectAll("g")
    .data(data.users)
    .enter().append("g")

  var circles = user.append("circle")
    .attr("r", 5)
    .attr("fill", function (d) { return color(d.group); })
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended));

  var labels = user.append("text")
    .text(function (d) {
      return d.name;
    })
    .attr('x', 6)
    .attr('y', 3);

  user.append("title")
    .text(function (d) { return d.userid; });

  simulation
    .nodes(data.users)
    .on("tick", ticked);

  simulation.force("link")
    .links(data.links);

  function ticked() {
    link
      .attr("x1", function (d) { return d.source.x; })
      .attr("y1", function (d) { return d.source.y; })
      .attr("x2", function (d) { return d.target.x; })
      .attr("y2", function (d) { return d.target.y; });

    user
      .attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
      })
  }
}(data));

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
