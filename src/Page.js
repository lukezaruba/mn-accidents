import React from "react";

const Page = ({ currentPage }) => {
  const pageUrls = [
    "https://fiona.readthedocs.io/en/stable/manual.html",
    "https://geopandas.org/en/stable/index.html",
  ];

  return (
    <div style={{ flexGrow: 1, height: "calc(100vh - 64px)" }}>
      <iframe
        title={`Page ${currentPage + 1}`}
        src={pageUrls[currentPage]}
        style={{ width: "100%", height: "100%", border: "none" }}
      />
    </div>
  );
};

export default Page;
