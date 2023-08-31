import React, { useState, useEffect } from "react";
import DeckGL from "@deck.gl/react";
import { Map } from "react-map-gl";
import { GeoJsonLayer } from "@deck.gl/layers";
import { EditableGeoJsonLayer } from "@nebula.gl/layers";
import mapboxgl from "mapbox-gl";
import {
  IconButton,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@material-ui/core";
import { Lock, LockOpen } from "@material-ui/icons";

// prettier-ignore
// eslint-disable-next-line import/no-webpack-loader-syntax
mapboxgl.workerClass = require("worker-loader!mapbox-gl/dist/mapbox-gl-csp-worker").default;

const MAPBOX_ACCESS_TOKEN =
  "pk.eyJ1IjoiemFydWIwMDYiLCJhIjoiY2xoOGFuaGZtMDZxYzNlcXJqNzAyb3RuaiJ9.51-GRZuvAnqX4z00ISy26w";

// Viewport settings
const INITIAL_VIEW_STATE = {
  longitude: -93.75,
  latitude: 46.25,
  zoom: 6,
  minZoom: 5,
  maxZoom: 16,
};

// Symbology settings
const colorMap = {
  Injury: [252, 196, 25, 175],
  Fatal: [199, 15, 15, 225],
};

function getColor(colorValue) {
  return colorMap[colorValue] || [255, 255, 255]; // Default to white if color not found
}

function getTooltip({ object }) {
  return (
    object && {
      html: `\
  <div><b>Incident ${object.properties.icr}</b></div>
  <div>Date: ${object.properties.incident_date}</div>
  <div>Type: ${object.properties.incident_type}</div>
  `,
    }
  );
}

function IncidentMap() {
  const [geojsonData, setGeojsonData] = useState(null);
  const [editingEnabled, setEditingEnabled] = useState(false);
  const [confirmPopupVisible, setConfirmPopupVisible] = useState(false);
  const [pointToMove, setPointToMove] = useState(null);

  const toggleEditing = () => {
    setEditingEnabled(!editingEnabled);
  };

  const handleDragEnd = (info) => {
    if (confirmPopupVisible) {
      // Update the position and close the confirmation popup
      const { index, lngLat } = info;
      const updatedData = JSON.parse(JSON.stringify(geojsonData));
      updatedData.features[index].geometry.coordinates = [lngLat[0], lngLat[1]];
      setGeojsonData(updatedData);
      setConfirmPopupVisible(false);

      // Update point position in the database and handle confirmation
      // ... (similar to previous code)
    } else {
      setPointToMove(info);
      setConfirmPopupVisible(true);
    }
  };

  useEffect(() => {
    // Fetch GeoJSON data from the API
    fetch("http://localhost:8080/points/geojson")
      .then((response) => response.json())
      .then((data) => setGeojsonData(data))
      .catch((error) => console.error("Error fetching GeoJSON data:", error));
  }, []);

  const layer = new EditableGeoJsonLayer({
    id: "GeoJsonLayer",
    data: geojsonData,
    pointType: "circle",
    filled: true,
    getFillColor: (d) => getColor(d.properties.incident_type),
    stroked: true,
    getPointRadius: 4,
    pointRadiusUnits: "pixels",
    opacity: 1,
    pickable: true,
    visible: true,
    getPosition: (d) => d.coordinates,
    editable: editingEnabled,
    onDragEnd: handleDragEnd,
  });

  return (
    <div style={{ position: "relative", height: "100vh", overflow: "hidden" }}>
      <IconButton
        onClick={toggleEditing}
        style={{
          position: "absolute",
          top: "10px",
          right: "10px",
          zIndex: 1,
        }}
      >
        {editingEnabled ? <LockOpen /> : <Lock />}
      </IconButton>
      <DeckGL
        layers={layer}
        //getTooltip={getTooltip}
        initialViewState={INITIAL_VIEW_STATE}
        controller={true}
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
        }}
      >
        <Map
          mapboxAccessToken={MAPBOX_ACCESS_TOKEN}
          initialViewState={{ ...INITIAL_VIEW_STATE }} // Pass the view state to ReactMapGL
          onViewportChange={() => {}}
          mapStyle="mapbox://styles/mapbox/streets-v12"
          style={{ width: "100%", height: "100%" }}
        />
      </DeckGL>
      <Dialog
        open={confirmPopupVisible}
        onClose={() => setConfirmPopupVisible(false)}
      >
        <DialogTitle>Confirm Move</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to move this point?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => handleDragEnd(pointToMove)}>Yes</Button>
          <Button onClick={() => setConfirmPopupVisible(false)}>No</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default IncidentMap;
