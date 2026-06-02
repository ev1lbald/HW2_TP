import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe

def test_ingredient_creation():
    ingr = Ingredient("Мука", 500.0, "г")
    assert ingr.name == "Мука"
    assert ingr.quantity == 500.0
    assert ingr.unit == "г"


def test_ingredient_str():
    ingr = Ingredient("Мука", 500.0, "г")
    assert str(ingr) == "Мука: 500.0 г"


def test_ingredient_eq():
    ingr1 = Ingredient("Мука", 500.0, "г")
    ingr2 = Ingredient("Мука", 300.0, "г")
    ingr3 = Ingredient("Сахар", 500.0, "г")
    ingr4 = Ingredient("Мука", 500.0, "кг")

    assert ingr1 == ingr2
    assert ingr1 != ingr3
    assert ingr1 != ingr4


def test_recipe_creation():
    ingr = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ingr])
    assert recipe.title == "Пицца"
    assert recipe.ingredients == [ingr]


def test_recipe_add_ingredient_new():
    recipe = Recipe("Пицца", [])
    ingr = Ingredient("Мука", 500.0, "г")
    recipe.add_ingredient(ingr)
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 500.0


def test_recipe_add_ingredient_duplicate():
    ingr1 = Ingredient("Мука", 500.0, "г")
    ingr2 = Ingredient("Мука", 300.0, "г")
    recipe = Recipe("Пицца", [ingr1])
    recipe.add_ingredient(ingr2)

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 800.0


def test_recipe_scale_success():
    ingr = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ingr])
    scaled = recipe.scale(2.0)

    assert scaled is not recipe
    assert recipe.ingredients[0].quantity == 500.0
    assert scaled.ingredients[0].quantity == 1000.0


def test_recipe_scale_invalid_ratio():
    ingr = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ingr])
    with pytest.raises(ValueError):
        recipe.scale(0)
    with pytest.raises(ValueError):
        recipe.scale(-1.5)


def test_recipe_len():
    ingr1 = Ingredient("Мука", 500.0, "г")
    ingr2 = Ingredient("Сахар", 200.0, "г")
    recipe = Recipe("Пицца", [ingr1, ingr2])
    assert len(recipe) == 2


def test_shopping_list_add_recipe_success():
    ingr = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ingr])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2.0)
    
    assert len(shopping_list._items) == 1
    assert shopping_list._items[0][0].quantity == 1000.0


def test_shopping_list_add_recipe_invalid_portions():
    ingr = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ingr])
    shopping_list = ShoppingList()
    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)
    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, -1)


def test_shopping_list_remove_recipe():
    ingr = Ingredient("Мука", 500.0, "г")
    recipe1 = Recipe("Пицца", [ingr])
    recipe2 = Recipe("Торт", [ingr])
    
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1.0)
    shopping_list.add_recipe(recipe2, 1.0)
    
    shopping_list.remove_recipe("Пицца")
    assert len(shopping_list._items) == 1
    assert shopping_list._items[0][1] == "Торт"
    
    shopping_list.remove_recipe("Несуществующий")
    assert len(shopping_list._items) == 1


def test_shopping_list_get_list():
    ingr1 = Ingredient("Мука", 500.0, "г")
    ingr2 = Ingredient("Мука", 300.0, "г")
    ingr3 = Ingredient("Апельсин", 2.0, "шт")
    
    recipe1 = Recipe("Пицца", [ingr1])
    recipe2 = Recipe("Пирог", [ingr2, ingr3])
    
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1.0)
    shopping_list.add_recipe(recipe2, 1.0)
    
    result = shopping_list.get_list()
    
    assert len(result) == 2
    assert result[0].name == "Апельсин"
    assert result[0].quantity == 2.0
    assert result[1].name == "Мука"
    assert result[1].quantity == 800.0


def test_shopping_list_add_operator():
    ingr1 = Ingredient("Мука", 500.0, "г")
    ingr2 = Ingredient("Сахар", 200.0, "г")
    
    recipe1 = Recipe("Пицца", [ingr1])
    recipe2 = Recipe("Торт", [ingr2])
    
    sl1 = ShoppingList()
    sl1.add_recipe(recipe1, 1.0)
    
    sl2 = ShoppingList()
    sl2.add_recipe(recipe2, 1.0)
    
    combined = sl1 + sl2
    
    assert combined is not sl1
    assert combined is not sl2
    assert len(sl1._items) == 1
    assert len(sl2._items) == 1
    assert len(combined._items) == 2
