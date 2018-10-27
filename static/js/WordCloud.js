function WordCloud(selector, options = {}) {

    // Options Defaults
    options.width = options.width || 500;
    options.height = options.height || 500;
    options.fill = options.fill || d3.scaleOrdinal(d3.schemeCategory10);

    // Private Vars
    let svg;
    let lastData;

    // Private Functions
    function createSvg() {
        d3.select(selector).selectAll("svg").remove();

        svg = d3.select(selector).append("svg")
            .attr("width", options.width)
            .attr("height", options.height)
            .append("g")
            .attr("transform", `translate(${options.width/2},${options.height/2})`);
    }
    function findMinMax(words) {
        return words.reduce( ({min, max}, {size}) => {
            if (!min) { min = size };
            if (!max) { max = size };
            max = Math.max(max, size);
            min = Math.min(min, size);
            return {min, max};
         }, {});
    };

    function draw(words) {
        svg.selectAll("g text")
            .transition()
            .duration(600)
            .style('fill-opacity', 1e-6)
            .attr('font-size', 1)
            .remove();
        
        createSvg();

        svg.selectAll("g text").data(words).enter()
            .append("text")
            .style("font-family", "Impact")
            .style("fill", (_, i) => options.fill(i) )
            .attr("text-anchor", "middle")
            .attr("font-size", 1)
            .attr("transform", "translate(0,0)")
            .text( ({ word }) => word );

        svg.selectAll("g text").transition().duration(500)
            .attr('font-size', ({ size }) => size )
            .attr("transform", ({x, y, rotate}) => 
                `translate(${x},${y})rotate(${rotate})`
            )

    };
    
    // Public Functions
    this.update = (words) => {
        lastData = words;
        const { min, max } = findMinMax(words);

        d3.layout.cloud().size([
            options.width,
            options.height 
        ]).words(words)
        .padding(1)
        .rotate(() => ~~(Math.random() * 2) * 90 )
        .font("Impact")
        .fontSize(({ size }) => 
            5+Math.pow(options.width*options.height, 1/3) * (size - min) / ( max - min )
        )
        .on("end", draw)
        .start();
    }

    this.updateOptions = newOptions => {
        options = {
            ...options,
            ...newOptions
        }
        createSvg();
        if (lastData) {
            this.update(lastData);
        }
    }


    // Constructor
    createSvg();

    // Return
    return this;
}