# Day 5 - Calculator API + Streamlit UI

This folder contains:

- A Flask Math API (`day5_flask_cals.py`)
- A Streamlit Calculator UI (`day5_streamlit_cals.py`) that calls the Flask API for operations
- API unit tests (`test_day5_flask_cals.py`)
- Streamlit UI Playwright tests (`test_gui_playwright.py`)

---

## 1) Flask Math API

File: `day5_flask_cals.py`

### Purpose
Provides HTTP APIs for 4 math operations using two inputs: addition, subtraction, multiplication, and division.

### Endpoints

- `GET /`
	- Returns API metadata and available endpoints.

- `POST /add`
- `POST /sub`
- `POST /mul`
- `POST /div`

Each POST endpoint expects JSON:

```json
{
	"a": 10,
	"b": 5
}
```

### Example Success Response

```json
{
	"operation": "add",
	"a": 10.0,
	"b": 5.0,
	"result": 15.0
}
```

### Example Error Responses

- Invalid input:

```json
{
	"error": "Please provide numeric 'a' and 'b'."
}
```

- Divide by zero:

```json
{
	"error": "Division by zero is not allowed."
}
```

### Run Flask API

```bash
python day5/day5_flask_cals.py
```

Default URL: `http://127.0.0.1:5000`

### Test API quickly with curl

```bash
curl -X POST http://127.0.0.1:5000/add -H "Content-Type: application/json" -d '{"a":10,"b":5}'
curl -X POST http://127.0.0.1:5000/sub -H "Content-Type: application/json" -d '{"a":10,"b":5}'
curl -X POST http://127.0.0.1:5000/mul -H "Content-Type: application/json" -d '{"a":10,"b":5}'
curl -X POST http://127.0.0.1:5000/div -H "Content-Type: application/json" -d '{"a":10,"b":5}'
```

---

## 2) Streamlit Calculator UI

File: `day5_streamlit_cals.py`

### Purpose
Provides a calculator UI and delegates math operations to the Flask API endpoints.

### UI Features

- Calculator heading and display box
- Number buttons (`0-9`)
- Operator buttons (`＋`, `−`, `×`, `÷`)
- Equals (`=`) and clear (`AC`)
- Input validation:
	- One binary operation at a time
	- Prevent invalid operator placement
	- Shows error for invalid expressions
- If Flask API is down, shows a clear API-not-reachable message

### Run Streamlit UI

```bash
streamlit run day5/day5_streamlit_cals.py
```

Default URL: `http://localhost:8501`

### Important
Start Flask API first, then Streamlit:

1. `python day5/day5_flask_cals.py`
2. `streamlit run day5/day5_streamlit_cals.py`

---

## 3) Unit Tests for Flask API

File: `test_day5_flask_cals.py`

### What it tests

- All operations: add, sub, mul, div
- Boundary conditions:
	- Large numbers
	- Zero numerator
	- Zero multiplication
- Edge/negative cases:
	- Divide by zero
	- Missing fields
	- Null input
	- Non-numeric input
	- Empty JSON
	- Invalid content type

### Logging in tests
Each test logs:

- Test case name
- Endpoint
- Input
- HTTP status code
- Result payload

### Run unit tests

```bash
python day5/test_day5_flask_cals.py
```

---

## 4) Playwright UI Tests for Streamlit

File: `test_gui_playwright.py`

### What it tests

- UI operation flows for add/sub/mul/div
- Negative scenarios:
	- Divide by zero
	- Equals with missing/invalid inputs
	- Operator rules (first operator ignored, second operator ignored)

### Visual behavior

- Runs browser in visible mode (`headless=False`)
- Adds waits so each action/result can be observed

### Run Playwright tests

```bash
python day5/test_gui_playwright.py
```

---

## 5) Dependencies

Install required packages:

```bash
pip install flask streamlit playwright
playwright install
```

---

## 6) Recommended Execution Order

1. Start Flask API
2. Start Streamlit UI
3. Run API unit tests
4. Run Playwright UI tests

Commands:

```bash
python day5/day5_flask_cals.py
streamlit run day5/day5_streamlit_cals.py
python day5/test_day5_flask_cals.py
python day5/test_gui_playwright.py
```

