function BarChart(selector, options={}) {
    var data = [5, 10, 12];
    // Option Defaults
    options.width =  options.width || 200;
    options.scaleFactor =  options.scaleFactor || 10;
    options.barHeight =  options.barHeight || 20;
    options.fill = options.fill || d3.scaleOrdinal(d3.schemeCategory10);
    options.fontFactor = options.fontFactor || 0.25;

    // Private Vars
    let svg, lastData;
        
    
    // Private Functions
    function createSvg() {
        d3.select(selector).selectAll('svg').remove();
        svg = d3.select(selector).append("svg");
    }
    function setDims(dataFactor) {
        svg.transition().duration(600)
            .attr("height", options.barHeight * dataFactor)
            .attr("width", options.width);
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
    
    function drawBar(data){
        svg.selectAll("rect").data(data).enter()
            .append("rect")
            .style("fill", (_, i) => options.fill(i) )
            .attr("transform", ({y}) => `translate(0,${y})`)
            .attr("height", ({ height }) => height)
            
            svg.selectAll("rect").transition().duration(600)
            .attr("transform", ({x, y}) => 
            `translate(${x}, ${y})`
            )
            .attr("width", ({ width }) => width)
    }
    function drawText(data) {
        svg.selectAll("text").data(data).enter()
            .append("text")
            .attr("dy", ".35em")
            .attr("transform", (d, i) => `translate(0,${ d.height/2 + i*options.barHeight })`)
            .text( ({ word }) => word );
        
        svg.selectAll("text").transition().duration(600)
            .attr("transform", (d, i) => 
                `translate(${
                    d.width
                }, ${ d.height/2 + i*options.barHeight })`
            )
    }
    function draw(data) {
        drawBar(data);
        drawText(data);
    }

    // Public Methods
    this.update = (data) => {
        lastData = data;
        createSvg();
        setDims(data.length);
        const {min, max} = findMinMax(data);
        draw(
            data.sort( (b, a) => a.size - b.size ).map( ({word, size}, idx) => ({
                width: 1+ (1- options.fontFactor)*options.width * (size - min) / ( max - min ),
                height: options.barHeight,
                x: 0, y: idx * options.barHeight,
                word, size
            }) )
        );
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