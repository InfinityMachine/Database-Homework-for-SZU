import flet as ft
from DataModel import *
from DefaultColors import *
import Userstate as us


# Settings panel (slide out from the left side),panel_container is a member of the products page
class Menu(ft.ResponsiveRow):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.init_ui()

    def init_ui(self):
        # head, including a button to return to the previous level and a title
        self.head = ft.Row(
            alignment="SPACE_BETWEEN",
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_size=18,
                    on_click=lambda _: self.goBack(),
                ),
                ft.Text("Menu", size=20, weight="bold", color="white"),
            ],
        )
        self.userInfo = ft.Row()
        self.account_column = ft.Column()

        if not us.isLogin:
            # User avatar and ID
            self.userInfo.controls.append(
                ft.Row(
                    controls=[
                        ft.CircleAvatar(
                            opacity=0.8,
                            foreground_image_src="",
                            bgcolor=FG,
                            # content=ft.Text("Hi", color="white", weight="bold"),
                        ),
                        ft.Text(
                            "Please Login",
                            size=18,
                            color="white",
                            weight="bold",
                            max_lines=1,
                            overflow="ellipsis",
                        ),
                    ]
                )
            )
            # User login
            self.usernameField = ft.TextField(
                label="Username",
                multiline=False,
                bgcolor="transparent",
                border_color="white",
                color="white",
                max_lines=1,
            )
            self.passWordField = ft.TextField(
                label="Password",
                multiline=False,
                bgcolor="transparent",
                border_color="white",
                password=True,
                can_reveal_password=True,
                color="white",
                max_lines=1,
            )
            self.account_column.controls.append(
                ft.Column(
                    controls=[
                        # login label
                        ft.Text(
                            "Login",
                            size=14,
                            color="white",
                            overflow="ellipsis",
                            weight="bold",
                        ),
                        # username field
                        self.usernameField,
                        # password field
                        self.passWordField,
                        # login and register buttons
                        ft.Row(
                            controls=[
                                ft.FilledButton(
                                    text="Login",
                                    bgcolor=FG,
                                    color="white",
                                    on_click=self.on_login_click,
                                    icon=ft.icons.LOGIN,
                                ),
                                ft.FilledButton(
                                    text="Register",
                                    bgcolor=FG,
                                    color="white",
                                    on_click=self.on_register_click,
                                    icon=ft.icons.APP_REGISTRATION_OUTLINED,
                                ),
                            ],
                            spacing=10,
                        ),
                    ]
                )
            )
        self.animate_offset = True
        self.rightColumn = ft.Column(
            col=3,
            controls=[
                self.head,
                self.userInfo,
                self.account_column,
            ],
            animate_offset=True,
            # scroll="auto",
            # expand=True,
        )
        # cartHead, a title
        self.cartHead = ft.Row(
            # alignment="SPACE_BETWEEN",
            controls=[
                ft.Text("Cart", size=20, weight="bold", color="white"),
            ],
        )
        # subtitle
        self.cartSubtitle = ft.Text("Your cart items", color="white")
        # cart items
        self.cartItemsContainer = ft.Column(
            spacing=10, scroll="auto", height=self.page.height - 200
        )

        # submit cart button
        buyButton = ft.IconButton(
            icon=ft.icons.SHOPPING_CART_CHECKOUT_OUTLINED,
            icon_size=18,
            on_click=lambda _: self.buyCart(),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                # bgcolor=FG,
            ),
            icon_color="white",
        )

        # go to order page
        goToOrderButton = ft.IconButton(
            icon=ft.icons.LOCAL_PRINT_SHOP_OUTLINED,
            icon_size=18,
            on_click=lambda _: self.page.go("/order"),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                # bgcolor=FG,
            ),
            icon_color="white",
        )
        self.bottomRow = ft.Row(
            controls=[
                buyButton,
                goToOrderButton,
            ],
        )
        # cart
        self.leftColumn = ft.Column(
            col=3,
            controls=[
                self.cartHead,
                self.cartSubtitle,
                self.cartItemsContainer,
                self.bottomRow,
            ],
            animate_offset=True,
            # scroll="auto",
            # expand=True,
        )
        # self.height = self.page.height - 60
        self.controls = [
            self.rightColumn,
            ft.Column(col=6),
            self.leftColumn,
        ]
        self.animate_offset = True
        self.login_success(us.isAdmin, us.img_src)

    def login_success(self, isAdmin, img_src):
        if not us.isLogin:
            return
        # Update user avatar and ID
        self.account_column.controls.clear()
        self.userInfo.controls.clear()
        self.userInfo.controls.append(
            ft.Row(
                controls=[
                    ft.CircleAvatar(
                        opacity=0.8,
                        foreground_image_src=img_src,
                        bgcolor=FG,
                        # content=ft.Text("Hi", color="white", weight="bold"),
                    ),
                    ft.Text(
                        "Hello! " + us.userName,
                        size=18,
                        color="white",
                        weight="bold",
                        max_lines=1,
                        overflow="ellipsis",
                    ),
                ]
            )
        )
        self.account_column.controls.append(
            ft.FilledButton(
                text="Order",
                bgcolor=BG,
                color="white",
                on_click=lambda _: self.page.go("/order"),
                icon=ft.icons.LOCAL_PRINT_SHOP_OUTLINED,
            )
        )
        self.account_column.controls.append(
            ft.FilledButton(
                text="Logout",
                bgcolor=BG,
                color="white",
                on_click=self.logout,
                icon=ft.icons.LOGOUT,
            )
        )
        self.account_column.controls.append(
            ft.FilledButton(
                text="Help",
                bgcolor=BG,
                color="white",
                url="https://www.baidu.com",
                icon=ft.icons.HELP_OUTLINED,
            )
        )
        # If the user is an admin
        if isAdmin:
            self.account_column.controls.insert(
                0,
                ft.Row(
                    controls=[
                        # admin label
                        ft.Text(
                            "Admin",
                            size=16,
                            color="white",
                            overflow="ellipsis",
                            weight="bold",
                        ),
                    ],
                ),
            )
            self.account_column.controls.append(
                # button to go to the admin page
                ft.FilledButton(
                    text="Admin",
                    bgcolor=BG,
                    color="white",
                    on_click=lambda _: self.page.go("/admin"),
                    icon=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                )
            )
        self.populate_cart_items()
        self.page.update()

    # y. todo add user information

    def on_login_click(self, e):
        entered_username = self.usernameField.value
        entered_password = self.passWordField.value
        data = Model.check_user_login(entered_username, entered_password)
        flag = data[0]
        if flag == 1 or flag == -1:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(data[1])))
            self.page.snack_bar.open = True
            self.page.update()
            return
        elif flag == 0:
            isAdmin = data[1]
            isFrozen = data[2]
            img_src = data[3]
            us.img_src = img_src
            us.isLogin = True
            us.userName = entered_username
            us.isAdmin = isAdmin
            us.isFrozen = isFrozen
            self.login_success(isAdmin, img_src)

            self.page.snack_bar = ft.SnackBar(ft.Text("Login successful"))
            self.page.snack_bar.open = True
            self.page.update()
            return

    def on_register_click(self, e):
        entered_username = self.usernameField.value
        entered_password = self.passWordField.value
        data = Model.register_user(entered_username, entered_password)
        flag = data[0]
        if flag == 1:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(data[1])))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.page.snack_bar = ft.SnackBar(ft.Text(str(data[1])))
        self.page.snack_bar.open = True
        self.page.update()

    def populate_cart_items(self):
        self.cartItemsContainer.controls.clear()
        if not us.isLogin:
            return
        data = Model.get_user_cart(us.userName)
        flag = data[0]
        if flag == 1 or flag == -1:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(data[1])))
            self.page.snack_bar.open = True
            self.page.update()
            return
        cartData = data[1]
        total = 0
        # Show total
        for row in cartData:
            card = self.create_cart_card(row)
            self.cartItemsContainer.controls.append(card)
            total += row["subtotal"]
        self.cartItemsContainer.controls.insert(
            0,
            ft.Text(
                f"Total: {total}",
                size=18,
                weight="bold",
                color="white",
            ),
        )
        self.page.update()

    def create_cart_card(self, p: dict):
        name = ft.Text(
            p["name"],
            size=18,
            weight="bold",
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
            color="white",
        )
        price = ft.Text(
            p["price"],
            size=14,
            weight="bold",
            color="white",
        )
        quantity = ft.Text(
            f"{p['quantity']} X",
            size=14,
            weight="bold",
            color="white",
        )
        infoRow = ft.Row(
            controls=[name, price],
        )
        # Increase item button
        addButton = ft.IconButton(
            icon=ft.icons.ADD,
            icon_size=18,
            icon_color="white",
            # bgcolor=FG,
            on_click=lambda e: self.add_to_cart(p["itemID"]),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        )
        # Decrease item button
        minusButton = ft.IconButton(
            icon=ft.icons.REMOVE,
            icon_size=18,
            icon_color="white",
            # bgcolor=FG,
            on_click=lambda e: self.minus_to_cart(p["itemID"]),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        )
        subtotal = ft.Text(
            f"Subtotal: {p['subtotal']}",
            size=14,
            weight="bold",
            color="white",
        )
        buttonRow = ft.Row(
            controls=[minusButton, quantity, addButton, subtotal],
        )
        card = ft.Container(
            bgcolor=BG,
            border=ft.border.all(2, "white"),
            height=100,
            content=ft.Column(
                controls=[infoRow, buttonRow],
                spacing=10,
            ),
            border_radius=8,
            ink=True,
            padding=10,
        )
        return card

    def add_to_cart(self, id):
        Model.add_item_to_cart(us.userName, id, 1)
        self.populate_cart_items()

    def minus_to_cart(self, id):
        Model.decrease_item_quantity(us.userName, id, 1)
        self.populate_cart_items()

    def goBack(self):
        if self.page.route == "/products":
            self.page.go("/")
        elif self.page.route == "/order":
            self.page.go("/products")
        elif self.page.route == "/admin":
            self.page.go("/products")

    def buyCart(self):
        flag, data = Model.create_order(us.userName)
        self.page.snack_bar = ft.SnackBar(ft.Text(str(data)))
        self.page.snack_bar.open = True
        self.populate_cart_items()
        self.page.update()
        return

    def logout(self, e):
        us.isLogin = False
        us.isAdmin = False
        us.isFrozen = False
        us.userName = ""
        us.img_src = ""
        us.password = ""
        self.page.go("/")
        return
