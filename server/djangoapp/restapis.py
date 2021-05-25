import requests
import json
from . import models
from django.conf import settings
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, apikey = None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if apikey:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth('apikey', apikey), params=kwargs)
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data



# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    # print(dir(json_result))
    if json_result:
        dealers = json_result["body"]["results"]
        for dealer_doc in dealers:
            dealer_obj = models.CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    print(dir(json_result))
    if json_result["statusCode"] != 200:
        return results
    if json_result:
        revs = json_result["body"]["results"]
        for review in revs:
            review_obj = models.DealerReview(
                review['_id'],
                review['dealership'],
                review['name'],
                review['purchase'] if hasattr(review, 'purchase') else False,
                review['review'],
                review['purchase_date'] if hasattr(review, 'purchase_date') else None,
                review['car_make'] if hasattr(review, 'car_make') else None,
                review['car_model'] if hasattr(review, 'car_model') else None,
                review['car_year'] if hasattr(review, 'car_year') else None
            )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    json_data = get_request(
        url=settings.NLU_URL + "/v1/analyze",
        apikey=settings.NLU_KEY,
        version="2021-05-24",
        text=dealer_review,
        features="sentiment",
        return_analyzed_text=True,
        language='en'
    )
    return json_data['sentiment']['document']['label']


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, apikey = None, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        if apikey:
            # Call get method of requests library with URL and parameters
            response = requests.post(url, json=json_payload,  headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth('apikey', apikey), params=kwargs)
        else:
            # Call get method of requests library with URL and parameters
            response = requests.post(url, json=json_payload, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    print(json.dumps(response.text))
    json_data = json.loads(response.text)
    return json_data


