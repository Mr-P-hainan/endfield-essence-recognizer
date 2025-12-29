<template>
  <v-container>
    <v-expansion-panels color="primary-darken-1" :model-value="[0, 1, 2]" multiple>
      <v-expansion-panel :value="0">
        <v-expansion-panel-title>武器基质预设</v-expansion-panel-title>
        <v-expansion-panel-text>
          <h2>将以下武器所对应的基质视为宝藏</h2>
          <template v-for="weaponType in weaponTypes" :key="weaponType">
            <h3>
              <v-checkbox
                density="compact"
                hide-details
                :indeterminate="isPartiallySelected(weaponType)"
                :model-value="isAllSelected(weaponType)"
                @click="selectAllForType(weaponType, !isAllSelected(weaponType))"
              >
                <template #prepend>
                  <h3 style="margin: 0">{{ weaponType }}</h3>
                </template>
              </v-checkbox>
            </h3>
            <div class="d-flex flex-row flex-wrap gc-4">
              <v-checkbox
                v-for="[weaponId, weapon] in Object.entries(weapons).filter(
                  ([weaponId, weapon]) => weapon.weaponType === weaponType
                )"
                :key="weaponId"
                v-model="selectedWeaponIds"
                color="primary"
                density="comfortable"
                hide-details
                :label="weapon.weaponName"
                :value="weaponId"
              />
              <!-- <v-btn
                v-for="[weaponId, weapon] in Object.entries(weapons).filter(
                  ([weaponId, weapon]) => weapon.weaponType === weaponType
                )"
                variant="outlined"
                :color="selectedWeaponIds.includes(weaponId) ? 'success' : 'error'"
                @click="
                  () => {
                    const index = selectedWeaponIds.indexOf(weaponId)
                    if (index === -1) {
                      selectedWeaponIds.push(weaponId)
                    } else {
                      selectedWeaponIds.splice(index, 1)
                    }
                  }
                "
              >
                <template v-slot:prepend>
                  <v-icon
                    :color="selectedWeaponIds.includes(weaponId) ? 'success' : 'error'"
                    :icon="selectedWeaponIds.includes(weaponId) ? 'mdi-check' : 'mdi-close'"
                  ></v-icon>
                </template>
                {{ weapon.weaponName }}
              </v-btn> -->
            </div>
          </template>
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel :value="1">
        <v-expansion-panel-title>自定义宝藏基质</v-expansion-panel-title>
        <v-expansion-panel-text>
          <h2>额外将以下属性的基质视为宝藏</h2>
          <v-alert v-if="false" border="start" class="my-4" type="info" variant="tonal">
            请点击右侧（或者下方）的加号按钮添加新的基质属性行，点击删除按钮删除对应行。上下箭头按钮可调整行顺序。
          </v-alert>
          <v-row v-for="(essenceStat, index) in treasureEssenceStats" :key="index" align="center">
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="essenceStat.attribute"
                density="comfortable"
                hide-details
                label="基础属性"
                variant="outlined"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="essenceStat.secondary"
                density="comfortable"
                hide-details
                label="附加属性"
                variant="outlined"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="essenceStat.skill"
                density="comfortable"
                hide-details
                label="技能属性"
                variant="outlined"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-btn
                color="primary"
                icon="mdi-plus"
                variant="text"
                @click="
                  treasureEssenceStats.splice(index + 1, 0, {
                    attribute: '',
                    secondary: '',
                    skill: '',
                  })
                "
              />
              <v-btn
                color="error"
                icon="mdi-delete"
                variant="text"
                @click="treasureEssenceStats.splice(index, 1)"
              />
              <v-btn
                :disabled="index === 0"
                icon="mdi-chevron-up"
                variant="text"
                @click="
                  () => {
                    const stat = treasureEssenceStats.splice(index, 1)[0]!
                    treasureEssenceStats.splice(index - 1, 0, stat)
                  }
                "
              />
              <v-btn
                :disabled="index === treasureEssenceStats.length - 1"
                icon="mdi-chevron-down"
                variant="text"
                @click="
                  () => {
                    const stat = treasureEssenceStats.splice(index, 1)[0]!
                    treasureEssenceStats.splice(index + 1, 0, stat)
                  }
                "
              />
            </v-col>
          </v-row>
          <v-row v-if="treasureEssenceStats.length === 0" class="my-4">
            <v-col cols="12" sm="6" md="9">
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="treasureEssenceStats.push({ attribute: '', secondary: '', skill: '' })"
              >
                添加自定义宝藏基质
              </v-btn>
            </v-col>
          </v-row>
          <v-row v-else>
            <v-col cols="12" sm="6" md="9" />
            <v-col cols="12" sm="6" md="3">
              <v-btn
                color="primary"
                icon="mdi-plus"
                variant="text"
                @click="treasureEssenceStats.push({ attribute: '', secondary: '', skill: '' })"
              />
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel :value="2">
        <v-expansion-panel-title>操作设置</v-expansion-panel-title>
        <v-expansion-panel-text>
          <h2>遇到宝藏或者垃圾基质时，该如何操作？</h2>
          <v-row>
            <v-col cols="12" md="6">
              <h3>对于<span class="text-success">宝藏基质</span>，我们</h3>
              <v-radio-group v-model="treasureAction" color="primary" density="comfortable">
                <v-radio label="不去动它" value="keep" />
                <v-radio label="把它锁上" value="lock" />
                <v-radio label="把它标记为弃用" value="deprecate" disabled />
                <v-radio label="如果锁着，则解锁" value="unlock"></v-radio>
                <v-radio label="如果已标记为弃用，则取消弃用" value="undeprecate" />
                <v-radio label="解锁且取消弃用" value="unlock_and_undeprecate"></v-radio>
              </v-radio-group>
            </v-col>
            <v-col cols="12" md="6">
              <h3>对于<span class="text-error">垃圾基质</span>，我们</h3>
              <v-radio-group v-model="trashAction" color="primary" density="comfortable">
                <v-radio label="不去动它" value="keep" />
                <v-radio label="把它锁上" value="lock" />
                <v-radio label="把它标记为弃用" value="deprecate" />
                <v-radio label="如果锁着，则解锁" value="unlock" />
                <v-radio label="如果已标记为弃用，则取消弃用" value="undeprecate" />
                <v-radio label="解锁且取消弃用" value="unlock_and_undeprecate" />
              </v-radio-group>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref, watch } from 'vue'

