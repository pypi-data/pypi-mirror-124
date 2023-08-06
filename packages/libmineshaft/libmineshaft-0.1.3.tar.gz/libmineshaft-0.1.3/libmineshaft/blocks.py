import os


class Block:
    def __init__(
        self,
        id,
        image,
        resistance=2,
        name="Block",
        unbreakable=False,
        falls=False,
        breaktime=10,  # seconds
    ):
        self.id = id
        self.image = os.path.join(image)
        self.resistance = resistance
        self.name = name
        self.unbreakable = unbreakable
        self.falls = falls
        self.breaktime = breaktime


class NoIDBlock(Block):
    def __init__(
        self,
        image,
        resistance=2,
        name="No ID Block",
        unbreakable=False,
        falls=False,
        breaktime=10,
    ):
        self.image = os.path.join(image)
        self.resistance = resistance
        self.name = name
        self.unbreakable = unbreakable
        self.falls = falls
        self.breaktime = breaktime


class MultipleStateBlock(Block):
    def __init__(self, id, blocks):
        if len(self.blocks) > 15:
            raise IndexError(
                "There is too much block IDs.\nMore block ID slots may be added in the future"
            )
        self.id = id
        self.blocks = blocks
        self.default = self.blocks[0]


air = Block(0, image=False, resistance=-1, name="Air", falls=False, breaktime=-1)
stone = MultipleStateBlock(
    1,
    [
        NoIDBlock(
            ["assets", "images", "blocks", "stone.png"],
            resistance=10,
            name="Stone",
            falls=False,
            breaktime=15,
        )
    ],
)

grass = Block(
    2,
    ["assets", "images", "blocks", "grass.png"],
    resistance=0,
    name="Grass Block",
    falls=False,
    breaktime=2,
)

dirt = Block(
    3,
    ["assets", "images", "blocks", "dirt.png"],
    resistance=0,
    name="Dirt",
    falls=False,
    breaktime=2,
)

cobblestone = Block(
    4,
    ["assets", "images", "blocks", "cobblestone.png"],
    resistance=10,
    name="Cobblestone",
    falls=False,
    breaktime=15,
)

bedrock = Block(
    7,
    ["assets", "images", "blocks", "bedrock.png"],
    resistance=-1,
    name="Bedrock",
    falls=False,
    breaktime=-1,
)


BLOCKS = {0: air, 1: stone, 2: grass, 3: dirt, 4: cobblestone}
