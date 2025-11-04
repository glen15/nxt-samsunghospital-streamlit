import streamlit as st

# 앱 제목
st.title("🏥 의료진 소개 앱 👨‍⚕️")

# 부제목
st.subheader("의료진 정보를 등록하고 관리하세요 🚀")

# 입력 폼과 결과를 두 개의 컬럼으로 구성
col1, col2 = st.columns(2)

with col1:
    st.write("👋 **의료진 정보를 입력해 주세요!**")
    name = st.text_input("👤 이름", "홍길동")  # 디폴트값 추가
    department = st.text_input("🏥 진료과", "내과")  # 디폴트값 추가
    specialty = st.text_input("💊 전문분야", "심장내과")  # 디폴트값 추가
    introduction = st.text_area(
        "🖊️ 의료진 소개",
        "안녕하세요! 저는 내과 전문의 홍길동입니다. 환자 중심의 진료를 위해 항상 최선을 다하겠습니다.",
    )  # 디폴트값 추가

with col2:
    st.write("### 🎯 의료진 정보")
    if st.button("✨ 등록하기"):
        # 입력 결과를 화면에 출력
        if name and department and specialty and introduction:
            st.success("✅ 의료진 정보가 성공적으로 등록되었습니다!")
            st.write(f"- **👤 이름**: {name}")
            st.write(f"- **🏥 진료과**: {department}")
            st.write(f"- **💊 전문분야**: {specialty}")
            st.write(f"- **✍️ 의료진 소개**: {introduction}")
            st.balloons()  # 풍선 애니메이션 출력
        else:
            st.error("❌ 모든 필드를 입력해 주세요!")

st.write("---")
# 장난 버튼
if st.button("👈 왼쪽을 보시오", type="primary"):
    # 토스트 메시지
    st.toast("여기가 왼쪽이냐? 👀", icon="🤔")

# 추가 정보 (하단 박스에 배치)
st.write("---")
st.info(
    """
    💡 **이 앱은 Streamlit으로 제작되었습니다!**  
    👉 간단한 Python 코드로 멋진 웹 앱을 만들어 보세요. 🎨  
    🚀 **AWS Bedrock을 이용해서 AI가 자동으로 진료 기록을 정리하고 분석해주는 웹페이지를 만들어보세요!** 📝🤖
    """
)
