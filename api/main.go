package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

// PointCollection represents a collection of points in the PostGIS table
type PointCollection struct {
	Type     string  `json:"type"`
	Features []Point `json:"features"`
}

// Point represents a point in the PostGIS table
type Point struct {
	Type       string            `json:"type"`
	Geometry   Geometry 		 `json:"geometry"`
	Properties map[string]interface{} `json:"properties"`
}

// Geometry represents the geometry object in the Point struct
type Geometry struct {
	Type        string      `json:"type"`
	Coordinates interface{} `json:"coordinates"`
}

func main() {
	// Connect to PostGIS database - fine to leave localhost creds
	db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost/mnaccidents?sslmode=disable")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Create a new Gin router
	router := gin.Default()

	// Handle GET request for GeoJSON
	router.GET("/points/geojson", func(c *gin.Context) {
		var pointCollection PointCollection

		// Query the PostGIS table and retrieve points as GeoJSON
		rows, err := db.Query("SELECT json_build_object('type', 'FeatureCollection', 'features', json_agg(ST_AsGeoJSON(tbl.*)::json)) FROM geo_accidents AS tbl")
		if err != nil {
			log.Println("Failed to query points:", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query points"})
			return
		}
		defer rows.Close()

		// Iterate over the result rows
		for rows.Next() {
			var jsonResult []byte
			err := rows.Scan(&jsonResult)
			if err != nil {
				log.Println("Failed to scan JSON result:", err)
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to scan JSON result"})
				return
			}

			// Unmarshal the JSON result into the PointCollection struct
			err = json.Unmarshal(jsonResult, &pointCollection)
			if err != nil {
				log.Println("Failed to unmarshal JSON:", err)
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to unmarshal JSON"})
				return
			}
		}

		c.JSON(http.StatusOK, pointCollection)
	})

	// Start the HTTP server
	if err := router.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}
