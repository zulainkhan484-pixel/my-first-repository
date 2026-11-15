# Pakistan Social Audience & Campaign Intelligence Engine

## Project 3 — Clustering-Based Marketing Intelligence

A Streamlit dashboard that analyzes public YouTube videos and a collected sample of comments from Pakistani fashion brands to answer five marketing questions:

1. What content attracts attention?
2. What does the audience want?
3. Which marketing patterns are unusual?
4. Which audience needs should the brand address?
5. What should the marketing team do next?

## Demonstrated dashboard
- 2,083 videos analyzed
- 6,220 comments analyzed
- 477 shopping-related comments
- 64 unusual videos flagged

## Main techniques
- Data cleaning and feature engineering
- Multilingual sentence embeddings
- K-Means clustering for audience needs
- Content-format performance analysis
- Isolation Forest / anomaly detection workflow
- Topic and sentiment summaries
- Evidence-based recommendation generation
- Streamlit dashboard

## Project structure

```text
project3/
├── app.py
├── Project_3_Final_Report.docx
├── requirements.txt
├── README.md
├── data/
│   └── clean/
│       ├── posts_features.csv
│       ├── comments_final.csv
│       ├── audience_needs_summary.csv
│       ├── unusual_posts_explained.csv
│       ├── content_performance_by_format.csv
│       ├── comment_mix_by_format.csv
│       ├── recommendations.csv
│       └── recommendations.json
└── screenshots/
    ├── 01_content_attention.png
    ├── 02_audience_wants.png
    ├── 03_unusual_posts.png
    ├── 04_audience_needs.png
    └── 05_what_to_do_next.png
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app expects the cleaned CSV files under `data/clean/`.

## Data note

The project uses public YouTube videos/comments collected with the YouTube Data API. Do not upload API keys, credentials, or private data to GitHub. Keep source URLs, collection dates, provenance, and reuse permissions with the dataset documentation where applicable.

## Screenshots

The five dashboard screenshots document the five required business questions.

## Limitations

This is a class/project demonstration based on a collected public-data sample. It is not a complete representation of every comment or every social platform. Anomaly findings are investigation prompts rather than proof of causation.

