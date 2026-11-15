import os

import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN = os.path.join(BASE_DIR, "data", "clean")
MIN_VIEWS = 1000

st.set_page_config(page_title="Campaign Intelligence Engine", layout="wide")


@st.cache_data
def load(name):
    path = os.path.join(CLEAN, name)
    return pd.read_csv(path) if os.path.exists(path) else None


posts = load("posts_features.csv")
comments = load("comments_final.csv")
unusual = load("unusual_posts_explained.csv")
needs = load("audience_needs_summary.csv")
recs = load("recommendations.csv")

if posts is None or comments is None:
    st.error("Run the notebook first: posts_features.csv and comments_final.csv are missing.")
    st.stop()

if "is_brand_reply_or_spam" in comments.columns:
    comments = comments[~comments["is_brand_reply_or_spam"].astype(bool)]

# ---------- sidebar filters ----------
st.sidebar.header("Filters")
all_brands = sorted(posts["brand"].dropna().unique())
brands = st.sidebar.multiselect("Brand", all_brands, default=all_brands)
min_views = st.sidebar.number_input("Minimum views per video", 0, 1_000_000, MIN_VIEWS, step=500)
st.sidebar.caption(
    "Data: public YouTube videos and comments of Khaadi, Sapphire and Limelight, collected with the "
    "YouTube Data API. Comments are a collected sample, not every comment."
)

p = posts[posts["brand"].isin(brands) & (posts["views"] >= min_views)].copy()
p["format_type"] = p["content_type"].astype(str).str.extract(r"^(.*?)\s*\(")[0].fillna(p["content_type"])
p["like_rate_per_1k"] = p["likes"] / p["views"] * 1000
c = comments[comments["brand"].isin(brands)].copy()

shop_cols = ["has_price", "has_discount", "has_availability", "has_delivery", "has_size", "has_buying_intent"]

st.title("Pakistan Social Audience & Campaign Intelligence Engine")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Videos analysed", f"{len(p):,}")
k2.metric("Comments analysed", f"{len(c):,}")
k3.metric("Shopping-related comments", f"{int(c[shop_cols].any(axis=1).sum()):,}")
k4.metric("Unusual videos flagged", f"{0 if unusual is None else int(unusual['brand'].isin(brands).sum()):,}")

t1, t2, t3, t4, t5 = st.tabs([
    "1. What content attracts attention",
    "2. What the audience wants",
    "3. Unusual posts",
    "4. Audience needs",
    "5. What to do next",
])

# ---------- tab 1 ----------
with t1:
    st.subheader("Which content attracts attention?")
    if p.empty:
        st.info("No videos match the filters.")
    else:
        g = p.groupby("format_type").agg(
            videos=("post_id", "count"),
            median_views=("views", "median"),
            median_likes_per_1k=("like_rate_per_1k", "median"),
            total_comments=("comments_count", "sum"),
            total_views=("views", "sum"),
        )
        g["comments_per_1k_views"] = (g["total_comments"] / g["total_views"] * 1000).round(3)
        g = g.drop(columns=["total_comments", "total_views"]).round(1).sort_values("median_views", ascending=False)
        a, b = st.columns(2)
        a.markdown("**Median views per video**")
        a.bar_chart(g["median_views"])
        b.markdown("**Median likes per 1,000 views**")
        b.bar_chart(g["median_likes_per_1k"])
        st.dataframe(g, use_container_width=True)
        st.caption("Small groups are noisy: check the videos column. Sale announcements are mostly Limelight videos.")

        mix = c.merge(p[["post_id", "format_type"]].drop_duplicates("post_id"), on="post_id", how="inner")
        if len(mix):
            st.markdown("**What people write under each format (% of comments)**")
            top_topics = ["price", "discount", "availability", "celebrity_music", "praise", "short_reaction"]
            mix["topic_group"] = mix["topic"].where(mix["topic"].isin(top_topics), "other")
            st.dataframe((pd.crosstab(mix["format_type"], mix["topic_group"], normalize="index") * 100).round(1),
                         use_container_width=True)

