import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    """서울 기온 데이터를 불러옵니다."""
    df = pd.read_csv(DATA_URL)

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 평균기온을 숫자형으로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 결측값 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    return df


# 데이터 불러오기
df = load_data()

# 연도 추출
df["연도"] = df["날짜"].dt.year

# 연도별 평균기온 계산
yearly_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

# 소수점 둘째 자리까지 표시
yearly_temp["평균기온"] = yearly_temp["평균기온"].round(2)


# -----------------------------
# 화면
# -----------------------------

st.title("🌡️ 서울의 연평균 기온 변화")
st.markdown(
    "서울의 기온 데이터를 이용해 **연도별 평균기온이 어떻게 변해 왔는지** 살펴봅니다."
)

st.divider()

# 전체 기간 표시
start_year = int(yearly_temp["연도"].min())
end_year = int(yearly_temp["연도"].max())

st.subheader(f"📈 {start_year}년 ~ {end_year}년 연평균 기온")

st.line_chart(
    yearly_temp,
    x="연도",
    y="평균기온",
    x_label="연도",
    y_label="평균기온 (℃)",
    height=500
)

st.caption(
    "※ 각 연도의 일별 평균기온을 평균하여 연평균 기온을 계산했습니다."
)

# 간단한 정보
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "분석 시작 연도",
        f"{start_year}년"
    )

with col2:
    st.metric(
        "분석 마지막 연도",
        f"{end_year}년"
    )

with col3:
    st.metric(
        "분석 연도 수",
        f"{len(yearly_temp):,}년"
    )

# 연도별 데이터 보기
with st.expander("📋 연도별 평균기온 데이터 보기"):
    display_df = yearly_temp.copy()
    display_df["평균기온"] = display_df["평균기온"].map(
        lambda x: f"{x:.2f} ℃"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
