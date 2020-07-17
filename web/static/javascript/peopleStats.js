function renderPeopleStats(body, data) {
    body.append("div")
        .attr("class", "subheader")
        .style("color", colors.black)
        .html("People")
    body.append("div")
        .attr("class", "caption")
        .style("color", colors.black)
        .html("Introducing Class 0.")
    let div = body.append("div")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "center")
        .style("width", "100%")
        .style("padding", "48px 0px 48px 0px")
    let svg = div.append("svg")
        .attr("height", 400)
        .attr("width", 1200)

    let height = svg.attr("height")
    let width = svg.attr("width")

    let highlights = [{
        title: data["num_members"],
        text: [
            "fellows, mentors, and staff"
        ],
        image:"../static/icons/fellows_mentors_staff.svg"
    }, {
        title: data["num_countries"],
        text: [
            "countries collaborated across"
        ],
        image: "../static/icons/countries_collaborated.svg"
    }, {
        title: data["num_timezone"],
        text: [
            "timezones bridged"
        ],
        image: "../static/icons/timezones_bridged.svg"
    }]

    let imageAttr = {
        height: 300,
        width: 300
    }

    let xScale = d3.scaleLinear()
        .domain([0, highlights.length - 1])
        .range([imageAttr.width / 2, width - 2 * imageAttr.width / 2])

    // fellows, countries, timezones.

    highlights.forEach((highlight, i) => {
        svg.append("image")
            .attr("href", highlight.image)
            .attr("height", imageAttr.height)
            .attr("width", imageAttr.width)
            .attr("x", xScale(i) - imageAttr.width / 2)
            .attr("y", 0)
        svg.append("text")
            .attr("class", "header")
            .attr("width", imageAttr.width)
            .attr("x", xScale(i))
            .attr("y", imageAttr.height + 12)
            .attr("fill", colors.black)
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle")
            .text(highlight.title)
        let textY = imageAttr.height + 48
        highlight.text.forEach(line => {
            svg.append("text")
                .attr("class", "caption")
                .attr("x", xScale(i))
                .attr("y", textY)
                .attr("fill", colors.black)
                .attr("text-anchor", "middle")
                .attr("alignment-baseline", "middle")
                .text(line)
            textY = textY + 20
        })
    })
}