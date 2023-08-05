# Python AyraDB client library

This module provides a simple interface to perform actions on an AyraDB installation.

## Initialization

The AyraDB class is the main interface to an AyraDB installation.  
In order to instantiate an AyraDB object, a valid <b>host</b> must be provided.

```
from ayradb import AyraDB

client = AyraDB(ip="192.168.0.1")
```

All possible operations a user can perform are described below.  
  
## Create a table

AyraDB allows users to create three different types of tables:
<ul>
<li>FIXED_LENGTH,</li>
<li>PADDED,</li>
<li>NOSQL</li>
</ul>
Convenient APIs to create tables of each type are available.    
  
### Fixed lenght tables
For <i>fixed_length</i> tables, maximum key column size, maximum table size, and at least one field must be provided.
New fields can be added later.
```
table = client.table("new_fixed_length_table")
fill_type = "fixed_length"
fields = [ {"column_label": "field0", "column_max_net_length": 1024},
           {"column_label": "field1", "column_max_net_length": 1024},
           {"column_label": "field2", "column_max_net_length": 1024}]
max_key_column_size_byte = 1024
rct = table.create(fill_type, columns=fields, key_max_size=max_key_column_size_byte).wait_response()
if rct.success is True:
    print("New fixed length table created!")
else:
    print(f"Error code: {rct.error_code}")
```  

### Padded   
For <i>padded</i> tables, at least one field must be provided, and new fields can be added later.  

```
table = client.table("new_padded_table")
fill_type = "padded"
fields = [ {"column_label": "field0"}, {"column_label": "field1"},{"column_label": "field2"}]
max_key_column_size_byte = 1024
rct = table.create(fill_type, columns=fields, key_max_size=max_key_column_size_byte).wait_response()
if rct.success is True:
    print("New padded table created!")
else:
    print(f"Error code: {rct.error_code}")
```  

### Nosql   

<i>Nosql</i> tables do not have a fixed structure, so the <b>fields</b> argument is omitted.

```
table = client.table("new_nosql_table")
fill_type = "nosql"
max_key_column_size_byte = 1024
rct = table.create(fill_type, columns=[], key_max_size=max_key_column_size_byte).wait_response()
if rct.success is True:
    print("New nosql table created!")
else:
    print(f"Error code: {rct.error_code}")
```

## Insert a record   
If the new record is not already contained in table, then it is inserted, otherwise it is updated.

```
key_value = 'key_column'
fields={
            "field0":b'111111111;'*10,
            "field1":b'a'*100,
            "field2":b'1'*100,
        }
ri = table.upsert_record(key_value, fields=fields).wait_response()
if ri.success is True:
    print("New record inserted!")
else:
    print (f"Error code: {ri.error_code}")

```
The <b>fields</b> argument must be specified, and the <b>field value</b> argument must be in the form of a byte Array.

## Read a record

Read can be limited to a subset of fields with the <b>fields</b> argument.
```
key_value = "key_column"
field_names = ["field0", "field2"]
rr = table.read_record(key_value, fields=field_names).wait_response()
if rr.success is True:
    for key, value in rr.content.items():
        print("Field name: " + key)
        print("Field value: " + value.decode())
else:
    print (f"Error code: {rr.error_code}")

```
If the <b>fields</b> argument is set to <i>null</i>, all fields are retrieved.   
```
key_value = "key_column"
rr = table.read_record(key_value, fields=[]).wait_response()
if rr.success is True:
    for key, value in rr.content.items():
        print("Field name: " + key)
        print("Field value: " + value.decode())
else:
    print (f"Error code: {rr.error_code}")

```   

## Delete a record
Deletion can be limited to a subset of fields with the <b>fields</b> argument.   
```
key_value = "first_record"
field_names = ["field0", "field1", "field4"]
rd = table.delete_record(key_value, fields=field_names).wait_response()
if rd.success is True: 
      print("Record successfully deleted!")
else:
    print (f"Error code: {rd.error_code}")

```
If the <b>fields</b> argument is set to <i>null</i>, the whole record is deleted. 
```
key_value = "first_record"
rd = table.delete_record(key_value, fields=[]).wait_response()
if rd.success is True: 
      print("Record successfully deleted!")
else:
    print (f"Error code: {rd.error_code}")

```
The operation completes even if a record with the provided key does not exist in the table.   
   

## Retrieve table structure
Retrieve table structure retrieves the structures of the record of a table.  

```
rts = table.get_structure().wait_response()
if rts.success is True:
    for i in range(len(rts.structure)):
        field = rts.structure[i]
        print(f"Position: {i}, Field name: {field.get('column_label')}, Field max length: {int(field.get('column_max_net_length',-1))} bytes")
else:
    print(f"Error code: {rts.error_code}")
```

## Truncate a table

Truncate table deletes all the records of an existing table, leaving the structure of the table intact and usable.   

```
rt = table.truncate().wait_response()
if rt.success is True:
    print("Table is now empty!")
else:
    print(f"Error code: {rt.error_code}")
```

## Delete a table

Delete table destroys an existing table.

```
rd = table.drop().wait_response()
if rd.success is True:
    print("Table destroyed!")
else:
    print(f"Error code: {rd.error_code}")
```

## Scan a table

A convenient API is provided to allow table scans.  
Each table is composed of a certain number of segments: in order to perform a scan, the number of segments of the table must be retrieved.   
Each segment must be scanned independently.

```
rsi = table.scan_init().wait_response()
if rsi.success is True:
    number_of_segments = rsi.segments
    field_names = ["field0", "field1"]

    for segment in range(0, number_of_segments-1):
        rs = table.scan(segment= segment, fields=field_names).wait_response()
        if rs.success is True:
            for i in range(len(rs.content)):
            //DO SOMETHING WITH CURRENT RECORD
        else:
            print (f"Error code: {rs.error_code}")
else:
        print (f"Error code: {rsi.error_code}")   
```

## Connection handling
When all operations are completed, it's best practice to close the connection with the following command.

```
client.close_connection()
```

## Error handling 

When an action fails, a response object is returned to the user. <i>Success</i> will return <i>false</i> in case of a failure.  
The response object contains a description of the error and an error code.

