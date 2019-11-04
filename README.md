## Http server with load-balancer, mongodb and redis cache

#### Balancer schema:

```
digraph {
    rankdir=LR;

    client -> balancer [label="key:value"]
    balancer -> cache [label="action == get"]
    balancer -> server0 [label="key%2 == 0"]
    balancer -> server1 [label="key%2 != 0"]
    server0 -> database
    server1 -> database
}
```

---

``start: docker-compose up``

``build: docker-compose build``

### endpoints:

- `/put POST, PUT `

    Create or update value by key
    
    *Request parameters*:
    
    - **key** - *string*
    
    - **value** - *any*
  
- `/get GET`

    Get value by key
    
    *Request parameters*:
    
    - **key** - *string*
    
    - **no-cache** - *boolean* optional
    
- `/delete DELETE`

    Delete by key
    
    *Request parameters*:
    
    - **key** - *string*
