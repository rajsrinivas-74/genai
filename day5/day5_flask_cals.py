from flask import Flask, jsonify, request


app = Flask(__name__)


def parse_numbers() -> tuple[float, float] | tuple[None, None]:
	payload = request.get_json(silent=True) or {}
	first = payload.get("a")
	second = payload.get("b")

	try:
		return float(first), float(second)
	except (TypeError, ValueError):
		return None, None


@app.get("/")
def home():
	return jsonify(
		{
			"message": "Calculator API",
			"endpoints": ["POST /add", "POST /sub", "POST /mul", "POST /div"],
			"input": {"a": "number", "b": "number"},
		}
	)


@app.post("/add")
def add():
	a, b = parse_numbers()
	if a is None:
		return jsonify({"error": "Please provide numeric 'a' and 'b'."}), 400

	return jsonify({"operation": "add", "a": a, "b": b, "result": a + b})


@app.post("/sub")
def sub():
	a, b = parse_numbers()
	if a is None:
		return jsonify({"error": "Please provide numeric 'a' and 'b'."}), 400

	return jsonify({"operation": "sub", "a": a, "b": b, "result": a - b})


@app.post("/mul")
def mul():
	a, b = parse_numbers()
	if a is None:
		return jsonify({"error": "Please provide numeric 'a' and 'b'."}), 400

	return jsonify({"operation": "mul", "a": a, "b": b, "result": a * b})


@app.post("/div")
def div():
	a, b = parse_numbers()
	if a is None:
		return jsonify({"error": "Please provide numeric 'a' and 'b'."}), 400
	if b == 0:
		return jsonify({"error": "Division by zero is not allowed."}), 400

	return jsonify({"operation": "div", "a": a, "b": b, "result": a / b})


if __name__ == "__main__":
	app.run(debug=True)
