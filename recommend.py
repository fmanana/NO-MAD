#! /usr/bin/env python3
import json
import requests

#get key of api
with open("key.txt",'r') as keyfile:
    key = keyfile.readline()

# takes in possible interval of dates from which
# arrival and departure is going to be chosen
def recommend(start, end, location):
    print(start,end,location)
    #split for calling with partial dates
    end = end.split('-')
    start = start.split('-')

    #request url
    req_str = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/FR/eur/en-US/"+ location +"/us/"+ ("-").join(start[0:2]) +"/" + ("-").join(end[0:2]) +"?apikey="+key
    response = requests.get(req_str)

    
    #Load the string into a json data
    quotes = json.loads(response.text)
    #List to contain possible quotes
    filtered_quotes = {"Quotes" : []}

    #Change to int for comparison
    start = [int(x) for x in start]
    end = [int(x) for x in end]

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
    return json.dumps(filtered_quotes)


def uni_data(university):
    #Get the university's data
    with open("dates.json",'r') as uni_file:
        data = json.loads(uni_file.read())
    
    #library to hold possible flights for each holiday
    flights = {}
    counter = 1

    #iterate through each holiday 
    for holiday in data["universities"][university]['holidays']:

        #call function with holiday details and save results
        flights[counter] = recommend(holiday["start"],holiday["end"],data["universities"][university]["code"])
        counter += 1
    
    return flights


result = uni_data("jacobs")
print(recommend("2019-01-01","2019-01-07","de")==result[1])