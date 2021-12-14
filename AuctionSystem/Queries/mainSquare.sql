select productID, productName, currentPrice  from in_bidding natural join Product
where status = "verified"
