
# Bedrock Agent with Astra DB Vector Search

A serverless AI agent implementation that enables semantic search capabilities by integrating Amazon Bedrock Agents with DataStax Astra DB through AWS Lambda.

## 🎯 Goal

Enable intelligent, context-aware information retrieval by creating a Bedrock Agent that performs vector similarity searches against a knowledge base stored in Astra DB. This solution allows natural language queries to find semantically similar content without exact keyword matching.

## 📋 Solution Overview

This project implements a RAG (Retrieval Augmented Generation) pattern where:

- **Amazon Bedrock Agent** acts as the intelligent interface that understands user queries
- **AWS Lambda** serves as the middleware that processes requests and communicates with the database
- **DataStax Astra DB** stores vectorized content and performs semantic similarity searches using embeddings
- The system returns the top-k most relevant results based on semantic meaning rather than keyword matching

### Key Features

- ✨ Semantic search using vector embeddings
- 🔄 Seamless integration between Bedrock Agents and Astra DB
- 📊 Returns top 5 most similar results with similarity scores
- 🛡️ Secure authentication using Astra DB tokens
- 📝 Structured response format compatible with Bedrock Agent standards

## 🏗️ Architecture Flow

```
┌─────────────────┐
│                 │
│  User Query     │
│  (Natural       │
│   Language)     │
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│                         │
│  Amazon Bedrock Agent   │
│  - Processes query      │
│  - Calls action group   │
│                         │
└────────┬────────────────┘
         │
         │ Invokes Lambda
         │ (with search_term)
         ▼
┌─────────────────────────┐
│                         │
│  AWS Lambda Function    │
│  - Extracts parameters  │
│  - Formats API request  │
│  - Handles errors       │
│                         │
└────────┬────────────────┘
         │
         │ HTTP POST
         │ (Vector similarity query)
         ▼
┌─────────────────────────┐
│                         │
│  DataStax Astra DB      │
│  - Vectorizes query     │
│  - Performs similarity  │
│    search               │
│  - Returns top-k docs   │
│                         │
└────────┬────────────────┘
         │
         │ Results
         ▼
┌─────────────────────────┐
│                         │
│  Lambda Response        │
│  - Formats for Bedrock  │
│  - Returns clean text   │
│                         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│                         │
│  Bedrock Agent          │
│  - Processes results    │
│  - Generates response   │
│                         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│                 │
│  User Response  │
│  (Contextualized│
│   Answer)       │
│                 │
└─────────────────┘
```

## 🔧 Technology Stack

### Cloud Services
- **Amazon Bedrock Agents**: AI agent orchestration and natural language understanding
- **AWS Lambda**: Serverless compute for API integration
- **DataStax Astra DB**: Distributed NoSQL database with vector search capabilities

### Programming & APIs
- **Python 3.x**: Lambda function runtime
- **OpenAPI 3.0**: API specification for Bedrock Agent action groups
- **Astra DB JSON API**: RESTful interface for database operations

### Key Libraries
- `json`: JSON data handling
- `urllib.request`: HTTP requests to Astra DB
- `os`: Environment variable management

## 📦 Components

### 1. Lambda Function (`lambda_function.py`)

**Purpose**: Bridge between Bedrock Agent and Astra DB

**Key Responsibilities**:
- Extract `search_term` from Bedrock Agent event
- Construct vector similarity search queries
- Execute HTTP requests to Astra DB
- Parse and clean results
- Format responses according to Bedrock Agent specifications

**Environment Variables**:
```
astra_token      # Astra DB authentication token
astra_endpoint   # Astra DB API endpoint
keyspace         # Database keyspace (default: default_keyspace)
collection       # Collection name (default: rag_filetranscript)
```

### 2. OpenAPI Specification

**Purpose**: Define the API contract for Bedrock Agent action groups

**Endpoint**: `POST /search`

**Request Body**:
```json
{
  "search_term": "your search query"
}
```

**Response**:
```json
{
  "search_term": "your search query",
  "results": ["result1", "result2", "..."],
  "result_count": 5
}
```

## 🚀 Setup Instructions

### Prerequisites

1. AWS Account with access to:
   - Amazon Bedrock
   - AWS Lambda
   - IAM for permissions

2. DataStax Astra DB:
   - Active database instance
   - Application token generated
   - Collection created with vector embeddings enabled


```

### Step 1: Deploy Lambda Function

1. Create a new Lambda function in AWS Console
2. Upload the `lambda_function.py` code
3. Configure environment variables:
   ```
   astra_token=AstraCS:xxxxx...
   astra_endpoint=https://xxxxx-region.apps.astra.datastax.com
   keyspace=your_keyspace
   collection=rag_filetranscript
   ```
4. Set appropriate timeout (recommended: 30 seconds)
5. Attach IAM role with necessary permissions

### Step 2: Configure Bedrock Agent

1. Create a new Bedrock Agent
2. Add an Action Group
3. Upload the OpenAPI specification
4. Link the Lambda function as the action executor
5. Configure the agent's foundation model
6. Test the integration


```



```





---

**Built with** ❤️ using Amazon Bedrock, AWS Lambda, and DataStax Astra DB



<p align="center">
  <img src="images/screenshot.png" alt="App Screenshot" width="500"/>
</p>



![Alt text]<img width="1479" height="620" alt="BedRockinputoutput" src="https://github.com/user-attachments/assets/c55560f0-1caf-4f61-8792-ecc0132b6fbb" />
