function renderPersonalCollaborators(body, collaborators) {
    if (Object.keys(collaborators).length == 0) {
        return
    }
    body.append("div")
        .attr("class", "subheader")
        .style("color", colors.black)
        .html("Collaborators")
    body.append("div")
        .attr("class", "caption")
        .style("color", colors.black)
        .html("This is who I spent my time working with.")
    let div = body.append("div")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "center")
    let svg = div.append("svg")
        .attr("height", 500 / 14 * Object.keys(collaborators).length)
        .attr("width", 900)

    let height = svg.attr("height")
    let width = svg.attr("width")

    collaborators = Object.keys(collaborators).map(name => {
        return {
            name: name,
            amount: collaborators[name]
        }
    })
    collaborators.sort((a, b) => {
        return a.amount > b.amount ? -1 : 1
    })
    let circleRadius = 8
    let textX = 100

    let minCollab = d3.min(collaborators, d => {
        return d.amount
    }) - 1
    let maxCollab = d3.max(collaborators, d => {
        return d.amount
    }) + 1
    let nameXScale = d3.scaleLinear()
        .domain([minCollab, maxCollab])
        .range([textX + circleRadius + 16, width - textX])
    let collabYScale = d3.scaleBand()
        .domain(collaborators.map(d => {
            return d.name
        }))
        .range([48, height - 16])

    collaborators.forEach(d => {
        let name = d.name
        let amount = Number(d.amount)
        let g = svg.append("g")

        let nameText = g.append("text")
            .attr("class", "caption")
            .attr("fill", colors.black)
            .attr("text-anchor", "end")
            .attr("alignment-baseline", "middle")
            .attr("x", textX)
            .attr("y", collabYScale(name))
            .text(name)

        g.append("circle")
            .attr("cx", nameXScale(minCollab))
            .attr("cy", collabYScale(name))
            .attr("r", circleRadius)
            .attr("fill", colors.blue)

        let line = g.append("line")
            .attr("x1", nameXScale(minCollab))
            .attr("x2", nameXScale(amount))
            .attr("y1", collabYScale(name))
            .attr("y2", collabYScale(name))
            .attr("stroke", colors.blue)
            .attr("stroke-width", circleRadius / 2)

        g.append("circle")
            .attr("cx", nameXScale(amount))
            .attr("cy", collabYScale(name))
            .attr("r", circleRadius)
            .attr("fill", colors.blue)

        g.on("mouseover", function() {
                line.transition()
                    .duration(40)
                    .ease(d3.easeLinear)
                    .attr("stroke-width", circleRadius * 2)
                nameText.attr("fill", colors.blue)
                showText(amount, name)
            })
            .on("mouseout", function() {
                line.transition()
                    .duration(40)
                    .ease(d3.easeLinear)
                    .attr("stroke-width", circleRadius / 2)
                nameText.attr("fill", colors.black)
                hideText()
            })
    })

    let hoverText = svg.append("text")
        .attr("font-family", "Space Mono")
        .attr("font-size", 12)
        .attr("text-anchor", "start")
        .attr("alignment-baseline", "middle")
        .attr("fill", colors.blue)
        .attr("visibility", "hidden")

    function showText(amount, name) {
        hoverText.attr("visibility", "visible")
            .attr("x", Number(nameXScale(amount)) + Number(circleRadius) + 12)
            .attr("y", collabYScale(name))
            .text(amount + (amount != 1 ? " PRs" : " PR"))
    }

    function hideText() {
        hoverText.attr("visibility", "hidden")
    }
}