interface Weapon {
  weaponType: string
  weaponName: string
}

interface EssenceStat {
  attribute: string
  secondary: string
  skill: string
}

const selectedWeaponIds = ref<string[]>([])
const treasureEssenceStats = ref<EssenceStat[]>([])
const treasureAction = ref('lock')
const trashAction = ref('unlock')

const weaponTypes = ['单手剑', '双手剑', '长柄武器', '手铳', '施术单元']
const weapons = ref<Record<string, Weapon>>({})

const notSelectedWeaponIds = computed(() => {
  return Object.keys(weapons.value).filter(
    (weaponId) => !selectedWeaponIds.value.includes(weaponId)
  )
})

function selectAllForType(weaponType: string, select: boolean) {
  const weaponIds = Object.entries(weapons.value)
    .filter(([_, weapon]: [string, Weapon]) => weapon.weaponType === weaponType)
    .map(([id, _]) => id)
  if (select) {
    selectedWeaponIds.value = [...new Set([...selectedWeaponIds.value, ...weaponIds])]
  } else {
    selectedWeaponIds.value = selectedWeaponIds.value.filter((id) => !weaponIds.includes(id))
  }
}

function isAllSelected(weaponType: string): boolean {
  const weaponIds = Object.entries(weapons.value)
    .filter(([_, weapon]) => weapon.weaponType === weaponType)
    .map(([id, _]) => id)
  return weaponIds.every((id) => selectedWeaponIds.value.includes(id))
}

function isPartiallySelected(weaponType: string): boolean {
  const weaponIds = Object.entries(weapons.value)
    .filter(([_, weapon]) => weapon.weaponType === weaponType)
    .map(([id, _]) => id)
  const selectedCount = weaponIds.filter((id) => selectedWeaponIds.value.includes(id)).length
  return selectedCount > 0 && selectedCount < weaponIds.length
}

const config = computed(() => {
  return {
    version: 0,
    trash_weapon_ids: notSelectedWeaponIds.value,
    treasure_essence_stats: treasureEssenceStats.value,
    treasure_action: treasureAction.value,
    trash_action: trashAction.value,
  }
})

async function getWeapons() {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/weapons`)
  const result = await response.json()
  weapons.value = result
}

async function getConfig() {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/config`)
  const result = await response.json()
  const { trash_weapon_ids, treasure_essence_stats, treasure_action, trash_action } = result
  treasureEssenceStats.value = treasure_essence_stats
  treasureAction.value = treasure_action
  trashAction.value = trash_action
  selectedWeaponIds.value = Object.keys(weapons.value).filter(
    (weaponId) => !trash_weapon_ids.includes(weaponId)
  )
}

async function postConfig() {
  await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/config`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(config.value),
  })
}

onMounted(async () => {
  await getWeapons()
  await getConfig()
  watch(config, postConfig)
})
</script>

<style scoped lang="scss"></style>
