import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";

const SeatbeltChart = ({ pieData, isVisible, expandedWidth }) => {
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  useEffect(() => {
    chartInstanceRef.current = echarts.init(chartRef.current);

    return () => {
      // Clean up the chart instance when component unmounts
      chartInstanceRef.current.dispose();
    };
  }, []);

  // Sorting Data
  pieData.sort(function (a, b) {
    return b.value - a.value;
  });

  function generateLinearColorRamp(startColor, endColor, count) {
    function hexToRgb(hex) {
      var bigint = parseInt(hex.slice(1), 16);
      var r = (bigint >> 16) & 255;
      var g = (bigint >> 8) & 255;
      var b = bigint & 255;
      return { r, g, b };
    }

    var colors = [];
    var startRGB = hexToRgb(startColor);
    var endRGB = hexToRgb(endColor);

    for (var i = 0; i < count; i++) {
      var r = Math.round(
        startRGB.r + (endRGB.r - startRGB.r) * (i / (count - 1))
      );
      var g = Math.round(
        startRGB.g + (endRGB.g - startRGB.g) * (i / (count - 1))
      );
      var b = Math.round(
        startRGB.b + (endRGB.b - startRGB.b) * (i / (count - 1))
      );
      colors.push(`rgb(${r},${g},${b})`);
    }

    return colors;
  }

  // Create Ramp based on input array length
  var linearColorRamp = generateLinearColorRamp(
    "#7a0019",
    "#ffcc33",
    pieData.length
  );

  useEffect(() => {
    if (chartInstanceRef.current && isVisible) {
      // Update chart data and options here
      const option = {
        tooltip: {
          trigger: "item",
          confine: true,
        },
        legend: {
          bottom: "-2.5%",
          left: "center",
        },
        series: [
          {
            name: "Seatbelt Usage",
            type: "pie",
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },
            label: {
              show: false,
              position: "center",
            },
            labelLine: {
              show: false,
            },
            data: pieData,
            color: linearColorRamp,
            global: false, // default is false
          },
        ],
      };
      chartInstanceRef.current.setOption(option);
    }
  }, [isVisible, pieData, linearColorRamp]);

  return (
    <div
      ref={chartRef}
      style={{
        width: isVisible ? expandedWidth : "0",
        height: expandedWidth,
        transition: "width 0.5s",
        overflow: "hidden",
        marginTop: isVisible ? "-25px" : "0",
      }}
    >
      {/* Chart will be rendered here */}
    </div>
  );
};

export default SeatbeltChart;
