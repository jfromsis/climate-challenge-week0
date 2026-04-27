import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from utils import load_data, preprocess

st.set_page_config(page_title="Climate Dashboard", layout="wide")

st.title("🌍 Climate Vulnerability Dashboard")

# Load & preprocess
try:
    df = load_data()
    df = preprocess(df)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# =========================
# 🎛 Sidebar Filters
# =========================
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

variable = st.sidebar.selectbox(
    "Select Variable",
    ["T2M", "PRECTOTCORR", "RH2M"]
)

# =========================
# 🔍 Filter Data
# =========================
filtered_df = df[
    (df["Country"].isin(countries)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# =========================
# 📈 Trend Chart
# =========================
st.subheader("📈 Climate Trend")

fig, ax = plt.subplots()

for country in countries:
    temp = filtered_df[filtered_df["Country"] == country]
    monthly = temp.groupby("Month")[variable].mean()

    ax.plot(monthly.index, monthly.values, label=country)

ax.set_xlabel("Month")
ax.set_ylabel(variable)
ax.legend()

st.pyplot(fig)

# =========================
# 📦 Boxplot
# =========================
st.subheader("📦 Precipitation Distribution")

fig2, ax2 = plt.subplots()

sns.boxplot(
    data=filtered_df,
    x="Country",
    y="PRECTOTCORR",
    ax=ax2
)

st.pyplot(fig2)