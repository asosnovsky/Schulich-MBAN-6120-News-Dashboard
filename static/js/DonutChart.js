function DonutChart(selector, options={}) {
    // Option Defaults
    options.width =  options.width || 200;
    options.height =  options.height || 200;

    // Private Vars
    let svg, g, lastData, lastArcs;

    // Private Classes
    const arcTools = new (function ArcTool() {
        let radius, finalArc, startArc;

        this.getArcRadiusCalculators = () => {
            const newRadius = 0.9 * Math.min(options.width, options.height) / 2;
            if (!radius || radius !== newRadius) {
                radius = newRadius;
                startArc = d3.arc().innerRadius(radius * 0.6).outerRadius(radius*0.65);
                finalArc = d3.arc().innerRadius(radius * 0.8).outerRadius(radius);
            }
            return {startArc, finalArc}
        }

        this.makeArcs = d3.pie()
            .padAngle(0.005)
            .sort(null)
            .value(d => d.count)

        return this;
    })();

    // Private Functions
    function createSvg() {
        d3.select(selector).selectAll('svg').remove();
        svg = d3.select(selector).append("svg");
        g = svg.append("g");
        reCalcDims();
    }
    function reCalcDims() {
        svg.transition().duration(600)
            .attr("width", options.width)
            .attr("height", options.height)
        g.transition().duration(600)
            .attr("transform", `translate(${options.width / 2},${options.height / 2})`);
    }
    function updateOptions(newOptions = {}) {
        options = {...options, ...newOptions};
    }
    function drawDonut(data, arcs){
        const { finalArc, startArc  } = arcTools.getArcRadiusCalculators();
        const color = d3.scaleOrdinal()
            .domain(data.map(d => d.word))
            .range(
                d3.quantize(
                    t => d3.interpolateSpectral(
                        t * 0.8 + 0.1
                    ), data.length).reverse()
            );
        window.TEST = {
            g, data, arcs, color, finalArc, startArc
        }
        g.selectAll("path").data(arcs).enter().append("path")
            .attr("fill", d => color(d.data.word))
            .attr("d", startArc)
            .append("title")
            .text(d => `${d.data.word}: ${d.data.count.toLocaleString()}`)
        
        g.selectAll("path").transition().duration(600)
                .attr("d", finalArc)
    }
    function drawText(_, arcs) {
        const { finalArc, startArc  } = arcTools.getArcRadiusCalculators();
        
        g.selectAll("text")
            .remove()
            .call( _ => {
                const text = g.selectAll("text")
                    .data(arcs)
                    .enter().append("text")
                    .attr("transform", d => `translate(${startArc.centroid(d)})`)
                    .attr("dy", "0.35em");
                    
                text.append("tspan")
                    .filter(d => (d.endAngle - d.startAngle) > 0.25)
                    .transition().duration(600)
                    .attr("transform", d => `translate(${finalArc.centroid(d)})`)
                    .attr("x", "-2.5em")
                    .attr("y", "-0.7em")
                    .style("fill", "rgba(126, 172, 40)")
                    .style("font-weight", "bold")
                    .text(d => `${d.data.word} - ${d.data.count}`);
            })
    }

    this.updateData = function(data){
        lastData = data;
        lastArcs = arcTools.makeArcs(data);

        reCalcDims();
        drawDonut(data, lastArcs);
        drawText(data, lastArcs);
    }  

    this.updateOptions = function(options) {
        updateOptions(options)
        reCalcDims();
        if (lastData) {
            this.updateData(lastData)
        }
    };
    
    updateOptions(options)
    createSvg()
    makeResize(selector, this);

    return this;
}