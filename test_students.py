import os
import time
from playwright.sync_api import Playwright, sync_playwright

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the main page
    page.goto("http://127.0.0.1:5000/")
    time.sleep(2)  # Delay to observe the page load

    # Click on "Top Students" link
    page.get_by_role("link", name="Top Students").click()
    time.sleep(2)  # Delay after navigating to the "Top Students" page

    # Fill the form
    page.get_by_label("Student Name:").fill("New student")
    time.sleep(1)  # Delay after filling in the student name

    page.get_by_label("Grade:").fill("good")
    time.sleep(1)  # Delay after filling in the grade

    # Upload a photo using an absolute file path
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "static", "images", "aram.jpg")
    
    page.get_by_label("Upload Photo:").set_input_files(file_path)
    time.sleep(2)  # Delay after uploading the file

    # Click the "Add Student" button
    page.get_by_role("button", name="Add Student").click()
    time.sleep(3)  # Delay to observe the result after clicking

    # Close the browser after a short delay
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
