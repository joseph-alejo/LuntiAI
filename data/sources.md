# LuntiAI — Philippine Crop Dataset: Data Sources & Methodology

## Overview
This document details the data sources, methodology, and validation approach
used to generate the `philippine_crop_dataset.csv` training data for the
LuntiAI crop recommendation model.

## Methodology: Domain-Constrained Synthetic Data Generation

This project uses **synthetic data generation** for its classroom prototype.
The records are not field measurements. The references below record the original
project's source claims; their inclusion does not independently validate each
range, correlation, or generated crop label.

### How It Works
1. **Expert Knowledge Extraction**: We collected optimal growing condition ranges
   (NPK, pH, temperature, humidity, rainfall) for 12 Philippine crops from
   authoritative government and research sources.
2. **Clipped Normal Sampling**: For each crop-feature pair, the generator samples
   a normal distribution, clips values to the profile bounds, and adds small
   boundary jitter. Despite the helper name `truncated_normal`, this is not
   sampling from a mathematically truncated normal distribution.
3. **Assumed Correlations**: The generator introduces correlations:
   - Rainfall ↔ pH (inverse: more rain → more acidic soil from base leaching)
   - Temperature ↔ Humidity (positive: tropical coupling)
   - Seasonal variation noise on rainfall values
4. **Validation**: All generated values are clipped to physically valid ranges.

---

## Data Sources by Crop

### Rice (Irrigated Lowland)
- **PhilRice** — Rice Crop Manager (RCM) nutrient decision tool
  - URL: https://www.philrice.gov.ph/
  - NPK recommendations for irrigated lowland rice in Region XI
- **DA-RFO XI** — Department of Agriculture Regional Field Office XI
  - Rice production protocols for Davao del Norte

### Banana (Cavendish)
- **Yara Philippines** — Banana Crop Nutrition Guide
  - URL: https://www.yara.ph/crop-nutrition/banana/
  - NPK requirements, tissue analysis targets
- **TADECO / Hijo Resources** — Commercial banana cultivation data (Tagum-based)
- **DA Region XI** — Banana Industry Roadmap

### Cacao
- **ACDI/VOCA** — Philippines Cacao Industry Development Program
- **ICRAF (World Agroforestry)** — Cacao agroforestry systems in Mindanao
- **DA Region XI Cacao Development Program** — Growing condition guides

### Coconut
- **PCA (Philippine Coconut Authority)** — Coconut Production Technoguide
  - URL: https://pca.gov.ph/
  - Fertilizer recommendations per tree, soil requirements
- **UPLB-BIOTECH** — Coconut tissue culture and nutrition studies

### Durian
- **DA Mindanao** — Durian Industry Development Program
- **PCARRD-DOST** — Durian production technology guide
- **Davao Region Durian Growers Association** — Best practices

### Corn (Yellow)
- **PhilMaize** — National Corn Program
  - Nutrient management for yellow corn varieties
- **DA Corn Production Guide** — Region XI specific recommendations

### Mango
- **PCARRD** — Mango Production Technology
- **National Mango Industry Development Program** — DA
- **UPLB Crop Science** — Mango nutrient management research

### Papaya
- **DA Crop Production Guide** — Papaya cultivation in Mindanao
- **PCAARRD** — Papaya production technology bulletin

### Cassava
- **PhilRootcrops (VSU)** — Visayas State University root crops program
  - Cassava nutrient requirements and soil tolerance ranges
- **DA Root Crops Program** — Region XI

### Sweet Potato (Kamote)
- **UPLB** — Sweet potato breeding and agronomy publications
- **DA Root Crops Program** — Production guide
- **PhilRootcrops** — Soil and nutrient requirements

### Eggplant (Talong)
- **PCAARRD** — Eggplant production technology
- **DA Vegetable Program** — Recommended practices for Region XI
- **UPLB Horticulture** — Nutrient management studies

### Tomato (Kamatis)
- **PCAARRD** — Tomato production technology
- **DA Vegetable Program** — Highland and lowland tomato production
- **UPLB** — Tomato nutrient and pH requirements

---

## Climate Data Sources

### PAGASA (Philippine Atmospheric, Geophysical & Astronomical Services Administration)
- **Climatological Normals** for Davao City / Tagum Station
  - 30-year averages (1991-2020)
  - Temperature: 23°C - 32°C (avg 27.5°C)
  - Humidity: 75% - 85% (avg ~80%)
  - Rainfall: ~2000mm/year (distributed, no distinct dry season)
  - URL: https://www.pagasa.dost.gov.ph/

---

## Soil Data Sources

### BSWM (Bureau of Soils and Water Management)
- **National Soil Sampling & Testing Program**
  - Soil types in Davao del Norte: Inceptisols (dominant), Alfisols, Ultisols
  - Textures: Clay loam, Sandy clay loam, Loam
  - pH range: 4.5 - 7.0 (mostly slightly acidic due to volcanic parent material)
  - URL: https://www.bswm.da.gov.ph/

### Tagum City Agriculture Office
- Barangay-level commodity profiles
- Soil type mapping for 23 barangays

---

## Dataset Statistics
- **Total samples**: 120,000
- **Crops**: 12
- **Features**: 8 (N, P, K, temperature, humidity, ph, rainfall, OM)
- **Distribution**: Slightly imbalanced by generator design; not a measured prevalence estimate

## Limitations & Future Work
The October 30, 2026 course notebook documents the split, provenance limitations,
and XAI evaluation. Its synthetic holdout scores do not establish farm performance.
Rainfall period, nutrient measurement protocols, and reference ranges require
independent verification before use with field measurements.
1. Synthetic data approximates real-world distributions but cannot capture all
   microclimate and soil heterogeneity within individual barangays
2. Future iterations should incorporate actual field measurements from the
   Tagum City Agriculture Office and BSWM Regional Laboratory
3. Soil sensor (IoT) integration would enable real-time data collection to
   continuously improve the model

---

*Document prepared by the LuntiAI Team for the Technopreneurship Academic Festival*
