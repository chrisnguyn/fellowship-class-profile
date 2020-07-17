function renderRepoContributions(body, globalData) {
    body.append("div")
        .attr("class", "subheader")
        .style("color", colors.black)
        .html("Repository contributions")
    body.append("div")
        .attr("class", "caption")
        .style("color", colors.black)
        .html("This is how we contributed across repositories.")
    let div = body.append("div")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "center")
        .style("width", "100%")
    let svg = div.append("svg")
        .attr("height", 700)
        .attr("width", 1000)
    let height = svg.attr("height")
    let width = svg.attr("width")
    let commits = globalData["num_commits_per_repo"]
    let filesChanged = globalData["num_files_changed_per_repo"]
    let linesAdded = globalData["num_lines_code_added_per_repo"]
    let linesDeleted = globalData["num_lines_code_deleted_per_repo"]
    let repos = []
    Object.keys(commits).forEach(repo => {
        repos.push({
            name: repo,
            commits: commits[repo],
            filesChanged: filesChanged[repo],
            linesAdded: linesAdded[repo],
            linesDeleted: linesDeleted[repo]
        })
    })
    if (repos.length == 0) {
        return
    }
    console.log(repos)
    let min = {}
    let max = {}
    Object.keys(repos[0]).forEach(variable => {
        if (variable != "name") {
            let varMin = d3.min(repos, repo => {
                return repo[variable]
            })
            let varMax = d3.max(repos, repo => {
                return repo[variable]
            })
            min[variable] = varMin
            max[variable] = varMax
        }
    })
    let chartPadding = 100
    let scales = {
        commits: d3.scaleSqrt()
            .domain([min.commits, max.commits])
            .range([height - chartPadding, chartPadding]),
        filesChanged: d3.scaleSqrt()
            .domain([min.filesChanged, max.filesChanged])
            .range([chartPadding, width - chartPadding * 2]),
        linesAdded: d3.scaleLinear()
            .domain([min.linesAdded, max.linesAdded])
            .range([10, 40]),
        linesDeleted: d3.scaleLinear()
            .domain([min.linesDeleted, max.linesDeleted])
            .range([10, 40])
    }
    svg.append("line")
        .attr("x1", scales.filesChanged(min.filesChanged))
        .attr("x2", scales.filesChanged(max.filesChanged))
        .attr("y1", scales.commits(min.commits) + 12)
        .attr("y2", scales.commits(min.commits) + 12)
        .attr("stroke", colors.grey)
        .attr("stroke-width", 2)
    svg.append("line")
        .attr("x1", scales.filesChanged(min.filesChanged) - 12)
        .attr("x2", scales.filesChanged(min.filesChanged) - 12)
        .attr("y1", scales.commits(max.commits))
        .attr("y2", scales.commits(min.commits))
        .attr("stroke", colors.grey)
        .attr("stroke-width", 2)
    svg.append("text")
        .attr("class", "caption")
        .attr("fill", colors.grey)
        .attr("alignment-baseline", "hanging")
        .attr("text-anchor", "middle")
        .attr("x", scales.filesChanged(min.filesChanged))
        .attr("y", scales.commits(min.commits) + 24)
        .text(min.filesChanged)
    svg.append("text")
        .attr("class", "caption")
        .attr("fill", "grey")
        .attr("alignment-baseline", "hanging")
        .attr("text-anchor", "start")
        .attr("x", scales.filesChanged(min.filesChanged))
        .attr("y", scales.commits(min.commits) + 48)
        .text("Files changed")
    svg.append("text")
        .attr("class", "caption")
        .attr("fill", colors.grey)
        .attr("alignment-baseline", "hanging")
        .attr("text-anchor", "middle")
        .attr("x", scales.filesChanged(max.filesChanged))
        .attr("y", scales.commits(min.commits) + 24)
        .text(max.filesChanged)
    svg.append("text")
        .attr("class", "caption")
        .attr("fill", colors.grey)
        .attr("alignment-baseline", "middle")
        .attr("text-anchor", "end")
        .attr("x", scales.filesChanged(min.filesChanged) - 24)
        .attr("y", scales.commits(min.commits))
        .text(min.commits)
    svg.append("text")
        .attr("class", "caption")
        .attr("fill", "grey")
        .attr("alignment-baseline", "middle")
        .attr("text-anchor", "end")
        .attr("x", scales.filesChanged(min.filesChanged) - 48)
        .attr("y", scales.commits(min.commits))
        .text("Commits")
    svg.append("text")
        .attr("class", "caption")
        .attr("fill", colors.grey)
        .attr("alignment-baseline", "middle")
        .attr("text-anchor", "end")
        .attr("x", scales.filesChanged(min.filesChanged) - 24)
        .attr("y", scales.commits(max.commits))
        .text(max.commits)
    repos.forEach(repo => {
        let rectWidth = 4
        let g = svg.append("g")
        g.append("rect")
            .attr("x", scales.filesChanged(repo.filesChanged) - rectWidth / 2)
            .attr("y", scales.commits(repo.commits) - scales.linesAdded(repo.linesAdded))
            .attr("width", rectWidth)
            .attr("height", scales.linesAdded(repo.linesAdded))
            .attr("rx", rectWidth / 2)
            .attr("fill", colors.green)
            .attr("opacity", 0.5)
        g.append("rect")
            .attr("x", scales.filesChanged(repo.filesChanged) - rectWidth / 2)
            .attr("y", scales.commits(repo.commits))
            .attr("width", rectWidth)
            .attr("height", scales.linesDeleted(repo.linesDeleted))
            .attr("rx", rectWidth / 2)
            .attr("fill", colors.red)
            .attr("opacity", 0.5)
        g.append("circle")
            .attr("cx", scales.filesChanged(repo.filesChanged))
            .attr("cy", scales.commits(repo.commits))
            .attr("r", rectWidth)
            .attr("fill", colors.white)
            .attr("stroke", colors.grey)
            .attr("stroke-width", 2)
        g.on("mouseover", function() {
            showTooltip(repo)
        }).on("mouseout", function() {
            hideTooltip()
        })
    })
    let tooltip = svg.append("g")
    let tooltipText = tooltip.append("text")
        .attr("font-size", 14)
        .attr("font-family", "Space Mono")
        .attr("fill", "grey")
        .attr("x", 0)
        .attr("y", 12)
    let commitsText = tooltip.append("text")
        .attr("class", "caption")
        .attr("fill", colors.black)
        .attr("x", 0)
        .attr("y", 18 * 2)
    let filesChangedText = tooltip.append("text")
        .attr("class", "caption")
        .attr("fill", colors.black)
        .attr("x", 0)
        .attr("y", 18 * 3)
    let linesAddedText = tooltip.append("text")
        .attr("class", "caption")
        .attr("fill", colors.black)
        .attr("x", 0)
        .attr("y", 18 * 4)
    let linesDeletedText = tooltip.append("text")
        .attr("class", "caption")
        .attr("fill", colors.black)
        .attr("x", 0)
        .attr("y", 18 * 5)

    function showTooltip(repo) {
        let x = scales.filesChanged(repo.filesChanged) + 24
        let y = scales.commits(repo.commits) - 32
        tooltip.attr("visibility", "visible")
            .attr("transform", "translate (" + x +
                ", " + y + ")")
        tooltipText.text(repo.name)
        commitsText.text("Commits: " + repo.commits)
        filesChangedText.text("Files changed: " + repo.filesChanged)
        linesAddedText.text("Additions: " + repo.linesAdded)
        linesDeletedText.text("Deletions: " + repo.linesDeleted)
    }

    function hideTooltip() {
        tooltip.attr("visibility", "hidden")
    }
}