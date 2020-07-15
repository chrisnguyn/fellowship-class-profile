// TODO: Replace dummy data.
// Do top 7, if more then have 7th be "Other" to minimize crowding.
let personalSummary = {
    contribution: {
        title: "Contribution",
        subtitle: "Total contributions",
        list: [{
            color: colors.green,
            percent: 0.6,
            name: "Commits"
        }, {
            color: colors.blue,
            percent: 0.25,
            name: "Code review"
        }, {
            color: colors.yellow,
            percent: 0.1,
            name: "Pull requests"
        }, {
            color: colors.red,
            percent: 0.05,
            name: "Issues"
        }],
        total: 343
    },
    languages: {
        title: "Languages",
        subtitle: "Different languages",
        list: [{
            color: "#3572A5",
            percent: 0.6,
            name: "Python"
        }, {
            color: "#e34c26",
            percent: 0.3,
            name: "HTML"
        }, {
            color: "#ffac45",
            percent: 0.1,
            name: "Swift"
        }],
        total: 3
    },
    repositories: {
        title: "Repositories",
        subtitle: "Repositories worked on",
        list: [{
            color: colors.green,
            percent: 0.7,
            name: "howdoi"
        }, {
            color: colors.yellow,
            percent: 0.2,
            name: "werkzeug"
        }, {
            color: colors.red,
            percent: 0.1,
            name: "fastapi"
        }],
        total: 3
    }
}