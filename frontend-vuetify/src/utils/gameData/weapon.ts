import {
  gemTable,
  gemTagIdTable,
  getTranslation,
  weaponBasicTable,
  worldEnergyPointGroupTable,
  worldEnergyPointTable,
  itemTable,
  wikiEntryDataTable,
  rarityColorTable,
  skillPatchTable,
  wikiEntryTable,
  wikiGroupTable,
} from '@/utils/gameData/gameData'
import { computed, ref } from 'vue'

const allAttributeStats = computed(() =>
  Object.values(gemTable.value)
    .filter((gem) => gem.termType === 0)
    .map((gem) => gem.gemTermId),
)
const allSecondaryStats = computed(() =>
  Object.values(gemTable.value)
    .filter((gem) => gem.termType === 1)
    .map((gem) => gem.gemTermId),
)
const allSkillStats = computed(() =>
  Object.values(gemTable.value)
    .filter((gem) => gem.termType === 2)
    .map((gem) => gem.gemTermId),
)

function getGroupIconUrl(iconId: string): string {
  return `https://cos.yituliu.cn/endfield/sprites_selective/wiki/groupicon/${iconId}.png`
}
