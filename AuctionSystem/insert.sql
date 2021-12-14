
INSERT INTO `Customer` (`customerName`, `customerEmail`, `customerPassword`, `balance`) VALUES
('yannan', 'yf1213@nyu.edu', 'Yannan123', 1000),
('user1', 'user1@nyu.edu', 'User1', 1000),
('user2', 'user2@nyu.edu', 'User2', 2000);


-- INSERT INTO `Product` (`productOwner`, `productName`, `productDescription`, `price`, `status`) VALUES
-- ('yannan', 'CS textbook', 'This is a textbook for Software Engineering', 500, 'verified'),
-- ('yannan', 'CS textbook', 'This is a textbook for Machine Learning', 1000, 'verified'),
-- ('user1', 'IMA textbook', 'This is a textbook for Live Coding, 2000', 2000, 'verified');



-- INSERT INTO `transaction` (`productID`, `buyer`, `transactionStatus`, `finalPrice`) VALUES
-- (1, "user1", 'paid', 1000),
-- (3, "user2", 'paid', 3000);


INSERT INTO `Admin` (`adminName`, `adminEmail`, `adminPassword`) VALUES
('admin1', 'admin1@nyu.edu', 'Admin1'),
('admin2', 'admin2@nyu.edu', 'Admin2');


-- INSERT INTO `in_bidding` (`ProductID`, `currentPrice`, `buyer`, `biddingStatus`) VALUES
-- (1, 1000, Null, "in_bidding"),
-- (2, 2000, Null, "in_bidding");
