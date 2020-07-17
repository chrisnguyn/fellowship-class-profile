function renderGlobalContributionOverTimeChart(body, globalData) {
    let globalContributions = globalData["num_contributions_by_day"]["days"]
    let contributionCalendar = {
        totalContributions: globalData["num_contributions_by_day"]["totalContributions"],
        weeks: []
    }
    Object.keys(globalContributions).forEach(date => {
        if (contributionCalendar.weeks.length <= globalContributions[date].week) {
            contributionCalendar.weeks.push({
                contributionDays: []
            })
        }
    })
    Object.keys(globalContributions).forEach(date => {
        let day = globalContributions[date]
        contributionCalendar.weeks[day.week].contributionDays.push({
            contributionCount: day.contributionCount,
            date: date,
            weekday: day.weekday
        })
    })

    renderContributionOverTimeChart(body, contributionCalendar, "This is how we contributed throughout the course of 12 weeks.")
}

function renderContributionOverTimeChart(body, contributionCalendar, subtitle = "This is how I contributed throughout the course of 12 weeks.") {
    let contributions = []
    contributionCalendar.weeks.forEach(week => {
        week.contributionDays.forEach(day => {
            contributions.push({
                count: day.contributionCount,
                date: day.date,
                weekday: day.weekday
            })
        })
    })

    if (contributions.length == 0) {
        return
    }

    body.append("div")
        .attr("class", "subheader")
        .style("color", colors.black)
        .html("Contributions over time")
    body.append("div")
        .attr("class", "caption")
        .style("color", colors.black)
        .html(subtitle)
    let div = body.append("div")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "center")
    let svg = div.append("svg")
        .attr("height", 500)
        .attr("width", 900)

    let height = svg.attr("height")
    let width = svg.attr("width")

    let chartWidth = width - 200
    let horizontalPadding = 24
    let tabHeight = 24
    let rectWidth = chartWidth / contributions.length

    let averageContributionPerDay = contributions.reduce((acc, d) => {
        return acc + d.count
    }, 0) / contributions.length

    let maxContributions = d3.max(contributions, d => {
        return d.count
    })
    let minContributions = d3.min(contributions, d => {
        return d.count
    })

    // console.log(averageContributionPerDay)
    // console.log(maxContributions)
    // console.log(minContributions)
    // console.log(halfRange)

    let dateXScale = d3.scaleLinear()
        .domain([0, contributions.length - 1])
        .range([width / 2 - chartWidth / 2, width / 2 + chartWidth / 2])

    let contributionYScale = d3.scaleLinear()
        .domain([minContributions, maxContributions])
        .range([height - 40, 200])

    svg.append("text")
        .attr("class", "caption")
        .attr("text-anchor", "end")
        .attr("alignment-baseline", "middle")
        .attr("fill", colors.black)
        .attr("x", width / 2 - chartWidth / 2 - horizontalPadding)
        .attr("y", contributionYScale(averageContributionPerDay))
        .text("June 01")

    svg.append("text")
        .attr("class", "caption")
        .attr("text-anchor", "start")
        .attr("alignment-baseline", "middle")
        .attr("fill", colors.black)
        .attr("x", width / 2 + chartWidth / 2 + horizontalPadding)
        .attr("y", contributionYScale(averageContributionPerDay))
        .text("Aug 24")

    svg.append("line")
        .attr("x1", width / 2 - chartWidth / 2 - rectWidth / 2 - 1)
        .attr("x2", width / 2 + chartWidth / 2 + rectWidth / 2 + 1)
        .attr("y1", contributionYScale(averageContributionPerDay))
        .attr("y2", contributionYScale(averageContributionPerDay))
        .attr("stroke", colors.black)
        .attr("stroke-width", 2)

    svg.append("line")
        .attr("x1", width / 2 - chartWidth / 2 - rectWidth / 2 - 1)
        .attr("x2", width / 2 - chartWidth / 2 - rectWidth / 2 - 1)
        .attr("y1", contributionYScale(averageContributionPerDay) - tabHeight / 2)
        .attr("y2", contributionYScale(averageContributionPerDay) + tabHeight / 2)
        .attr("stroke", colors.black)
        .attr("stroke-width", 2)

    svg.append("line")
        .attr("x1", width / 2 + chartWidth / 2 + rectWidth / 2 + 1)
        .attr("x2", width / 2 + chartWidth / 2 + rectWidth / 2 + 1)
        .attr("y1", contributionYScale(averageContributionPerDay) - tabHeight / 2)
        .attr("y2", contributionYScale(averageContributionPerDay) + tabHeight / 2)
        .attr("stroke", colors.black)
        .attr("stroke-width", 2)

    let dateLabel = svg.append("text")
        .attr("font-family", "Space Mono")
        .attr("font-size", 12)
        .attr("text-anchor", "end")
        .attr("alignment-baseline", "middle")
        .attr("fill", colors.green)
        .attr("visibility", "hidden")
    let countLabel = svg.append("text")
        .attr("font-family", "Space Mono")
        .attr("font-size", 12)
        .attr("alignment-baseline", "middle")
        .attr("fill", colors.green)
        .attr("visibility", "hidden")
    let lineLabel = svg.append("line")
        .attr("stroke", colors.green)
        .attr("stroke-width", 2)
        .attr("visibility", "hidden")
    let circleLabel = svg.append("circle")
        .attr("fill", colors.green)
        .attr("visibility", "hidden")
        .attr("r", 4)

    let dateTimeParser = d3.timeParse("%Y-%m-%d");
    let dateTimeFormat = d3.timeFormat("%a, %b %e")

    function showLabels(d, i) {
        let dateTime = dateTimeParser(d.date)
        let labelY = contributionYScale(d.count > averageContributionPerDay ? maxContributions : minContributions) +
            (rectWidth + 12) * (d.count > averageContributionPerDay ? -1 : 1)
        dateLabel.attr("visibility", "visible")
            .attr("x", dateXScale(i) - 12)
            .attr("y", labelY)
            .text(dateTimeFormat(dateTime))
        countLabel.attr("visibility", "visible")
            .attr("x", dateXScale(i) + 12)
            .attr("y", labelY)
            .text(d.count)
        lineLabel.attr("visibility", "visible")
            .attr("x1", dateXScale(i))
            .attr("x2", dateXScale(i))
            .attr("y1", labelY)
            .attr("y2", contributionYScale(d.count) + rectWidth / 2 * (d.count > averageContributionPerDay ? -1 : 1))
        circleLabel.attr("visibility", "visible")
            .attr("cx", dateXScale(i))
            .attr("cy", labelY)
    }

    function hideLabels() {
        dateLabel.attr("visibility", "hidden")
        countLabel.attr("visibility", "hidden")
        lineLabel.attr("visibility", "hidden")
        circleLabel.attr("visibility", "hidden")
    }

    contributions.forEach((d, i) => {
        svg.append("rect")
            .attr("x", dateXScale(i) - rectWidth / 2)
            .attr("y", d.count > averageContributionPerDay ?
                contributionYScale(d.count) - rectWidth / 2 :
                contributionYScale(averageContributionPerDay) + 1)
            .attr("height", d.count > averageContributionPerDay ?
                contributionYScale(averageContributionPerDay) - contributionYScale(d.count) + rectWidth / 2 - 1 :
                contributionYScale(d.count) - contributionYScale(averageContributionPerDay) + rectWidth / 2 - 1)
            .attr("width", rectWidth)
            .attr("fill", colors.green)
            .attr("opacity", 0.5)
            .attr("rx", Math.min(2, rectWidth / 2))
            .on("mouseover", function() {
                showLabels(d, i)
            })
            .on("mouseout", function() {
                hideLabels()
            })

        svg.append("rect")
            .attr("x", dateXScale(i) - rectWidth / 2)
            .attr("y", contributionYScale(d.count) - rectWidth / 2)
            .attr("height", rectWidth)
            .attr("width", rectWidth)
            .attr("fill", colors.green)
            .attr("rx", Math.min(2, rectWidth / 2))
            .on("mouseover", function() {
                showLabels(d, i)
            })
            .on("mouseout", function() {
                hideLabels()
            })
    })

    let legend = svg.append("g")
        .attr("transform", "translate( " + (width - 300) + "," + 24 + ")")

    let legendAttr = {
        totalY: 12,
        averageY: 12 + 72,
        verticalPadding: 4
    }

    legend.append("rect")
        .attr("x", 0)
        .attr("y", legendAttr.totalY - rectWidth / 2)
        .attr("height", rectWidth)
        .attr("width", rectWidth)
        .attr("fill", colors.green)
        .attr("rx", Math.min(2, rectWidth / 2))
    legend.append("text")
        .attr("class", "header")
        .attr("x", rectWidth + 12)
        .attr("y", legendAttr.totalY - legendAttr.verticalPadding / 2)
        .attr("alignment-baseline", "bottom")
        .attr("fill", colors.black)
        .text(contributionCalendar.totalContributions)
    legend.append("text")
        .attr("class", "caption")
        .attr("x", rectWidth + 12)
        .attr("y", legendAttr.totalY + legendAttr.verticalPadding / 2)
        .attr("alignment-baseline", "hanging")
        .attr("fill", colors.black)
        .text("Total contributions")
    legend.append("text")
        .attr("class", "header")
        .attr("x", rectWidth + 12)
        .attr("y", legendAttr.averageY - legendAttr.verticalPadding / 2)
        .attr("alignment-baseline", "bottom")
        .attr("fill", colors.black)
        .text(Math.round(averageContributionPerDay * 100) / 100)
    legend.append("text")
        .attr("class", "caption")
        .attr("x", rectWidth + 12)
        .attr("y", legendAttr.averageY + legendAttr.verticalPadding / 2)
        .attr("alignment-baseline", "hanging")
        .attr("fill", colors.black)
        .text("Average contributions per day")
    legend.append("line")
        .attr("x1", 0)
        .attr("x2", rectWidth)
        .attr("y1", legendAttr.averageY)
        .attr("y2", legendAttr.averageY)
        .attr("stroke", colors.black)
        .attr("stroke-width", 2)
    legend.append("line")
        .attr("x1", 0)
        .attr("x2", 0)
        .attr("y1", legendAttr.averageY - rectWidth / 2)
        .attr("y2", legendAttr.averageY + rectWidth / 2)
        .attr("stroke", colors.black)
        .attr("stroke-width", 2)
    legend.append("line")
        .attr("x1", rectWidth)
        .attr("x2", rectWidth)
        .attr("y1", legendAttr.averageY - rectWidth / 2)
        .attr("y2", legendAttr.averageY + rectWidth / 2)
        .attr("stroke", colors.black)
        .attr("stroke-width", 2)
}