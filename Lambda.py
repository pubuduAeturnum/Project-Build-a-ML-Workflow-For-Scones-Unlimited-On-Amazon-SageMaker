#Function-01: Serialize target data-------------------------------------------------------------------------------------
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event['s3_key']## TODO: fill in
    bucket = event['s3_bucket'] ## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket,key,"/tmp/image.png")
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

#Function-02: Classifying the data using ENDPOINT-----------------------------------------------------------------------
import json
import base64
import boto3
#from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT="image-classification-2023-03-04-14-26-35-483" ## TODO: fill in

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['image_data'])## TODO: fill in)
    sagemaker_runtime=boto3.client('sagemaker-runtime')
    
    #serializer = IdentitySerializer('image/png')

    # Instantiate a Predictor
    predictor = sagemaker_runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType="image/png",
        Body=image,
        #Serializer=serializer
    )## TODO: fill in
    
    # Make a prediction:
    inferences = json.loads(predictor['Body'].read().decode('utf-8'))## TODO: fill in
    
    # We return the data back to the Step Function    
    event["inferences"] = inferences
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

#Function-03: Check the inference threshold value-----------------------------------------------------------------------
import json


THRESHOLD = 0.7


def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event['inferences']## TODO: fill in
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = max(list(inferences))>THRESHOLD## TODO: fill in
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
