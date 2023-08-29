import React from "react";
import IncidentSidebar from "./IncidentSidebar";
import IncidentMap from "./IncidentMap";

const IncidentPage = () => {
  return (
    <div style={{ display: "flex" }}>
      <IncidentSidebar></IncidentSidebar>
      <div
        style={{
          flex: 1,
          transform: "translateX(0)", // Start with map centered
          transition: "transform 0.5s",
        }}
      >
        <IncidentMap />
      </div>
    </div>
  );
};

export default IncidentPage;
