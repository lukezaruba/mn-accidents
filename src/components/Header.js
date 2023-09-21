import React, { useState } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  SvgIcon,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";

const Header = () => {
  const [openDialog, setOpenDialog] = useState(false);

  const handleDialogOpen = () => {
    setOpenDialog(true);
  };

  const handleDialogClose = () => {
    setOpenDialog(false);
  };

  return (
    <AppBar position="static" sx={{ backgroundColor: "#7a0019" }}>
      <Toolbar>
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <a href="https://cla.umn.edu/mgis" target="_blank" rel="noreferrer">
            <img
              src={process.env.PUBLIC_URL + "/logo.png"}
              alt="Logo"
              height={40}
            />
          </a>
        </Box>
        <Typography variant="h6" sx={{ flexGrow: 1, textAlign: "center" }}>
          Minnesota Fatal & Serious Injury Accident Viewer
        </Typography>
        {/* Information Button */}
        <Tooltip title="Information">
          <IconButton color="inherit" onClick={handleDialogOpen}>
            <SvgIcon component={InfoIcon} />
          </IconButton>
        </Tooltip>
        <Dialog open={openDialog} onClose={handleDialogClose}>
          <DialogTitle>Information</DialogTitle>
          <DialogContent>
            <DialogContentText>
              This application enables users to view serious and fatal traffic
              accidents across Minnesota. The data contained in this application
              starts from 2017 and continues up to the present.
              <br></br>
              <br></br>
              Data and all analyses are currently updated weekly using data from
              the MN State Patrol{" "}
              <a href="https://app.dps.mn.gov/MSPMedia2/Current">
                Crash Updates
              </a>{" "}
              page. For other data and analyses, check out the{" "}
              <a href="https://mncrash.state.mn.us/">MNCrash</a> application
              from the MN DPS.
              <br></br>
              <br></br>
              <b>
                NOTE: The data contained within this application was scraped
                (collected) from the internet and may or may not be accurate.
              </b>
              <br></br>
              <br></br>
              Created by Luke Zaruba, University of Minnesota, MGIS Programs
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleDialogClose} color="primary">
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
