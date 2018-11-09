function BarChart(selector, options={}) {
    // Option Defaults
    options.width =  options.width || 200;
    options.scaleFactor =  options.scaleFactor || 10;
    options.barHeight =  options.barHeight || 20;
    options.fill = options.fill || d3.scaleOrdinal(d3.schemeCategory10);
    options.fontFactor = options.fontFactor || 0.25;
    options.toStart = options.toStart === true;
    options.negate = options.negate === true;
    options.fontColor = options.fontColor || "var(--md-theme-default-accent)";
    // Private Vars
    let svg, lastData;
      
    // Private Functions
    function createSvg() {
        d3.select(selector).selectAll('svg').remove();
        svg = d3.select(selector).append("svg");
    }
    function setDims(dataFactor) {
        options.barHeight = options.height / dataFactor;
        svg.transition().duration(600)
            .attr("height", options.height)
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
            .attr("transform", ({y}) => `translate(${
                 0
            },${y})`)
            .attr("width", ({ width }) => options.negate ? width : 0)
            .attr("height", ({ height }) => height)
            
        svg.selectAll("rect").transition().duration(600)
            .attr("transform", ({x, y, width}) => 
                `translate(${
                    options.negate ? options.width-x-width : x
                }, ${y})`
            )
            .attr("width", ({ width }) => width)
    }
    function drawText(data) {
        svg.selectAll("text").data(data).enter()
            .append("text")
            .attr("dy", ".35em")
            .attr("fill", options.fontColor)
            .attr("transform", (d, i) => `translate(0,${ d.height/2 + i*options.barHeight })`)
            .text( ({ word, size }) => `${word.toLowerCase()} (${size}w)` );
        
        svg.selectAll("text").transition().duration(600)
            .attr("transform", (d, i) => 
                `translate(${
                    options.toStart ? 0.01*options.width : (
                        options.negate ? 1+(options.width-d.width) : d.width 
                    )
                }, ${ d.height/2 + i*options.barHeight })`
            )
            .attr("text-anchor", options.negate ? "start" : options.toStart ? "start" : "end")
            .style("font-weight", "bold")
    }
    function draw(data) {
        drawBar(data);
        drawText(data);
    }

    // Public Methods
    this.updateData = (data) => {
        lastData = data;
        createSvg();
        setDims(data.length);
        const {min, max} = findMinMax(data);
        draw(
            data.sort( (b, a) => a.size - b.size ).map( ({word, size}, idx) => ({
                width: 1+ options.width * (size - min) / ( max - min ),
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
        if (lastData) {
            this.updateData(lastData);
        }
    }

    // Constructor
    createSvg();
    makeResize(selector, this);

    // Return
    return this;
}
