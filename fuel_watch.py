import requests
import json
from collections import OrderedDict
from xml.etree import ElementTree

DATA_FILE = "data.json"

PRODUCTS = "products"
DEFAULT_PRODUCT = "default_product"
SUBURBS = "suburbs"
DEFAULT_SUBURB = "default_suburb"
BRANDS = "brands"

# Data from file


# Load the JSON from the data file
def load_data():

    global data
    with open(DATA_FILE) as json_data:
        data = json.load(json_data, object_pairs_hook=OrderedDict)


# Ask the user to select a product
def select_product():

    print("Products:")
    for key, value in data[PRODUCTS].items():
        print("\t" + key + ": " + value)
    product_msg = "Select a product (default=" + data[DEFAULT_PRODUCT] + "): "
    product_choice = input(product_msg)

    if product_choice == '':
        product_choice = data[DEFAULT_PRODUCT]

    print("You selected " + data[PRODUCTS][product_choice])
    return product_choice


# Ask the user to select a suburb
def select_suburb():

    print("Suburbs:")
    for key, value in data[SUBURBS].items():
        print("\t" + key + ": " + value)
    suburb_msg = "Select a suburb (default=" + data[DEFAULT_SUBURB] + "): "
    suburb_choice = input(suburb_msg)

    if suburb_choice == '':
        suburb_choice = data[DEFAULT_SUBURB]

    print("You selected " + data[SUBURBS][suburb_choice])

    return suburb_choice


# Ask the user to select a brand
def select_brand():

    print("Brands:")
    for key, value in data[BRANDS].items():
        print("\t" + key + ": " + value)
    brand_msg = "Select a brand (default=none): "
    brand_choice = input(brand_msg)

    if brand_choice == "":
        print("No brand selected")
    else:
        print("You selected " + data[BRANDS][brand_choice])

    return brand_choice


# Get the prices with the specified criteria
def get_prices(product, suburb, brand):

    service = "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS"
    parameters = {
        "Product": product,
        "Suburb": suburb
    }

    if brand != '':
        parameters["Brand"] = brand

    # Build URL for request
    url = service + "?" + "&".join("{}={}".format(key, value) for key, value in parameters.items())

    response = requests.get(url)

    return response.text


# Get parameters from user
def get_parameters():

    print()
    product = select_product()
    print()
    suburb = select_suburb()
    print()
    brand = select_brand()
    print()
    response_text = get_prices(product, suburb, brand)

    return response_text


# Display results
def display_results(response_text):

    root = ElementTree.fromstring(response_text)

    print("Results:")
    for item in root.findall("./channel/item"):
        title = item.find("title")
        print("\t" + title.text)


# Main function
def main():

    load_data()
    response_text = get_parameters()
    display_results(response_text)


main()