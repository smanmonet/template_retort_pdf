import boto3
from boto3.dynamodb.conditions import Key

# สร้างทางเชื่อมกับ DynamoDB
AWS_DYNAMODB_URL = "http://localhost:8000"

def get_dynamodb_table(table_name):
    """
    เชื่อมต่อกับ DynamoDB และคืนค่า table object
    """
    dynamodb = boto3.resource('dynamodb', endpoint_url=AWS_DYNAMODB_URL)
    return dynamodb.Table(table_name)

#query ข้อมูลจาก Content_statement
def fetch_all_items(table_name_content,name_fk,fk):
    """
    ดึงข้อมูลทั้งหมดจาก DynamoDB table Content_statement
    """
    table = get_dynamodb_table(table_name_content)
    # Query แทนการใช้ Scan
    response = table.query(
        KeyConditionExpression=Key(name_fk).eq(fk)
    )   
    return response.get('Items', [])

# Query ข้อมูลจาก Data_statement,settlement โดยใช้ Contract No
def get_datastatement(table_name_data,name_sk,sk):
    """ 
    ดึงข้อมูลทั้งหมดจาก DynamoDB table Data_statement, settlement
    และเรียงลำดับ Sort Key (sk) จากน้อยไปมาก
    """
    table = get_dynamodb_table(table_name_data)
    response = table.query(
        KeyConditionExpression=Key(name_sk).eq(sk)
    )
    items = response.get('Items', [])
    
    # เรียงข้อมูลใน Python โดยใช้ line_data
    sorted_items = sorted(items, key=lambda x: int(x.get('line_data', float('inf'))))
    return sorted_items