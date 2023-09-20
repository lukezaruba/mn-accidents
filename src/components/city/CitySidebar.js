import React, { useState, useRef, useEffect } from "react";
import { IconButton } from "@mui/material";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import CityAlcoholChart from "./CityAlcoholChart";
import CitySeatbeltChart from "./CitySeatbeltChart";
import CityConditionChart from "./CityConditionChart";

const CitySidebar = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const [chartsVisibility, setChartsVisibility] = useState({
    alcohol: true,
    seatbelt: true,
    condition: true,
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

  // Alcohol Data
  const [alcoholData, setAlcoholData] = useState([]);

  useEffect(() => {
    // Make the API request here
    fetch("http://127.0.0.1:8080/api/v1/metrics/alcohol")
      .then((response) => response.json())
      .then((data) => {
        // Set the fetched data in the state
        setAlcoholData(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const transformedAlcoholData = alcoholData.map(([name, value]) => ({
    name,
    value,
  }));

  // Seatbelt Data
  const [seatbeltData, setSeatbeltData] = useState([]);

  useEffect(() => {
    // Make the API request here
    fetch("http://127.0.0.1:8080/api/v1/metrics/seatbelt")
      .then((response) => response.json())
      .then((data) => {
        // Set the fetched data in the state
        setSeatbeltData(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const transformedSeatbeltData = seatbeltData.map(([name, value]) => ({
    name,
    value,
  }));

  // Condition Data
  const [conditionData, setConditionData] = useState([]);

  useEffect(() => {
    // Make the API request here
    fetch("http://127.0.0.1:8080/api/v1/metrics/condition")
      .then((response) => response.json())
      .then((data) => {
        // Set the fetched data in the state
        setConditionData(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const transformedConditionData = conditionData.map(([name, value]) => ({
    name,
    value,
  }));

  const pieData = [
    { value: 4310, name: "Yes" },
    { value: 231, name: "No" },
    { value: 1732, name: "Unknown" },
  ];

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
              title="Alcohol Chart"
              isVisible={isSidebarOpen && chartsVisibility.alcohol}
              onToggle={() => toggleChartVisibility("alcohol")}
            >
              <CityAlcoholChart
                pieData={transformedAlcoholData}
                isVisible={isSidebarOpen}
                expandedWidth="250px"
              />
            </CollapsibleChart>
            <CollapsibleChart
              title="Seatbelt Chart"
              isVisible={isSidebarOpen && chartsVisibility.seatbelt}
              onToggle={() => toggleChartVisibility("seatbelt")}
            >
              <CitySeatbeltChart
                pieData={transformedSeatbeltData}
                isVisible={isSidebarOpen}
                expandedWidth="250px"
              />
            </CollapsibleChart>
            <CollapsibleChart
              title="Condition Chart"
              isVisible={isSidebarOpen && chartsVisibility.condition}
              onToggle={() => toggleChartVisibility("condition")}
            >
              <CityConditionChart
                pieData={transformedConditionData}
                isVisible={isSidebarOpen}
                expandedWidth="250px"
              />
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

export default CitySidebar;
