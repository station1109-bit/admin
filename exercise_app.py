import streamlit as st
import google.generativeai as genai

# 1. API 키 입력 (본인의 키로 교체하세요)
MY_KEY = st.secrets["GEMINI_API_KEY"] 
# 웹 페이지 설정
st.set_page_config(page_title="보험 스크립트 생성기", layout="centered")

# 2. Gemini 설정 및 모델 자동 선택
def setup_model(API_KEY):
    try:
        # 이 부분이 핵심입니다! 매개변수 이름을 소문자 api_key로 써야 합니다.
        genai.configure(api_key=API_KEY) 
        
        # 내 계정에서 사용 가능한 모델 리스트 확인
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # gemini-1.5-flash가 있으면 우선 사용, 없으면 첫 번째 사용 가능한 모델 선택
        target_model = 'models/gemini-1.5-flash'
        if target_model not in available_models:
            target_model = available_models[0]
            
        return genai.GenerativeModel(target_model)
    except Exception as e:
        st.error(f"모델 연결 중 오류: {e}")
        return None

# 모델 불러오기
model = setup_model(MY_KEY)

# 3. 화면 UI 디자인
st.title("🛡️ AI 보험 상담 스크립트")
st.write("상담 조건을 선택하면 베테랑 설계사의 스크립트가 생성됩니다.")

col1, col2 = st.columns(2)
with col1:
    age = st.selectbox("고객 연령대", ["20대 사회초년생", "30대 직장인/신혼부부", "40대 가장", "50대 이상"])
    product = st.selectbox("보험 상품", ["암/건강보험", "운전자보험", "종신/정기보험", "치매/간병보험"])
with col2:
    situation = st.selectbox("상담 단계", ["도입부(안부/명분)", "니즈환기", "거절처리", "클로징"])
    tone = st.radio("말투", ["부드럽게", "전문적으로"], horizontal=True)

st.divider()

# 4. 생성 버튼 및 로직
if st.button("스크립트 생성하기 ✨", use_container_width=True):
    if not MY_KEY or "여기에" in MY_KEY:
        st.warning("API 키를 먼저 입력해 주세요.")
    elif model:
        # AI에게 주는 상세 지시문
        prompt = f"""
        너는 15년 차 보험 전문가야. 아래 조건으로 상담 스크립트를 작성해줘.
        - 대상: {age}
        - 상품: {product}
        - 상황: {situation}
        - 말투: {tone} 스타일로
        - 특징: 고객의 거부감을 줄이고, 다음 대화로 이어질 수 있는 질문을 포함해줘.
        """
        
        with st.spinner("AI 설계사가 답변을 작성 중입니다..."):
            try:
                response = model.generate_content(prompt)
                st.info(response.text)
                
                # 결과물 복사 텍스트 영역
                st.text_area("결과물 복사하기", value=response.text, height=200)
            except Exception as e:

                st.error(f"생성 실패: {e}")






