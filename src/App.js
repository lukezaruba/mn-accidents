import React, { useState } from "react";
import CssBaseline from "@mui/material/CssBaseline"; // Import CssBaseline
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Header from "./components/common/Header";
import Page from "./components/common/Page";

const theme = createTheme({
  typography: {
    fontFamily: "Open Sans, sans-serif",
  },
});

function App() {
  const [currentPage, setCurrentPage] = useState("City");

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          height: "100vh",
          overflow: "hidden",
        }}
      >
        <Header currentPage={currentPage} onPageChange={handlePageChange} />
        <Page currentPage={currentPage} />
      </div>
    </ThemeProvider>
  );
}

export default App;
