-- Connect to ecommerce_analysis before running this file.
CREATE TABLE IF NOT EXISTS ecommerce_sales (
    Order_ID VARCHAR(30) PRIMARY KEY,
    Customer_ID VARCHAR(30),
    Order_Date DATE,
    Product_Category VARCHAR(100),
    Product_Name VARCHAR(150),
    Quantity INTEGER,
    Unit_Price_USD NUMERIC(12,2),
    Discount_Percent NUMERIC(5,2),
    Payment_Method VARCHAR(50),
    Shipping_City VARCHAR(100),
    Country VARCHAR(100),
    Order_Status VARCHAR(30),
    Customer_Rating NUMERIC(3,2),
    Flag_Future_Date BOOLEAN,
    Flag_Zero_Quantity BOOLEAN,
    Flag_Negative_Quantity BOOLEAN,
    Flag_Negative_Status_Mismatch BOOLEAN,
    Provisional_Line_Value_USD NUMERIC(12,2)
);
