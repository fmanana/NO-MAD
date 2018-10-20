#! /usr/bin/env python3
import json
import requests

#get key of api
with open("key.txt",'r') as keyfile:
    key = keyfile.readline()

def on_budget(university, budget):
    #format string into int
    budget = int(budget)

    #Get the university's data
    with open("dates.json",'r') as uni_file:
        data = json.loads(uni_file.read())

    #Location of University
    loc = data["universities"][university]["code"]
    #format request url string
    req_url = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/FR/eur/en-US/" + loc + "/anywhere" +"/"+ "anytime/" + "anytime" +"?apikey=" + key

    #perform request and load to json
    response = requests.get(req_url)
    print(response)
    data = json.loads(response.text)

    #Filter out the ones within budget
    filtered_quotes = {"Quotes" : []}
    for quote in data["Quotes"]:
        if quote["MinPrice"] <= budget:
            filtered_quotes["Quotes"].append(quote)

    #Places library. id:name
    new_places = {}
    for place in data["Places"]:
        new_places[str(place["PlaceId"])] = place["Name"]
    
    #Change ids to names for places and get date alone from time
    for quote in filtered_quotes["Quotes"]:
        quote["OutboundLeg"]["OriginId"] = new_places[str(quote["OutboundLeg"]["OriginId"])]
        quote["OutboundLeg"]["DestinationId"] = new_places[str(quote["OutboundLeg"]["DestinationId"])]
        quote["OutboundLeg"]["DepartureDate"] = quote["OutboundLeg"]["DepartureDate"].split('T')[0]
        quote["InboundLeg"]["OriginId"] = new_places[str(quote["InboundLeg"]["OriginId"])]
        quote["InboundLeg"]["DestinationId"] = new_places[str(quote["InboundLeg"]["DestinationId"])]
        quote["InboundLeg"]["DepartureDate"] = quote["InboundLeg"]["DepartureDate"].split('T')[0]

    return filtered_quotes