function renderNavbarIcon(body) {
    let iconAttr = {
        size: 48,
        padding: 3
    }
    let icon = body.append("div")
        .append("svg")
        .attr("height", iconAttr.size)
        .attr("width", 400)
    icon.append("rect")
        .attr("x", iconAttr.size / 2 + iconAttr.padding / 2)
        .attr("y", iconAttr.size / 2 + iconAttr.padding / 2)
        .attr("height", iconAttr.size / 2 - iconAttr.padding)
        .attr("width", iconAttr.size / 2 - iconAttr.padding)
        .attr("fill", colors.yellow)
    icon.append("rect")
        .attr("x", iconAttr.size / 2 + iconAttr.padding / 2)
        .attr("y", iconAttr.padding / 2)
        .attr("height", iconAttr.size / 2 - iconAttr.padding)
        .attr("width", iconAttr.size / 2 - iconAttr.padding)
        .attr("fill", colors.yellow)
    icon.append("rect")
        .attr("x", iconAttr.padding / 2)
        .attr("y", iconAttr.size / 2 + iconAttr.padding / 2)
        .attr("height", iconAttr.size / 2 - iconAttr.padding)
        .attr("width", iconAttr.size / 2 - iconAttr.padding)
        .attr("fill", colors.yellow)
    icon.append("text")
        .attr("font-family", "Righteous")
        .attr("font-size", 18)
        .attr("x", iconAttr.size + iconAttr.padding * 4)
        .attr("y", iconAttr.padding / 2)
        .attr("text-anchor", "start")
        .attr("alignment-baseline", "hanging")
        .attr("fill", colors.black)
        .text("MLH")
    icon.append("text")
        .attr("font-family", "Noto Sans TC")
        .attr("font-size", 32)
        .attr("font-weight", 700)
        .attr("x", iconAttr.size + iconAttr.padding * 4)
        .attr("y", iconAttr.size - iconAttr.padding / 2)
        .attr("text-anchor", "start")
        .attr("alignment-baseline", "bottom")
        .attr("fill", colors.black)
        .text("Fellowstats")
}

function renderNavbar(body) {
    let navbar = body.append("div")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "center")
    renderNavbarIcon(navbar)

    let div = navbar.append("div")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "flex-end")
        .style("width", "100%")
    let svg = div.append("svg")
        .attr("height", 48)
        .attr("width", 400)
    let width = svg.attr("width")
    let height = svg.attr("height")

    let textAttr = {
        size: 16,
        fontFamily: "Space Mono"
    }

    let tabRectWidth = 130
    let tabRect = svg.append("rect")
        .attr("height", 2)
        .attr("width", tabRectWidth)
        .attr("fill", colors.yellow)
        .attr("visibility", "hidden")
        .attr("y", height / 2 + textAttr.size + 4)

    svg.append("text")
        .attr("font-family", textAttr.fontFamily)
        .attr("font-size", textAttr.size)
        .attr("font-weight", 400)
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .attr("fill", colors.black)
        .attr("x", width * 0.25)
        .attr("y", height / 2)
        .attr("cursor", "pointer")
        .text("Class of 2020")
        .on("mouseover", function() {
            tabRect.attr("visibility", "visible")
                .attr("x", width * 0.25 - tabRectWidth / 2)
        })
        .on("mouseout", function() {
            tabRect.attr("visibility", "hidden")
        })
        .on("mousedown", function() {
            // Redirect to class stats.
        })
    svg.append("text")
        .attr("font-family", textAttr.fontFamily)
        .attr("font-size", textAttr.size)
        .attr("font-weight", 400)
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .attr("fill", colors.black)
        .attr("x", width * 0.75)
        .attr("y", height / 2)
        .attr("cursor", "pointer")
        .text("My Fellowship")
        .on("mouseover", function() {
            tabRect.attr("visibility", "visible")
                .attr("x", width * 0.75 - tabRectWidth / 2)
        })
        .on("mouseout", function() {
            tabRect.attr("visibility", "hidden")
        })
        .on("mousedown", function() {
            // Redirect to personal stats.
        })
}