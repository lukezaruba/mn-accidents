import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";

const TimeSeriesChart = ({ isVisible, expandedWidth }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!isVisible) return;

    const chart = echarts.init(chartRef.current);

    let base = +new Date(1988, 9, 3);
    let oneDay = 24 * 3600 * 1000;
    let data = [[base, Math.random() * 300]];
    for (let i = 1; i < 20000; i++) {
      let now = new Date((base += oneDay));
      data.push([
        +now,
        Math.round((Math.random() - 0.5) * 20 + data[i - 1][1]),
      ]);
    }

    const option = {
      tooltip: {
        trigger: "axis",
        position: function (pt) {
          return [pt[0], "10%"];
        },
      },
      title: {
        left: "center",
        text: "Large Area Chart",
      },
      toolbox: {
        feature: {
          restore: {},
        },
      },
      xAxis: {
        type: "time",
        boundaryGap: false,
      },
      yAxis: {
        type: "value",
        boundaryGap: [0, "100%"],
      },
      dataZoom: [
        {
          type: "inside",
          start: 0,
          end: 20,
        },
        {
          start: 0,
          end: 20,
        },
      ],
      series: [
        {
          name: "Fake Data",
          type: "line",
          smooth: true,
          symbol: "none",
          areaStyle: {},
          data: data,
        },
      ],
    };

    chart.setOption(option);

    // Clean up the chart instance when component unmounts
    return () => {
      chart.dispose();
    };
  }, [isVisible]);

  return (
    <div
      ref={chartRef}
      style={{
        width: isVisible ? expandedWidth : "0",
        height: "200px",
        transition: "width 0.5s",
        overflow: "hidden",
      }}
    >
      {/* Chart will be rendered here */}
    </div>
  );
};

export default TimeSeriesChart;
