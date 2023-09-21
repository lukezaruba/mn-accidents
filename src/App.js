import React from "react";
import CssBaseline from "@mui/material/CssBaseline"; // Import CssBaseline
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Header from "./components/Header";
import Page from "./components/Page";

const theme = createTheme({
  typography: {
    fontFamily: "Open Sans, sans-serif",
  },
});

function App() {
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
        <Header />
        <Page />
      </div>
    </ThemeProvider>
  );
}

export default App;
