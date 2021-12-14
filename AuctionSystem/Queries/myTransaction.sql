select transactionID, productName, transactionStatus, finalPrice, productID from transaction natural join product
where buyer = '{}'
