# Weather and Climate Change – Knowledge Graph

This repository contains the **Weather and Climate Change** project, developed following the **iTelos** methodology for building a **Knowledge Graph (KG)** focused on the analysis of meteorological phenomena and climate change in the **Trentino** region.

The project integrates heterogeneous data sources (open data, meteorological APIs, and historical datasets) with a semantic ontology, enabling advanced queries on climate trends, microclimates, and meteorological anomalies.

---

## 🎯 Project Objective

The main objective is to build a Knowledge Graph capable of:

- Modeling weather stations, meteorological observations, and geographical context
- Analyzing **climate trends** (e.g., temperature and precipitation variations)
- Identifying **microclimates** and **climatic anomalies**
- Supporting **Competency Questions (CQs)** defined from realistic personas and usage scenarios

The domain of interest is the **Trentino** region, with a primary temporal focus on **2010–2025**.

---

## 🧠 Methodology

The project follows the phases of the **iTelos** methodology:

1. **Purpose Definition**
   - Definition of the domain of interest
   - Personas, scenarios, and Competency Questions
   - Initial ER model

2. **Language Definition**
   - Ontology definition
   - Reuse of existing ontologies (Home Weather Ontology, Schema.org, DCAT)
   - Alignment between domain concepts and data sources

3. **Knowledge Definition**
   - Definition of classes, object properties, and data properties (OWL/RDF)
   - Complete semantic modeling of the domain

4. **Entity Definition**
   - Dataset cleaning and reduction
   - Data-to-ontology mapping using **Karma**
   - Generation of the final Knowledge Graph in **RDF/Turtle** format

---

## 📊 Data Sources

The main data sources used are:

- **Open Data Trentino**
  - Metadata and geolocation of weather stations
- **ilMeteo.it**
  - Historical daily weather data (temperature, precipitation, humidity, wind)
- **Historical Weather API (Open-Meteo)**
  - Historical and reanalysis meteorological data

The datasets were cleaned, normalized, and integrated before being transformed into RDF.

---

## 🔍 Project Output

The repository provides:

- OWL ontology for the meteorological and climatic domain
- Knowledge Graph in **RDF/Turtle** format
- Support for SPARQL queries on:
  - Temperature and precipitation trends
  - Urban microclimates
  - Anomalous and extreme weather events
  - Temporal and geographical analyses

The Knowledge Graph is ready to be loaded into **GraphDB** or any RDF-compatible triple store.

---

## 🛠️ Tools and Technologies

- **OWL / RDF / Turtle**
- **Karma** (data mapping)
- **GraphDB**
- **Protégé**
- **SPARQL**
- Reference ontologies:
  - Home Weather Ontology
  - Schema.org
  - DCAT (W3C)

---

## 👥 Authors

Project developed within the course **KGE 2025 – Weather and Climate Change**  
Department of Engineering and Information Science – University of Trento

- Michael Bernasconi  
- Gabriele Fronzoni  

---

## 📄 License

This project is released **for academic and educational use only**.  
Please refer to the individual data sources for their respective licenses.

---

## 🚧 Final Notes

The Knowledge Graph is designed to be **extensible**: new cities, time periods, or data sources can be integrated without altering the existing ontological structure.
