

window.addEventListener("load", () => {
    
    Vue.use(VueMaterial.default)
    const app = new Vue({
        delimiters: ['%(', ')%'],
        el: '#app',
        components: {
            "d3-bar-chart": d3AsVue(BarChart),
            "d3-donut-chart": d3AsVue(DonutChart),
        },
        data: {
            topics: [],
            topWords: [],
            wordCounts: [],
            top10: {
                "positive": [],
                "negative": [],
                "neutral": [],
            },
            charOptions: {
                bar_top10_pos: {
                    fill: () => "#a1b6ef",
                    toStart: true,
                    fontColor: "white"
                },
                bar_top10_neg: {
                    fill: () => "red",
                    toStart: false,
                    negate: true,
                    fontColor: "white"
                },
                bar_top10_neut: {
                    fill: () => "var(--md-theme-default-accent)",
                    toStart: true,
                    fontColor: "var(--md-theme-default-primary)"
                }
            }
        },
        methods: {
            setCurrentTopic(topic) {
                this.updateTopicCharts(topic);
                this.updateTopWordsCounts(topic);
                this.updateTop10Words(topic);
            },
            updateTopicCharts: async (keyword) => {
                const wordCountsReq = await fetch("/data/word-count/" + keyword);
                this.wordCounts = await wordCountsReq.json();
            },
            async updateTopWordsCounts(keyword) {
                const req = await fetch("data/nltk/counts/" + keyword)
                this.topWords = await req.json();
            },
            async updateTop10Words(keyword) {
                const req = await fetch("data/nltk/top_10/" + keyword)
                this.top10 = {
                    ...this.top10,
                    ...await req.json()
                }
            }
        },
        async created() {
            const req = await fetch("/data/topics");
            this.topics = await req.json();
            this.setCurrentTopic(this.topics[0]);
        }
    });
})

