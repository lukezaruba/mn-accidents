import React from "react";
import CitySidebar from "./CitySidebar";
import CityMap from "./CityMap";

const CityPage = () => {
  return (
    <div style={{ display: "flex" }}>
      <CitySidebar></CitySidebar>
      <div
        style={{
          flex: 1,
          transform: "translateX(0)", // Start with map centered
          transition: "transform 0.5s",
        }}
      >
        <CityMap />
      </div>
    </div>
  );
};

export default CityPage;
