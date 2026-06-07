### Interpolation Rules

For prediction data, interpolation gap limits should be based on the expected update frequency of each data source rather than assuming hourly data:

    - NDFD Predictions: Maximum interpolation gap of **3 hours** (recommended by Dr. Tissot).

    - CRPS Predictions: Maximum interpolation gap of **6 hours**.

    - Measured Data: Maximum interpolation gap of **1 data point** (pending confirmation).

### Legend Requirements
    - Use consistent naming: 
        - Median(50th Percentile)
        - 25th-75th Percentile
        - 5th-95th Percentile
        - Water Temperature Measurements
        - Air Temperature Measurements
        - Air Temperature Predictions
        - Interpolated Predicted Water Temperature
        - Interpolated Predicted Air Temperature
        - Interpolated Predicted Air Temperature
        - Water Temperature Predictions
        - Water Temperature Predictions
        - Ribbon Water Temperature Predictions

    - Use consistent colors:
        - Median(50th Percentile)
        - 25th-75th Percentile
        - 5th-95th Percentile
        - Water Temperature Measurements
        - Air Temperature Measurements
        - Air Temperature Predictions
        - Interpolated Predicted Water Temperature
        - Interpolated Predicted Air Temperature
        - Interpolated Predicted Air Temperature
        - Water Temperature Predictions
        - Water Temperature Predictions
        - Ribbon Water Temperature Predictions


### Global Graph Requirements

    The following rules should apply to all graphs unless explicitly overridden:

    == Y-Axis Minimum ==

    Use the greater of:

        - 30°F, or Minimum air temperature − 5°F

    == Y-Axis Maximum ==

        - Follow the maximum value calculation currently used by the **MRE model** code.

    == Thresholds ==

        - If a graph has a threshold, it must always be visibile even when zoomed into the graph

    == Degrees ==
        - Fahrenheit is the only dwegree used by graphs


