import pymysql
from pymysql.cursors import DictCursor


class Model:
    # Database connection configuration
    db_config = {
        "host": "*****",
        "user": "*****",
        "password": "*****",        # r. 抹去数据库信息
        "database": "*****",
        "charset": "*****",
        "cursorclass": DictCursor,
    }

    # g. create database link
    @staticmethod
    def get_db_connection():
        """
        Create and return a new database connection.
        """
        try:
            connection = pymysql.connect(**Model.db_config)
            return connection
        except pymysql.MySQLError as e:
            print(f"Error connecting to the database: {e}")
            return None

    # g. user registration
    @staticmethod
    def register_user(username: str, password: str):
        """
        Call the stored procedure RegisterUser to register a new user.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return 1, "Error"

        try:
            with connection.cursor() as cursor:

                # Call the stored procedure
                cursor.callproc("RegisterUser", [username, password])
                connection.commit()

                # Get the result of the stored procedure
                result = cursor.fetchone()
                if result:
                    print(result["Message"])
                    return 0, result["Message"]
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                # Error 1644 corresponds to a custom error thrown by SIGNAL
                print(f"Registration failed: {e.args[1]}")
                return 1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
                return 1, "Error"
        finally:
            connection.close()

    # g. check login
    @staticmethod
    def check_user_login(username: str, password: str):
        """
        Call the stored procedure CheckUserLogin to check user login information.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc("CheckUserLogin", [username, password])
                connection.commit()

                # Get the result of the stored procedure
                result = cursor.fetchone()
                if result:
                    print(
                        f"Login successful: Username={result['username']}, Is Admin={result['is_admin']}, Is Frozen={result['is_frozen']}"
                    )
                    return 0, result["is_admin"], result["is_frozen"], result["img_src"]
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                # Error 1644 corresponds to a custom error thrown by SIGNAL
                print(f"Login failed: {e.args[1]}")
                return 1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
                return -1, "Error"
        finally:
            connection.close()

    # g. get cart data
    @staticmethod
    def get_user_cart(username: str):
        """
        Call the stored procedure GetUserCart to get the user's cart data.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc("GetUserCart", [username])
                connection.commit()

                # Get the result set of the stored procedure
                result = cursor.fetchall()

                return 0, result
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                print(f"Failed to get cart: {e.args[1]}")
                return 1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
                return -1, "Error"
        finally:
            connection.close()

    # g. add item to cart
    @staticmethod
    def add_item_to_cart(username: str, item_id: int, quantity: int):
        """
        Call the stored procedure AddItemToCart to add an item to the user's cart.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc("AddItemToCart", [username, item_id, quantity])
                connection.commit()
                print(
                    f"Added item ID {item_id} with quantity {quantity} to user '{username}' cart."
                )
                return 0, "Success"
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                print(f"Failed to add item: {e.args[1]}")
                return 1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
                return -1, "Error"
        finally:
            connection.close()

    # g. remove item from cart
    @staticmethod
    def decrease_item_quantity(username: str, item_id: int, quantity: int):
        """
        Call the stored procedure DecreaseItemQuantity to decrease the quantity of a specific item in the user's cart.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc("DecreaseItemQuantity", [username, item_id, quantity])
                connection.commit()
                print(
                    f"Decreased quantity of item ID {item_id} by {quantity} for user '{username}'."
                )
                return 0, "Success"
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                print(f"Failed to decrease item quantity: {e.args[1]}")
                return 1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
                return -1, "Error"
        finally:
            connection.close()

    # g. get product data
    @staticmethod
    def get_products():
        """
        Get all product data from the MySQL database and return a dictionary.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1

        try:
            with connection.cursor() as cursor:
                query = "SELECT id, name, price, description, img_src FROM ITEM"
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except pymysql.MySQLError as e:
            print(f"Error fetching products: {e}")
            return -1
        finally:
            connection.close()

    # g. create order
    @staticmethod
    def create_order(username: str):
        """
        Call the stored procedure CreateOrder to create a new order.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc("CreateOrder", [username])
                connection.commit()

                # Get the result of the stored procedure
                result = cursor.fetchone()
                if result:
                    print(result["Message"])
                    print(f"New order ID: {result['OrderID']}")
                    return 0, f"New order! ID: {result['OrderID']}"
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                print(f"Failed to create order: {e.args[1]}")
                return -1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
                return -1, "Error"
        finally:
            connection.close()

    # g. get user orders
    @staticmethod
    def get_user_orders(username: str):
        """
        Call the stored procedure GetUserOrders to get all orders of the user.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc("GetUserOrders", [username])
                connection.commit()

                # Get the result set of the stored procedure
                orders = cursor.fetchall()
                if orders:
                    return 0, orders
                else:
                    return 1, "No orders found."
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                print(f"Failed to get orders: {e.args[1]}")
                return -1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
                return -1, "Error"
        finally:
            connection.close()

    # g. get order details
    @staticmethod
    def get_order_details(order_id: int):
        """
        Call the stored procedure GetOrderDetails to get the details of a specific order.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc("GetOrderDetails", [order_id])
                connection.commit()
                order_items = cursor.fetchall()
                if order_items:
                    return 0, order_items
                else:
                    print("No items found in the order.")
                    return -1, "No items found."
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                print(f"Failed to get order details: {e.args[1]}")
                return -1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
                return -1, "Error"
        finally:
            connection.close()

    # g. get all pending refund requests
    @staticmethod
    def get_pending_refund_requests():
        """
        Call the stored procedure GetPendingRefundRequests to get all pending refund requests.
        Return a list of refund requests or -1 to indicate failure.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"
        try:
            with connection.cursor() as cursor:
                cursor.callproc("GetPendingRefundRequests")
                refunds = cursor.fetchall()
                return 0, refunds
        except pymysql.MySQLError as e:
            print(f"Error calling stored procedure: {e}")
            return -1, "Error"
        finally:
            connection.close()

    # g. update order status
    @staticmethod
    def update_order_status(order_id: int, new_status: str):
        """
        Call the stored procedure UpdateOrderStatus to update the status of an order.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        # Define allowed status values
        allowed_statuses = [
            "Pending",
            "Confirmed",
            "Shipped",
            "Delivered",
            "Canceled",
            "Refund",
        ]
        if new_status not in allowed_statuses:
            print(f"Invalid status value. Allowed values: {allowed_statuses}")
            return -1, "Invalid status value."

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc("UpdateOrderStatus", [order_id, new_status])
                connection.commit()

                # Get the result of the stored procedure
                result = cursor.fetchone()
                if result:
                    print(result["Message"])
                    return 0, result["Message"]
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                print(f"Failed to update order status: {e.args[1]}")
                return -1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
                return -1, "Error"
        finally:
            connection.close()

    # g. submit refund request
    def submit_refund_request(order_id: int, username: str, reason: str):
        """
        Call the stored procedure SubmitRefundRequest to submit a refund request.
        Return the refund ID or -1 to indicate failure.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                cursor.callproc("SubmitRefundRequest", [order_id, username, reason])
                connection.commit()
                result = cursor.fetchone()
                if result:
                    print(result["Message"])
                    print(f"Refund request ID: {result['RefundID']}")
                    return 0, f"Refund request ID: {result['RefundID']}"
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                # Error 1644 corresponds to a custom error thrown by SIGNAL
                print(f"Failed to submit refund request: {e.args[1]}")
                return -1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
            return -1, "Error"
        finally:
            connection.close()

    # g. process refund request
    @staticmethod
    def process_refund_request(refund_id: int, status: str, admin_reason: str):
        """
        Call the stored procedure ProcessRefundRequest to process a refund request.
        Return True to indicate success, False to indicate failure.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                cursor.callproc(
                    "ProcessRefundRequest", [refund_id, status, admin_reason]
                )
                connection.commit()
                result = cursor.fetchone()
                if result:
                    print(result["Message"])
                    return 1, result["Message"]
        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                # Error 1644 corresponds to a custom error thrown by SIGNAL
                print(f"Failed to process refund request: {e.args[1]}")
                return 1, e.args[1]
            else:
                print(f"Error calling stored procedure: {e}")
                return -1, "Error"
        finally:
            connection.close()

    # g. get reason for request
    @staticmethod
    def get_admin_reason_for_refund(order_id: int):
        """
        Call the stored procedure GetAdminReasonForRefund to get the admin reason for processing the order.
        Return the admin reason or -1 to indicate failure.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                cursor.callproc("GetAdminReasonForRefund", [order_id])
                # Get the result set
                result = cursor.fetchone()
                if result:
                    return 0, result["admin_reason"]
                else:
                    return -1, "Error"
        except pymysql.MySQLError as e:
            if e.args[0] == 45000:
                # Custom error
                return -1, e.args[1]
            else:
                return -1, "Error"
        finally:
            connection.close()

    # g. get refund status
    @staticmethod
    def get_refund_status(refund_id: int):
        """
        Call the stored procedure GetRefundStatus to get the status of a refund request.
        Return the status value or -1 to indicate failure.
        """
        connection = Model.get_db_connection()
        if connection is None:
            return -1, "Error"

        try:
            with connection.cursor() as cursor:
                cursor.callproc("GetRequestStatus", [refund_id])
                result = cursor.fetchone()
                if result:
                    return 0, result["status"]
                else:
                    return 0, "NULL"
        except pymysql.MySQLError as e:
            if e.args[0] == 45000:
                return -1, e.args[1]
            else:
                return -1, "Error"
        finally:
            connection.close()
