select productID, productName, price, auctionTime from Product
where status = "verified" and productName like "%{}%"
