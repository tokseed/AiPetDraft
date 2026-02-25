import flet as ft
from flet import Colors


def main(page: ft.Page):
    page.title = "PlacePet"

    # Настройки окна
    page.window.width = 300
    page.window.height = 400
    page.window.resizable = False
    page.window.frameless = True
    page.window.title_bar_hidden = True

    # Прозрачность
    page.bgcolor = "#00000000"
    page.window.bgcolor = "#00000000"

    # Перетаскивание окна
    def on_pan_update(e: ft.DragUpdateEvent):
        page.window.left = (page.window.left or 0) + e.global_delta.x
        page.window.top = (page.window.top or 0) +  e.global_delta.y
        page.update()

    # Контент
    content_text = ft.Text("Главная\nВыберите питомца", size=16, color=Colors.WHITE, text_align=ft.TextAlign.CENTER)

    # Используем простую кнопку
    button = ft.FilledButton("Floating Button")

    # Функция смены контента
    def change_content(index):
        page.drawer.open = False
        texts = [
            "Главная\nВыберите питомца",
            "Питомцы\nСписок ваших питомцев",
            "Магазин\nКупите новые скины",
            "Настройки\nНастройте поведение",
            "О программе\nPlacePet v1.0"
        ]
        if index < len(texts):
            content_text.value = texts[index]
        elif index == 5:
            page.window.close()
        page.update()

    # Меню (без иконок)
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Text("PlacePet", size=20, weight=ft.FontWeight.BOLD, color=Colors.WHITE),
                padding=20,
                bgcolor=Colors.BLUE_400,
            ),
            ft.Container(height=10),
            ft.TextButton("Главная", on_click=lambda _: change_content(0)),
            ft.TextButton("Питомцы", on_click=lambda _: change_content(1)),
            ft.TextButton("Магазин", on_click=lambda _: change_content(2)),
            ft.Divider(),
            ft.TextButton("Настройки", on_click=lambda _: change_content(3)),
            ft.TextButton("О программе", on_click=lambda _: change_content(4)),
            ft.TextButton("Выход", on_click=lambda _: change_content(5)),
        ],
    )
    page.drawer = drawer

    # Верхняя панель - используем обычный текст для кнопок, обернутый в Container
    menu_container = ft.Container(
        content=ft.Text("☰", color=Colors.WHITE, size=18),
        on_click=lambda _: setattr(page.drawer, 'open', True),
        padding=ft.padding.all(5),
    )

    close_container = ft.Container(
        content=ft.Text("✕", color=Colors.WHITE, size=18),
        on_click=lambda _: page.window.close(),
        padding=ft.padding.all(5),
    )

    # Панель с тремя цветными точками (только для декора)
    dots = ft.Row([
        ft.Container(width=10, height=10, border_radius=5, bgcolor=Colors.RED_400),
        ft.Container(width=10, height=10, border_radius=5, bgcolor=Colors.YELLOW_400),
        ft.Container(width=10, height=10, border_radius=5, bgcolor=Colors.GREEN_400),
    ], spacing=5)

    # Заголовок
    title_text = ft.Text("PlacePet", color=Colors.WHITE, size=14)

    # Верхняя панель
    title_bar = ft.GestureDetector(
        content=ft.Container(
            content=ft.Row(
                [dots, title_text, ft.Row([menu_container, close_container])],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#66000000",
            padding=ft.padding.all(12),
        ),
        on_pan_update=on_pan_update,
    )

    # Основной контейнер
    main_container = ft.Container(
        content=ft.Column(
            [
                title_bar,
                ft.Container(
                    content=ft.Column(
                        [
                            content_text,
                            ft.Container(height=20),
                            button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    bgcolor="#44000000",
                    padding=20,
                    expand=True,
                ),
            ],
            spacing=0,
        ),
        width=300,
        height=400,
        border_radius=15,
        border=ft.border.all(2, Colors.WHITE24),
    )

    page.add(main_container)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)