import unittest

try:
    from day5.day5_flask_cals import app
except ModuleNotFoundError:
    from day5_flask_cals import app


class TestFlaskCalculatorAPI(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        print(f"\n[TEST START] {self._testMethodName}")

    def log_case(self, endpoint: str, inputs, status_code: int, payload) -> None:
        print(f"[TEST CASE] {self._testMethodName}")
        print(f"[ENDPOINT] {endpoint}")
        print(f"[INPUTS] {inputs}")
        print(f"[STATUS] {status_code}")
        print(f"[RESULT] {payload}")

    def test_home_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.log_case("/", "N/A", response.status_code, payload)
        self.assertEqual(payload["message"], "Calculator API")
        self.assertIn("POST /add", payload["endpoints"])

    def test_add_valid(self):
        inputs = {"a": 10, "b": 5}
        response = self.client.post("/add", json={"a": 10, "b": 5})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.log_case("/add", inputs, response.status_code, payload)
        self.assertEqual(payload["result"], 15.0)

    def test_add_boundary_large_numbers(self):
        inputs = {"a": 1e308, "b": 1e308}
        response = self.client.post("/add", json={"a": 1e308, "b": 1e308})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.log_case("/add", inputs, response.status_code, payload)
        self.assertEqual(payload["result"], float("inf"))

    def test_sub_valid_negative_result(self):
        inputs = {"a": 3, "b": 10}
        response = self.client.post("/sub", json={"a": 3, "b": 10})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.log_case("/sub", inputs, response.status_code, payload)
        self.assertEqual(payload["result"], -7.0)

    def test_sub_boundary_zero_result(self):
        inputs = {"a": 5, "b": 5}
        response = self.client.post("/sub", json={"a": 5, "b": 5})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.log_case("/sub", inputs, response.status_code, payload)
        self.assertEqual(payload["result"], 0.0)

    def test_mul_valid_decimal(self):
        inputs = {"a": 2.5, "b": 4}
        response = self.client.post("/mul", json={"a": 2.5, "b": 4})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.log_case("/mul", inputs, response.status_code, payload)
        self.assertEqual(payload["result"], 10.0)

    def test_mul_boundary_with_zero(self):
        inputs = {"a": 0, "b": 999999}
        response = self.client.post("/mul", json={"a": 0, "b": 999999})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.log_case("/mul", inputs, response.status_code, payload)
        self.assertEqual(payload["result"], 0.0)

    def test_div_valid(self):
        inputs = {"a": 10, "b": 4}
        response = self.client.post("/div", json={"a": 10, "b": 4})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.log_case("/div", inputs, response.status_code, payload)
        self.assertEqual(payload["result"], 2.5)

    def test_div_boundary_zero_numerator(self):
        inputs = {"a": 0, "b": 5}
        response = self.client.post("/div", json={"a": 0, "b": 5})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.log_case("/div", inputs, response.status_code, payload)
        self.assertEqual(payload["result"], 0.0)

    def test_div_by_zero_edge_case(self):
        inputs = {"a": 10, "b": 0}
        response = self.client.post("/div", json={"a": 10, "b": 0})
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.log_case("/div", inputs, response.status_code, payload)
        self.assertEqual(payload["error"], "Division by zero is not allowed.")

    def test_missing_input_fields_edge_case(self):
        inputs = {"a": 1}
        response = self.client.post("/add", json={"a": 1})
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.log_case("/add", inputs, response.status_code, payload)
        self.assertEqual(payload["error"], "Please provide numeric 'a' and 'b'.")

    def test_non_numeric_input_edge_case(self):
        inputs = {"a": "hello", "b": 5}
        response = self.client.post("/mul", json={"a": "hello", "b": 5})
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.log_case("/mul", inputs, response.status_code, payload)
        self.assertEqual(payload["error"], "Please provide numeric 'a' and 'b'.")

    def test_null_input_edge_case(self):
        inputs = {"a": None, "b": 2}
        response = self.client.post("/sub", json={"a": None, "b": 2})
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.log_case("/sub", inputs, response.status_code, payload)
        self.assertEqual(payload["error"], "Please provide numeric 'a' and 'b'.")

    def test_empty_json_edge_case(self):
        inputs = {}
        response = self.client.post("/div", json={})
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.log_case("/div", inputs, response.status_code, payload)
        self.assertEqual(payload["error"], "Please provide numeric 'a' and 'b'.")

    def test_invalid_content_type_edge_case(self):
        inputs = "a=1&b=2"
        response = self.client.post("/add", data="a=1&b=2", content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.log_case("/add", inputs, response.status_code, payload)
        self.assertEqual(payload["error"], "Please provide numeric 'a' and 'b'.")


if __name__ == "__main__":
    unittest.main()
