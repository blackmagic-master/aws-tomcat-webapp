# checking if the response wasn't an error using Metadata
def check_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Error: {}".format(response.status))
        raise Exception(response.text)

# checking if the response wasn't an error using Return
def check_if_true(response):
    if response['Return'] != True:
        print("Error: {}".format(response.status))
        raise Exception(response.text)