

window.addEventListener("load", () => {
    
    Vue.use(VueMaterial.default)
    new Vue({
        delimiters: ['%(', ')%'],
        el: '#app',
        components: {
            "d3-word-cloud": d3AsVue(WordCloud),
            "d3-line-chart": d3AsVue(LineChart),
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
            },
        },
        data: {
            loadingStatus: {
                topics: true,
                wordCounts: true,
                newsfeeds: {
                    "Very Positive": true,
                    "Positive": true,
                    "Negative": true,
                    "Very Negative": true,
                },
                timeseries: true,
                topWords: true,
            },
            currentTopic: null,
            charOptions: {},

            topics: [],
            newsfeeds: {
                "Very Positive": [],
                "Positive": [],
                "Negative": [],
                "Very Negative": [],
            },
            wordCounts: [],
            topWords: [],
            timeseries: [],
        },
        methods: {
            setCurrentTopic(topic) {
                this.currentTopic = topic;
                this.updateTopWords(topic);
                this.updateNewsFeed(topic);
                this.updateWordsCounts(topic);
                this.updateTimeseries(topic);
            },
            async updateWordsCounts(keyword) {
                const wordCountsReq = await fetch("/data/word-count/" + keyword);
                this.wordCounts = await wordCountsReq.json();
                this.loadingStatus.wordCounts = false
            },
            async updateTopWords(keyword) {
                const topWordsReq = await fetch("/data/nltk/counts/" + keyword);
                this.topWords = await topWordsReq.json();
                this.loadingStatus.topWords = false
            },
            async updateTimeseries(keyword) {
                const timeseriesReq = await fetch("/data/nltk/sentiment-timeseries/" + keyword);
                this.timeseries = await timeseriesReq.json();
                this.loadingStatus.timeseries = false
                console.log(this.timeseries)
            },
            async updateNewsFeed(keyword) {
                return Promise.all(
                    Object.keys(this.newsfeeds).map( async sent => {
                        const newsReq = await fetch("/data/nltk/newsfeed/" + keyword + '/' + sent);
                        this.newsfeeds[sent] = await newsReq.json();
                        this.loadingStatus.newsfeeds[sent] = false
                    } )
                )
            },
        },
        async created() {
            const req = await fetch("/data/topics");
            this.topics = await req.json();
            this.setCurrentTopic(this.topics[0]);
        }
    });
})

