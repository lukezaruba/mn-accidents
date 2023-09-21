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
              This is a test layout for the framework of the Minnesota Accident
              Viewer application.
              <br></br>
              <br></br>
              <b>
                ALL DATA CURRENTLY USED IN THIS APPLICATION IS FAKE AND IS FOR
                TESTING ONLY.
              </b>
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
