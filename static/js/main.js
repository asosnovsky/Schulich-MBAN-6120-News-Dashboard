

window.addEventListener("load", () => {
    
    Vue.use(VueMaterial.default)
    
    function resize() {
        const elm = document.querySelector("#data-container");
        wordCloud.updateOptions({
            width: elm.clientWidth/2,
            height: elm.clientHeight,
        });
        barChart.updateOptions({
            width: elm.clientWidth * 0.35,
            height: elm.clientHeight,
        });
    }
    
    const app = new Vue({
        delimiters: ['%(', ')%'],
        el: '#app',
        data: {
            topics: [],
        },
        methods: {
            updateWordCloud: (keyword) => {
                console.log(keyword)
                return async (event) => {
                    console.log(keyword)
                    if (event) event.preventDefault();
                        const wordCountsReq = await fetch("/data/word-count/" + keyword);
                        const wordCounts = await wordCountsReq.json();
                        wordCloud.update(wordCounts);
                        barChart.update(wordCounts)
                }
            }
        },
        async beforeMount() {
            const req = await fetch("/data/topics");
            this.topics = await req.json();
            this.updateWordCloud(this.topics[0])();
        },
        created(){
            window.addEventListener("resize", resize)
        }
    });
    const wordCloud = new WordCloud("#word-cloud");
    const barChart = new BarChart("#bar-chart");
    resize();
})

