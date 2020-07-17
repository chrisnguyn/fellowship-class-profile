function renderPersonalHighlights(body, data) {
    body.append("div")
        .attr("class", "subheader")
        .style("color", colors.black)
        .html("Highlights")
    body.append("div")
        .attr("class", "caption")
        .style("color", colors.black)
        .html("Here are some highlights of my fellowship.")
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

    let mostPopularPRLang = data["most_popular_pr"]["pullRequest"]["repository"]["languages"]["nodes"]
    mostPopularPRLang = mostPopularPRLang.length > 4 ? mostPopularPRLang.slice(0, 4) : mostPopularPRLang
    mostPopularPRLang = mostPopularPRLang.reduce((acc, lang) => {
        return lang["name"] + ", " + acc
    }, "")
    mostPopularPRLang = mostPopularPRLang.substring(0, mostPopularPRLang.length - 2)

    let dateTimeParser = d3.timeParse("%Y-%m-%d")
    let dateTimeFormat = d3.timeFormat("%a, %b %e")
    let highlights = [{
        title: dateTimeFormat(dateTimeParser(data["most_active_day"]["date"])),
        text: [
            "This was my most active day.",
            "I made " + data["most_active_day"]["contributions"] + " contributions."
        ],
        image: "../static/icons/day.svg"
    }, {
        title: data["most_popular_pr"]["pullRequest"]["title"],
        text: [
            "This was my most popular pull request.",
            "I made this PR for " + data["most_popular_pr"]["pullRequest"]["repository"]["name"] + " using",
            mostPopularPRLang + "."
        ],
        image: "../static/icons/pull_request.svg"
    }, {
        title: "Week " + data["most_active_week"]["week_number"],
        text: [
            "This was my most active week.",
            "I made " + data["most_active_week"]["contributions"] + " contributions."
        ],
        image: "../static/icons/week.svg"
    }]

    let imageAttr = {
        height: 300,
        width: 300
    }

    let xScale = d3.scaleLinear()
        .domain([0, highlights.length - 1])
        .range([imageAttr.width / 2, width - 2 * imageAttr.width / 2])

    // Most active week, most active day, most popular pr.

    highlights.forEach((highlight, i) => {
        svg.append("image")
            .attr("href", highlight.image)
            .attr("height", imageAttr.height)
            .attr("width", imageAttr.width)
            .attr("x", xScale(i) - imageAttr.width / 2)
            .attr("y", 0)
        svg.append("text")
            .attr("class", "header")
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