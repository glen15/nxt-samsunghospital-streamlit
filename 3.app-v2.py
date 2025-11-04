import streamlit as st
import json
import boto3

# AWS Bedrock 클라이언트 초기화
bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# 앱 제목
st.title("🏥 의료진 소개 앱 👨‍⚕️")

# 부제목
st.subheader("의료진 정보를 등록하고 관리하세요 🚀")


def generate_doctor_introduction(name, department, specialty, original_intro):
    """
    Bedrock을 사용하여 의료진 소개문을 전문적이고 환자 친화적으로 생성하는 함수
    """
    try:
        prompt = f"""다음 의료진 정보를 바탕으로 전문적이고 환자 친화적인 소개문을 작성해주세요.

의료진 정보:
- 이름: {name}
- 진료과: {department}
- 전문분야: {specialty}
- 기존 소개: {original_intro}

요구사항:
1. 환자들이 이해하기 쉬운 문체로 작성
2. 전문성과 신뢰감을 주는 내용
3. 2-3문장으로 간결하게 작성
4. 기존 소개 내용의 장점을 유지하면서 개선

개선된 소개문만 작성해주세요:"""

        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    }
                ],
            }
        )

        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",  # Claude 모델 ID
            body=body,
        )
        response_body = json.loads(response.get("body").read())

        # Claude 응답에서 텍스트 추출
        output_text = response_body["content"][0]["text"]

        return output_text.strip()
    except Exception as e:
        st.error(f"AI 소개문 생성 중 오류가 발생했습니다: {str(e)}")
        return None


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
            with st.spinner("🤖 AI가 전문적인 소개문을 생성 중입니다..."):
                # AI를 사용하여 소개문 개선
                ai_intro = generate_doctor_introduction(
                    name, department, specialty, introduction
                )

            st.success("✅ 의료진 정보가 성공적으로 등록되었습니다!")
            st.write(f"- **👤 이름**: {name}")
            st.write(f"- **🏥 진료과**: {department}")
            st.write(f"- **💊 전문분야**: {specialty}")

            # 원본 소개문과 AI 생성 소개문 비교 표시
            st.write("---")
            st.write("### 📝 소개문")

            with st.expander("📌 원본 소개문", expanded=False):
                st.write(introduction)

            if ai_intro:
                st.write("### ✨ AI 개선 소개문")
                st.info(ai_intro)
                st.write("💡 *위 소개문은 AI가 자동으로 생성한 전문적인 소개문입니다.*")
            else:
                st.write("### 📝 원본 소개문")
                st.write(introduction)

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
    💡 **이 앱은 Streamlit과 AWS Bedrock으로 제작되었습니다!**  
    🤖 **AI 기능**: 등록하기 버튼을 누르면 AWS Bedrock의 Claude 모델이 자동으로 전문적이고 환자 친화적인 소개문을 생성합니다.  
    🚀 **확장 가능**: 이 기능을 응용하여 진료 기록 정리, 환자 상담 내용 요약 등 다양한 의료 업무에 활용할 수 있습니다! 📝🤖
    """
)
