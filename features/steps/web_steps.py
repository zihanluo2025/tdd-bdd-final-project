######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions

ID_PREFIX = "product_"


@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.driver.get(context.base_url)
    # context.driver.save_screenshot('home_page.png')


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the document title for a message"""
    assert message in context.driver.title


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    """Check that text is not anywhere in the page body"""
    element = context.driver.find_element(By.TAG_NAME, "body")
    assert text_string not in element.text


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set a text field by element name (mapped to product_<name>)"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Select a dropdown value by visible text"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Verify selected dropdown value"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    assert element.first_selected_option.text == text


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """Verify a text field is empty"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute("value") == u""


##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """Copy a text field value into a clipboard variable"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute("value")
    logging.info("Clipboard contains: %s", context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """Paste clipboard value into a text field"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)


##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html that is the button text
# in lowercase followed by '-btn' so the Clear button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################

# ----------------------------
# Task 7a: Button click step
# ----------------------------
@when('I press the "{button}" button')
def step_impl(context, button):
    """Click a button by its text using <lower>-btn naming convention"""
    button_id = button.lower().replace(" ", "-") + "-btn"
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.element_to_be_clickable((By.ID, button_id))
    )
    element.click()


# ----------------------------
# Task 7b: Verify text/message present
# ----------------------------
@then('I should see the message "{message}"')
def step_impl(context, message):
    """
    Verify the flash/message area contains text.
    Common ids used in this project: flash_message / message / flash
    """
    possible_ids = ["flash_message", "message", "flash"]
    found = False
    for msg_id in possible_ids:
        elements = context.driver.find_elements(By.ID, msg_id)
        if elements:
            WebDriverWait(context.driver, context.wait_seconds).until(
                expected_conditions.text_to_be_present_in_element((By.ID, msg_id), message)
            )
            found = True
            break
    assert found, "Could not find a message element (flash_message/message/flash)"


# (Used by Task 6d-6g) Verify names appear in the search results table/list
@then('I should see "{text}" in the results')
def step_impl(context, text):
    """
    Verify a text appears in the results area.
    Common result container ids: search_results / results
    Fallback to body if not found.
    """
    possible_ids = ["search_results", "results"]
    container = None
    for rid in possible_ids:
        elems = context.driver.find_elements(By.ID, rid)
        if elems:
            container = elems[0]
            break

    if container is None:
        container = context.driver.find_element(By.TAG_NAME, "body")

    WebDriverWait(context.driver, context.wait_seconds).until(
        lambda d: text in container.text
    )
    assert text in container.text


@then('I should not see "{text}" in the results')
def step_impl(context, text):
    """Verify a text does NOT appear in the results area"""
    possible_ids = ["search_results", "results"]
    container = None
    for rid in possible_ids:
        elems = context.driver.find_elements(By.ID, rid)
        if elems:
            container = elems[0]
            break

    if container is None:
        container = context.driver.find_element(By.TAG_NAME, "body")

    assert text not in container.text


##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by ID_PREFIX so the Name field has an id='product_name'
# We can then lowercase the name and prefix with product_ to get the id
##################################################################

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    """Verify a text input field contains the expected value"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value((By.ID, element_id), text_string)
    )
    assert found


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Change an input field value"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)
