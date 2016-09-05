import gameconfig

class Item:
    # an Object that can be picked up and used
    def __init__(self, special=None, use_function=None):
        self.special = special
        self.use_function = use_function

    def use(self):
        if self.use_function is None:
            return('The ' + self.owner.name.upper() + ' cannot be used.')
        else:
            if self.use_function(self) != 'cancelled':
                gameconfig.player.player.consume_item_inventory(self)