function makeResize(selector, ctx) {
    function resize() {
        const elm = document.querySelector(selector);
        const parentElm = elm.parentElement;
        const widthDef = elm.getAttribute("d3-width") || 'w:100';
        const heightDef = elm.getAttribute("d3-height") || 'h:100';
        const [widthFrom, widthPer] = widthDef.split(":");
        const [heightFrom, heightPer] = heightDef.split(":");
        const width = widthFrom === 'h' ? parentElm.clientHeight * Number(widthPer) / 100 : parentElm.clientWidth * Number(widthPer) / 100
        const height = heightFrom === 'h' ? parentElm.clientHeight * Number(heightPer) / 100 : parentElm.clientWidth * Number(heightPer) / 100
        
        elm.style.height = height+'px';
        elm.style.width = width+'px';
        ctx.updateOptions({
            width, height
        })
    }
    resize();
    window.addEventListener('resize', resize);
    return resize;
}

function d3AsVue(D3Class) {
    return {
        template: '<div ref="chart" :id="id" :d3-height="height" :d3-width="width"></div>',
        props: {
            data: Array,
            id: String,
            height: {
                type: String,
                default: 'h:100'
            },
            width: {
                type: String,
                default: 'w:100'
            },
            options: {
                type: Object,
                default: {}
            }
        },
        watch: {
            data: function() {
                this.chart.updateData([...this.data]);
            },
            options: function() {
                this.chart.updateOptions({...this.options})
            }
        },
        mounted() {
            this.chart = new D3Class('#'+this.id, this.options);
        },
    }
}