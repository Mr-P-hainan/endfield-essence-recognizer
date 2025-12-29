<template>
  <v-app>
    <v-navigation-drawer v-model="drawer">
      <v-card to="/" variant="flat" class="pa-4" rounded="0">
        <h1 class="text-center ma-4">终末地基质<br />妙妙小工具</h1>
      </v-card>
      <v-divider />
      <v-list nav density="comfortable">
        <v-list-item
          v-for="(route, index) in router.options.routes"
          :key="index"
          :to="route.path"
          color="primary"
          :prepend-icon="(route.meta as any)?.icon"
        >
          {{ route.meta?.title ?? route.name }}
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary" flat density="comfortable">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title>{{ route.meta?.title || '终末地基质妙妙小工具' }}</v-app-bar-title>
      <template #append>
        <v-btn icon="mdi-theme-light-dark" @click="theme.toggle()" />
      </template>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTheme } from 'vuetify'
import { useLogs } from '@/composables/useLogs'

const route = useRoute()
const router = useRouter()
const theme = useTheme()

const drawer = ref<boolean | null>(null)

// 初始化日志 WebSocket 连接
useLogs()
</script>

<style scoped lang="scss"></style>
