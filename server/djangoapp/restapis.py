import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print(f'GET from {url}')
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url=url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(f'With status {status_code}')
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(json_payload)
    print(url)
    try:
        response = requests.post(url=url, json=json_payload, params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print(f'With status {status_code}')
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url=url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['body']
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer['address'], city=dealer['city'], full_name=dealer['full_name'],
                                   id=dealer['id'], lat=dealer['lat'], long=dealer['long'],
                                   short_name=dealer['short_name'], st=dealer['st'], state=dealer['state'],
                                   zip=dealer['zip'])
            results.append(dealer_obj)
    return results


def get_dealer_by_id(url, id, **kwargs):
    result = {}
    json_result = get_request(url=url, id=id)
    if json_result:
        dealer = json_result['body'][0]
        dealer_obj = CarDealer(address=dealer['address'], city=dealer['city'], full_name=dealer['full_name'],
                               id=dealer['id'], lat=dealer['lat'], long=dealer['long'],
                               short_name=dealer['short_name'], st=dealer['st'], state=dealer['state'],
                               zip=dealer['zip'])
        result = dealer_obj
    return result


def get_dealer_by_state(url, state, **kwargs):
    results = []
    json_result = get_request(url=url, state=state)
    if json_result:
        dealers = json_result['body']
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer['address'], city=dealer['city'], full_name=dealer['full_name'],
                                   id=dealer['id'], lat=dealer['lat'], long=dealer['long'],
                                   short_name=dealer['short_name'], st=dealer['st'], state=dealer['state'],
                                   zip=dealer['zip'])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealership, **kwargs):
    results = []
    json_result = get_request(url=url, dealership=dealership)
    if json_result:
        reviews = json_result['body']
        for review in reviews:
            review_obj = DealerReview(car_make=review['car_make'], car_model=review['car_model'], car_year=review['car_year'],
                                      dealership=review['dealership'], id=review['id'], name=review['name'],
                                      purchase=review['purchase'], purchase_date=review['purchase_date'], review=review['review'])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    authenticator = IAMAuthenticator('0vNTt1VTbkQCwZw8SHr7BUshxxg7k-mNsTu4tAyQ1EF8')
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=authenticator)
    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/63f9457d-a054-4381-b73e-ec32508f678a')
    response = natural_language_understanding.analyze(features=Features(sentiment=SentimentOptions(targets=[dealer_review])), text=dealer_review).get_result()
    return response['sentiment']['document']['label']
