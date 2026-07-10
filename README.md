# Dutch Healthcare Cost Benchmark Analysis Using Vektis Open Data 2023

An end-to-end healthcare analytics project that compares actual municipality-level healthcare costs with age–sex-adjusted expected costs across the Netherlands.

**Author:** Mahdi Dadgar  
**Data source:** Vektis Open Databestand Zorgverzekeringswet 2023 — municipality level

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vektis-healthcare-benchmark.streamlit.app)

[Live Application](https://vektis-healthcare-benchmark.streamlit.app) | [GitHub Profile](https://github.com/mahdidadgar-data) | [LinkedIn](https://www.linkedin.com/in/mahdi-dadgar-777240116/)

---

## Project overview

Dutch municipalities differ considerably in population structure. A municipality with a relatively older population may naturally have higher healthcare expenditure than a younger municipality.

For that reason, comparing raw healthcare costs alone can be misleading.

In this project, I use indirect age–sex standardisation to estimate how much each municipality would be expected to spend if its residents experienced the national average healthcare cost rate for their age and sex group.

The central analytical question is:

> Which Dutch municipalities show higher or lower healthcare costs than expected after accounting for differences in age and sex composition?

The results are presented through reproducible Jupyter notebooks, analytical tables, professional visualisations, and an interactive Streamlit application.

---

## Live interactive application

The project includes a deployed Streamlit application that allows users to explore the benchmark results for all 342 municipalities.

### Open the application

**[Launch the Dutch Healthcare Cost Benchmark app](https://vektis-healthcare-benchmark.streamlit.app)**

The application allows users to:

- select any Dutch municipality
- view actual and expected healthcare costs
- inspect the municipality's Standardised Cost Ratio
- review the percentage difference from expectation
- examine the euro gap per insured year
- see the municipality's position in the national SCR distribution
- explore category-level actual-to-expected ratios
- inspect positive and negative category-level euro contributions
- review the complete municipality ranking
- identify municipalities marked by the population-size caution heuristic

---

## Why I built this project

My background is in scientific research, applied statistics, and evidence-based analysis. I am now applying that foundation to Data Science and healthcare analytics.

I developed this project to better understand how healthcare benchmark analysis can support the investigation of regional cost variation.

The project allowed me to practise several areas that are important in real healthcare-data work:

- translating a broad healthcare question into a measurable analytical problem
- checking the structure and quality of public healthcare data
- creating a fairer comparison using case-mix adjustment
- distinguishing relative differences from absolute financial impact
- testing the stability of headline rankings
- communicating findings without making claims that the available data cannot support
- presenting analytical outputs through an interactive decision-support application

---

## Dataset

The project uses the:

**Vektis Open Databestand Zorgverzekeringswet 2023 — gemeente**

Official source:

https://www.vektis.nl/open-data

The source data contains aggregated healthcare costs paid by Dutch health insurers under the Zorgverzekeringswet, grouped by:

- municipality
- five-year age class
- sex

The dataset contains:

- 12,989 original rows
- 342 municipalities
- 19 age classes
- 2 sex categories
- 26 detailed healthcare cost fields

One Vektis rest-category row without usable municipality, age, and sex dimensions is excluded from municipality-level standardisation.

The final analytical dataset contains 12,988 rows.

Eight possible municipality–age–sex combinations are absent from the published data. These combinations are documented but are not imputed because the aggregated dataset does not provide defensible replacement values.

### Repository data policy

The original Vektis CSV and the locally generated processed Parquet file are not stored in this repository.

Instructions for downloading and placing the source file are available in:

```text
data/README.md
```

The repository contains only:

- analytical code
- notebooks
- derived summary tables
- visualisations
- documentation
- the Streamlit application

---

## Analytical method

### 1. National age–sex reference rates

For every age–sex group, I calculate the national healthcare cost rate:

```text
National age–sex cost rate =
Total healthcare cost in the age–sex group
÷
Total insured years in the age–sex group
```

The rates are weighted by insured years rather than municipality count.

### 2. Expected municipality cost

For each municipality–age–sex combination:

```text
Expected cost =
Municipality insured years
×
National age–sex cost rate
```

The expected values are then summed across all age–sex groups within each municipality.

### 3. Standardised Cost Ratio

The main relative benchmark is the Standardised Cost Ratio:

```text
SCR =
Actual municipality healthcare cost
÷
Expected municipality healthcare cost
```

Interpretation:

- **SCR above 1.00:** actual costs are above the age–sex-adjusted expectation
- **SCR close to 1.00:** actual costs are close to the expectation
- **SCR below 1.00:** actual costs are below the expectation

### 4. Absolute financial difference

The analysis also calculates:

```text
Euro gap =
Actual cost
-
Expected cost
```

SCR and euro gap answer different questions:

- SCR shows the proportional difference from expectation.
- Euro gap shows the absolute financial scale of the difference.

A municipality can have a high SCR but a relatively small euro gap, while a large municipality can have a moderate SCR and a substantial euro gap.

---

## Data-quality checks

The analytical workflow includes checks for:

- missing dimension values
- duplicate municipality–age–sex combinations
- missing combinations
- zero or negative insured-year values
- negative healthcare costs
- rest-category records
- category-to-total reconciliation
- national actual-versus-expected reconciliation

Key quality results:

| Check | Result |
|---|---:|
| Rows available for analysis | 12,988 |
| Municipalities | 342 |
| Age classes | 19 |
| Sex categories | 2 |
| Missing municipality–age–sex combinations | 8 |
| Duplicate dimension combinations | 0 |
| Rest-category rows excluded | 1 |
| Zero or negative insured-year rows | 0 |
| Negative total-cost rows | 0 |
| Rest-category share of national cost | Approximately 0.24% |

National actual and expected healthcare costs reconcile, apart from negligible floating-point precision.

---

## Population-size sensitivity

The public dataset does not provide enough information to calculate formal confidence intervals around municipality SCR values.

To support cautious interpretation, municipalities in the bottom quartile by insured years receive a:

```text
small_population_caution_flag
```

This is a descriptive sensitivity heuristic, not a statistical confidence classification.

The threshold is approximately:

```text
22,492 insured years
```

A total of 86 out of 342 municipalities are marked by this heuristic.

The sensitivity check showed:

- 9 of the top 10 SCR municipalities remained in the headline list after excluding size-flagged municipalities.
- Only 2 of the bottom 10 remained.

This suggests that the higher-than-expected end of the ranking is relatively stable under this rule, while the lower-than-expected end is more sensitive to municipality size.

The association between municipality size and absolute SCR deviation was weak:

```text
Pearson association: -0.088
Spearman rank association: -0.168
```

These associations are descriptive and should not be interpreted as statistical evidence.

---

## Care-category analysis

The 26 detailed Vektis cost fields are mapped transparently into 11 broader categories:

1. Dental care
2. General practice
3. Maternity care
4. Medical devices
5. Medical specialist care
6. Mental health care (GGZ)
7. Nursing, rehabilitation, and short-stay care
8. Other Zvw care
9. Paramedical care
10. Patient transport
11. Pharmacy

The same age–sex standardisation method is applied separately to every category.

This makes it possible to distinguish:

- the category with the highest relative actual-to-expected ratio
- the category contributing the largest absolute euro amount to the municipality-level gap

These are not necessarily the same category.

---

## Selected results

Among municipalities not marked by the population-size heuristic, the strongest higher-than-expected signals were:

| Municipality | SCR | Difference from expected |
|---|---:|---:|
| Heerlen | 1.243 | +24.3% |
| Brunssum | 1.219 | +21.9% |
| Kerkrade | 1.210 | +21.0% |
| Stadskanaal | 1.187 | +18.7% |
| Emmen | 1.181 | +18.1% |

The strongest lower-than-expected signals not marked by the heuristic included:

| Municipality | SCR | Difference from expected |
|---|---:|---:|
| Koggenland | 0.847 | -15.3% |
| Nieuwkoop | 0.856 | -14.4% |
| Medemblik | 0.866 | -13.4% |
| Bergen NH | 0.867 | -13.3% |
| Aalsmeer | 0.870 | -13.0% |

In the highest-SCR spotlight municipalities, medical specialist care was an important absolute contributor to the positive euro gap.

The category analysis also demonstrated that the highest relative ratio was not always the category with the largest euro contribution.

These results are descriptive signals for further investigation. They do not prove inappropriate care, inefficiency, or differences in healthcare quality.

---

## Visual results

### Municipalities furthest from the age–sex-adjusted expectation

![Top and bottom municipality benchmark results](outputs/figures/01_top_bottom_scr.png)

### Distribution of Standardised Cost Ratios

![Distribution of municipality SCR values](outputs/figures/02_scr_distribution.png)

### SCR versus municipality population size

![Municipality SCR versus insured years](outputs/figures/03_scr_vs_population_size.png)

### Care-category ratios for selected municipalities

![Care-category breakdown for spotlight municipalities](outputs/figures/04_category_breakdown_outliers.png)

---

## Streamlit application

The application reads the derived analytical tables produced by the notebook workflow. It does not recalculate the benchmark when a user selects a municipality.

This separation keeps the application:

- fast
- transparent
- reproducible
- independent of the excluded raw data file

### Public application

**https://vektis-healthcare-benchmark.streamlit.app**

### Run the application locally

From the project root:

```bash
streamlit run app/streamlit_app.py
```

The app uses:

```text
outputs/tables/municipality_benchmark.csv
```

and:

```text
outputs/tables/category_breakdown_all_municipalities.csv
```

---

## Project structure

```text
dutch-healthcare-cost-benchmark-vektis-2023/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── .gitkeep
│   └── README.md
│
├── notebooks/
│   ├── 01_data_understanding_and_quality_check.ipynb
│   ├── 02_age_sex_adjusted_benchmarking.ipynb
│   └── 03_results_and_visualization.ipynb
│
├── outputs/
│   ├── figures/
│   │   ├── 01_top_bottom_scr.png
│   │   ├── 02_scr_distribution.png
│   │   ├── 03_scr_vs_population_size.png
│   │   └── 04_category_breakdown_outliers.png
│   │
│   └── tables/
│
├── reports/
│   └── findings_report.md
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Notebook workflow

### Notebook 01 — Data understanding and quality checks

```text
notebooks/01_data_understanding_and_quality_check.ipynb
```

This notebook:

- loads the Vektis source data
- inspects columns and data types
- identifies healthcare cost variables
- creates analytical variables
- checks municipality–age–sex completeness
- documents the Vektis rest category
- validates the final analytical dataset
- saves the processed local Parquet file
- saves reproducible quality-control tables

### Notebook 02 — Age–sex-adjusted benchmarking

```text
notebooks/02_age_sex_adjusted_benchmarking.ipynb
```

This notebook:

- calculates national age–sex reference rates
- calculates municipality expected costs
- creates SCR and euro-gap measures
- applies the population-size caution heuristic
- performs ranking-sensitivity analysis
- maps 26 detailed cost fields into 11 broader categories
- calculates category-level actual and expected costs
- verifies category reconciliation
- saves benchmark tables for reporting and the application

### Notebook 03 — Results and visualisation

```text
notebooks/03_results_and_visualization.ipynb
```

This notebook:

- creates headline benchmark tables
- produces four portfolio-ready figures
- analyses the SCR distribution
- examines the relationship between SCR deviation and municipality size
- compares category ratios across six spotlight municipalities
- distinguishes relative and absolute category drivers
- prepares interview-ready analytical findings

---

## Analytical output tables

The project includes derived analytical tables such as:

- `municipality_benchmark.csv`
- `category_breakdown_all_municipalities.csv`
- `category_breakdown_outliers.csv`
- `national_age_sex_reference_rates.csv`
- `benchmark_sensitivity_summary.csv`
- `category_mapping.csv`
- `data_quality_summary.csv`
- `missing_dimension_combinations.csv`
- `rest_category_summary.csv`
- `distribution_summary.csv`
- `headline_findings.csv`
- `size_association_summary.csv`
- `spotlight_category_drivers.csv`
- `visualization_headline_table.csv`

These tables improve transparency and allow the application and reports to use the same validated analytical outputs.

---

## Installation and reproducibility

### 1. Clone the repository

```bash
git clone https://github.com/mahdidadgar-data/dutch-healthcare-cost-benchmark-vektis-2023.git
cd dutch-healthcare-cost-benchmark-vektis-2023
```

### 2. Create a virtual environment

On Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 4. Download the Vektis dataset

Download the municipality-level 2023 dataset from:

https://www.vektis.nl/open-data

Place it at:

```text
data/raw/Vektis Open Databestand Zorgverzekeringswet 2023 - gemeente.csv
```

### 5. Run the notebooks in order

```text
01_data_understanding_and_quality_check.ipynb
02_age_sex_adjusted_benchmarking.ipynb
03_results_and_visualization.ipynb
```

### 6. Run the Streamlit application

```powershell
streamlit run app/streamlit_app.py
```

---

## Technologies used

- Python
- pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- PyArrow
- Jupyter Notebook
- indirect age–sex standardisation
- descriptive sensitivity analysis
- healthcare cost benchmarking
- interactive data visualisation

---

## Limitations

This analysis has several important limitations:

- The source data is aggregated, creating a risk of ecological interpretation.
- Adjustment covers age and sex only.
- Morbidity and disease severity are not included.
- Socioeconomic conditions and deprivation are not included.
- Urbanisation and regional healthcare supply are not included.
- Coding behaviour and patient preferences are not included.
- Clinical outcomes and healthcare quality indicators are unavailable.
- The analysis covers one year only.
- The population-size flag is a heuristic rather than a confidence interval.
- No formal spatial model or statistical significance test is used.
- Municipality-level results cannot be attributed to individual hospitals, clinicians, or providers.

A stronger future extension would combine multiple years, richer case-mix variables, uncertainty intervals, and spatial or provider-level data.

---

## Responsible interpretation

An SCR above 1.00 does not automatically mean that care is inefficient, unnecessary, or inappropriate.

An SCR below 1.00 does not automatically mean that care is more efficient or better.

Observed variation may reflect:

- differences in population health
- socioeconomic conditions
- healthcare availability
- regional referral patterns
- coding and declaration practices
- patient preferences
- unobserved clinical need

The results should therefore be used to generate questions and priorities for further analysis, not to make unsupported judgements.

---

## What I learned

This project strengthened my understanding of several important healthcare-data principles:

- fair benchmarking requires more than comparing raw totals
- adjustment variables must be chosen and explained carefully
- data-quality limitations should be visible rather than hidden
- relative ratios and absolute financial impact should be reported together
- ranking stability should be tested before presenting headline conclusions
- aggregated data supports investigation but not individual-level or causal conclusions
- technical results become more useful when translated into clear decision-support language
- analytical findings can be made more accessible through an interactive application

---

## Possible future extensions

Potential next steps include:

1. combining multiple years of Vektis data
2. evaluating whether municipality patterns persist over time
3. incorporating socioeconomic and deprivation indicators
4. adding urbanisation and healthcare-supply variables
5. incorporating morbidity or chronic-disease indicators
6. calculating formal uncertainty intervals or funnel plots
7. performing spatial analysis across neighbouring municipalities
8. connecting cost patterns with clinical outcome or quality indicators
9. developing provider-level analyses where appropriate data is legally and ethically available

---

## Full findings report

A detailed interpretation of the methodology, findings, sensitivity analysis, and limitations is available here:

**[Read the full findings report](reports/findings_report.md)**

---

## Author

**Mahdi Dadgar**

PhD-trained analytical professional transitioning into Data Science, Machine Learning, Business Intelligence, healthcare analytics, and Responsible AI.

- Live application: https://vektis-healthcare-benchmark.streamlit.app
- GitHub: https://github.com/mahdidadgar-data
- LinkedIn: https://www.linkedin.com/in/mahdi-dadgar-777240116/