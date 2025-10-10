# brew_coffee_start
def brew_coffee(request):
    print("brewing coffee...")
    return {"coffee": "yes"}


# brew_coffee_end


# add_milk_start
def add_milk(brew_coffee):
    def with_add_milk(request):
        brew = brew_coffee(request)
        if request.get("wants_milk", False):
            print("adding milk...")
            brew["milk"] = "yes"
        return brew

    return with_add_milk


# add_milk_end


# cafe_start
class Cafe:
    def __init__(self, brew_coffee):
        self.brew_coffee = brew_coffee

    def brew_coffee(self, request):
        return self.brew_coffee(request)


# cafe_end

# using
brew_coffee_with_milk = add_milk(brew_coffee)
cafe = Cafe(brew_coffee_with_milk)
cafe.brew_coffee({"wants_milk": True})
