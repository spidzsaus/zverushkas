from bio import Preset

Mamal = Preset(leg_count=2, straightness=(6, 20), gradation=(10, 50))
Insect = Preset(leg_count=3, straightness=(0.01, 10), distribution=(0.01, 20), gradation=(0.01, 5))
Bird = Preset(leg_count=1, straightness=(1, 15), gradation=(1, 50), length=(6, 9))
Dragon = Preset(length=(14, 20), distribution=(40, 100), leg_count=4, straightness=(7, 15))
