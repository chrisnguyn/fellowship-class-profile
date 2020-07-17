function getPersonalSummary(data) {
    let personalSummary = {}
    let totalContributions = data["num_contributions"]

    let contributions = [{
        color: colors.green,
        percent: data["num_commits"] / totalContributions,
        name: "Commits"
    }, {
        color: colors.blue,
        percent: data["num_code_reviews"] / totalContributions,
        name: "Code review"
    }, {
        color: colors.yellow,
        percent: data["num_prs"] / totalContributions,
        name: "Pull requests"
    }, {
        color: colors.red,
        percent: data["num_issues_opened"] / totalContributions,
        name: "Issues"
    }]

    contributions = contributions.sort((a, b) => { return a["percent"] > b["percent"] ? -1 : 1 })

    personalSummary.contribution = {
        title: "Contribution",
        subtitle: "Total contributions",
        list: contributions,
        total: totalContributions
    }
    personalSummary.repositories = {
        title: "Repositories",
        subtitle: "Repositories worked on",
        list: [],
        total: data["num_repos"]
    }

    let repos = []
    Object.keys(data["repo_changes"]).forEach(repo => {
        data["repo_changes"][repo]["name"] = repo
        repos.push(data["repo_changes"][repo])
    })
    repos = repos.sort((a, b) => { return a["commits"] > b["commits"] ? -1 : 1 })

    // Handle too much data. Cap at 7, replace lowest percentages with "Other" tag.
    if (repos.length > 7) {
        let other = repos.slice(6, repos.length)
        repos = repos.slice(0, 6)
        let repo = {
            name: "other",
            commits: other.reduce((acc, d) => { return acc + d["commits"] }, 0)
        }
        repos.push(repo)
    }

    let totalCommits = repos.reduce((acc, d) => { return acc + d["commits"] }, 0)
    let colorScale = d3.scaleOrdinal()
        .domain(repos.map(repo => { return repo["name"] }))
        .range([colors.yellow, colors.blue, colors.red, colors.green, "orange", "purple", colors.grey])

    repos.forEach(repo => {
        // Calculate percent by number of commits.
        personalSummary.repositories.list.push({
            color: colorScale(repo["name"]),
            percent: repo["commits"] / totalCommits,
            name: repo["name"]
        })
    })

    return personalSummary
}

// TODO: Replace dummy data.
// let personalSummary = {
//     contribution: {
//         title: "Contribution",
//         subtitle: "Total contributions",
//         list: [{
//             color: colors.green,
//             percent: 0.6,
//             name: "Commits"
//         }, {
//             color: colors.blue,
//             percent: 0.25,
//             name: "Code review"
//         }, {
//             color: colors.yellow,
//             percent: 0.1,
//             name: "Pull requests"
//         }, {
//             color: colors.red,
//             percent: 0.05,
//             name: "Issues"
//         }],
//         total: 343
//     },
//     languages: {
//         title: "Languages",
//         subtitle: "Different languages",
//         list: [{
//             color: "#3572A5",
//             percent: 0.6,
//             name: "Python"
//         }, {
//             color: "#e34c26",
//             percent: 0.3,
//             name: "HTML"
//         }, {
//             color: "#ffac45",
//             percent: 0.1,
//             name: "Swift"
//         }],
//         total: 3
//     },
//     repositories: {
//         title: "Repositories",
//         subtitle: "Repositories worked on",
//         list: [{
//             color: colors.green,
//             percent: 0.7,
//             name: "howdoi"
//         }, {
//             color: colors.yellow,
//             percent: 0.2,
//             name: "werkzeug"
//         }, {
//             color: colors.red,
//             percent: 0.1,
//             name: "fastapi"
//         }],
//         total: 3
//     }
// }