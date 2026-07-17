# Data Dictionary

## Gold Fact Sales
The `gold_fact_sales` table stores sales transaction information.

| Column Name | Data Type | Description |
|---|---|---|
| sale_id | String | Unique identifier for each sales transaction |
| date_id | Integer | Foreign key connected to the Date Dimension |
| model_id | Integer | Foreign key connected to the Model Dimension |
| dealer_id | String | Foreign key connected to the Dealer Dimension |
| customer_id | String | Foreign key connected to the Customer Dimension |
| manufacturing_year | Bigint | Manufacturing year of the vehicle |
| mileage_km | Bigint | Total vehicle mileage in kilometres |
| transmission | String | Transmission type of the vehicle |
| listing_price_inr | Bigint | Original listed price of the vehicle in INR |
| discount_percent | Double | Discount percentage applied to the vehicle |
| sale_price_inr | Bigint | Final sale price of the vehicle in INR |
| quantity | Bigint | Number of vehicles sold |
| data_layer | String | Indicates that the record belongs to the Gold layer |
| gold_processed_timestamp | Timestamp | Time when the record was processed into the Gold layer |


## Gold Model Dimension
The `gold_dim_model` table stores vehicle model and technical information.

| Column Name | Data Type | Description |
|---|---|---|
| model_id | Integer | Unique identifier for each model |
| model | String | Mercedes-Benz model name |
| vehicle_class | String | Vehicle category or class |
| engine_size_l | Double | Engine size in litres |
| fuel_type | String | Fuel type of the vehicle |
| fuel_efficiency_mpg | Double | Fuel efficiency measured in miles per gallon |
| data_layer | String | Indicates that the record belongs to the Gold layer |
| gold_processed_timestamp | Timestamp | Time when the record was processed |


## Gold Dealer Dimension
The `gold_dim_dealer` table stores dealer and geographic information.

| Column Name | Data Type | Description |
|---|---|---|
| dealer_id | String | Unique identifier for each dealer |
| dealer_name | String | Name of the dealer |
| city | String | City where the dealer is located |
| state | String | State where the dealer is located |
| region | String | Geographic region of the dealer |
| data_layer | String | Indicates that the record belongs to the Gold layer |
| gold_processed_timestamp | Timestamp | Time when the record was processed |


## Gold Date Dimension
The `gold_dim_date` table stores date-related attributes for time-based analysis.

| Column Name | Data Type | Description |
|---|---|---|
| date_id | Integer | Unique identifier for each date |
| sale_date | Date | Date when the sale occurred |
| day | Integer | Day of the month |
| month_number | Integer | Numeric month value |
| month_name | String | Name of the month |
| quarter | Integer | Quarter of the year |
| year | Integer | Year of the sale |
| data_layer | String | Indicates that the record belongs to the Gold layer |
| gold_processed_timestamp | Timestamp | Time when the record was processed |


## Gold Customer Dimension
The `gold_dim_customer` table stores customer category information.

| Column Name | Data Type | Description |
|---|---|---|
| customer_id | String | Unique identifier for each customer |
| customer_type | String | Type or category of the customer |
| data_layer | String | Indicates that the record belongs to the Gold layer |
| gold_processed_timestamp | Timestamp | Time when the record was processed |