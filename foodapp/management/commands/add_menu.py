from django.core.management.base import BaseCommand
from foodapp.models import Category, Menu


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # CATEGORY CREATION

        starters, _ = Category.objects.get_or_create(name="Starters")

        main_course, _ = Category.objects.get_or_create(name="Main Course")

        biryani, _ = Category.objects.get_or_create(name="Rice & Biryani")

        breads, _ = Category.objects.get_or_create(name="Breads")

        beverages, _ = Category.objects.get_or_create(name="Beverages")

        desserts, _ = Category.objects.get_or_create(name="Desserts")

        cold_drinks, _ = Category.objects.get_or_create(name="Cold Drinks")


        # STARTERS

        Menu.objects.get_or_create(
            name="Paneer Tikka",
            category=starters,
            price=280,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Veg Cutlet",
            category=starters,
            price=120,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Chicken 65",
            category=starters,
            price=150,
            is_veg=False
        )

        Menu.objects.get_or_create(
            name="Chicken Pakora",
            category=starters,
            price=180,
            is_veg=False
        )


        # MAIN COURSE

        Menu.objects.get_or_create(
            name="Paneer Butter Masala",
            category=main_course,
            price=199,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Dal Tadka",
            category=main_course,
            price=99,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Butter Chicken",
            category=main_course,
            price=249,
            is_veg=False
        )

        Menu.objects.get_or_create(
            name="Chicken Curry",
            category=main_course,
            price=220,
            is_veg=False
        )


        # RICE & BIRYANI

        Menu.objects.get_or_create(
            name="Chicken Biryani",
            category=biryani,
            price=250,
            is_veg=False
        )

        Menu.objects.get_or_create(
            name="Mutton Biryani",
            category=biryani,
            price=350,
            is_veg=False
        )

        Menu.objects.get_or_create(
            name="Veg Pulao",
            category=biryani,
            price=140,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Jeera Rice",
            category=biryani,
            price=120,
            is_veg=True
        )


        # BREADS

        Menu.objects.get_or_create(
            name="Naan",
            category=breads,
            price=40,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Garlic Naan",
            category=breads,
            price=50,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Tandoori Roti",
            category=breads,
            price=30,
            is_veg=True
        )


        # BEVERAGES

        Menu.objects.get_or_create(
            name="Masala Chai",
            category=beverages,
            price=20,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Coffee",
            category=beverages,
            price=40,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Sweet Lassi",
            category=beverages,
            price=60,
            is_veg=True
        )


        # COLD DRINKS

        Menu.objects.get_or_create(
            name="Coca Cola",
            category=cold_drinks,
            price=40,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Pepsi",
            category=cold_drinks,
            price=40,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Sprite",
            category=cold_drinks,
            price=40,
            is_veg=True
        )


        # DESSERTS

        Menu.objects.get_or_create(
            name="Gulab Jamun",
            category=desserts,
            price=80,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Rasmalai",
            category=desserts,
            price=120,
            is_veg=True
        )

        Menu.objects.get_or_create(
            name="Ice Cream",
            category=desserts,
            price=90,
            is_veg=True
        )


        self.stdout.write(self.style.SUCCESS("Menu added successfully"))