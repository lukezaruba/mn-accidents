import React from "react";
import DeckGL from "@deck.gl/react";
import { Map } from "react-map-gl";
import { GeoJsonLayer } from "@deck.gl/layers";
import maplibregl from "maplibre-gl";

const MAP_STYLE =
  "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json";

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
          reuseMaps
          mapLib={maplibregl}
          mapStyle={MAP_STYLE}
          initialViewState={{ ...INITIAL_VIEW_STATE }}
          onViewportChange={() => {}}
          preventStyleDiffing={true}
          style={{ width: "100%", height: "100%" }}
        />
      </DeckGL>
    </div>
  );
}

export default IncidentMap;
