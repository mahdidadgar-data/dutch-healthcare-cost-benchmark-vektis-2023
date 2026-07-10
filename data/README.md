# Data

## Source

This project uses the **Vektis Open Databestand Zorgverzekeringswet 2023 — gemeente** dataset.

Official source:

https://www.vektis.nl/open-data

The dataset contains aggregated healthcare costs paid by Dutch health insurers under the Zorgverzekeringswet (Zvw), grouped by municipality, five-year age class, and sex.

## Local file placement

The raw dataset is not stored in this GitHub repository.

After downloading the municipality-level 2023 CSV from Vektis, place it at:

```text
data/raw/Vektis Open Databestand Zorgverzekeringswet 2023 - gemeente.csv
```

Running Notebook 01 creates the cleaned local file:

```text
data/processed/vektis_2023_clean.parquet
```

## Data-use conditions

The Vektis open datasets are available for personal and research purposes. Vektis states that the data may not be resold or used for commercial purposes and that the source must be acknowledged whenever the data is used.

**Source: Vektis**

## Privacy and aggregation

The dataset is aggregated and does not contain patient-level information.

Records based on fewer than 10 underlying people are assigned to a rest category to reduce disclosure risk. The rest category also includes records for which one or more demographic characteristics are unknown in the source data.

## Repository policy

To respect the source conditions and keep the repository lightweight:

- The original CSV is excluded from version control.
- The processed Parquet file is excluded from version control.
- Analytical code, derived summary tables, figures, and documentation are included.