<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :clipped="clipped"
      fixed
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer />
    </v-app-bar>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'AuthLayout',
  data () {
    return {
      clipped: true,
      drawer: false,
      items: [
        {
          icon: 'mdi-chart-bubble',
          title: 'Dashboard',
          to: '/dashboard'
        },
        {
          icon: 'mdi-apps',
          title: 'Cerradura Inteligente',
          to: '/devices/smart-lock'
        },
        {
          icon: 'mdi-apps',
          title: 'Foco Inteligente',
          to: '/devices/smart-light'
        },
        {
          icon: 'mdi-apps',
          title: 'LED',
          to: '/devices/led'
        }
      ],
      title: 'BCIOT'
    }
  }
}
</script>
