import React from "react";
import CityPage from "../city/CityPage";
import IncidentPage from "../incident/IncidentPage";

const Page = ({ currentPage }) => {
  return (
    <div style={{ flexGrow: 1, height: "calc(100vh - 64px)" }}>
      {currentPage === "City" && <CityPage />}
      {currentPage === "Incident" && <IncidentPage />}
    </div>
  );
};

export default Page;
