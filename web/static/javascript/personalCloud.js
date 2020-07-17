anychart.onDocumentReady(function() {
    let display_data = []
    let org_statistics = fetch("https://fellowship-class-profile.herokuapp.com/user_stats?username=chrisngyn")
                         .then(response => response.json())
                         .then(json_response => json_response["top_repos"])
                         .then(data => generate_word_cloud(data))

    function generate_word_cloud(top_repos) {
        let ranking = top_repos.length;
        for (let i = 0; i < top_repos.length; i++) {
            let repository = top_repos[i]["repository"]["name"];
            let repository_language = top_repos[i]["repository"]["primaryLanguage"]["name"];
            display_data.push({"x": `${repository}`, "value": `${ranking}`});
            ranking -= 1;
        }
    
        let chart = anychart.tagCloud(display_data);
        chart.title("Your Top Repositories");
        chart.angles([0])
        chart.colorRange().length('80%');
        chart.container("container");
        chart.draw();
    }
});
