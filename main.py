if __name__ == '__main__':
    from bio import Animal
    from random import randint
    seed = randint(1, 99999999)
    print(seed)
    test = Animal.from_seed(seed)
    print(test.spine)
    test.draw().show()
    