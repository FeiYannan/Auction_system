select productID, productName, price, currentPrice, status from Product left join in_bidding using (productID)
where productOwner = '{}'
