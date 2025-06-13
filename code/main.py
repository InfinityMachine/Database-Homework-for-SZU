import flet as ft
from DefaultColors import *
from Landing import *
from Product import *
from Order import *
from Admin import *
from DataModel import *


def main(page: ft.Page):
    page.title = "Shopping Platform"
    page.window.width = 1200
    page.window.height = 800
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.theme_mode = "DARK"

    def router(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(Landing(page))
        elif page.route == "/products":
            page.views.append(Product(page))
        elif page.route == "/order":
            page.views.append(Order(page))
        elif page.route == "/admin":
            page.views.append(Admin(page))
        else:
            page.go("/")

        page.update()

    page.on_resize = router
    page.on_route_change = router
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
