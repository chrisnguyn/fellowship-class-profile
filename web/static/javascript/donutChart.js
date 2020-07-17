function renderDonutChart(body, section) {
    body.append("div")
        .attr("class", "subheader")
        .style("color", colors.black)
        .html(section.title)
    let div = body.append("div")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "center")
    let svg = div.append("svg")
        .attr("height", 200)
        .attr("width", 700)

    let height = svg.attr("height")
    let width = svg.attr("width")

    let donutAttr = {
        outerRadius: height / 2 - 4,
        innerRadius: height / 2 - 54
    }
    let horizontalPadding = 40
    let verticalPadding = 20

    svg.append("text")
        .attr("class", "header")
        .attr("x", width / 2 - donutAttr.outerRadius - horizontalPadding)
        .attr("y", height / 2 - verticalPadding / 2)
        .attr("fill", colors.black)
        .attr("text-anchor", "end")
        .attr("alignment-baseline", "bottom")
        .text(section.total)
    svg.append("text")
        .attr("class", "caption")
        .attr("x", width / 2 - donutAttr.outerRadius - horizontalPadding)
        .attr("y", height / 2 + verticalPadding / 2)
        .attr("fill", colors.black)
        .attr("text-anchor", "end")
        .attr("alignment-baseline", "hanging")
        .text(section.subtitle)


    renderDonutChartDonut(svg, section, donutAttr)
    renderDonutChartLegend(svg, section, donutAttr, horizontalPadding)
}

function renderDonutChartDonut(svg, section, donutAttr) {
    let height = svg.attr("height")
    let width = svg.attr("width")

    svg.append("path")
        .datum({
            endAngle: 2 * Math.PI
        })
        .attr("d", d3.arc()
            .innerRadius(donutAttr.innerRadius - 4)
            .outerRadius(donutAttr.outerRadius + 4)
            .startAngle(0))
        .attr("fill", colors.grey)
        .attr("transform", "translate(" + (width / 2) + "," + (height / 2) + ")")

    let startAngle = 0
    section.list.forEach((d, i) => {
        // Draw donut slice.
        svg.append("path")
            .datum({
                endAngle: startAngle + d.percent * 2 * Math.PI
            })
            .attr("d", d3.arc()
                .innerRadius(donutAttr.innerRadius)
                .outerRadius(donutAttr.outerRadius)
                .startAngle(startAngle))
            .attr("fill", d.color)
            .attr("transform", "translate(" + (width / 2) + "," + (height / 2) + ")")

        // Set new start angle for next slice.
        startAngle = startAngle + d.percent * 2 * Math.PI
    })
}

function renderDonutChartLegend(svg, section, donutAttr, horizontalPadding) {
    let height = svg.attr("height")
    let width = svg.attr("width")

    let legendAttr = {
        lineX: width / 2 + donutAttr.outerRadius + horizontalPadding + 48,
        horizontalPadding: 12,
        verticalPadding: 8,
        squareSize: 12,
        yScale: d3.scaleLinear()
            .domain([0, section.list.length - 1])
            .range([24, height - 24])
    }

    svg.append("line")
        .attr("x1", legendAttr.lineX)
        .attr("x2", legendAttr.lineX)
        .attr("y1", 0)
        .attr("y2", height)
        .attr("stroke", colors.grey)
        .attr("stroke-width", 2)

    section.list.forEach((d, i) => {
        svg.append("text")
            .attr("class", "caption")
            .attr("x", legendAttr.lineX - legendAttr.horizontalPadding)
            .attr("y", legendAttr.yScale(i))
            .attr("fill", colors.black)
            .attr("text-anchor", "end")
            .attr("alignment-baseline", "middle")
            .text(Math.round(d.percent * 1000) / 10 + "%")
        svg.append("rect")
            .attr("height", legendAttr.squareSize)
            .attr("width", legendAttr.squareSize)
            .attr("x", legendAttr.lineX - legendAttr.squareSize / 2)
            .attr("y", legendAttr.yScale(i) - legendAttr.squareSize / 2)
            .attr("fill", d.color)
        svg.append("text")
            .attr("class", "caption")
            .attr("x", legendAttr.lineX + legendAttr.horizontalPadding)
            .attr("y", legendAttr.yScale(i))
            .attr("fill", colors.black)
            .attr("text-anchor", "start")
            .attr("alignment-baseline", "middle")
            .text(d.name)
    })
}