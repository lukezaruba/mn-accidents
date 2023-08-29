import React from "react";
import DeckGL from "@deck.gl/react";
import { Map } from "react-map-gl";
import { GeoJsonLayer } from "@deck.gl/layers";
import mapboxgl from "mapbox-gl";

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

// Map
function IncidentMap() {
  const layer = new GeoJsonLayer({
    id: "GeoJsonLayer",
    data: "http://localhost:8080/points/geojson",
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
  });

  return (
    <div style={{ position: "relative", height: "100vh", overflow: "hidden" }}>
      <DeckGL
        layers={layer}
        getTooltip={getTooltip}
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
    </div>
  );
}

export default IncidentMap;
