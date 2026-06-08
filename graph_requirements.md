### Global Graph Requirements

#### Graph Series Names, Colors and Line Type

- Median (50th Percentile) [dashStyle: "Dash"]: `#5F98CA`
- 25th–75th Percentile [type: 'arearange']: `#9ACDFF`
- 5th–95th Percentile[type: 'arearange']: `#DDEEFF`
- Water Temperature Measurements[type: "line"]: `#000000`
- Air Temperature Measurements[type: "line"]: `#73C5DA`
- NDFD Air Temperature Predictions[type: "line"]: `#800080`
- Interpolated Water Temperature Predictions[dashStyle: "2.5, 2.5"]: `#000000`
- Interpolated Air Temperature Predictions[dashStyle: "2.5, 2.5"]: `#FFA500`
- Air Temperature Predictions[type: "line"]: `#008000`
- Water Temperature Predictions[type: "line"]: `#800080`
- Box Plot 'Series'[]:

#### Threshold Names and Colors

- Sea Turtle Threshold[dashStyle: "Dash"]: `#FF0000`
- Fisheries Threshold[dashStyle: "Dash"]: `#720000`
- Now Line[dashStyle: "Solid"]: `#FF0000`

#### Y-Axis Minimum

Use the greater of:

- `30°F`
- `Minimum Air Temperature − 5°F`

#### Y-Axis Maximum

- Use the same calculation as the MRE model.
- All graphs must use the same calculation.

#### Thresholds

- Threshold lines must remain visible when zooming.

#### Temperature Units

- Display all temperatures in Fahrenheit (`°F`).

#### Time

- Display timestamps in the user's local timezone.
- The "Now" line should use the client's current time.

#### Legends

- Use consistent naming across all graphs.
- Display historical measurements before predictions.
- Display median lines before percentile ranges.

#### Graph Behavior

- Historical and predicted values must be visually distinct.
- Zooming must not alter data or calculations.
- Missing data must be handled by displaying a "missing data banner".