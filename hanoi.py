class Tower:
    TOWER_WIDTH = 5

    def __init__(self, n) -> None:
        self.pegs = [[], [], []]
        self.history = []
        self.n = n
        self.moves = 0
        for i in reversed(range(1, n + 1)):
            self.pegs[0].append(i)

    def move(self, source, destination):
        if len(self.pegs[source]) == 0:
            raise IndexError(f"Peg {source} is empty")
        if (
            len(self.pegs[destination]) > 0
            and self.pegs[destination][-1] < self.pegs[source][-1]
        ):
            raise IndexError(f"Destination peg {destination} is smaller than source")
        peg = self.pegs[source].pop()
        self.pegs[destination].append(peg)
        self.history.append((source, destination))
        self.moves += 1
        return len(self.pegs[destination]) - 1

    def is_solved(self):
        goal_peg = self.pegs[2]
        if len(goal_peg) < self.n:
            return False
        for i in range(len(goal_peg) - 1):
            if goal_peg[i] < goal_peg[i + 1]:
                return False
        return True

    def get_peg(self, i):
        return self.pegs[i]

    def __str__(self) -> str:
        height = max([len(peg) for peg in self.pegs])
        picture = ["\n"]
        for i in range(height - 1, -1, -1):
            for peg in self.pegs:
                if len(peg) > i:
                    img = f"{peg[i]: ^{Tower.TOWER_WIDTH}}"
                    picture.append(img)
                    # picture.append(format(peg[i], f"<{Tower.TOWER_WIDTH}"))
                else:
                    picture.append(" " * Tower.TOWER_WIDTH)
            picture.append("\n")
        picture.append("█" * Tower.TOWER_WIDTH * len(self.pegs))
        picture.append("\n")
        return "".join(picture)


def move_tower(tower: Tower, source, index, destination):
    # If we are at the top of the tower
    if index == len(tower.get_peg(source)) - 1:
        our_index = tower.move(source, destination)
        return our_index
    # get index of the other peg
    other = 3 - (source + destination)
    hat_index = move_tower(tower, source, index + 1, other)
    our_index = tower.move(source, destination)
    move_tower(tower, other, hat_index, destination)
    return our_index


def simpler(tower: Tower, n, source, destination):
    if n == 1:
        tower.move(source, destination)
        return
    # get index of the other peg
    other = 3 - (destination + source)
    simpler(tower, n - 1, source, other)
    tower.move(source, destination)
    simpler(tower, n - 1, other, destination)


if __name__ == "__main__":
    tower_a = Tower(20)
    print(tower_a)
    move_tower(tower_a, 0, 0, 2)
    print(tower_a)

    tower_b = Tower(20)
    simpler(tower_b, 20, 0, 2)

    print(tower_a.history == tower_b.history)
