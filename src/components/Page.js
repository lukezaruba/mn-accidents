import React from "react";
import Sidebar from "./Sidebar";

const Page = () => {
  return (
    <div style={{ flexGrow: 1, overflow: "hidden" }}>
      <div style={{ display: "flex", height: "100%" }}>
        <Sidebar></Sidebar>
        <div
          style={{
            flex: 1,
            transform: "translateX(0)",
            transition: "transform 0.5s",
          }}
        >
          <iframe
            title="Embedded Map"
            src="https://experience.arcgis.com/experience/5f93e10e830f4ea3a33d816bf35b8885/"
            width="100%"
            height="100%"
          ></iframe>
        </div>
      </div>
    </div>
  );
};

export default Page;
