#! /usr/bin/env python3

import json
import requests
import datetime


#Get key of API
with open("key.txt",'r') as keyfile:
    key = keyfile.readline()

def spont(university,end):
    #Get the university's data
    with open("dates.json",'r') as uni_file:
        data = json.loads(uni_file.read())

    #Location of University
    loc = data["universities"][university]["code"]

    #Get the date tomorrow
    start = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    #request data
    req_str = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/FR/eur/en-US/"+ loc +"/anywhere/"+ start +"/" + end +"?apikey="+key
    response = requests.get(req_str)
    
    dat = json.loads(response.text)

    #Places library. id:name
    new_places = {}
    for place in dat["Places"]:
        new_places[str(place["PlaceId"])] = place["Name"]
    
    #Carrier library. id:name
    new_airlines = {}
    for airline in dat["Carriers"]:
        new_airlines[str(airline["CarrierId"])] = airline["Name"]

    #Change ids, to names for places and get date alone from time
    for quote in dat["Quotes"]:
        quote["OutboundLeg"]["OriginId"] = new_places[str(quote["OutboundLeg"]["OriginId"])]
        quote["OutboundLeg"]["DestinationId"] = new_places[str(quote["OutboundLeg"]["DestinationId"])]
        quote["OutboundLeg"]["CarrierIds"][0] = new_airlines[str(quote["OutboundLeg"]["CarrierIds"][0])]
        quote["OutboundLeg"]["DepartureDate"] = quote["OutboundLeg"]["DepartureDate"].split('T')[0]
        quote["InboundLeg"]["OriginId"] = new_places[str(quote["InboundLeg"]["OriginId"])]
        quote["InboundLeg"]["DestinationId"] = new_places[str(quote["InboundLeg"]["DestinationId"])]
        quote["InboundLeg"]["CarrierIds"][0] = new_airlines[str(quote["InboundLeg"]["CarrierIds"][0])]
        quote["InboundLeg"]["DepartureDate"] = quote["InboundLeg"]["DepartureDate"].split('T')[0]

    return dat
    
