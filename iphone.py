import requests
import boto3
import os


part_by_name = {
    "128 black": "MPXT3LL/A",
    "128 silver": "MQ003LL/A",
    "128 gold": "MQ063LL/A",
#    "1tb silver": "MQ2L3LL/A",
}

class SnsWrapper:
    """Encapsulates Amazon SNS topic and subscription functions."""
    def __init__(self, client):
        """
        :param sns_resource: A Boto3 Amazon SNS resource.
        """
        self.client = client

    def publish_message(self, message):
        self.client.publish(
            TopicArn=os.getenv("TOPIC_ARN"), Message=message)


def handler(event, context):
    available = []
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
            available.append(f"{name}, {store['storeName']}: available")
        print()
    if available:
        wrapper = SnsWrapper(boto3.client('sns'))
        wrapper.publish_message("\n".join(available))


if __name__ == "__main__":
    handler({}, {})