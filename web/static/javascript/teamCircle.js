function renderTeamCircle(body, teamData, pod, username) {
    body.append("div")
        .attr("class", "subheader")
        .style("color", colors.black)
        .html("Team")
    body.append("div")
        .attr("class", "caption")
        .style("color", colors.black)
        .html("Here is who I collaborated with as part of " + pod + ".")
    let div = body.append("div")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "center")
    let svg = div.append("svg")
        .attr("height", 500)
        .attr("width", 900)

    let height = svg.attr("height")
    let width = svg.attr("width")

    let team = teamData[pod]

    let angleScale = d3.scaleLinear()
        .domain([0, team.length])
        .range([0, 2 * Math.PI])

    let radius = {
        pod: pod.length * 4 + 4,
        memberRing: Math.min(height, width) - 400,
        member: 10
    }

    svg.append("circle")
        .attr("cx", width / 2)
        .attr("cy", height / 2)
        .attr("r", radius.pod)
        .attr("fill", colors.grey)
    svg.append("circle")
        .attr("cx", width / 2)
        .attr("cy", height / 2)
        .attr("r", radius.pod + 4)
        .attr("fill", "none")
        .attr("stroke", colors.grey)
        .attr("stroke-width", 2)
    svg.append("circle")
        .attr("cx", width / 2)
        .attr("cy", height / 2)
        .attr("r", radius.memberRing)
        .attr("fill", "none")
        .attr("stroke", colors.grey)
        .attr("stroke-width", 2)
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", height / 2)
        .attr("font-family", "Space Mono")
        .attr("font-size", 12)
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .attr("fill", colors.black)
        .text(pod)

    team.forEach((member, i) => {
        let angle = angleScale(i)
        let x = width / 2 + radius.memberRing * Math.cos(angle)
        let y = height / 2 + radius.memberRing * Math.sin(angle)
        svg.append("circle")
            .attr("cx", x)
            .attr("cy", y)
            .attr("r", radius.member)
            .attr("fill", colors.grey)
        x += (radius.member + 12) * Math.cos(angle)
        y += (radius.member + 12) * Math.sin(angle)
        angle = angle * 180 / Math.PI + 75

        svg.append("text")
            .attr("class", "caption")
            .attr("x", x)
            .attr("y", y)
            .attr("font-weight", member == username ? 700 : 400)
            .attr("text-anchor", (angle > 90 && angle < 270) ? "end" : "start")
            .attr("alignment-baseline", "middle")
            .attr("fill", colors.black)
            .attr("transform", "rotate (" + ((angle > 90 && angle < 270) ? angle + 180 : angle) + " " + x + " " + y + ")")
            .text(member)
    })
}