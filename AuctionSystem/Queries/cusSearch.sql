select productID, productName, price from Product
where status = "verified" and productName like "%{}%"