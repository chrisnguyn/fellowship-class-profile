anychart.onDocumentReady(function() {
    let display_data = []
    let org_stats = {  // dummy data
        "None": 3,
        "JavaScript": 34,
        "TypeScript": 9,
        "Julia": 19,
        "Python": 14,
        "Jupyter Notebook": 2,
        "C": 1,
        "C++": 2,
        "Shell": 4,
        "Ruby": 3,
        "HTML": 3,
        "Java": 2
    }

    for (let key in org_stats) {
        let val = org_stats[key];
        display_data.push({"x": `${key}`, "value": `${val}`, category: `${key}`})  // {"x": "howdoi", "value": 10, category: "Python"}
    }

    let chart = anychart.tagCloud(display_data);
    chart.title("MLH-Fellowship Repository Language Popularity");
    chart.angles([0])
    chart.colorRange(true);
    chart.colorRange().length('80%');
    chart.container("container");
    chart.draw();
});
