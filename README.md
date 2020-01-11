# Data Storage Rest API with Influx

You can store your data with the help of this RestFul API into InfluxDB.


### Installation

That is the hardest part of all. That's gonna take a very long fight with you and your terminal, so better let's get started immediately.

1. `git clone https://gitlab.fokus.fraunhofer.de/iiot/tub-projects/ws1920_sourcing_aggregation/tree/data_forw`
2. `cd Data-Storage-with-Influx/`
3. `docker-compose up`

and that's it!! 

## How to use this RestFul API:

There are 4 endpoints that the api offers. These are:
1. /newdb
2. /getdbs
3. /deletedb
4. /writereaddata

## 1. New DB
You can create a new database with this. A sample request looks like this:

* URL: `http://localhost:4545/newdb?db_name=mynewdb`
* Method: Post
* Params: db_name
* Response:
```
  If there is not any db with the same name
  
    "A new db with the name mynewdb created"
    
  else there is already a db with exact same name
  
    "Already exists"
```
  
## 2. Get DBs
You get the list of existing databases. A sample might look like following:

* URL: `http://localhost:4545/getdbs`
* Method: Get
* Params: None
* Response:
```
{
    "Existing Databases": [
        "_internal",
        "example",
        "mynewdb"
    ]
}
```


## 3. Delete DB

You can delete an unnecessary database. 

* URL: `localhost:4545/deletedb?db_name=mydb3`
* Method: Post
* Params: db_name
* Response:
```
  If successful
    ` "Database deleted successfully" `
  else
    `"DB does not exist!"`
```

## 4. Writing and Reading Data

You can write data to or read from the database. 

### To write some data, use the following scheme.

* URL: `http://localhost:4545/writereaddata?db_name=mydb2&measurement=machine_1`
* Method: Post
* Params: db_name
* Response: 
```
  If successful
    true
  else
    "Something went wrong during the write process!"
```
Content-Type: `application/json`

Body:
```
{
    "data": [
        {
            "measurement": "machine_1",
            "tags": {
                "writer": "kerem95reiz",
                "thread": 3
            },
            "fields": {
                "max_latency": 10,
                "min_latency": 10
            }
        }

    ]
}
```


### To read data, use the following scheme.

URL: `http://localhost:4545/writereaddata?db_name=mydb2&measurement=machine_1`

Method: Get

Params: db_name, measurement

Response: 
```
  If successful
    `"ResultSet({'('machine_1', None)': [{'time': '2019-11-24T12:21:41.8787895Z', 'max_latency': 10, 'min_latency': 10, 'thread': '3', 'writer': 'kerem95reiz'}]})"`
  else
    `"ResultSet({})"`
```
