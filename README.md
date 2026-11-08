# Big Data Analytics - Project 1: Limelight YouTube Analysis

From 470 YouTube videos to a marketing decision.

## Business question
Which kinds of Limelight videos get the most attention and the best audience response, and what should the marketing team publish and test next?

## Dataset
- File: `Limelight_YouTube_Data.csv`
- Content: public metadata of videos on the *Limelight Official* YouTube channel (470 rows, 11 columns): title, description, publish date, views, likes, comment count, duration, tags, URL.
- Source / provenance: The dataset was collected by me using the YouTube Data API v3 on 8 November 2026. It contains public metadata of the videos on the Limelight Official YouTube channel (470 videos, published between November 2018 and November 2026). Views, likes and comments are a snapshot of the collection date and will change over time. The data was collected through the official API and used only for this academic project.
- One row = one video.

## Tools
CSV, Google Colab, Pandas, Matplotlib, scikit-learn (small demo only).

## Files
| File | Purpose |
|---|---|
| `Limelight_Project1.ipynb` | Full analysis notebook (data quality, EDA, charts, interpretation, scaling experiment, analytics demo) |
| `Limelight_YouTube_Data.csv` | Original dataset (unmodified) |
| `README.md` | This file |

## How to run
1. Open `Limelight_Project1.ipynb` in Google Colab.
2. Upload `Limelight_YouTube_Data.csv` in the Colab file panel.
3. Run all cells (Runtime > Run all).

## Method (summary)
1. **Inspect** shape, types, missing values and duplicates.
2. **Data dictionary** and observational unit (a video).
3. **EDA**: statistics (mean vs median, concentration of views) and charts.
4. **Content categories** derived from title keywords (approximate, rule-based).
5. **Business interpretation**: finding, evidence, action, limitation.
6. **Scaling experiment**: the same data repeated 1x, 10x and 100x to measure load time, analysis time, file size and memory. This is a scaling experiment, not new real-world evidence.
7. **Analytics preview**: classification demo that avoids data leakage (the target is not used as a feature; train/test split).

## Key limitations
- No reach, impressions or subscriber counts per date.
- Older videos have had longer to collect views.
- No paid-versus-organic information.
- Categories come from simple title keywords and some groups are small.
- One channel on one platform (YouTube); does not cover Instagram.

## Author
Zulain Khan (f2023332089), Big Data Analytics, 8 November 2026
