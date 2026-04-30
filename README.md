# Getting Started
This repo has happy-path tests with Selenium and unhappy-path tests with Playwright. The Selenium tests can be run using a Chrome browser or a Firefox browser. The Playwright tests are run using a Chome browser. 

## Set Up
This project uses `uv` to manage packages and dependencies. To set up the virtual environment, run  
```
uv sync
```

This should create a virtual environment which can be activated by running 
```
source .venv/bin/activate
```


# Running Tests
## Run all tests
```
pytest
```

## Run a single test
```
pytest tests/<test_framework.py>::<test_name>
```

For example,
```
pytest::tests/test_playwright.py::test_invalid_input_login_wrong_password
```

## Running on Chrome/Firefox
The Selenium tests can be run on a Chrome or Firefox browser. To run the tests on the desired browser, run
```
pytest tests/test_selenium.py --browser <chrome/firefox>
```
**Note:** If no `--browser` option is specified, the Selenium tests will be run with Chrome browser. The Playwright tests are only on Chrome browser.

For example,
```
pytest      # or
pytest --browser chrome
```
will run all tests on Chrome.

```
pytest --browser firefox
```
will run Selenium tests on Firefox and Playwright tests on Chrome.

# Note: Demoblaze pagination
There appears to be a pagination bug on Demoblaze. If you go directly to the home page (https://www.demoblaze.com/), you will see the following products.

![](images/initial-products.png)

However, if you click "Next" then "Previous", the products on the page will change and you will see the following products instead.

![](images/stable-products.png)

Subsequent clicking of "Next" then "Previous" will return the 'new' product list. Because of this inconsistency on the first clicking "Next" then "Previous", the Arrange section of `test_pagination_next_then_previous_returns_original_products` in `tests/test_selenium.py` clicks "Next" then "Previous" to stabilize the product list.