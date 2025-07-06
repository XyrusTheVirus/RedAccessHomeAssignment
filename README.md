# Red Access Home Assignment 
## Description 
The REST API implemented with FastAPI using the MVC pattern, supporting clear separation of concerns across controllers, models, services, and repositories.
* Database: MongoDB is used as the primary NoSQL document store, leveraging motor for asynchronous access and pydantic for schema validation.
* Task Queue & Caching: Background tasks are handled via Celery over Redis, which also serves as a high-performance caching and rate-limiting layer.
* Asynchronous Design: Built fully asynchronous for high concurrency and non-blocking I/O using async def, including DB, Redis, and background tasks.
* Containerized Environment: All components run in isolated Docker containers within a shared Docker network, enabling service discovery, scaling, and easy orchestration.
* Extensibility & Maintainability: The API is designed to be highly modular and easily extensible, following clean architecture principles while minimizing boilerplate code and strictly adhering to DRY practices.
* Environment Management: Configuration is managed via .env files and injected cleanly using pydantic.BaseSettings for environment-specific overrides.
This architecture supports rapid iteration, clean scaling, and easy maintainability, while remaining flexible enough to support evolving business logic and integrations.

## Installation 
To run the project, please run the following command:
``` 
docker-compose up -d
```
The root directory inside the api container is **app**, therefore to enable the interpreter import service to work in IDE like PyCharm, require to set root directory as **app/**

## Endpoints
The API endpoints in a formation of: customers{customer_id}/rules/*.
The REST API endpoints, describes as follow:
* Create endpoint:
  ```
  curl --location 'http://localhost:8000/customers/68695dd46c9b624871baa8b9/rules/' \
  --header 'Content-Type: application/json' \
  --data '{
    "name": "ruleOfAllRules6",
    "description": "This is the rule of all rules",
    "ip": "192.168.132.1",
    "expired_date": "2025-07-04"
  }'

* Update endpoint:
  ```
  curl --location --request PUT 'http://localhost:8000/customers/68695dd46c9b624871baa8b9/rules/6869877a2d9ec9831f9fac74' \
  --header 'Content-Type: application/json' \
  --data '{
    "name": "ruleOfAllRules"
  }'

* Delete endpoint:
  ```
  curl --location --request DELETE 'http://localhost:8000/customers/68695dd46c9b624871baa8b9/rules/6869877a2d9ec9831f9fac74'

* Batch endpoint:
  ```
  curl --location 'http://localhost:8000/customers/6868e23dedb77701c2baa8ba/rules/~' \
  --header 'Content-Type: application/json' \
  --data '[
    {
      "operation": "create",
      "data": {
        "name": "rule9",
        "description": "test",
        "ip": "127.0.0.1",
        "expired_date": "2025-12-01T00:00:00Z"
      }
    },
    {
      "operation": "update",
      "data": {
        "id": "68692dbb8c7a3eb3f0e58bef",
        "name": "updated name"
      }
    },
    {
      "operation": "delete",
      "data": {
        "id": "68692dbb8c7a3eb3f0e58bef"
      }
    }
  ]'

**NOTE:** To simulate the endpoints, you should create customer in customers collection inside MongoDB (Sorry, didn't have time to implement one 😞 )

## API Structure
The API as mentioned, built on the MVC methodology (Excerpts for the views) and support extensibility and easy interfacing for further implementation.
The API components, will describe as follow: 
* **controllers-** Responsible to define routes, parsing requests and response bodies and connect between the other parts of the system
* **middlewares-** Gateway for the controllers. Determine whether requests are valid or not
* **validators-** Responsible to examine the data integrity, which not necessarily doming form request body 
* **models-** Define DB entity. In our case MongoDB collections
*  **models.dto-** Responsible to validate request bodies field for each model
*  **repositories-** Responsible to handle data coming to/from DB
*  **events-** Responsible to define behaviour happened before/after each request
*  **services-**- Responsible to serve advance utility implementation for the API components
*  **decorators-** Responsible to extend functions behaviour and reduce boilerplates
*  **tasks-** Responsible to schedule API timing requirements
*  **migrations-** Responsible to populate DB entities  

## Assignments Concepts Keys
* Each request support validation, either on the request body and the customer id existence
* **Automatic Expiration Cleanup-** Implemented with celery tasks mechanism through Redis and it run every midnight to delete expired rules
* **Bulk Operations Endpoint-** Designed to support multiple operations (cerate, update and delete) by possessing a ** operation ** field to describe the action behaviour
* **Audit Logging-** Implemented with python decorator, attached to each repository method, hence ensure all requests with their request body and extra information, will be documented
* **Rate Limiting Customer-** Here, the customer’s request rate limit is configured inside the customer's collection. The rate limit validation is being conducted inside middleware and the rate limit information is being managed by Redis caching mechanism for each customer. We also use redis locking mechanism to ensure data integrity, when playing in multi process environment

  ## Keys For Improvements
  There are some keys for improvement I would add to the API for better performance and scalability. I'll describe the here:
* Although the bulk operation is implement with async behaviour i would recommended to dispatch each operation or sub groups of them to task queue so we can return rapid response to the end user and then publish him the final result via Redis pub/sub for instance 😜
* For the audit logging in case it is prone to gain high volume, I would suggest to use MongoDB sharding to mitigate the I/O operations
* As a consequence, I would also try to separate the logging operations to event driven utility like Kafka so we reduce all Http requests responsibility 
