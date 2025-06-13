import flet as ft
from DefaultColors import *
from DataModel import *
from Menu import *
import Userstate as us


# Admin refund management page
class Admin(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(bgcolor=BG)
        self.page = page
        self.init_ui()

    def init_ui(self):
        # Check if user is admin
        if not us.isAdmin:
            self.controls = [
                ft.Text("Do not have permission", size=20, color="white"),
            ]
            return

        # AppBar settings
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

        # Page title and subtitle
        title = ft.Text(
            "Manage user refund requests", size=32, weight="bold", color="white"
        )
        subtitle = ft.Text(
            "Review and process refund requests submitted by users", color="white"
        )

        # Refund request list
        self.refund_list = ft.ExpansionPanelList(
            expand=True,
            spacing=10,
            expand_icon_color="white",
            divider_color=BG,
        )

        # Main content container
        self.main_content = ft.Container(
            content=ft.Column(
                controls=[title, subtitle, self.refund_list],
                spacing=20,
                scroll="auto",
            ),
            height=self.page.height - 60,
            bgcolor=BG,
            animate_offset=500,
            offset=ft.transform.Offset(0, 0),
            padding=20,
        )

        self.populate_refunds()

        # Menu
        self.menu = Menu(self.page)

        # Assemble page controls
        self.controls = [
            ft.Stack(
                controls=[self.menu, self.main_content],
                height=self.page.height - 60,
            )
        ]
        self.reason_TextField = ft.TextField(
            label="Enter reason",
            multiline=True,
            bgcolor="transparent",
            border_color="white",
            color="white",
            expand=True,
        )
        self.dia = ft.AlertDialog(
            title=ft.Text("Please enter the reason for the processing"),
            bgcolor=BG,
            content=self.reason_TextField,
            actions=[
                ft.ElevatedButton(
                    "Submit",
                    on_click=self.submit_reason,
                    icon=ft.icons.CHECK,
                    bgcolor=BG,
                    color="white",
                ),
                ft.ElevatedButton(
                    "Cancel",
                    on_click=self.cancel_reason,
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

    def populate_refunds(self):
        # Get all refund requests
        flag, data = Model.get_pending_refund_requests()
        if flag == -1:
            self.page.snack_bar = ft.SnackBar(ft.Text(data))
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.refund_list.controls.clear()

        if not data:
            no_refund_text = ft.Container(
                bgcolor=BG,
                content=ft.Text(
                    "There are no refund requests at this time...",
                    size=18,
                    color="white",
                ),
                border=ft.border.all(2, "white"),
                border_radius=8,
                padding=10,
                ink=True,
            )
            self.main_content.content.controls.insert(2, no_refund_text)
            self.page.update()
            return
        else:
            for refund in data:
                panel = self.create_refund_panel(refund)
                self.refund_list.controls.append(panel)
        self.page.update()

    def create_refund_panel(self, refund):
        order_id = str(refund["order_id"])
        total_amount = refund["total_amount"]
        order_status = refund["order_status"]
        request_reason = refund["request_reason"]
        username = refund["username"]
        created_at = refund["application_date"].strftime("%Y-%m-%d %H:%M:%S")
        refund_id = str(refund["refund_id"])
        # Refund request header info
        header = ft.Row(
            controls=[
                ft.Text(
                    f"Order ID: {order_id}",
                    size=18,
                    weight="bold",
                    color="white",
                    expand=2,
                ),
                ft.Text(f"Name: {username}", size=16, color="white", expand=2),
                ft.Text(f"Date: {created_at}", size=16, color="white", expand=4),
                ft.Text(
                    f"Total: ${total_amount:.2f}",
                    size=16,
                    color="white",
                    expand=2,
                ),
                ft.Text(f"Status: {order_status}", size=16, color="white", expand=2),
            ],
        )

        # Refund request details
        content = ft.Column(
            controls=[
                ft.Text(
                    f"Reason for Refund: ",
                    size=16,
                    color="white",
                    weight="bold",
                ),
                ft.Text(
                    request_reason,
                    size=16,
                    color="white",
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Approve",
                            on_click=lambda e: self.process_refund(
                                refund_id, "Approved"
                            ),
                            bgcolor=BG,
                            color="white",
                            icon=ft.icons.CHECK,
                        ),
                        ft.ElevatedButton(
                            "Reject",
                            on_click=lambda e: self.process_refund(
                                refund_id, "Rejected"
                            ),
                            bgcolor=BG,
                            color="white",
                            icon=ft.icons.CLOSE,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Row(height=10),
            ],
            spacing=10,
        )

        # Create ExpansionPanel
        panel = ft.ExpansionPanel(
            header=header,
            content=content,
            # is_expanded=False,
            bgcolor=BG,
        )
        return panel

    def process_refund(self, refund_id: str, status: str):
        # Pop up a dialog for the admin to fill in the reason for processing
        self.processing_refund_id = refund_id
        self.processing_status = status
        self.page.open(self.dia)
        self.page.update()

    def submit_reason(self, e):
        admin_reason = self.reason_TextField.value
        if not admin_reason:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please provide a reason!"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Call Model method to process refund request
        flag, massage = Model.process_refund_request(
            self.processing_refund_id, self.processing_status, admin_reason
        )
        self.page.snack_bar = ft.SnackBar(ft.Text(massage))
        self.page.snack_bar.open = True
        self.populate_refunds()
        self.page.close(self.dia)
        self.page.update()
        return

    def cancel_reason(self, e):
        self.page.close(self.dia)
        self.page.update()
