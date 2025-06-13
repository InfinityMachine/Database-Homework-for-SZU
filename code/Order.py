import flet as ft
from DefaultColors import *
from DataModel import *
from Menu import *
import Userstate as us


# Orders page
class Order(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(bgcolor=BG)
        self.page = page
        self.init_ui()

    def init_ui(self):
        self.appbar = ft.AppBar(
            title=ft.Text("Simple X Shop", size=20, weight="bold", color="white"),
            bgcolor=BG,
            color="white",
            leading=ft.IconButton(
                icon=ft.icons.MENU, icon_size=18, on_click=self.open_settings
            ),
            actions=[
                ft.IconButton(
                    icon=ft.icons.SHOPPING_CART_OUTLINED,
                    icon_size=18,
                    on_click=self.open_cart,
                )
            ],
        )

        orders_title = ft.Text("Your Orders", size=32, weight="bold", color="white")
        orders_subtitle = ft.Text("Manage your orders below", color="white")

        self.order_List = ft.ExpansionPanelList(
            expand=True,
            spacing=10,
            expand_icon_color="white",
            divider_color=BG,
        )

        self.main_content = ft.Container(
            content=ft.Column(
                controls=[orders_title, orders_subtitle, self.order_List],
                spacing=20,
                scroll="auto",
            ),
            height=self.page.height - 60,
            bgcolor=BG,
            animate_offset=500,
            offset=ft.transform.Offset(0, 0),
            padding=20,
        )

        self.populate_orders()

        self.menu = Menu(self.page)

        self.controls = [
            ft.Stack(
                controls=[self.menu, self.main_content],
                height=self.page.height - 60,
            )
        ]
        self.refund_TextField = ft.TextField(
            label="Enter reason",
            multiline=True,
            bgcolor="transparent",
            border_color="white",
            color="white",
            expand=True,
        )
        self.dia = ft.AlertDialog(
            title=ft.Text("Please enter the reason for refund"),
            bgcolor=BG,
            content=self.refund_TextField,
            actions=[
                ft.ElevatedButton(
                    "Submit",
                    on_click=self.submit_refund,
                    icon=ft.icons.CHECK,
                    bgcolor=BG,
                    color="white",
                ),
                ft.ElevatedButton(
                    "Cancel",
                    on_click=self.cancel_refund,
                    icon=ft.icons.CLOSE,
                    bgcolor=BG,
                    color="white",
                ),
            ],
            actions_alignment="end",
            shape=ft.RoundedRectangleBorder(8),
        )

    def open_settings(self, e):
        if self.main_content.offset.x == 0:
            self.main_content.offset = ft.transform.Offset(0.25, 0)
        else:
            self.main_content.offset = ft.transform.Offset(0, 0)
        self.page.update()

    def open_cart(self, e):
        # If the user is not logged in
        if not us.isLogin:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please login first!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        if self.main_content.offset.x == 0:
            self.main_content.offset = ft.transform.Offset(-0.25, 0)
        else:
            self.main_content.offset = ft.transform.Offset(0, 0)
        self.page.update()

    def populate_orders(self):
        flag, data = Model.get_user_orders(us.userName)
        if flag == -1:
            self.page.snack_bar = ft.SnackBar(ft.Text(data))
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.order_List.controls.clear()

        if flag == 1:
            no_order_text = ft.Container(
                bgcolor=BG,
                content=ft.Text("You have no orders yet...", size=18, color="white"),
                border=ft.border.all(2, "white"),
                border_radius=8,
                padding=10,
                ink=True,
            )
            self.main_content.content.controls.insert(2, no_order_text)
            self.page.update()
            return
        else:
            for order in data:
                card = self.create_order_card(order)
                self.order_List.controls.append(card)
        self.page.update()

    def create_order_card(self, order):
        order_id = str(order["order_id"])
        order_date = order["order_date"].strftime("%Y-%m-%d %H:%M:%S")
        total_amount = f"${order['total_amount']:.2f}"
        status = order["status"]

        order_info = ft.Row(
            controls=[
                ft.Text(
                    f"Order ID: {order_id}",
                    size=18,
                    weight="bold",
                    color="white",
                    expand=2,
                ),
                ft.Text(f"Date: {order_date}", size=16, color="white", expand=2),
                ft.Text(f"Total: {total_amount}", size=16, color="white", expand=2),
                ft.Text(f"Status: {status}", size=16, color="white", expand=2),
                # view_details_button,
            ],
            # spacing=20,
        )

        exp = ft.ExpansionPanel(
            header=order_info,
            content=ft.ListView(
                # padding=20,
                spacing=10,
            ),
            bgcolor=BG,
            # spacing=10,
        )

        flag, order_details = Model.get_order_details(order_id)
        if flag == -1:
            self.page.snack_bar = ft.SnackBar(ft.Text("Failed to get order details!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        else:
            for row in order_details:
                item_id = row["item_id"]
                item_name = row["item_name"]
                unit_price = f"${row['unit_price']:.2f}"
                quantity = row["quantity"]
                subtotal = f"${row['subtotal']:.2f}"
                item_row = ft.Row(
                    controls=[
                        ft.Text(
                            item_name,
                            size=16,
                            weight="bold",
                            color="white",
                            expand=2,
                        ),
                        ft.Text(
                            "unit price: " + unit_price,
                            size=14,
                            color="white",
                            expand=2,
                        ),
                        ft.Text(
                            "quantity: " + str(quantity),
                            size=14,
                            color="white",
                            expand=2,
                        ),
                        ft.Text(
                            "subtotal: " + subtotal,
                            size=14,
                            color="white",
                            expand=2,
                        ),
                        ft.Row(
                            width=46,
                        ),
                    ],
                    # spacing=20,
                )
                exp.content.controls.append(item_row)
        if status == "Refund":
            exp.content.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(
                            "Refund Requested", size=18, color="white12", weight="bold"
                        ),
                    ],
                    alignment="center",
                )
            )
        elif status == "Canceled":
            exp.content.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(
                            "Order Canceled", size=18, color="white12", weight="bold"
                        ),
                    ],
                    alignment="center",
                )
            )
        else:
            exp.content.controls.append(
                ft.FilledButton(
                    text="Request Refund",
                    bgcolor=BG,
                    color="white",
                    on_click=lambda e: self.request_refund(order_id),
                    icon=ft.icons.REMOVE_SHOPPING_CART_OUTLINED,
                )
            )
        flag, requestStatus = Model.get_refund_status(order_id)
        if flag == -1:
            self.page.snack_bar = ft.SnackBar(ft.Text(requestStatus))
            self.page.snack_bar.open = True
            self.page.update()
            return
        if requestStatus == "Approved" or requestStatus == "Rejected":
            # Button to display the admin's reason
            flag, data = Model.get_admin_reason_for_refund(order_id)
            if flag == -1:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text("Failed to get admin reason!")
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
            else:
                dia = ft.AlertDialog(
                    title=ft.Text("Admin Reason"),
                    bgcolor=BG,
                    content=ft.Text("Reason: " + data),
                    actions=[
                        ft.ElevatedButton(
                            "OK",
                            on_click=lambda e: self.page.close(dia),
                            icon=ft.icons.CHECK,
                            bgcolor=BG,
                            color="white",
                        ),
                    ],
                    actions_alignment="end",
                    shape=ft.RoundedRectangleBorder(8),
                )
                exp.content.controls.append(
                    ft.FilledButton(
                        text="View Admin Reason",
                        bgcolor=BG,
                        color="white",
                        on_click=lambda e: self.page.open(dia),
                        icon=ft.icons.INFO,
                    )
                )
        exp.content.controls.append(
            ft.Row(height=10),
        )
        return exp

    def request_refund(self, order_id):
        # Pop up a dialog for the user to fill in the refund reason
        self.processing_order_id = order_id
        self.processing_user_name = us.userName
        self.page.open(self.dia)
        self.page.update()
        return

    def submit_refund(self, e):
        reason = self.refund_TextField.value
        if not reason:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please provide a reason!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        # Submit refund request
        flag, message = Model.submit_refund_request(
            self.processing_order_id, self.processing_user_name, reason
        )
        if flag == -1:
            self.page.snack_bar = ft.SnackBar(ft.Text(message))
            self.page.snack_bar.open = True
            self.page.update()
            return
        # Update order status
        flag, message = Model.update_order_status(self.processing_order_id, "Refund")
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True

        self.populate_orders()
        self.page.close(self.dia)
        self.page.update()
        return

    def cancel_refund(self, e):
        self.page.close(self.dia)
        self.page.update()
        return
