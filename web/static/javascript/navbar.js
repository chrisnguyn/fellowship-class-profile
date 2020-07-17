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
    let tabRectTransition = 50

    function getTabPosition(pathname = window.location.pathname) {
        switch (pathname) {
            case pages.CLASS_0:
                return width * 0.25 - tabRectWidth / 2
            case pages.PERSONAL:
                return width * 0.75 - tabRectWidth / 2
            case pages.LOGIN:
                return width * 0.75 - tabRectWidth / 2
            case _:
                return 0
        }
    }

    let tabRect = svg.append("rect")
        .attr("height", 2)
        .attr("width", tabRectWidth)
        .attr("fill", colors.yellow)
        .attr("x", getTabPosition())
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
        .text("Class 0")
        .on("mouseover", function() {
            tabRect.transition()
                .duration(tabRectTransition)
                .ease(d3.easeLinear)
                .attr("x", getTabPosition(pages.CLASS_0))
        })
        .on("mouseout", function() {
            tabRect.transition()
                .duration(tabRectTransition)
                .ease(d3.easeLinear)
                .attr("x", getTabPosition())
        })
        .on("mousedown", function() {
            window.location.pathname = pages.CLASS_0
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
            tabRect.transition()
                .duration(tabRectTransition)
                .ease(d3.easeLinear)
                .attr("x", getTabPosition(pages.LOGIN))
        })
        .on("mouseout", function() {
            tabRect.transition()
                .duration(tabRectTransition)
                .ease(d3.easeLinear)
                .attr("x", getTabPosition())
        })
        .on("mousedown", function() {
            window.location.pathname = pages.LOGIN
        })
}