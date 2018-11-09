function LineChart(selector, options={}) {
    // Option Defaults
    options.width =  options.width || 200;
    options.scaleFactor =  options.scaleFactor || 10;
    options.barHeight =  options.barHeight || 20;
    options.fontFactor = options.fontFactor || 0.25;
    options.toStart = options.toStart === true;
    options.negate = options.negate === true;
    options.fontColor = options.fontColor || "var(--md-theme-default-accent)";
    
    // Private Vars
    let lastData, svg;
    const margin = ({top: 20, right: 20, bottom: 30, left: 40});
    
    // Private Methods
    function createSvg() {
        d3.select(selector).selectAll('svg').remove();
        svg = d3.select(selector).append("svg");
        setDims();
    }
    function setDims() {
        svg.transition().duration(600)
        .attr("height", options.height)
        .attr("width", options.width);
    }
    function makeAxes(data) {
        const { width, height } = options;
        
        const x = d3.scaleTime()
        .domain(d3.extent(data.dates))
        .range([margin.left, width - margin.right])
        const xAxis = g => g
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))
        const y = d3.scaleLinear()
        .domain([0, d3.max(data.series, d => 
            d3.max(d.values)
            )]).nice()
            .range([height - margin.bottom, margin.top])
            const yAxis = g => g
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y))
            .call(g => g.select(".domain").remove())
            .call(g => g.select(".tick:last-of-type text").clone()
            .attr("x", 3)
            .attr("text-anchor", "start")
            .attr("font-weight", "bold")
            .text("Count"))
            const line = d3.line()
            .defined(d => !isNaN(d))
            .x((_, i) => x(data.dates[i]))
            .y(d => y(d));
            return {xAxis, x, yAxis, y, line};
        }
        function hover(data, x, y) {
            return (svg, path) => {
                svg
                .style("position", "relative");
                
                if ("ontouchstart" in document) svg
                    .style("-webkit-tap-highlight-color", "transparent")
                    .on("touchmove", moved)
                    .on("touchstart", entered)
                    .on("touchend", left)
                else svg
                    .on("mousemove", moved)
                    .on("mouseenter", entered)
                    .on("mouseleave", left);
                
                const dot = svg.append("g")
                .attr("display", "none");
                
                dot.append("circle")
                .attr("r", 2.5);
                
                dot.append("text")
                .style("font", "10px sans-serif")
                .attr("text-anchor", "middle")
                .attr("y", -8);
                
                function moved() {
                    d3.event.preventDefault();
                    const ym = y.invert(d3.event.layerY);
                    const xm = x.invert(d3.event.layerX);
                    const i1 = d3.bisectLeft(data.dates, xm, 1);
                    const i0 = i1 - 1;
                    const i = xm - data.dates[i0] > data.dates[i1] - xm ? i1 : i0;
                    const s = data.series.reduce((a, b) => Math.abs(a.values[i] - ym) < Math.abs(b.values[i] - ym) ? a : b);
                    path.attr("stroke", d => {
                        return d === s ? "white" : d.color.static
                    }).filter(d => d === s).raise();
                    dot.attr("transform", `translate(${x(data.dates[i])},${y(s.values[i])})`);
                    dot.select("text").text(`${s.values[i]} ${s.name} Articles`);
                }
                
                function entered() {
                    dot.attr("display", null);
                }
                
                function left() {
                    dot.attr("display", "none");
                }
            }
        }
        function draw(data) {
            const {xAxis, x, yAxis, y, line} = makeAxes(data);
            
            svg.append("g")
            .call(xAxis);
            
            svg.append("g")
            .call(yAxis);
            
            const path = svg.append("g")
            .attr("fill", "none")
            .attr("stroke-width", 1.5)
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .selectAll("path")
            .data(data.series)
            .enter().append("path")
            .attr("stroke", ({color}) => {
                return color.static
            })
            .attr("d", d => line(d.values));
            
            svg.call(hover(data, x,y), path);
        }
        function cleanUpData(data) {
            const colorMaps = {
                "Very Positive": {
                    "static": "#7aff00",
                    "hovered": "#7aff10"
                },
                "Positive": {
                    "static": "#4b7b1e",
                    "hovered": "#4b0b1e"
                },
                "Negative": {
                    "static": "#9e3232",
                    "hovered": "#9e3200"
                },
                "Very Negative": {
                    "static": "#ff0000",
                    "hovered": "#ff0010"
                },
            }

            const moddedData = data.reduce( (agg, row) => {
                if (!agg[row.date]) {
                    agg[row.date] = {};
                }                
                agg[row.date][row.sentiment_state] = row.count
                return agg;
            }, { });
            const series = Object.keys(moddedData).reduce( (agg, date) => {
                Object.keys(moddedData[date]).forEach( name => {
                    if( !agg[name] ) {
                        agg[name] = { name, values: [], color: colorMaps[name] };
                    }
                    agg[name].values.push(moddedData[date][name]);
                } )
                return agg;
            }, {})
            return {
                series: Object.keys(series).map( k => series[k] ),
                dates: Object.keys(moddedData).map( date => moment(date).toDate() ),
            }
        }

        // Public Methods
        this.updateData = (data) => {
            lastData = data;
            
            createSvg();
            draw(cleanUpData(data))
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
    