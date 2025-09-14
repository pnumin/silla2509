# cal.py
import streamlit as st
def add(x, y):
    """두 수를 더합니다."""
    return x + y

def subtract(x, y):
    """두 수를 뺍니다."""
    return x - y

def multiply(x, y):
    """두 수를 곱합니다."""
    return x * y

def divide(x, y):
    """두 수를 나눕니다. 0으로 나누는 경우 오류 메시지를 반환합니다."""
    if y == 0:
        return "오류: 0으로 나눌 수 없습니다."
    return x / y

# 연산자와 함수를 딕셔너리로 매핑
operations = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide
}

# --- Streamlit 웹 앱 인터페이스 ---
st.title("웹 계산기")

# 1. 상태 초기화 (Session State)
# 앱이 재실행되어도 값을 기억하기 위한 저장 공간
if 'display' not in st.session_state:
    st.session_state.display = '0'         # 화면에 표시될 값
    st.session_state.operand1 = 0.0        # 첫 번째 피연산자
    st.session_state.operator = None       # 현재 선택된 연산자
    st.session_state.new_input = True      # 새 숫자 입력 시작 여부

# 2. 계산기 디스플레이 (화면)
st.markdown(f"""
<div style="
    background-color: #262730;
    color: white;
    border: 1px solid #caced1;
    border-radius: 5px;
    padding: 15px;
    text-align: right;
    font-size: 2.5em;
    font-family: 'Helvetica', sans-serif;
    margin-bottom: 10px;
    overflow-x: auto;
    white-space: nowrap;
">
    {st.session_state.display}
</div>
""", unsafe_allow_html=True)

# 3. 버튼 로직을 처리할 함수들
def handle_number(num_str):
    """숫자 버튼 클릭 시 display 값을 업데이트합니다."""
    if st.session_state.new_input:
        st.session_state.display = num_str
        st.session_state.new_input = False
    else:
        st.session_state.display = num_str if st.session_state.display == '0' else st.session_state.display + num_str

def handle_decimal():
    """소수점 버튼 클릭 시 처리합니다."""
    if st.session_state.new_input:
        st.session_state.display = '0.'
        st.session_state.new_input = False
    elif '.' not in st.session_state.display:
        st.session_state.display += '.'

def handle_operator(op):
    """연산자 버튼 클릭 시, 필요하면 중간 계산을 수행하고 상태를 업데이트합니다."""
    if st.session_state.operator is not None and not st.session_state.new_input:
        handle_equals()

    try:
        st.session_state.operand1 = float(st.session_state.display)
        st.session_state.operator = op
        st.session_state.new_input = True
    except ValueError:
        st.session_state.display = "Error"
        st.session_state.new_input = True

def handle_equals():
    """'=' 버튼 클릭 시 최종 계산을 수행하고 결과를 표시합니다."""
    if st.session_state.operator is None: return

    try:
        operand2 = float(st.session_state.display)
        calc_func = operations.get(st.session_state.operator)
        result = calc_func(st.session_state.operand1, operand2)

        st.session_state.display = str(int(result) if isinstance(result, float) and result.is_integer() else result)
    except (ValueError, TypeError):
        st.session_state.display = "Error"
    
    st.session_state.new_input = True
    st.session_state.operator = None

def handle_clear():
    """'C' 버튼: 모든 상태를 초기화합니다."""
    st.session_state.display = '0'
    st.session_state.operand1 = 0.0
    st.session_state.operator = None
    st.session_state.new_input = True

# 4. 버튼 레이아웃
op_map = {"➕": "+", "➖": "-", "✖️": "*", "➗": "/"}
button_grid = [("7", "8", "9", "➕"), ("4", "5", "6", "➖"), ("1", "2", "3", "✖️"), ("C", "0", ".", "➗")]

for row_items in button_grid:
    cols = st.columns(4)
    for i, item in enumerate(row_items):
        if cols[i].button(item, use_container_width=True, key=f"btn_{item}"):
            if item.isdigit(): handle_number(item)
            elif item in op_map: handle_operator(op_map[item])
            elif item == ".": handle_decimal()
            elif item == "C": handle_clear()

if st.button("=", use_container_width=True, key="btn_equals"):
    handle_equals()