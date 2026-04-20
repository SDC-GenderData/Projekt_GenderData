# LGBTQ+ Visibility in TV Series (2020–2025)

## Project Overview
This project examines the representation of LGBTQ+ characters in television series released between 2020 and 2025. By leveraging data from Wikipedia and Wikidata, we analyze which identities are prominently featured and which groups remain underrepresented.

## Research Questions
1. **Gender Distribution**: How are LGBTQ+ characters distributed by gender?
2. **Identities**: Which forms of queer identity (lesbian, gay, bisexual, trans, non-binary) appear most frequently?
3. **Visibility**: Which groups within the LGBTQ+ community are significantly less visible or underrepresented?

## Project Structure
* **data/**: Separated into `raw` (initial data) and `processed` (cleaned data).
* **scripts/**: Contains the Python code for data extraction and preprocessing.
* **quarto/**: Modularized Quarto documents for the manuscript (e.g., introduction, methods, analysis).
* **output/**: Storage for final plots, visualizations, and result tables.

## Methodology & Tools
* **Sample**: Series with central LGBTQ+ storylines from the 2020–2025 period.
* **Data Sources**: Wikipedia lists serve as the basis; structured metadata (such as gender identity P21) is retrieved via the Wikidata Query Service (SPARQL).
* **Tech Stack**: Data analysis and visualization are performed in Python within a Quarto publishing system.