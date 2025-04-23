from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

def run_bot(job):
    options = Options()
    # Run in non-headless mode for debugging
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        successful_signups = 0
        for i in range(job.limit):
            # Generate dynamic data
            fullName = f"{job.username_prefix}{i+1:03}"
            email = f"{fullName}@example.com"
            password = "Test@1234"
            phone = f"0300{i+1:07}"
            dob_raw = "2010-01-01"  # User is 15 years old
            dob = datetime.strptime(dob_raw, "%Y-%m-%d").strftime("%d/%m/%Y")  # DD/MM/YYYY (e.g., "01/01/2010")
            school = f"School {i+1}"
            city = "Lahore"  # Confirm this value
            gender = "Male"
            grade = "66ed9c880763f6a5e24a74a7"

            # Open the target page
            driver.get(job.target_url)
            time.sleep(2)

            # Fill form fields using placeholders
            driver.find_element(By.XPATH, '//input[@placeholder="e.g. John Doe"]').send_keys(fullName)
            driver.find_element(By.XPATH, '//input[@placeholder="e.g. johndoe@gmail.com"]').send_keys(email)
            driver.find_element(By.XPATH, '//input[@placeholder="e.g. 03001234567"]').send_keys(phone)

            # Handle DOB field with React DatePicker
            dob_field = driver.find_element(By.XPATH, '//input[@placeholder="Date of Birth"]')
            dob_field.click()  # Open the date picker

            # Wait for the date picker popup to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker"))
            )

            # Navigate to the year (2010)
            # Click the year/month header to show the year selection view
            try:
                # Update selector based on actual DatePicker structure
                year_month_header = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'react-datepicker__month') or contains(@class, 'react-datepicker__header')]"))
                )
                year_month_header.click()
                time.sleep(0.5)
            except:
                print("Year/month header not found. Inspect the DatePicker structure.")

            # Select the year (2010)
            while True:
                try:
                    year = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'react-datepicker__year-text') and text()='2010']"))
                    )
                    year.click()
                    break
                except:
                    # Click the "previous" arrow to go to earlier years
                    try:
                        prev_arrow = driver.find_element(By.XPATH, "//*[contains(@class, 'react-datepicker__navigation--previous')]")
                        prev_arrow.click()
                        time.sleep(0.5)
                    except:
                        print("Previous arrow not found. Adjust the selector.")
                        break

            # Select the month (January)
            try:
                month = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'react-datepicker__month-text') and text()='Jan']"))
                )
                month.click()
                time.sleep(0.5)
            except:
                print("Month 'Jan' not found. Adjust the selector or month text.")

            # Select the day (1st)
            try:
                day = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'react-datepicker__day') and text()='1' and not(contains(@class, 'react-datepicker__day--outside-month'))]"))
                )
                day.click()
                time.sleep(1)
            except:
                print("Day '1' not found. Adjust the selector.")

            # Verify the field value (for debugging)
            dob_value = dob_field.get_attribute("value")
            print(f"DOB field value after selection: {dob_value}")

            driver.find_element(By.XPATH, '//input[@placeholder="e.g. Beaconhouse School System"]').send_keys(school)
            driver.find_element(By.XPATH, '//input[@placeholder="Password"]').send_keys(password)
            driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys(password)

            # Dropdowns
            Select(driver.find_element(By.XPATH, '//select[.//option[contains(text(), "Select Grade")]]')).select_by_value(grade)
            Select(driver.find_element(By.XPATH, '//select[.//option[contains(text(), "Select City")]]')).select_by_value(city)
            Select(driver.find_element(By.XPATH, '//select[.//option[contains(text(), "Select Gender")]]')).select_by_visible_text(gender)

            # Submit button
            driver.find_element(By.XPATH, "//button[contains(text(), 'Play Now')]").click()
            time.sleep(3)  # Wait for submission to process

            # Verify registration success
            try:
                success_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Thank you')]").text
                print(f"Signup {i+1} successful for {email}: {success_message}")
                successful_signups += 1
            except:
                try:
                    error_message = driver.find_element(By.XPATH, "//*[contains(@class, 'error')] | //*[contains(text(), 'already exists')] | //*[contains(text(), 'required')]").text
                    print(f"Signup {i+1} failed for {email}: {error_message}")
                except:
                    current_url = driver.current_url
                    if "success" in current_url.lower():
                        print(f"Signup {i+1} successful for {email}: Redirected to success page ({current_url})")
                        successful_signups += 1
                    else:
                        print(f"Signup {i+1} failed for {email}: Unknown reason (no success or error message found)")

        # Update job status
        if successful_signups == job.limit:
            job.status = "Completed"
            print(f"All {job.limit} signups completed successfully")
        else:
            job.status = "Failed"
            print(f"Only {successful_signups}/{job.limit} signups succeeded")
        job.save()

    except Exception as e:
        print("Bot error:", e)
        job.status = "Failed"
        job.save()

    finally:
        driver.quit()