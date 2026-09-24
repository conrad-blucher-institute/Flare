# Flare Log Summary

## Overview

- **Monitoring period:** 2026-07-29 07:45:00 UTC through 2026-08-07 17:17:19 UTC
- **UTC calendar days monitored:** 10
- **Expected interval:** Every 15 minutes per chart
- **Charts monitored:** 7
- **Expected successes per chart:** 903
- **Total expected successes:** 6321
- **Total unique errors:** 2317
- **Total successes:** 4681
- **Success gap from expected:** 1640
- **Total successes without missing data:** 4176
- **Overall success rate:** 74.1%
- **Overall success rate without missing data:** 66.1%

> Both success rates use expected 15-minute runs as their denominator. A unique error is one chart/timestamp combination and remains a separate diagnostic count. Multiple errors for the same chart at the exact same timestamp count once in error totals. A success is considered to have no missing data only when that chart has no Data Validation error at the exact same timestamp.

## Charts ranked by unique errors

| Rank | Chart | Unique errors | Expected successes | Actual successes | Gap from expected | Successes without missing data |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Laguna-Madre_Water-Level_Air-Temperature_120hrs | 498 | 903 | 790 | 113 | 650 |
| 2 | CRPS_120hrs | 486 | 903 | 778 | 125 | 654 |
| 3 | MRE_Bird-Island_Water-Temperature_Ribbon | 423 | 903 | 758 | 145 | 689 |
| 4 | TWC-NDFD-Laguna-Madre_Air-Temperature-Predictions_240hrs | 317 | 903 | 795 | 108 | 704 |
| 5 | TWC-NDFD-Laguna-Madre_Air-Temperature-Predictions_Box-Plot_240hrs | 274 | 903 | 802 | 101 | 721 |
| 6 | TWC-Laguna-Madre_Air-Temperature-Predictions_240hrs | 185 | 903 | 758 | 145 | 758 |
| 7 | test_1-0-0 | 134 | 903 | 0 | 903 | 0 |

## Chart details

### Laguna-Madre_Water-Level_Air-Temperature_120hrs

- **Expected successes:** 903
- **Total successes:** 790
- **Gap from expected:** 113
- **Successes without missing data:** 650
- **Unique errors:** 498
- **Raw error rows:** 937
- **Success rate:** 87.5%
- **Success rate without missing data:** 72.0%
- **Average unique errors per UTC calendar day:** 49.80
- **Worst UTC day:** 2026-07-31 (72 unique errors)
- **Worst UTC hour of day:** 03:00–03:59 (54 unique errors)
- **Worst UTC minute of hour:** minute 31 (79 unique errors)
- **Worst exact timestamp:** 2026-07-29 09:00:36 UTC (5 error rows)

#### Error-type distribution

| Error type | Unique timestamp/type occurrences | Percentage |
|---|---:|---:|
| HTTPError | 383 | 60.3% |
| DATA VALIDATION ERROR | 140 | 22.0% |
| PipelineError | 111 | 17.5% |
| ERROR | 1 | 0.2% |

> Error-type percentages use unique timestamp/type pairs. If several different error types occur at one timestamp, the timestamp counts once for each represented type in this table but only once in the chart's unique-error total.

### CRPS_120hrs

- **Expected successes:** 903
- **Total successes:** 778
- **Gap from expected:** 125
- **Successes without missing data:** 654
- **Unique errors:** 486
- **Raw error rows:** 774
- **Success rate:** 86.2%
- **Success rate without missing data:** 72.4%
- **Average unique errors per UTC calendar day:** 48.60
- **Worst UTC day:** 2026-08-03 (80 unique errors)
- **Worst UTC hour of day:** 03:00–03:59 (35 unique errors)
- **Worst UTC minute of hour:** minute 16 (89 unique errors)
- **Worst exact timestamp:** 2026-07-29 19:00:39 UTC (4 error rows)

#### Error-type distribution

| Error type | Unique timestamp/type occurrences | Percentage |
|---|---:|---:|
| HTTPError | 373 | 59.8% |
| DATA VALIDATION ERROR | 124 | 19.9% |
| PipelineError | 123 | 19.7% |
| ERROR | 4 | 0.6% |

> Error-type percentages use unique timestamp/type pairs. If several different error types occur at one timestamp, the timestamp counts once for each represented type in this table but only once in the chart's unique-error total.

### MRE_Bird-Island_Water-Temperature_Ribbon

- **Expected successes:** 903
- **Total successes:** 758
- **Gap from expected:** 145
- **Successes without missing data:** 689
- **Unique errors:** 423
- **Raw error rows:** 783
- **Success rate:** 83.9%
- **Success rate without missing data:** 76.3%
- **Average unique errors per UTC calendar day:** 42.30
- **Worst UTC day:** 2026-08-05 (57 unique errors)
- **Worst UTC hour of day:** 03:00–03:59 (48 unique errors)
- **Worst UTC minute of hour:** minute 01 (75 unique errors)
- **Worst exact timestamp:** 2026-07-29 08:00:11 UTC (5 error rows)

#### Error-type distribution

