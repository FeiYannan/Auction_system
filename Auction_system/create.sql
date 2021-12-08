


create table `Customer`(
    -- `customerID` int(10) AUTO_INCREMENT PRIMARY KEY,
    `customerName` varchar(50) PRIMARY KEY,
    `customerPassword` varchar(50) not null,
    `customerEmail` varchar(50),
    `balance` int(20) not null
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

create table `Product`(
    `productID` int(10) AUTO_INCREMENT PRIMARY KEY,
    `productOwner` varchar(50) not null,
    `productName` varchar(50) not null,
    `productDescription` varchar(1000) not null,
    `price` int(10) not null,
    `status` varchar(50) not null,
    `auctionTime` datetime not null,
    foreign key(`productOwner`) references `Customer`(`customerName`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- check `status` in ("to_be_verified", "verified", "rejected", "in_auction", "unpaid", "paid", "payment_expired", "abortive", "deleted"),


create table `in_bidding`(
    `biddingID` int(10) AUTO_INCREMENT PRIMARY KEY,
    `productID` int(10) not null,
    `currentPrice` int(10) not null,
    `buyer` varchar(50),
    `biddingStatus` int(10) not null,
    foreign key(`productID`) references Product(`productID`),
    foreign key(`buyer`) references Customer(`customerName`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




create table `transaction`(
    `transactionID` int(10) AUTO_INCREMENT PRIMARY KEY,
    `product` int(10) not null,
    `buyer` varchar(50) not null,
    `transactionStatus` varchar(50),
    `finalPrice` int(10) not null,
    foreign key (`buyer`) references `Customer`(`customerName`),
    foreign key (`product`) references `Product`(`productID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--  check `transactionStatus` in ("paid", "unpaid")

create table `Admin`(
    -- `adminID` int(10) AUTO_INCREMENT PRIMARY KEY,
    `adminName` varchar(50) PRIMARY KEY,
    `adminPassword` varchar(50) not null,
    `adminEmail` varchar(50) not null
) ENGINE=InnoDB DEFAULT CHARSET=latin1;