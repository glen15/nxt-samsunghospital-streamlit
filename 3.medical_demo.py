# ============================================
# Streamlit 의료진용 데모 앱
# 삼성서울병원 파이썬 교육용
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="의료진을 위한 Streamlit 데모", page_icon="🏥", layout="wide"
)

# 타이틀
st.title("🏥 의료진을 위한 Streamlit 데모 앱")
st.markdown("---")

# 사이드바에 메뉴 만들기
menu = st.sidebar.selectbox(
    "메뉴를 선택하세요",
    ["홈", "BMI 계산기", "환자 데이터 대시보드", "약물 투여 계산기"],
)

# 홈 페이지
if menu == "홈":
    st.header("Streamlit이란?")
    st.write(
        """
    **Streamlit**은 Python으로 데이터 애플리케이션을 빠르게 만들 수 있는 오픈소스 프레임워크입니다.
    
    ### 왜 의료진에게 유용한가요?
    - 🚀 **빠른 개발**: 몇 줄의 코드로 웹 앱 제작
    - 📊 **데이터 시각화**: 환자 데이터를 쉽게 시각화
    - 🔄 **실시간 업데이트**: 데이터가 바뀌면 즉시 반영
    - 💻 **코딩 지식 최소화**: Python 기초만 알면 OK
    
    ### 의료 현장 활용 예시
    - 환자 모니터링 대시보드
    - 임상 계산기 (BMI, 약물 용량 등)
    - 데이터 분석 및 리포트 생성
    - 의료 영상 분석 도구
    """
    )

    st.info("👈 왼쪽 사이드바에서 다른 예제들을 확인해보세요!")

# BMI 계산기
elif menu == "BMI 계산기":
    st.header("📏 BMI (체질량지수) 계산기")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("환자 정보 입력")
        height = st.number_input(
            "키 (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.1
        )
        weight = st.number_input(
            "체중 (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1
        )

        if st.button("BMI 계산", type="primary"):
            height_m = height / 100
            bmi = weight / (height_m**2)

            st.session_state["bmi"] = bmi

    with col2:
        if "bmi" in st.session_state:
            bmi = st.session_state["bmi"]
            st.subheader("계산 결과")
            st.metric("BMI", f"{bmi:.1f}")

            # BMI 분류
            if bmi < 18.5:
                category = "저체중"
                color = "blue"
            elif 18.5 <= bmi < 23:
                category = "정상"
                color = "green"
            elif 23 <= bmi < 25:
                category = "과체중"
                color = "orange"
            elif 25 <= bmi < 30:
                category = "비만 1단계"
                color = "orange"
            else:
                category = "비만 2단계 이상"
                color = "red"

            st.markdown(f"### 분류: :{color}[{category}]")

            # 목표 체중 계산 (BMI 22 기준)
            목표_BMI = 22
            목표_체중 = 목표_BMI * (height_m**2)
            차이 = weight - 목표_체중

            st.markdown("### 💡 목표 체중 정보")
            st.write(f"**정상 BMI (22) 기준 목표 체중**: {목표_체중:.1f} kg")
            if 차이 > 0:
                st.write(f"**현재 체중에서 감량 필요**: {차이:.1f} kg")
            elif 차이 < 0:
                st.write(f"**현재 체중에서 증량 필요**: {abs(차이):.1f} kg")
            else:
                st.write("**현재 정상 체중입니다!**")

            # BMI 차트
            st.subheader("BMI 기준표 (WHO 아시아-태평양)")
            reference_data = pd.DataFrame(
                {
                    "분류": ["저체중", "정상", "과체중", "비만 1단계", "비만 2단계"],
                    "BMI 범위": [
                        "< 18.5",
                        "18.5 - 22.9",
                        "23.0 - 24.9",
                        "25.0 - 29.9",
                        "≥ 30.0",
                    ],
                }
            )
            st.table(reference_data)