| Error type | Unique timestamp/type occurrences | Percentage |
|---|---:|---:|
| HTTPError | 312 | 58.9% |
| PipelineError | 143 | 27.0% |
| DATA VALIDATION ERROR | 69 | 13.0% |
| ERROR | 6 | 1.1% |

> Error-type percentages use unique timestamp/type pairs. If several different error types occur at one timestamp, the timestamp counts once for each represented type in this table but only once in the chart's unique-error total.

### TWC-NDFD-Laguna-Madre_Air-Temperature-Predictions_240hrs

- **Expected successes:** 903
- **Total successes:** 795
- **Gap from expected:** 108
- **Successes without missing data:** 704
- **Unique errors:** 317
- **Raw error rows:** 499
- **Success rate:** 88.0%
- **Success rate without missing data:** 78.0%
- **Average unique errors per UTC calendar day:** 31.70
- **Worst UTC day:** 2026-08-05 (46 unique errors)
- **Worst UTC hour of day:** 03:00–03:59 (33 unique errors)
- **Worst UTC minute of hour:** minute 00 (65 unique errors)
- **Worst exact timestamp:** 2026-07-29 10:00:34 UTC (3 error rows)

#### Error-type distribution

| Error type | Unique timestamp/type occurrences | Percentage |
|---|---:|---:|
| HTTPError | 239 | 54.3% |
| PipelineError | 106 | 24.1% |
| DATA VALIDATION ERROR | 91 | 20.7% |
| ERROR | 4 | 0.9% |

> Error-type percentages use unique timestamp/type pairs. If several different error types occur at one timestamp, the timestamp counts once for each represented type in this table but only once in the chart's unique-error total.

### TWC-NDFD-Laguna-Madre_Air-Temperature-Predictions_Box-Plot_240hrs

- **Expected successes:** 903
- **Total successes:** 802
- **Gap from expected:** 101
- **Successes without missing data:** 721
- **Unique errors:** 274
- **Raw error rows:** 459
- **Success rate:** 88.8%
- **Success rate without missing data:** 79.8%
- **Average unique errors per UTC calendar day:** 27.40
- **Worst UTC day:** 2026-08-05 (45 unique errors)
- **Worst UTC hour of day:** 08:00–08:59 (20 unique errors)
- **Worst UTC minute of hour:** minute 45 (55 unique errors)
- **Worst exact timestamp:** 2026-07-29 17:15:30 UTC (3 error rows)

#### Error-type distribution

| Error type | Unique timestamp/type occurrences | Percentage |
|---|---:|---:|
| HTTPError | 215 | 54.2% |
| PipelineError | 99 | 24.9% |
| DATA VALIDATION ERROR | 81 | 20.4% |
| ERROR | 2 | 0.5% |

> Error-type percentages use unique timestamp/type pairs. If several different error types occur at one timestamp, the timestamp counts once for each represented type in this table but only once in the chart's unique-error total.

### TWC-Laguna-Madre_Air-Temperature-Predictions_240hrs

- **Expected successes:** 903
- **Total successes:** 758
- **Gap from expected:** 145
- **Successes without missing data:** 758
- **Unique errors:** 185
- **Raw error rows:** 284
- **Success rate:** 83.9%
- **Success rate without missing data:** 83.9%
- **Average unique errors per UTC calendar day:** 18.50
- **Worst UTC day:** 2026-08-03 (25 unique errors)
- **Worst UTC hour of day:** 16:00–16:59 (17 unique errors)
- **Worst UTC minute of hour:** minute 00 (47 unique errors)
- **Worst exact timestamp:** 2026-07-29 08:00:22 UTC (2 error rows)

#### Error-type distribution

| Error type | Unique timestamp/type occurrences | Percentage |
|---|---:|---:|
| PipelineError | 143 | 50.4% |
| HTTPError | 136 | 47.9% |
| ERROR | 5 | 1.8% |

> Error-type percentages use unique timestamp/type pairs. If several different error types occur at one timestamp, the timestamp counts once for each represented type in this table but only once in the chart's unique-error total.

### test_1-0-0

- **Expected successes:** 903
- **Total successes:** 0
- **Gap from expected:** 903
- **Successes without missing data:** 0
- **Unique errors:** 134
- **Raw error rows:** 185
- **Success rate:** 0.0%
- **Success rate without missing data:** 0.0%
- **Average unique errors per UTC calendar day:** 13.40
- **Worst UTC day:** 2026-08-03 (21 unique errors)
- **Worst UTC hour of day:** 08:00–08:59 (10 unique errors)
- **Worst UTC minute of hour:** minute 01 (43 unique errors)
- **Worst exact timestamp:** 2026-07-29 14:00:29 UTC (3 error rows)

#### Error-type distribution

| Error type | Unique timestamp/type occurrences | Percentage |
|---|---:|---:|
| HTTPError | 127 | 77.0% |
| PipelineError | 33 | 20.0% |
| DATA VALIDATION ERROR | 4 | 2.4% |
| ERROR | 1 | 0.6% |

> Error-type percentages use unique timestamp/type pairs. If several different error types occur at one timestamp, the timestamp counts once for each represented type in this table but only once in the chart's unique-error total.
