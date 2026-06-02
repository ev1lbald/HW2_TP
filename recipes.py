class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity  
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        try:
            float_value = float(value)
        except (ValueError, TypeError):
            raise ValueError("Количество должно быть числом")

        if float_value <= 0:
            raise ValueError("Количество должно быть положительным")
        
        self._quantity = float_value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, value):
        if not isinstance(value, Ingredient):
            return False
        return self.name == value.name and self.unit == value.unit


class Recipe:
    def __init__(self, title: str, ingredients: list):
        self.title = title
        self.ingredients = list(ingredients)

    def add_ingredient(self, ingredient: Ingredient):
        if ingredient in self.ingredients:
            idx = self.ingredients.index(ingredient)
            self.ingredients[idx].quantity += ingredient.quantity
        else:
            self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if isinstance(ratio, (int, float)):
            return ratio > 0
        return False

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        
        new_ingredients = [
            Ingredient(ingr.name, ingr.quantity * ratio, ingr.unit)
            for ingr in self.ingredients
        ]
        return Recipe(title=self.title, ingredients=new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        ingredients_str = "\n".join(str(ingr) for ingr in self.ingredients)
        return f"Рецепт: {self.title}\nИнгредиенты:\n{ingredients_str}"


class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list = None):
        if ingredients is None:
            ingredients = []
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scaled_base = super().scale(ratio)
        return DietaryRecipe(
            title=scaled_base.title,
            diet_type=self.diet_type,
            ingredients=scaled_base.ingredients
        )

    def __str__(self):
        ingredients_str = "\n".join(str(ingr) for ingr in self.ingredients)
        return f"[{self.diet_type}] {self.title}\nИнгредиенты:\n{ingredients_str}"


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        
        scaled_recipe = recipe.scale(portions)
        for ingr in scaled_recipe.ingredients:
            self._items.append((ingr, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        aggregated = {}
        for ingr, _ in self._items:
            key = (ingr.name, ingr.unit)
            if key in aggregated:
                aggregated[key] += ingr.quantity
            else:
                aggregated[key] = ingr.quantity

        result = [
            Ingredient(name, quantity, unit)
            for (name, unit), quantity in aggregated.items()
        ]
        
        result.sort(key=lambda x: x.name)
        return result

    def __add__(self, other: "ShoppingList"):
        if not isinstance(other, ShoppingList):
            return NotImplemented
        
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list
