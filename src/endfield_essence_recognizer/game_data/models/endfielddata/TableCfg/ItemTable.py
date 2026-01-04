from typing import TypedDict

from endfield_essence_recognizer.game_data.models.common import TranslationKey


class Item(TypedDict):
    backpackCanDiscard: bool
    decoDesc: TranslationKey
    desc: TranslationKey
    iconCompositeId: str
    iconId: str
    id: str
    maxBackpackStackCount: int
    maxStackCount: int
    modelKey: str
    name: TranslationKey
    noObtainWayConditionId: list[str]
    noObtainWayHint: TranslationKey
    noObtainWayId: list[str]
    obtainWayIds: list[str]
    outcomeItemIds: list[str]
    rarity: int
    showAllDepotCount: bool
    showingType: int
    sortId1: int
    sortId2: int
    type: int
    valuableTabType: int


type ItemTable = dict[str, Item]
