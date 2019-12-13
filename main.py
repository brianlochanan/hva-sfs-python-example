from api.amsterdam_api import AmsterdamApi
from api.ns_api import NSApi
from collections import Counter

def trash_bins():
    amsterdam_api = AmsterdamApi()
    list_trash_bins = amsterdam_api.get_trash_bins()

    print("Overview of trash bins in Amsterdam")

    for trash_bin in list_trash_bins:
        print(
            str(trash_bin['id']) + "\t" +
            trash_bin['name'] + "\t" +
            trash_bin['type'] + "\t" +
            trash_bin['address']
        )

# Get keys by duplicate values
def getKeysByValues(dictOfElements, listOfValues):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        # If value is duplicated then append key to the list
        if item[1] in listOfValues:
            listOfKeys.append(item[0])
    return  listOfKeys

def main():
    print("NS API Test")
    ns_api = NSApi()

    # NSApiGet a list of train stations
    # print(ns_api.get_train_stations())

    # Get a list of disruptions
    # print(ns_api.get_disruptions())

    # Extend all stations with disruptions to get 1 array
    disruption_list = []
    for disruption in ns_api.get_disruptions():
        disruption_list.extend(disruption.get("stations"))

    # Get the amount of total stations with and without disruptions
    counter = 0
    for train_stations in ns_api.get_train_stations():
        counter = counter + 1

    # Get a dict of counters foreach disruption
    c = (Counter(disruption_list))

    # Divide the amount of disruptions by the total amount of trainstations
    print(str("Percentage of total disruptions is: ") + str((len(c)/counter)*100))

    # Get the station with the most disruptions
    key_with_max_value = (max(c, key=c.get))

    print("Station, Amount of disruption")
    for key, value in sorted(c.items()):
        for trainstation in ns_api.get_train_stations():
                if trainstation.get("code") == str(key).upper():
                    print(trainstation.get("name"), ": ", value)

    # Get all the stations with the most disruptions
    listOfKeys = getKeysByValues(c, [c[key_with_max_value]])

    print("\nMost common disruptions for trainstations: ")

    # Iterate over the list of values
    for key in listOfKeys:
        for trainstation in ns_api.get_train_stations():
                if trainstation.get("code") == str(key).upper():
                    print(trainstation.get("name"))

    # Variable for getting the train station with the most delay in seconds
    max_sum_seconds = 0

    # Loop through all the train stations
    for train_station in ns_api.get_train_stations():

        id = train_station.get('id')
        sum_seconds = 0

        # Loop through all departures for each train station
        for delay_in_seconds in ns_api.get_departures(id):
            seconds = delay_in_seconds.get('delay_seconds')

            # Sum delay seconds for each departure on that trainstation
            if seconds != 0:
                sum_seconds = sum_seconds + seconds

            # Get the train station with the most delay in seconds
            if sum_seconds > max_sum_seconds:
                max_sum_seconds = sum_seconds
                trainstation = train_station.get("name")

    print(str("\nTrainstation: ") + trainstation + str(" has the most delay with: ") + str(max_sum_seconds) + str(
        " seconds delay."))

if __name__ == "__main__":
    main()
