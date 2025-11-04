import streamlit as st
import json
import boto3

# AWS Bedrock 클라이언트 초기화
bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# 앱 제목
st.title("🏥 환자 안내 메시지 생성 앱 👨‍⚕️")

# 부제목
st.subheader("환자 정보를 입력하면 맞춤형 안내 메시지를 자동으로 생성합니다 🚀")


def generate_patient_guidance(patient_name, age, diagnosis, symptoms, treatment_plan):
    """
    Bedrock을 사용하여 환자에게 필요한 안내 메시지를 자동으로 생성하는 함수
    """
    try:
        prompt = f"""다음 환자 정보를 바탕으로 환자에게 필요한 안내 메시지를 작성해주세요.

환자 정보:
- 이름: {patient_name}
- 나이: {age}세
- 진단명: {diagnosis}
- 증상: {symptoms}
- 치료 계획: {treatment_plan}

요구사항:
1. 환자가 이해하기 쉬운 문체로 작성
2. 다음 항목을 포함하여 작성:
   - 진료 후 주의사항
   - 투약 안내 (필요시)
   - 생활 관리 방법
   - 증상이 악화될 경우 대응 방법
   - 추후 방문 안내
3. 친절하고 명확한 안내 문구로 작성
4. 항목별로 구분하여 작성

환자 안내 메시지만 작성해주세요:"""

        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
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
        st.error(f"AI 안내 메시지 생성 중 오류가 발생했습니다: {str(e)}")
        return None


# 입력 폼과 결과를 두 개의 컬럼으로 구성
col1, col2 = st.columns(2)

with col1:
    st.write("👋 **환자 정보를 입력해 주세요!**")
    patient_name = st.text_input("👤 환자 이름", "홍길동")
    age = st.number_input("🎂 나이", min_value=0, max_value=150, value=45)
    diagnosis = st.text_input("🏥 진단명", "고혈압")
    symptoms = st.text_area(
        "🩺 증상", "두통, 어지러움", help="환자가 호소하는 증상을 입력해주세요."
    )
    treatment_plan = st.text_area(
        "💊 치료 계획",
        "혈압약 복용, 생활습관 개선",
        help="처방된 약물이나 치료 방법을 입력해주세요.",
    )

with col2:
    st.write("### 🎯 환자 안내 메시지")
    if st.button("✨ 안내 메시지 생성하기", type="primary"):
        # 입력 결과를 화면에 출력
        if patient_name and age and diagnosis and symptoms and treatment_plan:
            with st.spinner("🤖 AI가 환자 맞춤형 안내 메시지를 생성 중입니다..."):
                # AI를 사용하여 환자 안내 메시지 생성
                guidance = generate_patient_guidance(
                    patient_name, age, diagnosis, symptoms, treatment_plan
                )

            st.success("✅ 환자 안내 메시지가 생성되었습니다!")
            st.write("---")
            st.write("### 📋 환자 정보 요약")
            st.write(f"- **👤 환자 이름**: {patient_name}")
            st.write(f"- **🎂 나이**: {age}세")
            st.write(f"- **🏥 진단명**: {diagnosis}")
            st.write(f"- **🩺 증상**: {symptoms}")
            st.write(f"- **💊 치료 계획**: {treatment_plan}")

            # AI 생성 안내 메시지 표시
            st.write("---")
            if guidance:
                st.write("### 📝 환자 안내 메시지")
                st.success(guidance)
                st.write(
                    "💡 *위 안내 메시지는 AI가 환자 정보를 바탕으로 자동으로 생성했습니다.*"
                )
            else:
                st.warning("⚠️ 안내 메시지 생성에 실패했습니다. 다시 시도해주세요.")

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
    🤖 **AI 기능**: 환자 정보를 입력하면 AWS Bedrock의 Claude 모델이 자동으로 환자 맞춤형 안내 메시지를 생성합니다.  
    📋 **생성 내용**: 진료 후 주의사항, 투약 안내, 생활 관리 방법, 증상 악화 시 대응 방법, 추후 방문 안내 등이 포함됩니다.  
    🚀 **활용**: 이 기능을 통해 진료 후 환자 안내 시간을 단축하고, 일관된 안내 메시지를 제공할 수 있습니다! 📝🤖
    """
)
