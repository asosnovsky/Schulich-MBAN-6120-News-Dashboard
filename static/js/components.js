const KeyNumbers = {
    template: `
        <div id="key-numbers" class="md-layout-item md-layout md-size-100 md-center">
            <div v-for="topWord in topwords" class="top-word md-layout-item md-elevation-5"> 
                <div class="md-title">
                    %(topWord.word)%
                </div>
                <div>
                    <span class="md-display-2" style="font-size: 2em;">%(topWord.percent)%%</span>
                    <span class="md-caption" style="color: #949494">/%(topWord.count)%w</span>
                </div>
            </div>
        </div>
    `,
    props: {
        topwords: Array
    }
}