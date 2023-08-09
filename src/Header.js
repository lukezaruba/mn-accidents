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

const Header = ({ currentPage, onPageChange }) => {
  const pages = ["Page 1", "Page 2"];

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
          <img src="/logo.png" alt="Logo" height={40} />
        </Box>
        <Typography variant="h6" sx={{ flexGrow: 1, textAlign: "center" }}>
          Minnesota Fatal & Serious Injury Accident Viewer
        </Typography>
        {pages.map((page, index) => (
          <Button
            key={index}
            color="inherit"
            onClick={() => onPageChange(index)}
            sx={{
              borderBottom: index === currentPage ? "2px solid #fff" : "none",
              "&:hover": {
                borderBottom: "2px solid #fff",
              },
            }}
          >
            {page}
          </Button>
        ))}
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
              This is the information you want to display.
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
