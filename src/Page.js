import React from "react";

const Page = ({ currentPage }) => {
  const pageUrls = [
    "https://clausa.app.carto.com/map/edd66e07-995f-43a8-aaf2-8b20dad7bdbd",
    "https://clausa.app.carto.com/map/12dae3a8-a096-472c-8ab8-baabcfe1de9c",
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
