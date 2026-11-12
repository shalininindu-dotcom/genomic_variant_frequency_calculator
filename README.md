# Genomic Variant Frequency Calculator

A web app that calculates how frequently a genetic variant (mutation) appears
across a group of samples, built with Python and Streamlit.

## What it does

You upload a CSV file listing genetic variants and the genotype of each
sample at that position. The app calculates the **allele frequency** for
each variant and shows it in a table and a chart.

**Allele frequency** = how often the mutant (alternate) version of a
position shows up, compared to the normal (reference) version, across all
samples.

## Input file format

Your CSV needs these columns:

| Chromosome | Position | Ref | Alt | Sample1 | Sample2 | ... |
|---|---|---|---|---|---|---|
| 1 | 12345 | A | G | 0/0 | 0/1 | ... |

- `Chromosome`, `Position`, `Ref`, `Alt` describe the variant itself.
- Each `SampleX` column holds that sample's genotype:
  - `0/0` = no mutation (homozygous reference)
  - `0/1` = one mutant copy (heterozygous)
  - `1/1` = mutation on both copies (homozygous alternate)
  - `./.` = missing data

A working example is included: `sample_data.csv`.

## Running it locally

1. Install Python 3.9+.
2. Open a terminal in this folder and install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```
4. It will open automatically in your browser at `http://localhost:8501`.

## Deploying it for free (so it's live on the internet)

1. Push this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with
   GitHub.
3. Click "New app", pick your repository, and set the main file to `app.py`.
4. Click Deploy. You'll get a public URL you can share and put in your
   GitHub README.

Note: GitHub Pages alone can't run this app, since it only hosts static
HTML/CSS/JS and this app needs a live Python backend. Streamlit Community
Cloud (above) is the free way to actually run it.

## Team roles (example split)

- **Person A:** Variant frequency calculation logic (`calculate_allele_frequency`,
  `calculate_samples_genotyped` in `app.py`), testing with different datasets.
- **Person B:** Streamlit interface, file upload, chart, filtering, deployment,
  README/documentation.

## Possible extensions (if you want to go further)

- Support real VCF files (not just CSV) using the `pysam` or `cyvcf2` library.
- Group frequency by population/ancestry if that data is available.
- Highlight variants above a frequency threshold (e.g., common vs. rare).
- Add a search box to look up a specific gene or position.
