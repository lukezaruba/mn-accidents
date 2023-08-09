import React, { useState } from "react";
import CssBaseline from "@mui/material/CssBaseline"; // Import CssBaseline
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Header from "./Header";
import Page from "./Page";

const theme = createTheme({
  typography: {
    fontFamily: "Open Sans, sans-serif",
  },
});

function App() {
  const [currentPage, setCurrentPage] = useState(0);

  const handlePageChange = (index) => {
    setCurrentPage(index);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div
        style={{ display: "flex", flexDirection: "column", height: "100vh" }}
      >
        <Header currentPage={currentPage} onPageChange={handlePageChange} />
        <Page currentPage={currentPage} />
      </div>
    </ThemeProvider>
  );
}

export default App;
