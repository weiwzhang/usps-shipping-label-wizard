# Unit tests for app.py

import easypost
import app.py
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import uuid
import time
import pytest

# verify creating an address
def test_address_creation_verification(driver):
    driver.get("/")

    driver.implicitly_wait(1)
    target_city = driver.find_element_by_css_selector('[name=to_city]')
    target_country = driver.find_element_by_css_selector('[name=to_country]')
    target_street1 = driver.find_element_by_css_selector('[name=to_street1]')
    target_street2 = driver.find_element_by_css_selector('[name=to_street2]')
    target_state = driver.find_element_by_css_selector('[name=state]')
    target_zip = driver.find_element_by_css_selector('[name=to_zip]')
    target_city = str(uuid.uuid4())
    target_country = str(uuid.uuid4())
    target_street1 = str(uuid.uuid4())
    target_street2 = str(uuid.uuid4())
    target_state = str(uuid.uuid4())
    target_zip = str(uuid.uuid4())

    test_address = easypost.Address.create(
        street1='118 2nd St',
        street2='4th Fl',
        city='San Francisco',
        state='CA',
        zip='94105',
        country='U.S.'
    )

    assert test_address.country == target_country
    assert test_address.email is None
    assert test_address.federal_tax_id is None
    assert test_address.state == target_state
    assert test_address.zip == target_zip
    assert test_address.city == target_city
    assert test_address.street1 == target_street1
    assert test_address.street2 == target_street2

# making simple parcel
def test_parcel_creation():
    driver.get("/")

    driver.implicitly_wait(1)
    target_length = driver.find_element_by_css_selector('[name=length]')
    target_height = driver.find_element_by_css_selector('[name=height]')
    target_weight = driver.find_element_by_css_selector('[name=weight]')
    target_width = driver.find_element_by_css_selector('[name=width]')
    target_length = str(uuid.uuid4())
    target_height = str(uuid.uuid4())
    target_width = str(uuid.uuid4())
    target_weight = str(uuid.uuid4())

    test_parcel = easypost.Parcel.create(
        length=10.2,
        width=7.8,
        height=4.3,
        weight=21.2
    )

    assert test_parcel.height == target_height
    assert test_parcel.width == target_width
    assert test_parcel.weight == target_weight
    assert test_parcel.length == target_length

