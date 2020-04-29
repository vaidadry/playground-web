import random
import views


def choose_dinner(selectmeal, selections):
    meal_list = []
    no_recipe = str('No recipes for this selection available. Contribute!')
    try:
        if selections == "comfortfood":
            mealtime_filter = views.models.FoodMood.query.filter_by(meal=selectmeal, comfortfood=True).all()
            for dish in mealtime_filter:
                name = dish.name
                meal_list.append(name)
        elif selections == "fish":
            mealtime_filter = views.models.FoodMood.query.filter_by(meal=selectmeal, fish=True).all()
            for dish in mealtime_filter:
                name = dish.name
                meal_list.append(name)
        else:
            mealtime_filter = views.models.FoodMood.query.filter_by(meal=selectmeal).all()
            for dish in mealtime_filter:
                name = dish.name
                meal_list.append(name)
        suggestion = random.choice(meal_list)
        return suggestion
    except IndexError:
        return no_recipe


def select_url(suggestion):
    meal = views.models.FoodMood.query.filter_by(name=suggestion).first()
    try:
        url = meal.recipe
        return url
    except AttributeError:
        pass


# convert url in correct form
def url_convert(recipe):
    if recipe.startswith("http://") or recipe.startswith("https://"):
        return recipe
    else:
        recipe_upd = "http://" + recipe
        return recipe_upd