# ---------- tab 2 ----------
with t2:
    st.subheader("What does the audience want?")
    a, b = st.columns(2)
    a.markdown("**Comment topics**")
    a.bar_chart(c["topic"].value_counts())
    b.markdown("**Sentiment**")
    b.bar_chart(c["sentiment"].value_counts())
    st.markdown("**Topic mix by brand (% of the brand's comments)**")
    st.dataframe((pd.crosstab(c["topic"], c["brand"], normalize="columns") * 100).round(1), use_container_width=True)
    st.caption("Limelight has few comments, so its percentages are less reliable.")

    st.markdown("**Comment explorer**")
    f1, f2, f3 = st.columns(3)
    pick_topic = f1.selectbox("Topic", ["(all)"] + sorted(c["topic"].dropna().unique()))
    pick_int = f2.selectbox("Purchase intent", ["(all)", "Strong intent", "Possible inquiry", "None"])
    query = f3.text_input("Contains text")
    view = c
    if pick_topic != "(all)":
        view = view[view["topic"] == pick_topic]
    if pick_int != "(all)":
        view = view[view["purchase_intent"] == pick_int]
    if query:
        view = view[view["comment_text"].astype(str).str.contains(query, case=False, regex=False)]
    st.caption(f"{len(view):,} comments match")
    st.dataframe(view[["brand", "topic", "sentiment", "purchase_intent", "language_type", "comment_text"]].head(300),
                 use_container_width=True)

# ---------- tab 3 ----------
with t3:
    st.subheader("Which marketing patterns are unusual?")
    if unusual is None:
        st.info("unusual_posts_explained.csv not found.")
    else:
        u = unusual[unusual["brand"].isin(brands)]
        types = sorted(u["anomaly_type"].dropna().unique())
        pick = st.multiselect("Pattern type", types, default=types)
        u = u[u["anomaly_type"].isin(pick)]
        st.caption("Unusual means different from comparable videos of the same format. It is a prompt to investigate, "
                   "not a verdict. The cause of very high views with almost no likes cannot be confirmed from public data.")
        st.dataframe(
            u[["brand", "title", "content_type", "views", "likes", "comments_count", "anomaly_type", "explanation", "video_url"]],
            use_container_width=True,
            column_config={"video_url": st.column_config.LinkColumn("Video")},
        )

# ---------- tab 4 ----------
with t4:
    st.subheader("Which audience needs should the brand address?")
    st.markdown("**All comments: audience segments by brand (% of the brand's comments)**")
    st.dataframe((pd.crosstab(c["segment"], c["brand"], normalize="columns") * 100).round(1), use_container_width=True)
    st.markdown("**Shopping comments only: need groups**")
    if needs is None:
        st.info("audience_needs_summary.csv not found.")
    else:
        st.dataframe(needs.drop(columns=["examples"]), use_container_width=True)
        pick = st.selectbox("See example comments for", needs["need_name"])
        for ex in str(needs.loc[needs["need_name"] == pick, "examples"].iloc[0]).split(" | "):
            st.write("- " + ex)
    st.caption("Groups come from multilingual sentence embeddings and K-Means. They are soft themes: short comments overlap a lot.")

# ---------- tab 5 ----------
with t5:
    st.subheader("What should the marketing team do next?")
    if recs is None:
        st.info("recommendations.csv not found.")
    else:
        area = st.selectbox("Area", ["(all)"] + sorted(recs["area"].unique()))
        r = recs if area == "(all)" else recs[recs["area"] == area]
        for _, row in r.iterrows():
            with st.expander(f"[{row['priority']}] {row['area']}: {row['recommendation']}"):
                st.write("**Evidence:** " + str(row["evidence"]))
                if str(row.get("how_to_test", "")) not in ("", "nan"):
                    st.write("**How to test:** " + str(row["how_to_test"]))
