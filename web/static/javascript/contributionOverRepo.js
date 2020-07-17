function renderRepoContributionChart(body, repos) {
    repos = Object.keys(repos).map(key => {
        let repo = repos[key]
        return {
            name: repo.name,
            additions: repo.additions,
            changed_files: repo.changed_files,
            commits: repo.commits,
            deletions: repo.deletions
        }
    })

    body.append("div")
        .attr("class", "subheader")
        .style("color", colors.black)
        .html("Contributions by repository")
    body.append("div")
        .attr("class", "caption")
        .style("color", colors.black)
        .html("Here is a closer look at how I contributed to each repository.")
    let div = body.append("div")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "center")
        .style("width", "100%")
    let svg = div.append("svg")
        .attr("height", 500 / 7 * repos.length)
        .attr("width", 1200)

    let height = svg.attr("height")
    let width = svg.attr("width")

    let padding = {
        horizontal: 200,
        vertical: 72
    }

    let xScale = d3.scaleLinear()
        .domain([0, Object.keys(repos[0]).length - 1])
        .range([padding.horizontal, width - padding.horizontal])

    let minMap = {}
    let maxMap = {}
    Object.keys(repos[0]).forEach(variable => {
        let min = d3.min(repos, repo => {
            return repo[variable]
        })
        let max = d3.max(repos, repo => {
            return repo[variable]
        })
        min = isNaN(min) ? 0 : min
        max = isNaN(max) ? (repos.length - 1) : max
        minMap[variable] = min
        maxMap[variable] = max
    })

    let yScales = {}
    let labels = {}
    Object.keys(repos[0]).forEach((variable, i) => {
        let yScale = d3.scaleLinear()
            .domain([minMap[variable], maxMap[variable]])
            .range([height - padding.vertical, padding.vertical])
        yScales[variable] = yScale
        if (variable != "name") {
            svg.append("text")
                .attr("font-family", "Space Mono")
                .attr("font-size", 12)
                .attr("text-anchor", "middle")
                .attr("alignment-baseline", "bottom")
                .attr("fill", colors.black)
                .attr("x", xScale(i))
                .attr("y", yScales[variable](maxMap[variable]) - 36)
                .text(variable)
            labels[variable] = svg.append("text")
                .attr("class", "caption")
                .attr("fill", colors.grey)
                .attr("text-anchor", "middle")
                .attr("alignment-baseline", "bottom")
                .attr("x", xScale(i))
                .attr("y", yScales[variable](maxMap[variable]) - 12)
                .text(maxMap[variable])
            svg.append("text")
                .attr("class", "caption")
                .attr("fill", colors.grey)
                .attr("text-anchor", "middle")
                .attr("alignment-baseline", "hanging")
                .attr("x", xScale(i))
                .attr("y", yScales[variable](minMap[variable]) + 12)
                .text(minMap[variable])
        }
    })

    for (let i = 1; i < Object.keys(repos[0]).length; i++) {
        svg.append("line")
            .attr("x1", xScale(i))
            .attr("x2", xScale(i))
            .attr("y1", padding.vertical)
            .attr("y2", height - padding.vertical)
            .attr("stroke", colors.grey)
            .attr("stroke-width", 2)
    }

    let lineGen = d3.line()
        .curve(d3.curveLinear)
    repos.forEach((repo, i) => {
        let g = svg.append("g")
        let nameText = g.append("text")
            .attr("font-family", "Space Mono")
            .attr("font-size", 12)
            .attr("fill", colors.black)
            .attr("text-anchor", "end")
            .attr("alignment-baseline", "middle")
            .attr("x", xScale(0) - 12)
            .attr("y", yScales.name(i))
            .text(repo.name)

        let points = [
            [xScale(0), yScales.name(i)],
            [xScale(1), yScales.additions(repo.additions)],
            [xScale(2), yScales.changed_files(repo.changed_files)],
            [xScale(3), yScales.commits(repo.commits)],
            [xScale(4), yScales.deletions(repo.deletions)]

        ];
        let lineData = lineGen(points);
        let linePath = g.append("path")
            .attr("d", lineData)
            .attr("fill", "none")
            .attr("stroke", colors.yellow)
            .attr("stroke-width", 2)
        g.on("mouseover", function() {
                nameText.attr("fill", colors.green)
                linePath.attr("stroke", colors.green)
                    .attr("stroke-width", 8)
                Object.keys(repos[0]).forEach((variable) => {
                    if (variable != "name") {
                        labels[variable].attr("fill", colors.green)
                            .text(repo[variable])
                    }
                })
            })
            .on("mouseout", function() {
                nameText.attr("fill", colors.black)
                linePath.attr("stroke", colors.yellow)
                    .attr("stroke-width", 2)
                Object.keys(repos[0]).forEach((variable) => {
                    if (variable != "name") {
                        labels[variable].attr("fill", colors.grey)
                            .text(maxMap[variable])
                    }
                })
            })
    })
}