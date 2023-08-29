import React, { useState, useRef, useEffect } from "react";
import { IconButton } from "@mui/material";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import TimeSeriesChart from "./TimeSeriesChart";

const IncidentSidebar = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const [chartsVisibility, setChartsVisibility] = useState({
    timeseries: true,
    incidentcount: true,
  });

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const toggleChartVisibility = (chartKey) => {
    setChartsVisibility((prevVisibility) => ({
      ...prevVisibility,
      [chartKey]: !prevVisibility[chartKey],
    }));
  };

  return (
    <div
      style={{
        width: isSidebarOpen ? "250px" : "40px",
        height: "100vh",
        position: "relative",
        top: 0,
        left: 0,
        backgroundColor: "#f9f7f6",
        boxShadow: isSidebarOpen ? "2px 0px 5px rgba(0, 0, 0, 0.2)" : "none",
        overflowX: "hidden",
        transition: "width 0.5s, background-color 0.5s, box-shadow 0.5s",
        zIndex: 1000,
      }}
    >
      <div
        style={{
          position: "sticky",
          top: "50%",
          transform: "translateY(-50%)",
          left: isSidebarOpen ? "0" : `-250px`,
          zIndex: 1001,
          transition: "left 0.5s",
        }}
      >
        <IconButton
          onClick={toggleSidebar}
          style={{
            position: "absolute",
            top: "50%",
            left: "0",
            zIndex: 1001,
          }}
        >
          <ChevronLeftIcon />
        </IconButton>
      </div>
      {children}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
        }}
      >
        {isSidebarOpen && (
          <>
            <CollapsibleChart
              title="Time Series Chart"
              isVisible={isSidebarOpen && chartsVisibility.timeseries}
              onToggle={() => toggleChartVisibility("timeseries")}
            >
              <TimeSeriesChart
                isVisible={isSidebarOpen}
                expandedWidth="250px"
              />
            </CollapsibleChart>
            <CollapsibleChart
              title="Total Incident Count"
              isVisible={isSidebarOpen && chartsVisibility.incidentcount}
              onToggle={() => toggleChartVisibility("incidentcount")}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  flexDirection: "column",
                }}
              >
                <h1 style={{ height: "0px", textAlign: "center" }}>123456</h1>
                <h6 style={{ height: "0px", textAlign: "center" }}>
                  <i>total incidents</i>
                </h6>
              </div>
            </CollapsibleChart>
          </>
        )}
      </div>
    </div>
  );
};

const CollapsibleChart = ({ title, isVisible, onToggle, children }) => {
  const [chartHeight, setChartHeight] = useState(isVisible ? "auto" : 0);
  const chartRef = useRef(null);

  useEffect(() => {
    if (isVisible && chartRef.current) {
      setChartHeight(`${chartRef.current.scrollHeight}px`);
    } else {
      setChartHeight(0);
    }
  }, [isVisible]);

  return (
    <div>
      <div
        onClick={onToggle}
        style={{
          display: "flex",
          alignItems: "center",
          cursor: "pointer",
        }}
      >
        <span style={{ marginRight: "8px", marginLeft: "10px" }}>{title}</span>
        <span>{isVisible ? "▲" : "▼"}</span>
      </div>
      <div
        style={{
          height: chartHeight,
          overflow: "hidden",
          transition: "height 0.3s",
        }}
      >
        <div ref={chartRef}>{children}</div>
      </div>
    </div>
  );
};

export default IncidentSidebar;
