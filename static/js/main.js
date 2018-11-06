

window.addEventListener("load", () => {
    
    Vue.use(VueMaterial.default)
    const app = new Vue({
        delimiters: ['%(', ')%'],
        el: '#app',
        components: {
            "d3-bar-chart": d3AsVue(BarChart),
            "d3-donut-chart": d3AsVue(DonutChart),
            "d3-word-cloud": d3AsVue(WordCloud),
            "loading-cover-up": {
                template: `<div :class="displayClassName">
                    <md-progress-spinner v-if="loading" class="md-accent" md-mode="indeterminate"></md-progress-spinner>
                </div>`,
                props: {
                    loading: Boolean
                },
                computed: {
                    displayClassName() {
                        return this.loading ? "loading-cover-up" : "loading-cover-down"
                    }
                }
            }
        },
        data: {
            loadingStatus: {
                articles: true,
                topics: true,
                topWords: true,
                wordCounts: true,
                top10: true,
            },
            currentTopic: null,
            articles: [],
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
                    toStart: false,
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
                this.currentTopic = topic;
                this.resetLoadingStatus();
                this.updateNewsFeed(topic);
                this.updateTopicCharts(topic);
                this.updateTopWordsCounts(topic);
                this.updateTop10Words(topic);
            },
            async updateTopicCharts(keyword) {
                const wordCountsReq = await fetch("/data/word-count/" + keyword);
                this.wordCounts = await wordCountsReq.json();
                this.loadingStatus.wordCounts = false
            },
            async updateTopWordsCounts(keyword) {
                const req = await fetch("data/nltk/counts/" + keyword)
                this.topWords = await req.json();
                this.loadingStatus.topWords = false
            },
            async updateTop10Words(keyword) {
                const req = await fetch("data/nltk/top_10/" + keyword)
                this.top10 = {
                    ...this.top10,
                    ...await req.json()
                }
                this.loadingStatus.top10 = false
            },
            async updateNewsFeed(keyword) {
                const newsReq = await fetch("/data/articles/" + keyword);
                this.articles = await newsReq.json();
                this.loadingStatus.articles = false
            },
            resetLoadingStatus() {
                this.loadingStatus = {
                    articles: true,
                    topics: true,
                    topWords: true,
                    wordCounts: true,
                    top10: true,
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

