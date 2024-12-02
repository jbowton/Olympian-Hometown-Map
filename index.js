const tooltip = d3.select("#tooltip");


// Define dimensions for the SVG
const width = 1500, height = 1000;

// Select the SVG element
const svg = d3.select("svg")
    .attr("width", width)
    .attr("height", height);

// Load the GeoJSON or TopoJSON data from a local file
d3.json("https://unpkg.com/us-atlas@3/counties-10m.json").then(us => {
    // Create GeoJSON features using the topojson object
    const counties = topojson.mesh(us, us.objects.counties, (a, b) => a !== b);
    const states = topojson.mesh(us, us.objects.states, (a, b) => a !== b);
    const nation = topojson.feature(us, us.objects.nation);

    const projection = d3.geoAlbersUsa()
        .translate([width / 2, height / 2])  // Center the map
        .scale(1500);  // Adjust scale for zoom level

    const path = d3.geoPath().projection(projection);

    // Draw counties
    svg.append("path")
        .datum(counties)
        .attr("fill", "none")
        .attr("stroke", "#aaa")
        .attr("stroke-width", 0.5)
        .attr("d", path);

    // Draw state borders
    svg.append("path")
        .datum(states)
        .attr("fill", "none")
        .attr("stroke", "#000")
        .attr("stroke-width", 0.5)
        .attr("d", path);

    // Draw national border
    svg.append("path")
        .datum(nation)
        .attr("fill", "none")
        .attr("stroke", "#000")
        .attr("stroke-width", 1)
        .attr("d", path);

    // Zoom functionality
    const zoom = d3.zoom()
          .scaleExtent([1, 8])
          .on("zoom", zoomed);

      svg.call(zoom);

      let currentZoom = d3.zoomIdentity;

      // Define zoomed function that updates the map position and scale
      function zoomed(event) {
          currentZoom = event.transform
          svg.selectAll("path")
              .attr("transform", currentZoom);

          // Apply transformation to circles (data points)
          svg.selectAll("circle")
              .attr("transform", currentZoom)
              .attr("r", 3 / currentZoom.k);  // Scale circle size based on zoom level
      }

      d3.csv("./combined_athletes_data.csv").then(data => {
          // Get unique years from data
          const years = [...new Set(data.map(d => d.Year))].sort();
          const sports = [...new Set(data.map(d => d.Sport))].sort();

          const yearSelect = d3.select("#yearSelect");
          yearSelect.selectAll("option").remove();
          yearSelect.append("option")
                  .text("All Years")
                  .attr("value", "all");

          // Populate dropdown
          yearSelect.selectAll("option.year")
              .data(years)
              .enter()
              .append("option")
              .attr("class", "year")
              .text(d => d)
              .attr("value", d => d);

          // Populate sports dropdown
          const sportSelect = d3.select("#sportSelect");
          sportSelect.selectAll("option").remove();
          sportSelect.append("option")
                  .text("All Sports")
                  .attr("value", "all");

          sportSelect.selectAll("option.sport")
              .data(sports)
              .enter()
              .append("option")
              .attr("class", "sport")
              .text(d => d)
              .attr("value", d => d);

          // Function to update circles
          function updateMap(selectedYear, selectedSport) {
              const validData = data.filter(d => {
                  const hasCoords = d.latitude && d.longitude && !isNaN(d.latitude) && !isNaN(d.longitude);
                  const yearMatch = selectedYear === "all" ? true : d.Year === selectedYear;
                  const sportMatch = selectedSport === "all" ? true : d.Sport === selectedSport;
                  return hasCoords && yearMatch && sportMatch;
              });

              // Update circles
              const circles = svg.selectAll("circle")
                  .data(validData);

              // Remove old circles
              circles.exit().remove();

              // Add new circles
              circles.enter()
                  .append("circle")
                  .merge(circles)
                  .attr("cx", d => {
                      // Group data points by location
                      const sameLocation = validData.filter(point =>
                          point.latitude === d.latitude &&
                          point.longitude === d.longitude
                      );
                      const index = sameLocation.indexOf(d);
                      const total = sameLocation.length;

                      // If multiple points exist, create a circle pattern
                      if (total > 1) {
                          const angle = (2 * Math.PI * index) / total;
                          const radius = 1.5; // Radius of the circle pattern
                          const baseX = projection([+d.longitude, +d.latitude])[0];
                          return baseX + (radius * Math.cos(angle));
                      }

                      return projection([+d.longitude, +d.latitude])[0];
                  })
                  .attr("cy", d => {
                      // Group data points by location
                      const sameLocation = validData.filter(point =>
                          point.latitude === d.latitude &&
                          point.longitude === d.longitude
                      );
                      const index = sameLocation.indexOf(d);
                      const total = sameLocation.length;

                      // If multiple points exist, create a circle pattern
                      if (total > 1) {
                          const angle = (2 * Math.PI * index) / total;
                          const radius = 1.5; // Radius of the circle pattern
                          const baseY = projection([+d.longitude, +d.latitude])[1];
                          return baseY + (radius * Math.sin(angle));
                      }

                      return projection([+d.longitude, +d.latitude])[1];
                  })
                  .attr("r", 3/currentZoom.k)
                  .attr("fill", "red")
                  .attr("transform", currentZoom)
                  .on("mouseover", function(event, d) {
                      d3.select("#tooltip")
                          .html(`<strong>${d["First Name"]} ${d["Last Name"]}</strong><br>Sport: ${d.Sport}<br>City: ${d.Hometown}, ${d.state_id}`)
                          .style("left", (event.pageX + 10) + "px")
                          .style("top", (event.pageY + 10) + "px")
                          .classed("visible", true);
                  })
                  .on("mousemove", function(event) {
                      d3.select("#tooltip")
                          .style("left", (event.pageX + 10) + "px")
                          .style("top", (event.pageY + 10) + "px");
                  })
                  .on("mouseout", function() {
                      d3.select("#tooltip").classed("visible", false);
                  });
          }

          // Event listener on dropdown
          yearSelect.on("change", function() {
              updateMap(this.value, sportSelect.property("value"));
          });
          sportSelect.on("change", function() {
              updateMap(yearSelect.property("value"), this.value);
          });

          // Initial map render
          updateMap("all", "all");
      });
}).catch(error => {
    console.error("Error loading or parsing data:", error);
});
