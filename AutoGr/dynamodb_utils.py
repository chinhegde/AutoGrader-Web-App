import boto3
from decimal import Decimal

def save_score_to_dynamodb(email, best_score):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('autograder_students')
    
    # Convert the best_score to Decimal
    best_score_decimal = Decimal(str(best_score))

    # Put item into DynamoDB
    response = table.put_item(
        Item={
            'autograder': email,
            'email': email,
            'best_score': best_score_decimal
        }
    )
    
    print(response)

    return response