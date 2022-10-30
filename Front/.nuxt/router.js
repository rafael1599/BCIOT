import Vue from 'vue'
import Router from 'vue-router'
import { normalizeURL, decode } from 'ufo'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _d3b4dad0 = () => interopDefault(import('..\\src\\pages\\dashboard.vue' /* webpackChunkName: "pages/dashboard" */))
const _d9f31a44 = () => interopDefault(import('..\\src\\pages\\inspire.vue' /* webpackChunkName: "pages/inspire" */))
const _5ab99f0c = () => interopDefault(import('..\\src\\pages\\devices\\led.vue' /* webpackChunkName: "pages/devices/led" */))
const _e7fcdffe = () => interopDefault(import('..\\src\\pages\\devices\\smart-light.vue' /* webpackChunkName: "pages/devices/smart-light" */))
const _2a9d9090 = () => interopDefault(import('..\\src\\pages\\devices\\smart-lock.vue' /* webpackChunkName: "pages/devices/smart-lock" */))
const _827dd054 = () => interopDefault(import('..\\src\\pages\\index.vue' /* webpackChunkName: "pages/index" */))

const emptyFn = () => {}

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: '/',
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/dashboard",
    component: _d3b4dad0,
    name: "dashboard"
  }, {
    path: "/inspire",
    component: _d9f31a44,
    name: "inspire"
  }, {
    path: "/devices/led",
    component: _5ab99f0c,
    name: "devices-led"
  }, {
    path: "/devices/smart-light",
    component: _e7fcdffe,
    name: "devices-smart-light"
  }, {
    path: "/devices/smart-lock",
    component: _2a9d9090,
    name: "devices-smart-lock"
  }, {
    path: "/",
    component: _827dd054,
    name: "index"
  }],

  fallback: false
}

export function createRouter (ssrContext, config) {
  const base = (config._app && config._app.basePath) || routerOptions.base
  const router = new Router({ ...routerOptions, base  })

  // TODO: remove in Nuxt 3
  const originalPush = router.push
  router.push = function push (location, onComplete = emptyFn, onAbort) {
    return originalPush.call(this, location, onComplete, onAbort)
  }

  const resolve = router.resolve.bind(router)
  router.resolve = (to, current, append) => {
    if (typeof to === 'string') {
      to = normalizeURL(to)
    }
    return resolve(to, current, append)
  }

  return router
}
