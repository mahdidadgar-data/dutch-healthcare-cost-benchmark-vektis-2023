"""Interactive explorer for the Vektis 2023 municipality benchmark.

The app reads analytical tables produced by Notebook 02. It does not
recalculate the benchmark.
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"

BENCHMARK_PATH = TABLES_DIR / "municipality_benchmark.csv"
CATEGORY_PATH = TABLES_DIR / "category_breakdown_all_municipalities.csv"


def format_eur(value: float) -> str:
    """Format a euro amount for compact display."""
    if abs(value) >= 1_000_000_000:
        return f"€{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"€{value / 1_000_000:.1f}M"
    return f"€{value:,.0f}"


def to_bool(series: pd.Series) -> pd.Series:
    """Convert a CSV-loaded boolean column safely."""
    if pd.api.types.is_bool_dtype(series):
        return series

    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .map({"true": True, "false": False})
        .fillna(False)
        .astype(bool)
    )


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load and validate the benchmark output tables."""
    missing_files = [
        path.name
        for path in (BENCHMARK_PATH, CATEGORY_PATH)
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Missing output file(s): "
            + ", ".join(missing_files)
            + ". Run Notebook 02 first."
        )

    benchmark = pd.read_csv(BENCHMARK_PATH)
    category = pd.read_csv(CATEGORY_PATH)

    required_benchmark_columns = {
        "rank_by_scr",
        "gemeentenaam",
        "insured_years",
        "actual_cost",
        "expected_cost",
        "scr",
        "percentage_difference",
        "euro_gap",
        "euro_gap_per_insured_year",
        "small_population_caution_flag",
    }

    required_category_columns = {
        "gemeentenaam",
        "care_category",
        "actual_cost",
        "expected_cost",
        "ratio",
        "euro_gap",
    }

    missing_benchmark_columns = required_benchmark_columns.difference(
        benchmark.columns
    )
    missing_category_columns = required_category_columns.difference(
        category.columns
    )

    if missing_benchmark_columns:
        raise ValueError(
            "The municipality benchmark is missing columns: "
            f"{sorted(missing_benchmark_columns)}"
        )

    if missing_category_columns:
        raise ValueError(
            "The category table is missing columns: "
            f"{sorted(missing_category_columns)}"
        )

    benchmark["small_population_caution_flag"] = to_bool(
        benchmark["small_population_caution_flag"]
    )

    return benchmark, category


st.set_page_config(
    page_title="Vektis 2023 Healthcare Cost Benchmark",
    layout="wide",
)

st.title("Dutch Healthcare Cost Benchmark — Vektis 2023")
st.caption(
    "Municipality-level actual healthcare cost compared with an "
    "age–sex-adjusted expected cost. An SCR of 1.00 means actual cost "
    "matches the benchmark expectation."
)

try:
    benchmark, category = load_data()
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()

municipality_names = sorted(benchmark["gemeentenaam"].dropna().unique())
default_index = (
    municipality_names.index("HEERLEN")
    if "HEERLEN" in municipality_names
    else 0
)

selected_municipality = st.selectbox(
    "Select a municipality",
    municipality_names,
    index=default_index,
)

municipality_row = benchmark.loc[
    benchmark["gemeentenaam"] == selected_municipality
].iloc[0]

if municipality_row["small_population_caution_flag"]:
    st.warning(
        "Population-size caution: this municipality is in the bottom "
        "quartile by insured years. Its SCR should be interpreted with "
        "additional care. This is a descriptive heuristic, not a formal "
        "confidence interval."
    )

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

metric_1.metric(
    "Standardised Cost Ratio",
    f"{municipality_row['scr']:.2f}",
    delta=f"{municipality_row['percentage_difference']:+.1f}%",
)

metric_2.metric(
    "Actual cost",
    format_eur(municipality_row["actual_cost"]),
)

metric_3.metric(
    "Expected cost",
    format_eur(municipality_row["expected_cost"]),
)

metric_4.metric(
    "Gap per insured year",
    f"€{municipality_row['euro_gap_per_insured_year']:,.0f}",
)

st.markdown("---")

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Position in the national SCR distribution")

    distribution_figure = go.Figure()

    distribution_figure.add_trace(
        go.Histogram(
            x=benchmark["scr"],
            nbinsx=35,
            name="Municipalities",
            hovertemplate=(
                "SCR %{x:.2f}<br>"
                "%{y} municipalities"
                "<extra></extra>"
            ),
        )
    )

    distribution_figure.add_vline(
        x=1.0,
        line_dash="dash",
        annotation_text="Expected",
        annotation_position="top left",
    )

    distribution_figure.add_vline(
        x=municipality_row["scr"],
        line_dash="dot",
        annotation_text=selected_municipality.title(),
        annotation_position="top right",
    )

    distribution_figure.update_layout(
        showlegend=False,
        xaxis_title="Standardised Cost Ratio",
        yaxis_title="Number of municipalities",
        height=420,
        margin=dict(t=40, b=40, l=40, r=20),
    )

    st.plotly_chart(
        distribution_figure,
        width="stretch",
    )

