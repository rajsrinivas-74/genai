import re
from json import dumps, loads
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import streamlit as st


OPERATORS = {"+", "-", "*", "/"}
BINARY_EXPRESSION = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)\s*$")
API_BASE_URL = "http://127.0.0.1:5000"
OPERATOR_TO_ENDPOINT = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "/": "div",
}


def call_math_api(operator: str, first_number: float, second_number: float) -> tuple[str, str]:
    endpoint = OPERATOR_TO_ENDPOINT[operator]
    url = f"{API_BASE_URL}/{endpoint}"
    body = dumps({"a": first_number, "b": second_number}).encode("utf-8")
    request = Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})

    try:
        with urlopen(request, timeout=5) as response:
            payload = loads(response.read().decode("utf-8"))

        result = payload.get("result")
        if isinstance(result, float) and result.is_integer():
            return str(int(result)), ""
        return str(result), ""
    except HTTPError as error:
        try:
            payload = loads(error.read().decode("utf-8"))
            return "Error", payload.get("error", "Calculation failed.")
        except Exception:
            return "Error", "Calculation failed."
    except URLError:
        return "Error", "Flask API is not reachable. Please start day5_flask_cals.py."
    except Exception:
        return "Error", "Unexpected error while calling Flask API."


def evaluate_expression(expression: str) -> tuple[str, str]:
    expression = expression.strip()
    if not expression:
        return "", ""

    match = BINARY_EXPRESSION.match(expression)
    if not match:
        return "Error", "Please enter two numbers with one valid operator before pressing =."

    try:
        left_operand, operator, right_operand = match.groups()
        left_number = float(left_operand)
        right_number = float(right_operand)
        return call_math_api(operator, left_number, right_number)
    except Exception:
        return "Error", "Unexpected calculation error."


def press(value: str) -> None:
    current = st.session_state.display

    if value == "AC":
        st.session_state.display = ""
        st.session_state.error_message = ""
        return

    if value == "=":
        result, message = evaluate_expression(current)
        st.session_state.display = result
        st.session_state.error_message = message
        return

    if current == "Error":
        current = ""
        st.session_state.error_message = ""

    if value in OPERATORS:
        if not current:
            return

        if current[-1] in OPERATORS:
            return

        if any(operator in current for operator in OPERATORS):
            return

        st.session_state.display = current + value
        st.session_state.error_message = ""
        return

    st.session_state.display = current + value
    st.session_state.error_message = ""


def main() -> None:
    st.set_page_config(page_title="Calculator")

    if "display" not in st.session_state:
        st.session_state.display = ""
    if "error_message" not in st.session_state:
        st.session_state.error_message = ""

    st.markdown(
        """
        <style>
        input[disabled] {
            background-color: #fff9c4 !important;
            color: #000000 !important;
        }
        button[kind="primary"] {
            font-weight: 700 !important;
            background-color: #add8e6 !important;
            color: #000000 !important;
            border: 1px solid #87ceeb !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Calculator")
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
    st.text_input("Display", key="display", disabled=True)

    row1 = st.columns(4)
    row2 = st.columns(4)
    row3 = st.columns(4)
    row4 = st.columns(4)

    row1[0].button("7", use_container_width=True, on_click=press, args=("7",))
    row1[1].button("8", use_container_width=True, on_click=press, args=("8",))
    row1[2].button("9", use_container_width=True, on_click=press, args=("9",))
    row1[3].button("÷", use_container_width=True, type="primary", on_click=press, args=("/",))

    row2[0].button("4", use_container_width=True, on_click=press, args=("4",))
    row2[1].button("5", use_container_width=True, on_click=press, args=("5",))
    row2[2].button("6", use_container_width=True, on_click=press, args=("6",))
    row2[3].button("×", use_container_width=True, type="primary", on_click=press, args=("*",))

    row3[0].button("1", use_container_width=True, on_click=press, args=("1",))
    row3[1].button("2", use_container_width=True, on_click=press, args=("2",))
    row3[2].button("3", use_container_width=True, on_click=press, args=("3",))
    row3[3].button("−", use_container_width=True, type="primary", on_click=press, args=("-",))

    row4[0].button("AC", use_container_width=True, on_click=press, args=("AC",))
    row4[1].button("0", use_container_width=True, on_click=press, args=("0",))
    row4[2].button("=", use_container_width=True, type="primary", on_click=press, args=("=",))
    row4[3].button("＋", use_container_width=True, type="primary", on_click=press, args=("+",))


if __name__ == "__main__":
    main()