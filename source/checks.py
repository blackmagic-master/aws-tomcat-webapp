def check_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Error: {}".format(response.status))
        raise Exception(response.text)

def check_if_true(response):
    if response['Return'] != True:
        print("Error: {}".format(response.status))
        raise Exception(response.text)