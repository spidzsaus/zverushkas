from bio import AnimalGenerator

Default = AnimalGenerator()
Mamal = AnimalGenerator(leg_count=2, straightness=(6, 20), gradation=(10, 50))
Insect = AnimalGenerator(leg_count=3, straightness=(0.01, 10), distribution=(0.01, 20), gradation=(0.01, 5))
Bird = AnimalGenerator(leg_count=1, straightness=(1, 15), gradation=(1, 50), length=(6, 9))
Dragon = AnimalGenerator(length=(14, 20), distribution=(40, 100), leg_count=2, straightness=(7, 15), spreadvalue=(10, 30), gibbosity=(10, 30))