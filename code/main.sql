-- This table stores cart information for each user, including when it was created.
CREATE TABLE `cart`  (
  `cartID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cartID`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  INDEX `idx_cart_username`(`username` ASC) USING BTREE,
  INDEX `idx_cart_created_at`(`created_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- This table associates specific items with a given cart, tracking quantity.
CREATE TABLE `cart_items`  (
  `cartItemID` int NOT NULL AUTO_INCREMENT,
  `cartID` int NOT NULL,
  `itemID` int NOT NULL,
  `quantity` int NOT NULL DEFAULT 1,
  PRIMARY KEY (`cartItemID`) USING BTREE,
  UNIQUE INDEX `unique_cart_item`(`cartID` ASC, `itemID` ASC) USING BTREE,
  INDEX `idx_cart_items_cartID_itemID`(`cartID` ASC, `itemID` ASC) USING BTREE,
  INDEX `idx_cart_items_cartID`(`cartID` ASC) USING BTREE,
  INDEX `idx_cart_items_itemID`(`itemID` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 39 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- This table holds all item records, each with a name, price, description, and image source.
CREATE TABLE `item`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `img_src` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_item_name`(`name` ASC) USING BTREE,
  INDEX `idx_item_price`(`price` ASC) USING BTREE,
  FULLTEXT INDEX `ft_idx_item_name_description`(`name`, `description`)
) ENGINE = InnoDB AUTO_INCREMENT = 64 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- This table represents items within an order, including the price at the time of ordering.
CREATE TABLE `order_items`  (
  `order_item_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `item_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  PRIMARY KEY (`order_item_id`) USING BTREE,
  INDEX `idx_order_items_order_id`(`order_id` ASC) USING BTREE,
  INDEX `idx_order_items_item_id`(`item_id` ASC) USING BTREE,
  INDEX `idx_order_items_orderID_itemID`(`order_id` ASC, `item_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- This table keeps basic information about an order, including total amount and status.
CREATE TABLE `orders`  (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `order_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total_amount` decimal(10, 2) NOT NULL,
  `status` enum('Pending','Confirmed','Shipped','Delivered','Canceled','Refund') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Pending',
  PRIMARY KEY (`order_id`) USING BTREE,
  INDEX `idx_orders_username`(`username` ASC) USING BTREE,
  INDEX `idx_orders_order_date`(`order_date` ASC) USING BTREE,
  INDEX `idx_orders_status`(`status` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- This table maintains refund requests, storing user reasons and admin reasons for any status updates.
CREATE TABLE `refund_requests`  (
  `refund_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `request_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` enum('Pending','Approved','Rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Pending',
  `admin_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`refund_id`) USING BTREE,
  INDEX `idx_refund_order_id`(`order_id` ASC) USING BTREE,
  INDEX `idx_refund_username`(`username` ASC) USING BTREE,
  INDEX `idx_refund_status`(`status` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- This trigger updates the related order status to 'Canceled' when a refund request is approved
-- and reverts it back to 'Pending' when a request is rejected.
CREATE DEFINER = `CaoBoyu`@`%` TRIGGER `after_refund_approval` AFTER UPDATE ON `refund_requests` FOR EACH ROW BEGIN
    -- Check if the status is updated from 'Pending' to 'Approved'
    IF OLD.`status` = 'Pending' AND NEW.`status` = 'Approved' THEN
        -- Update the corresponding order's status to 'Canceled'
        UPDATE `orders`
        SET `status` = 'Canceled'
        WHERE `order_id` = NEW.`order_id`;
    END IF;
    IF OLD.`status` = 'Pending' AND NEW.`status` = 'Rejected' THEN
        -- Update the corresponding order's status to 'Pending'
        UPDATE `orders`
        SET `status` = 'Pending'
        WHERE `order_id` = NEW.`order_id`;
    END IF;
END;

-- This table stores user credentials, information about admin rights, and whether the account is frozen.
CREATE TABLE `user`  (
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  `is_frozen` tinyint(1) NOT NULL DEFAULT 0,
  `img_src` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/%E5%A4%B4%E5%83%8F.png',
  PRIMARY KEY (`username`) USING BTREE,
  INDEX `idx_user_is_admin`(`is_admin` ASC) USING BTREE,
  INDEX `idx_user_is_frozen`(`is_frozen` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- This trigger automatically creates a new cart entry for every newly inserted user record.
CREATE DEFINER = `CaoBoyu`@`%` TRIGGER `after_user_insert` AFTER INSERT ON `user` FOR EACH ROW BEGIN
    -- Insert the corresponding cart record
    INSERT INTO `cart` (`username`) VALUES (NEW.`username`);
END;

-- Foreign key constraints linking carts, items, orders, refund requests, and users.
ALTER TABLE `cart` ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `cart_items` ADD CONSTRAINT `cart_items_ibfk_1` FOREIGN KEY (`cartID`) REFERENCES `cart` (`cartID`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `cart_items` ADD CONSTRAINT `cart_items_ibfk_2` FOREIGN KEY (`itemID`) REFERENCES `item` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `order_items` ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `order_items` ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `orders` ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `refund_requests` ADD CONSTRAINT `refund_requests_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `refund_requests` ADD CONSTRAINT `refund_requests_ibfk_2` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE RESTRICT;

-- This procedure adds an item to a user's cart or updates its quantity if already present.
DELIMITER %%
DROP PROCEDURE `first`.`AddItemToCart`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`AddItemToCart`(
    IN `input_username` VARCHAR(255),
    IN `input_itemID` INT,
    IN `input_quantity` INT
)
BEGIN
    DECLARE v_cartID INT;
    DECLARE v_existing_quantity INT DEFAULT 0;
    -- Check if the item already exists in the cart
    SELECT `cartID` INTO v_cartID FROM `cart` WHERE `username` = input_username;
    SELECT `quantity` INTO v_existing_quantity 
    FROM `cart_items` 
    WHERE `cartID` = v_cartID AND `itemID` = input_itemID;

    -- If item already exists, update the quantity
    IF v_existing_quantity > 0 THEN
        UPDATE `cart_items` 
        SET `quantity` = `quantity` + input_quantity 
        WHERE `cartID` = v_cartID AND `itemID` = input_itemID;
    ELSE
        -- If item does not exist, insert a new record
        INSERT INTO `cart_items` (`cartID`, `itemID`, `quantity`) 
        VALUES (v_cartID, input_itemID, input_quantity);
    END IF;
END%%
DELIMITER ;

-- This procedure checks the user login by verifying password and account status.
DELIMITER %%
DROP PROCEDURE `first`.`CheckUserLogin`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`CheckUserLogin`(
    IN `input_username` VARCHAR(255),
    IN `input_password` VARCHAR(255)
)
BEGIN
    DECLARE v_stored_password VARCHAR(255);
    
    -- Check if the username exists
    IF NOT EXISTS (SELECT 1 FROM `user` WHERE `username` = input_username) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The username does not exist';
    END IF;
    
    -- Get the stored password
    SELECT `password` INTO v_stored_password 
    FROM `user` 
    WHERE `username` = input_username;
    
    -- Verify the password
    IF v_stored_password != input_password THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Incorrect password';
    END IF;
    
    -- Check if the user is frozen
    IF EXISTS (SELECT 1 FROM `user` WHERE `username` = input_username AND `is_frozen` = TRUE) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The user account is frozen';
    END IF;
    
    -- Return success message and user information
    SELECT 
        `username`,
        `is_admin`,
        `is_frozen`,
        `img_src`
    FROM `user`
    WHERE `username` = input_username;
END%%
DELIMITER ;

-- This procedure creates a new order from the user's cart items and clears their cart.
DELIMITER %%
DROP PROCEDURE `first`.`CreateOrder`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`CreateOrder`(
    IN `input_username` VARCHAR(255)
)
BEGIN
    DECLARE v_cartID INT;
    DECLARE v_total_amount DECIMAL(10,2);
    
    START TRANSACTION;
    
    -- Get the user's cartID
    SELECT `cartID` INTO v_cartID FROM `cart` WHERE `username` = input_username;
        
    -- Calculate the total amount
    SELECT SUM(ci.`quantity` * i.`price`) INTO v_total_amount
    FROM `cart_items` ci
    JOIN `ITEM` i ON ci.`itemID` = i.`id`
    WHERE ci.`cartID` = v_cartID;
    
    -- Check if the cart is empty
    IF v_total_amount IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The cart is empty, cannot create an order';
    END IF;
    
    -- Create a new order
    INSERT INTO `orders` (`username`, `total_amount`, `status`)
    VALUES (input_username, v_total_amount, 'Pending');
    
    SET @new_order_id = LAST_INSERT_ID();
    
    -- Insert order items
    INSERT INTO `order_items` (`order_id`, `item_id`, `quantity`, `price`)
    SELECT @new_order_id, ci.`itemID`, ci.`quantity`, i.`price`
    FROM `cart_items` ci
    JOIN `ITEM` i ON ci.`itemID` = i.`id`
    WHERE ci.`cartID` = v_cartID;
    
    -- Clear the cart
    DELETE FROM `cart_items` WHERE `cartID` = v_cartID;
    
    COMMIT;
    
    SELECT 'Order created successfully' AS Message, @new_order_id AS OrderID;
END%%
DELIMITER ;

-- This procedure decreases the quantity of an item in the cart, removing the entry if quantity reaches zero.
DELIMITER %%
DROP PROCEDURE `first`.`DecreaseItemQuantity`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`DecreaseItemQuantity`(
    IN `input_username` VARCHAR(255),
    IN `input_itemID` INT,
    IN `input_quantity` INT
)
BEGIN
    DECLARE v_cartID INT;
    DECLARE v_current_quantity INT;

    -- Get the user's cartID
    SELECT `cartID` INTO v_cartID FROM `cart` WHERE `username` = input_username;

    -- Get the current item quantity
    SELECT `quantity` INTO v_current_quantity 
    FROM `cart_items` 
    WHERE `cartID` = v_cartID AND `itemID` = input_itemID;

    -- Update the item quantity
    UPDATE `cart_items` 
    SET `quantity` = `quantity` - input_quantity 
    WHERE `cartID` = v_cartID AND `itemID` = input_itemID;

    -- If the quantity is zero, delete the item
    -- Check if the updated quantity is NULL, if so, delete the item
    IF (SELECT `quantity` FROM `cart_items` WHERE `cartID` = v_cartID AND `itemID` = input_itemID) <= 0 THEN
        DELETE FROM `cart_items` 
        WHERE `cartID` = v_cartID AND `itemID` = input_itemID;
    END IF;

END%%
DELIMITER ;

-- This procedure retrieves the admin_reason field for a given order's refund request.
DELIMITER %%
DROP PROCEDURE `first`.`GetAdminReasonForRefund`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`GetAdminReasonForRefund`(
    IN `input_order_id` INT
)
BEGIN
    -- Get the admin reason for the refund request
    SELECT `admin_reason`
    FROM `refund_requests`
    WHERE `order_id` = input_order_id;
END%%
DELIMITER ;

-- This procedure returns detailed information about a specific order, including item details and subtotals.
DELIMITER %%
DROP PROCEDURE `first`.`GetOrderDetails`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`GetOrderDetails`(
    IN `input_order_id` INT
)
BEGIN
    DECLARE v_username VARCHAR(255);
    
    -- Get the username for the order
    SELECT `username` INTO v_username FROM `orders` WHERE `order_id` = input_order_id;
    
    -- Return detailed information about the order items
    SELECT 
        oi.`order_item_id`,
        oi.`item_id`,
        i.`name` AS `item_name`,
        i.`description`,
        i.`price` AS `unit_price`,
        oi.`quantity`,
        (oi.`quantity` * oi.`price`) AS `subtotal`
    FROM `order_items` oi
    JOIN `ITEM` i ON oi.`item_id` = i.`id`
    WHERE oi.`order_id` = input_order_id;
END%%
DELIMITER ;

-- This procedure retrieves all pending refund requests, along with basic order info.
DELIMITER %%
DROP PROCEDURE `first`.`GetPendingRefundRequests`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`GetPendingRefundRequests`()
BEGIN
    -- Get all pending refund requests, including order total amount and order status
    SELECT 
        rr.`order_id`,
        o.`total_amount`,
        o.`status` AS `order_status`,
        rr.`request_reason`,
        rr.`username`,
        rr.`created_at` AS `application_date`,
        rr.`refund_id`
    FROM `refund_requests` rr
    INNER JOIN `orders` o ON rr.`order_id` = o.`order_id`
    WHERE rr.`status` = 'Pending'
    ORDER BY rr.`created_at` DESC;
END%%
DELIMITER ;

-- This procedure fetches the current status of a refund request based on order ID.
DELIMITER %%
DROP PROCEDURE `first`.`GetRequestStatus`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`GetRequestStatus`(
    IN `input_order_id` INT
)
BEGIN
    SELECT `status`
    FROM `refund_requests`
    WHERE `order_id`= input_order_id;
END%%
DELIMITER ;

-- This procedure retrieves all items in a given user's cart, including sub-total prices.
DELIMITER %%
DROP PROCEDURE `first`.`GetUserCart`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`GetUserCart`(
    IN `input_username` VARCHAR(255)
)
proc_end: BEGIN
    DECLARE v_cartID INT;

    -- Get the user's cartID
    SELECT `cartID` INTO v_cartID FROM `cart` WHERE `username` = input_username;

    -- Get the items in the cart
    SELECT 
        ci.`itemID`,
        i.`name`,
        i.`price`,
        i.`description`,
        i.`img_src`,
        ci.`quantity`,
        (ci.`quantity` * i.`price`) AS `subtotal`
    FROM `cart_items` ci
    JOIN `ITEM` i ON ci.`itemID` = i.`id`
    WHERE ci.`cartID` = v_cartID;

END proc_end%%
DELIMITER ;

-- This procedure gets all orders of a given user, ordered by date.
DELIMITER %%
DROP PROCEDURE `first`.`GetUserOrders`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`GetUserOrders`(
    IN `input_username` VARCHAR(255)
)
BEGIN
    -- Get all orders for the user
    SELECT 
        `order_id`,
        `order_date`,
        `total_amount`,
        `status`
    FROM `orders`
    WHERE `username` = input_username
    ORDER BY `order_date` DESC;
END%%
DELIMITER ;

-- This procedure updates the status of a refund request and sets the admin_reason message.
DELIMITER %%
DROP PROCEDURE `first`.`ProcessRefundRequest`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`ProcessRefundRequest`(
    IN `input_refund_id` INT,
    IN `input_status` ENUM('Approved', 'Rejected'),
    IN `input_admin_reason` TEXT
)
BEGIN
    DECLARE v_current_status ENUM('Pending', 'Approved', 'Rejected');

    -- Get the current status
    SELECT `status` INTO v_current_status FROM `refund_requests` WHERE `refund_id` = input_refund_id;

    -- Update the refund request status and admin reason
    UPDATE `refund_requests`
    SET `status` = input_status,
        `admin_reason` = input_admin_reason
    WHERE `refund_id` = input_refund_id;

    -- Return success message
    SELECT 'Refund request processed successfully' AS Message;
END%%
DELIMITER ;

-- This procedure registers a new user, ensuring the username is unique, then inserts a row into the 'user' table.
DELIMITER %%
DROP PROCEDURE `first`.`RegisterUser`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`RegisterUser`(
    IN `input_username` VARCHAR(255),
    IN `input_password` VARCHAR(255)
)
BEGIN
    -- Check if the username already exists
    IF EXISTS (SELECT 1 FROM `user` WHERE `username` = input_username) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The username already exists';
    END IF;

    -- Insert the new user
    INSERT INTO `user` (`username`, `password`)
    VALUES (input_username, input_password);

    -- Return success message
    SELECT 'User registered successfully' AS Message;
END%%
DELIMITER ;

-- This procedure submits a new refund request for a given order, storing the user's reason.
DELIMITER %%
DROP PROCEDURE `first`.`SubmitRefundRequest`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`SubmitRefundRequest`(
    IN `input_order_id` INT,
    IN `input_username` VARCHAR(255),
    IN `input_reason` TEXT
)
BEGIN
    -- Insert the refund request
    INSERT INTO `refund_requests` (`order_id`, `username`, `request_reason`)
    VALUES (input_order_id, input_username, input_reason);

    -- Return success message and refund ID
    SELECT 'Refund request submitted successfully' AS Message, LAST_INSERT_ID() AS RefundID;
END%%
DELIMITER ;

-- This procedure updates the status of an existing order (e.g., from Pending to Shipped).
DELIMITER %%
DROP PROCEDURE `first`.`UpdateOrderStatus`%%
CREATE DEFINER=`CaoBoyu`@`%` PROCEDURE `first`.`UpdateOrderStatus`(
    IN `input_order_id` INT,
    IN `new_status` ENUM('Pending', 'Confirmed', 'Shipped', 'Delivered', 'Canceled','Refund')
)
BEGIN
    -- Update the order status
    UPDATE `orders`
    SET `status` = new_status
    WHERE `order_id` = input_order_id;
    
    SELECT 'Order status updated successfully' AS Message;
END%%
DELIMITER ;