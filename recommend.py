#! /usr/bin/env python3
import json
import requests

#get key of api
with open("key.txt",'r') as keyfile:
    key = keyfile.readline()

# takes in possible interval of dates from which
# arrival and departure is going to be compared
def recommend(start, end, location):
    
    #Get int value for camparison
    end = end.split('-')
    #split for calling with partial dates
    start = start.split('-')
    req_str = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/FR/eur/en-US/"+ location +"/us/"+ ("-").join(start[0:2]) +"/" + ("-").join(end[0:2]) +"?apikey="+key
    response = requests.get(req_str)
    #Change to int for comparison
    start = [int(x) for x in start]
    end = [int(x) for x in end]
    #Load the string into a json data
    quotes = json.loads(response.text)
    #List to contain possible quotes
    filtered_quotes = {"Quotes" : []}
    #filter return dates that are before end of holiday and after break starts
    for quote in quotes["Quotes"]:
        #get the date part
        ret_date = quote["InboundLeg"]["DepartureDate"].split('T')[0]
        dep_date = quote["OutboundLeg"]["DepartureDate"].split('T')[0]

        #format strings for comparison
        ret_date = [int(x) for x in ret_date.split('-')]
        dep_date = [int(x) for x in dep_date.split('-')]

        #condition to satisfy
        if dep_date[0] >= start[0] and dep_date[1] >= start[1] and dep_date[2] >= start[2]:
            if ret_date[0] <= end[0] and ret_date[1] <= end[1] and ret_date[2] <= end[2]:
                filtered_quotes["Quotes"].append(quote)
    
    #return filtered json
    return quotes


'''def uni_data(university):
    with open("dates.json",'r') as uni_file:
        data = json.loads(uni_file.read())
    
    for holiday in data["universities"][university]:
'''

recommend("2019-01-01","2019-01-07","de")
