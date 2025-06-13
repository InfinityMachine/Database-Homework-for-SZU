import flet as ft
from DefaultColors import *


# Landing page (Login/Welcome page)
class Landing(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            horizontal_alignment="center", vertical_alignment="center", bgcolor=BG
        )
        self.page = page

        title = ft.Text("SIMPLE STORE", size=28, weight="bold", color="white")
        subtitle = ft.Text("Made With Flet", size=11, color="white")
        cart_logo = ft.Icon(
            name="shopping_cart_outlined",
            size=64,
            color="white",
        )

        product_page_btn = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD,
            width=54,
            height=54,
            style=ft.ButtonStyle(
                bgcolor=BG,
                shape=ft.RoundedRectangleBorder(radius=8),
                side=ft.BorderSide(2, "white54"),
            ),
            icon_color="white",
            on_click=lambda _: self.page.go("/products"),
        )

        self.controls = [
            cart_logo,
            ft.Divider(height=25, color="transparent"),
            title,
            subtitle,
            ft.Divider(height=10, color="transparent"),
            product_page_btn,
        ]
        dia = ft.AlertDialog(
            title=ft.Text("Warning"),
            bgcolor=BG,
            content=ft.Text(
                "Note: Because the project's database is deployed on Microsoft Azure cloud servers, the application may need a longer loading time in some cases (especially when opening the order page), possibly up to 10 seconds. If the application doesn't respond immediately, please be patient and wait a few seconds..\n\n注意: 由于本项目的数据库部署在微软 Azure 云端服务器上，因此，在某些情况下(尤其是当用户打开订单页面时)，应用程序将需要较长的时间加载(至多可能 10 秒钟)。\n因此，当您点击某个按钮时，如果应用程序没有立刻响应，请耐心等待几秒钟。"
            ),
            actions=[
                ft.ElevatedButton(
                    "understood",
                    on_click=lambda _: self.page.close(dia),
                    icon=ft.icons.CHECK,
                    bgcolor=BG,
                    color="white",
                ),
            ],
            actions_alignment="end",
            shape=ft.RoundedRectangleBorder(radius=8),
        )
        self.page.open(dia)