# 환자 데이터 대시보드
elif menu == "환자 데이터 대시보드":
    st.header("📊 환자 데이터 대시보드")

    # 샘플 데이터 생성
    @st.cache_data
    def generate_patient_data():
        dates = pd.date_range(start="2024-10-01", end="2024-10-31", freq="D")
        np.random.seed(42)

        data = pd.DataFrame(
            {
                "날짜": dates,
                "혈압(수축기)": np.random.randint(110, 140, len(dates)),
                "혈압(이완기)": np.random.randint(70, 90, len(dates)),
                "혈당": np.random.randint(90, 130, len(dates)),
                "체온": np.round(np.random.uniform(36.0, 37.5, len(dates)), 1),
            }
        )
        return data

    patient_data = generate_patient_data()

    # 필터
    st.subheader("기간 선택")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("시작일", value=patient_data["날짜"].min())
    with col2:
        end_date = st.date_input("종료일", value=patient_data["날짜"].max())

    # 데이터 필터링
    mask = (patient_data["날짜"].dt.date >= start_date) & (
        patient_data["날짜"].dt.date <= end_date
    )
    filtered_data = patient_data[mask]

    # 주요 지표 표시
    st.subheader("📈 주요 지표")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_sys = filtered_data["혈압(수축기)"].mean()
        st.metric("평균 수축기 혈압", f"{avg_sys:.0f} mmHg")

    with col2:
        avg_dia = filtered_data["혈압(이완기)"].mean()
        st.metric("평균 이완기 혈압", f"{avg_dia:.0f} mmHg")

    with col3:
        avg_glucose = filtered_data["혈당"].mean()
        st.metric("평균 혈당", f"{avg_glucose:.0f} mg/dL")

    with col4:
        avg_temp = filtered_data["체온"].mean()
        st.metric("평균 체온", f"{avg_temp:.1f}°C")

    # 그래프
    st.subheader("📉 추세 그래프")

    tab1, tab2, tab3 = st.tabs(["혈압", "혈당", "체온"])

    with tab1:
        fig1 = px.line(
            filtered_data,
            x="날짜",
            y=["혈압(수축기)", "혈압(이완기)"],
            title="혈압 추세",
            labels={"value": "혈압 (mmHg)", "variable": "구분"},
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.line(
            filtered_data,
            x="날짜",
            y="혈당",
            title="혈당 추세",
            labels={"혈당": "혈당 (mg/dL)"},
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        fig3 = px.line(
            filtered_data,
            x="날짜",
            y="체온",
            title="체온 추세",
            labels={"체온": "체온 (°C)"},
        )
        st.plotly_chart(fig3, use_container_width=True)

    # 원본 데이터 표시
    with st.expander("📋 원본 데이터 보기"):
        st.dataframe(filtered_data, use_container_width=True)

        # CSV 다운로드
        csv = filtered_data.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 데이터 다운로드 (CSV)",
            data=csv,
            file_name=f"환자데이터_{start_date}_{end_date}.csv",
            mime="text/csv",
        )

# 약물 투여 계산기
elif menu == "약물 투여 계산기":
    st.header("💊 약물 투여 계산기")

    st.write("체중 기반 약물 용량을 계산합니다.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("환자 정보")
        patient_weight = st.number_input(
            "환자 체중 (kg)", min_value=1.0, max_value=200.0, value=70.0, step=0.1
        )

        st.subheader("약물 정보")
        drug_name = st.text_input("약물명", value="예) 아미카신")
        dose_per_kg = st.number_input(
            "용량 (mg/kg)", min_value=0.1, max_value=100.0, value=15.0, step=0.1
        )
        frequency = st.selectbox(
            "투여 빈도", ["1일 1회", "1일 2회", "1일 3회", "1일 4회"]
        )

    with col2:
        st.subheader("계산 결과")
        total_dose = patient_weight * dose_per_kg

        st.metric("1회 투여량", f"{total_dose:.1f} mg")

        freq_map = {"1일 1회": 1, "1일 2회": 2, "1일 3회": 3, "1일 4회": 4}
        daily_dose = total_dose * freq_map[frequency]

        st.metric("1일 총 투여량", f"{daily_dose:.1f} mg")

        # 경고 기능 추가
        임계값 = 2000  # mg
        if daily_dose > 임계값:
            st.error(f"⚠️ 경고: 일일 총 투여량이 {임계값}mg을 초과합니다!")
            st.write(f"현재 계산된 일일 총량: {daily_dose:.1f} mg")
            st.write("약물 가이드라인을 반드시 확인하세요.")
        else:
            st.success("✅ 일일 총 투여량이 안전 범위 내에 있습니다.")

        st.info(
            f"""
        **처방 요약**
        - 약물: {drug_name}
        - 1회 용량: {total_dose:.1f} mg
        - 투여 빈도: {frequency}
        - 1일 총량: {daily_dose:.1f} mg
        """
        )

        st.warning(
            "⚠️ 이 계산기는 교육 목적의 데모입니다. 실제 임상에서는 반드시 약물 가이드라인을 확인하세요."
        )

# 푸터
st.markdown("---")
st.markdown(
    """
<div style='text-align: center'>
    <p>🏥 의료진을 위한 Streamlit 데모 앱 | Made with Streamlit</p>
</div>
""",
    unsafe_allow_html=True,
)
