import requests


part_by_name = {
    "128 black": "MPXT3LL/A",
    "128 silver": "MQ003LL/A",
    "128 gold": "MQ063LL/A",
#    "1tb silver": "MQ2L3LL/A",
}


for name, part in part_by_name.items():
    r = requests.get(f"https://www.apple.com/shop/fulfillment-messages?pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/US&parts.0={part}&location=11217")
    data = r.json()

    stores = data["body"]["content"]["pickupMessage"]["stores"]
    print(name)
    for store in stores:
        availability = store["partsAvailability"][part]["pickupDisplay"]
        if availability != "available":
            continue
        print(f"{store['storeName']}: {availability}")
    print()

