anychart.onDocumentReady(function() {
    let display_data = []
    let org_statistics = fetch("https://fellowship-class-profile.herokuapp.com/global_stats")
                         .then(response => response.json())
                         .then(json_response => json_response["repo_lang_stats"])
                         .then(data => generate_word_cloud(data))

    function generate_word_cloud(org_stats) {
        for (let key in org_stats) {
            if (key === "TOTAL NUMBER REPOS" || key === "None") {
                continue;
            }

            let val = org_stats[key];
            display_data.push({"x": `${key}`, "value": `${val}`, category: `${key}`})
        }
    
        let chart = anychart.tagCloud(display_data);
        chart.title("MLH Fellowship Repository Language Popularity");
        chart.angles([0])
        chart.colorRange(true);
        chart.colorRange().length('80%');
        chart.container("container");
        chart.draw();
    }
});
