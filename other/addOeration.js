const callEndpoint = {
            "path": `/{solution_id}`,
            "method": "GET",
            "script": "return request.parameters.param",
            "parameters": [{ in : "query",
                name: "param",
                type: "string",
                description: "A testing query parameter"
            }]
        };
return
{
    "swagger": "2.0",
    "info": {
        "version": "v1",
        "title": "test22787",
        "description": "Test service: test22787-1490670475870",
        "contact": {
            "name": "Testing",
            "email": "testing@exosite.com"
        }
    },
    "schemes": [
        "https"
    ],
    "host": "testing-test22787-1490670475870-qa.apps.exosite-staging.io",
    "x-healthPath": "/",
    "basePath": "/",
    "paths": {
        "/{solution_id}": {
            "get": {
                "description": "A testing operation",
                "operationId": "TEST85081",
                "parameters": [],
                "responses": {
                    "204": {
                        "description": "Return the operation result"
                    }
                }
            },
            "parameters": [
                {
                    "in": "path",
                    "name": "solution_id",
                    "type": "string",
                    "description": "A test parameter"
                }
            ]
        }
    }
}

        