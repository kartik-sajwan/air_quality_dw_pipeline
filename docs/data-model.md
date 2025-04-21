# Data Model Design

This data model is in 3rd Normal Form (3NF) as

- each column holds atomic values (no arrays or nested objects)
- all non-key attributes are fully functionally dependent on the whole primary key
- no transitive dependencies (non-key fields are not dependedn on other non-key fields)


# Further improvements

- we can add a dimension table for time, to optimize query performance
- we can track SCD (Slowly Changing Dimensions)
 ex: location_name changes or sensor co-ordinates change