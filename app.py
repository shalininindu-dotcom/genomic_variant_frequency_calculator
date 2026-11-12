"""
Genomic Variant Frequency Calculator
-------------------------------------
A beginner-friendly Streamlit web app.

WHAT THIS APP DOES:
1. Lets a user upload a CSV file of genetic variants and sample genotypes.
2. For each variant (a specific position in the genome), it calculates the
   "allele frequency" - how often the ALTERNATE (mutant) version of that
   position shows up, compared to the REFERENCE (normal) version.
3. Displays the results in a table and a bar chart.

GENETICS BACKGROUND (so the code makes sense):
- Humans have 2 copies of each chromosome, so 2 "alleles" per position.
- A genotype like "0/1" means: one copy has the Reference (Ref) allele (0),
  and the other copy has the Alternate (Alt) allele (1).
- "0/0" = homozygous reference (no mutation on either copy)
- "0/1" or "1/0" = heterozygous (one normal, one mutant copy)
- "1/1" = homozygous alternate (mutation on both copies)
- "./." = missing/unknown data (that sample wasn't measured at this position)

Allele Frequency = (total number of Alt alleles counted)
                    / (total number of alleles counted, ignoring missing data)
"""

import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Genomic Variant Frequency Calculator", layout="wide")
st.title("🧬 Genomic Variant Frequency Calculator")
st.write(
    "Upload a CSV file of genetic variants and sample genotypes to calculate "
    "how frequently each variant appears in your population."
)

# ---------------------------------------------------------------------------
# STEP 1: Let the user upload a file (or use our sample data)
# ---------------------------------------------------------------------------
st.subheader("1. Upload your data")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

use_sample = st.checkbox("Or use the built-in sample dataset instead", value=not uploaded_file)

if uploaded_file is not None and not use_sample:
    df = pd.read_csv(uploaded_file)
elif use_sample:
    df = pd.read_csv("sample_data.csv")
else:
    st.info("Upload a CSV file or check the sample dataset box to get started.")
    st.stop()  # stops the app here until the user provides data

st.write("Preview of your data:")
st.dataframe(df.head())

# ---------------------------------------------------------------------------
# STEP 2: Figure out which columns are metadata vs. which are sample genotypes
# ---------------------------------------------------------------------------
# We expect columns: Chromosome, Position, Ref, Alt, then one column per sample
metadata_columns = ["Chromosome", "Position", "Ref", "Alt"]
sample_columns = [col for col in df.columns if col not in metadata_columns]

missing_columns = [col for col in metadata_columns if col not in df.columns]
if missing_columns:
    st.error(f"Your CSV is missing required columns: {missing_columns}")
    st.stop()

# ---------------------------------------------------------------------------
# STEP 3: Calculate allele frequency for each variant (each row)
# ---------------------------------------------------------------------------
def calculate_allele_frequency(row):
    """
    Given one row (one variant), look across all sample genotype columns
    and count how many alleles are Alt (1) vs total alleles counted.
    """
    alt_count = 0
    total_count = 0

    for sample in sample_columns:
        genotype = str(row[sample])

        if genotype == "./." or genotype == "nan":
            continue  # skip missing data

        # genotype looks like "0/1", "1/1", "0/0" etc.
        alleles = genotype.replace("|", "/").split("/")

        for allele in alleles:
            if allele in ("0", "1"):
                total_count += 1
                if allele == "1":
                    alt_count += 1

    if total_count == 0:
        return 0.0  # avoid dividing by zero if all samples are missing

    return round(alt_count / total_count, 3)


def calculate_samples_genotyped(row):
    """Count how many samples had usable (non-missing) genotype data."""
    count = 0
    for sample in sample_columns:
        genotype = str(row[sample])
        if genotype != "./." and genotype != "nan":
            count += 1
    return count


df["Alt_Allele_Frequency"] = df.apply(calculate_allele_frequency, axis=1)
df["Samples_Genotyped"] = df.apply(calculate_samples_genotyped, axis=1)

# ---------------------------------------------------------------------------
# STEP 4: Let the user filter results by chromosome
# ---------------------------------------------------------------------------
st.subheader("2. Results")

chromosomes = ["All"] + sorted(df["Chromosome"].astype(str).unique().tolist())
selected_chrom = st.selectbox("Filter by chromosome", chromosomes)

if selected_chrom != "All":
    filtered_df = df[df["Chromosome"].astype(str) == selected_chrom]
else:
    filtered_df = df

# Build a friendly label for each variant, e.g. "chr1:12345 A>G"
filtered_df = filtered_df.copy()
filtered_df["Variant"] = (
    "chr" + filtered_df["Chromosome"].astype(str)
    + ":" + filtered_df["Position"].astype(str)
    + " " + filtered_df["Ref"] + ">" + filtered_df["Alt"]
)

st.dataframe(
    filtered_df[["Variant", "Chromosome", "Position", "Ref", "Alt",
                 "Alt_Allele_Frequency", "Samples_Genotyped"]],
    use_container_width=True,
)

# ---------------------------------------------------------------------------
# STEP 5: Show a bar chart of allele frequencies
# ---------------------------------------------------------------------------
st.subheader("3. Allele Frequency Chart")

chart_data = filtered_df.set_index("Variant")["Alt_Allele_Frequency"]
st.bar_chart(chart_data)

# ---------------------------------------------------------------------------
# STEP 6: Let the user download the results
# ---------------------------------------------------------------------------
st.subheader("4. Download results")

csv_output = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download results as CSV",
    data=csv_output,
    file_name="variant_frequencies.csv",
    mime="text/csv",
)
