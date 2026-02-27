import subprocess
import sys
import time
import unittest
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:8501"
ACTION_WAIT_MS = 1200
SLOW_MO_MS = 300
RESULT_WAIT_MS = 2500
ERROR_TEXT = "Please enter two numbers with one valid operator before pressing =."


class TestStreamlitCalculatorWithPlaywright(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		app_file = Path(__file__).with_name("day5_streamlit_cals.py")
		cls.server_process = subprocess.Popen(
			[
				sys.executable,
				"-m",
				"streamlit",
				"run",
				str(app_file),
				"--server.headless",
				"true",
				"--server.port",
				"8501",
			],
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)
		time.sleep(4)

	@classmethod
	def tearDownClass(cls):
		cls.server_process.terminate()
		cls.server_process.wait(timeout=5)

	def open_calculator(self, playwright):
		browser = playwright.chromium.launch(headless=False, slow_mo=SLOW_MO_MS)
		page = browser.new_page()
		page.goto(BASE_URL)
		page.wait_for_selector("text=Calculator")
		return browser, page

	def click_sequence(self, page, button_labels: list[str]) -> None:
		for label in button_labels:
			page.get_by_role("button", name=label).click()
			page.wait_for_timeout(ACTION_WAIT_MS)

	def read_display(self, page) -> str:
		return page.get_by_label("Display").input_value()

	def wait_and_close(self, page, browser):
		page.wait_for_timeout(RESULT_WAIT_MS)
		browser.close()

	def test_addition_via_streamlit_ui(self):
		with sync_playwright() as playwright:
			browser, page = self.open_calculator(playwright)
			self.click_sequence(page, ["AC", "2", "＋", "3", "="])
			self.assertEqual(self.read_display(page), "5")
			self.wait_and_close(page, browser)

	def test_subtraction_via_streamlit_ui(self):
		with sync_playwright() as playwright:
			browser, page = self.open_calculator(playwright)
			self.click_sequence(page, ["AC", "9", "−", "4", "="])
			self.assertEqual(self.read_display(page), "5")
			self.wait_and_close(page, browser)

	def test_multiplication_via_streamlit_ui(self):
		with sync_playwright() as playwright:
			browser, page = self.open_calculator(playwright)
			self.click_sequence(page, ["AC", "6", "×", "7", "="])
			self.assertEqual(self.read_display(page), "42")
			self.wait_and_close(page, browser)

	def test_division_via_streamlit_ui(self):
		with sync_playwright() as playwright:
			browser, page = self.open_calculator(playwright)
			self.click_sequence(page, ["AC", "8", "÷", "2", "="])
			self.assertEqual(self.read_display(page), "4")
			self.wait_and_close(page, browser)

	def test_divide_by_zero_shows_error_in_streamlit_ui(self):
		with sync_playwright() as playwright:
			browser, page = self.open_calculator(playwright)
			self.click_sequence(page, ["AC", "9", "÷", "0", "="])
			self.assertTrue(page.get_by_text(ERROR_TEXT).is_visible())
			self.assertEqual(self.read_display(page), "Error")
			self.wait_and_close(page, browser)

	def test_equals_without_inputs_shows_error(self):
		with sync_playwright() as playwright:
			browser, page = self.open_calculator(playwright)
			self.click_sequence(page, ["AC", "="])
			self.assertTrue(page.get_by_text(ERROR_TEXT).is_visible())
			self.assertEqual(self.read_display(page), "Error")
			self.wait_and_close(page, browser)

	def test_equals_with_only_one_number_shows_error(self):
		with sync_playwright() as playwright:
			browser, page = self.open_calculator(playwright)
			self.click_sequence(page, ["AC", "7", "="])
			self.assertTrue(page.get_by_text(ERROR_TEXT).is_visible())
			self.assertEqual(self.read_display(page), "Error")
			self.wait_and_close(page, browser)

	def test_equals_with_missing_second_operand_shows_error(self):
		with sync_playwright() as playwright:
			browser, page = self.open_calculator(playwright)
			self.click_sequence(page, ["AC", "5", "＋", "="])
			self.assertTrue(page.get_by_text(ERROR_TEXT).is_visible())
			self.assertEqual(self.read_display(page), "Error")
			self.wait_and_close(page, browser)

	def test_operator_cannot_be_first_character(self):
		with sync_playwright() as playwright:
			browser, page = self.open_calculator(playwright)
			self.click_sequence(page, ["AC", "＋", "2"])
			self.assertEqual(self.read_display(page), "2")
			self.wait_and_close(page, browser)

	def test_second_operator_is_ignored(self):
		with sync_playwright() as playwright:
			browser, page = self.open_calculator(playwright)
			self.click_sequence(page, ["AC", "8", "＋", "−", "2", "="])
			self.assertEqual(self.read_display(page), "10")
			self.wait_and_close(page, browser)


if __name__ == "__main__":
	unittest.main()
