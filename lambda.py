

import json 
import os 
import urllib.request 
def lambda_handler(event, context): 
    print("Function has now entered LAMBDA FUNCTION") 
    print(event) 
    # Extract search term from event 
    # Print  event to check  the structure 
    print("Complete event:", json.dumps(event, indent=2)) 
     
    # Extract parameters from Bedrock Agent’s event structure 
    # Bedrock Agents parameters are passed in event['parameters'] 
    search_term = None 
     
    # Extract as per Bedrock Agent format’s parameters array  
    if 'parameters' in event: 
        for param in event['parameters']: 
            if param.get('name') == 'search_term': 
                search_term = param.get('value') 
                break 
         
    if not search_term: 
        return { 
            'statusCode': 400, 
            'body': json.dumps({'error': 'search_term is required'}) 
        } 
     
    # Read and check configuration parameters from  respective environment variables 
    astra_token = os.environ.get('astra_token') 
    astra_endpoint = os.environ.get('astra_endpoint') 
    keyspace = os.environ.get('keyspace', 'default_keyspace') 
    collection = os.environ.get('collection', 'rag_filetranscript') 
     
    # Create appropriate API URL 
    api_url = f"{astra_endpoint}/api/json/v1/{keyspace}/{collection}" 
     
    # Vector similarity search query  to search based on semantic similarity 
    query_data = { 
        "find": { 
            "sort": { 
                "$vectorize": search_term  # This will find semantically similar content 
            }, 
            "projection": { 
                "$vectorize": 1  # Only return the text content 
            }, 
            "options": { 
                "limit": 5,  # Return top 5 most similar results 
                "includeSimilarity": True  # Include similarity scores 
            } 
        } 
    } 
     
    try: 
        # Prepare request 
        headers = { 
            'Content-Type': 'application/json', 
            'X-Cassandra-Token': astra_token 
        } 
         
        # Make HTTP request 
        req = urllib.request.Request( 
            api_url, 
            data=json.dumps(query_data).encode('utf-8'), 
            headers=headers, 
            method='POST' 
        ) 
         
        # Execute request 
        with urllib.request.urlopen(req) as response: 
            result = json.loads(response.read().decode('utf-8')) 
         
        # Extract only the text content from all of the ‘top-k’ $vectorize fields 
        clean_results = [] 
        if 'data' in result and 'documents' in result['data']: 
            for doc in result['data']['documents']: 
                if '$vectorize' in doc: 
                    clean_results.append(doc['$vectorize']) 
         
        print("Full event:", json.dumps(clean_results, indent=2)) 
        # Return response in Bedrock Agent format 
        return format_bedrock_response( 
            event, 
            200, 
            { 
                'search_term': search_term, 
                'results': clean_results, 
                'result_count': len(clean_results) 
            } 
        ) 
         
    except json.JSONDecodeError as e: 
        print(f"JSON parsing error: {str(e)}") 
        return format_bedrock_response( 
            event, 
            400, 
            {'error': f'Invalid JSON format: {str(e)}'} 
        ) 
     
    except urllib.error.HTTPError as e: 
        print(f"HTTP error: {str(e)}") 
        return format_bedrock_response( 
            event, 
            500, 
            {'error': f'Astra DB request failed: {str(e)}'} 
        ) 
     
    except Exception as e: 
        print(f"Unexpected error: {str(e)}") 
        return format_bedrock_response( 
            event, 
            500, 
            {'error': str(e)} 
        ) 
def format_bedrock_response(event, status_code, body): 
    """ 
    Format response for Amazon Bedrock Agent. 
    Bedrock expects a very specific response format. 
    """ 
    return { 
        "messageVersion": "1.0", 
        "response": { 
            "actionGroup": event.get('actionGroup', 'default'), 
            "apiPath": event.get('apiPath', '/search'), 
            "httpMethod": event.get('httpMethod', 'POST'), 
            "httpStatusCode": status_code, 
            "responseBody": { 
                "application/json": { 
                    "body": str(body) if isinstance(body, str) else json.dumps(body) 
                } 
            } 
        } 
    } 
