import flet as ft
from DefaultColors import *
from DataModel import *
from Menu import *
import Userstate as us


# Product page
class Product(ft.View):
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

        shop_title = ft.Text("Shop", size=32, weight="bold", color="white")
        shop_subtitle = ft.Text("Select items from the list below", color="white")

        self.product_gridView = ft.GridView(
            expand=1,
            runs_count=3,
            spacing=10,
            run_spacing=10,
            max_extent=400,
        )

        self.populate_products()

        # self.bottom_appbar = ft.AppBar(title="Simple X Shop", bgcolor=BG, color="white")
        self.main_content = ft.Container(
            content=ft.Column(
                controls=[shop_title, shop_subtitle, self.product_gridView],
                # spacing=20,
                # height=550,
            ),
            bgcolor=BG,
            animate_offset=500,
            offset=ft.transform.Offset(0, 0),
            padding=20,
        )

        self.menu = Menu(self.page)

        self.controls = [
            ft.Stack(
                controls=[self.menu, self.main_content],
                height=self.page.height - 60,
            )
        ]

    def open_settings(self, e):
        if self.main_content.offset.x == 0:
            self.main_content.offset = ft.transform.Offset(0.25, 0)
        else:
            self.main_content.offset = ft.transform.Offset(0, 0)
        self.page.update()

    def open_cart(self, e):
        # If the user has not logged in yet
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

    def populate_products(self):
        products = Model.get_products()
        if products == -1:
            self.page.snack_bar = ft.SnackBar(ft.Text("Failed to get products!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        for row in products:
            card = self.create_product_card(row)
            self.product_gridView.controls.append(card)

    def create_product_card(self, row):
        productId = str(row["id"])
        img = ft.Image(
            src=row["img_src"],
            fit=ft.ImageFit.CONTAIN,
            # width=220,
            height=200,
            border_radius=8,
        )
        img_row = ft.Row(
            controls=[img],
            alignment="center",
        )
        name = ft.Text(
            row["name"],
            size=18,
            weight="bold",
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
            color="white",
        )
        description = ft.Text(
            row["description"],
            size=11,
            max_lines=5,
            overflow=ft.TextOverflow.ELLIPSIS,
            color=ft.Colors.WHITE54,
        )
        bottom_row = ft.Row(
            controls=[
                ft.Text(str(row["price"]), size=14, weight="bold", color="white"),
                ft.IconButton(
                    icon=ft.icons.ADD_SHOPPING_CART_OUTLINED,
                    icon_size=18,
                    icon_color="white",
                    bgcolor=BG,
                    on_click=lambda _: self.add_to_cart(productId),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                ),
            ],
            spacing=10,
        )
        card = ft.Container(
            bgcolor=BG,
            border=ft.border.all(2, "white"),
            border_radius=8,
            padding=10,
            ink=True,
            # alignment="center",
            # width=300,
            # height=400,
            content=ft.Column(
                controls=[img_row, name, description, bottom_row],
                spacing=10,
            ),
            margin=10,
        )
        return card

    def add_to_cart(self, product_id: str):
        # If the user is not logged in
        if not us.isLogin:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please login first!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        Model.add_item_to_cart(us.userName, product_id, 1)
        # Update the cart information on the page
        self.menu.populate_cart_items()
        self.page.snack_bar = ft.SnackBar(ft.Text("Item added to cart!"))
        self.page.snack_bar.open = True
        self.page.update()
