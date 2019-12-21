import kitchen
import shop
import time
import argparse
import units


def buy_ingredients(n_eaters):
    amount = n_eaters * 250 * units.g
    try:
        flour = shop.buy(spätzle_flour=amount)
    except shop.NotAvailable:
        flour = shop.buy(flour=amount)

    eggs = shop.buy(eggs=3 * n_eaters)
    water = kitchen.tap(water=n_eaters * 0.1 * units.approx_glass)
    salt = kitchen.get(salt=1 * units.some)
    emmentaler = shop.buy(emmentaler=n_eaters * 100 / 3 * units.g)
    appenzeller = shop.buy(appenzeller=n_eaters * 100 / 3 * units.g)
    gruyere = shop.buy(gruyere=n_eaters * 100 / 3 * units.g)
    return [flour, eggs, water, salt], [emmentaler, appenzeller, gruyere]


def make_spätzle(cooks, ingredients):
    dough = kitchen.get(bowl=units.large).fill_with(*ingredients)
    while not dough.has_air_bubbles():
        spoon = kitchen.get(wooden_spoon=units.one)
        for cook in cooks:
            try:
                cook.mix(
                    dough,
                    utensil=spoon,
                    until='getting_tired'
                )
            except kitchen.BrokenSpoon:
                cook.say('Scheiße!')
                spoon = kitchen.get(wooden_spoon=units.one)
    pot = (
        kitchen
        .get(hotplate=units.one)
        .put(
            kitchen
            .get(pot=units.big)
            .fill_with(kitchen.get(water=units.pot))
            .add(kitchen.get(salt=units.a_lot))
        )
        .wait(until='rolling_boil')
    )
    bowl = kitchen.get(bowl=units.large)
    while not dough.empty:
        portion = dough.content().take_some()
        (
            pot
            .add(
                kitchen
                .get(presse=units.one)
                .fill_with(portion)
            )
            .press()
            .wait(until='rolling_boil')
            .take(portion)
            .quench('cold_water')
            .add_to(bowl)
        )
    return bowl.content()


def make_kässpätzle(spätzle, cheese):
    bowl = kitchen.get(gratin_dish=units.one)
    cheese_bowl = kitchen.get(bowl=units.medium)

    grater = kitchen.get(grater=units.one)
    for some_cheese in cheese:
        cheese_bowl.add(grater.grate(some_cheese))

    for some_spätzle, some_cheese in zip(
        spätzle.content().subdivide(5),
        cheese_bowl.content().subdivide(5),
    ):
        bowl.add(some_spätzle)
        bowl.add(some_cheese)

    bowl.add(kitchen.get(broth=100 * units.ml))

    oven = kitchen.get(oven=units.one).heat(180 * units.degree_C).wait()
    oven.add(bowl)
    time.sleep(30 * 60)
    return oven.remove(bowl)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cooks', nargs='+')
    parser.add_argument('guests', nargs='*')
    args = parser.parse_args()
    
    ingredients, cheese = buy_ingredients(len(args.guests) + len(args.cooks))
    spätzle = make_spätzle(args.cooks, ingredients)
    food = make_kässpätzle(spätzle, cheese)
    leftover = food.eat(*args.cooks, *args.guests)
    if leftover:
        args.cooks.celebrate()


if __name__ == '__main__':
    main()