with right_column:
    st.subheader(
        f"Care-category breakdown — {selected_municipality.title()}"
    )

    category_rows = (
        category.loc[
            category["gemeentenaam"] == selected_municipality
        ]
        .copy()
    )

    ratio_tab, contribution_tab = st.tabs(
        [
            "Ratio to expected",
            "Euro contribution",
        ]
    )

    with ratio_tab:
        ratio_rows = category_rows.sort_values("ratio")

        ratio_figure = go.Figure(
            go.Bar(
                x=ratio_rows["ratio"],
                y=ratio_rows["care_category"],
                orientation="h",
                hovertemplate=(
                    "%{y}<br>"
                    "Actual / expected: %{x:.2f}"
                    "<extra></extra>"
                ),
            )
        )

        ratio_figure.add_vline(
            x=1.0,
            line_dash="dash",
        )

        ratio_figure.update_layout(
            showlegend=False,
            xaxis_title="Actual cost / expected cost",
            yaxis_title="",
            height=500,
            margin=dict(t=20, b=40, l=180, r=20),
        )

        st.plotly_chart(
            ratio_figure,
            width="stretch",
        )

        st.caption(
            "A high ratio does not necessarily mean a large financial "
            "contribution. Small categories can have high ratios while "
            "adding relatively few euros to the total municipality gap."
        )

    with contribution_tab:
        total_gap = municipality_row["euro_gap"]

        contribution_rows = (
            category_rows
            .assign(
                absolute_euro_gap=lambda frame: frame[
                    "euro_gap"
                ].abs()
            )
            .sort_values(
                "absolute_euro_gap",
                ascending=False,
            )
        )

        material_gap = (
            abs(total_gap)
            > 0.01 * municipality_row["actual_cost"]
        )

        if material_gap:
            direction = (
                "above" if total_gap >= 0 else "below"
            )

            top_drivers = contribution_rows.head(3)
            driver_text = []

            for _, driver in top_drivers.iterrows():
                effect = (
                    "adds"
                    if driver["euro_gap"] >= 0
                    else "offsets"
                )

                driver_text.append(
                    f"**{driver['care_category']}** "
                    f"({effect} "
                    f"{format_eur(abs(driver['euro_gap']))})"
                )

            st.markdown(
                f"**{selected_municipality.title()}** is "
                f"**{format_eur(abs(total_gap))} {direction} expected**. "
                "The largest category-level contributions are "
                + ", ".join(driver_text)
                + "."
            )
        else:
            st.markdown(
                f"**{selected_municipality.title()}** is within 1% of "
                "its expected total cost. Positive and negative "
                "category-level differences largely offset one another."
            )

        contribution_figure = go.Figure(
            go.Bar(
                x=contribution_rows["euro_gap"],
                y=contribution_rows["care_category"],
                orientation="h",
                hovertemplate=(
                    "%{y}<br>"
                    "Euro contribution: €%{x:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

        contribution_figure.add_vline(
            x=0,
            line_dash="dash",
        )

        contribution_figure.update_layout(
            showlegend=False,
            xaxis_title=(
                "Contribution to actual-minus-expected cost (€)"
            ),
            yaxis_title="",
            height=500,
            margin=dict(t=20, b=40, l=180, r=20),
        )

        st.plotly_chart(
            contribution_figure,
            width="stretch",
        )

        st.caption(
            "Positive values increase the municipality's total euro gap; "
            "negative values offset it. Category contributions sum to the "
            "municipality-level actual-minus-expected cost."
        )

st.markdown("---")

st.subheader("Full municipality ranking")

ranking_table = benchmark[
    [
        "rank_by_scr",
        "gemeentenaam",
        "insured_years",
        "scr",
        "percentage_difference",
        "actual_cost",
        "expected_cost",
        "euro_gap",
        "euro_gap_per_insured_year",
        "small_population_caution_flag",
    ]
].sort_values("rank_by_scr")

st.dataframe(
    ranking_table,
    width="stretch",
    hide_index=True,
    column_config={
        "rank_by_scr": "SCR rank",
        "gemeentenaam": "Municipality",
        "insured_years": st.column_config.NumberColumn(
            "Insured years",
            format="%.0f",
        ),
        "scr": st.column_config.NumberColumn(
            "SCR",
            format="%.3f",
        ),
        "percentage_difference": st.column_config.NumberColumn(
            "Difference from expected",
            format="%+.1f%%",
        ),
        "actual_cost": st.column_config.NumberColumn(
            "Actual cost",
            format="€%.0f",
        ),
        "expected_cost": st.column_config.NumberColumn(
            "Expected cost",
            format="€%.0f",
        ),
        "euro_gap": st.column_config.NumberColumn(
            "Euro gap",
            format="€%.0f",
        ),
        "euro_gap_per_insured_year": st.column_config.NumberColumn(
            "Gap per insured year",
            format="€%.0f",
        ),
        "small_population_caution_flag": (
            "Population-size caution"
        ),
    },
)

with st.expander("Method and limitations"):
    st.markdown(
        """
The expected cost is calculated by applying national age–sex-specific
healthcare cost rates to each municipality's own insured-year structure.

The resulting SCR is a descriptive benchmark:

- **Above 1.00:** actual cost is above the age–sex-adjusted expectation.
- **Near 1.00:** actual cost is close to the expectation.
- **Below 1.00:** actual cost is below the expectation.

The analysis adjusts for age and sex only. It does not control for
morbidity, socioeconomic conditions, healthcare supply, coding
practices, patient preferences, or clinical outcomes. Municipality-level
signals cannot be attributed to individual hospitals or providers.
"""
    )
