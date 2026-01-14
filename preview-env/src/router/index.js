import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/special-equipment/entrust'
  },
  {
    path: '/special-equipment/entrust',
    name: 'EntrustList',
    component: () => import('@/views/specialEquipment/entrust/index.vue')
  },
  {
    path: '/special-equipment/record-entry',
    name: 'RecordEntry',
    component: () => import('@/views/specialEquipment/record/entry.vue')
  },
  {
    path: '/special-equipment/audit',
    name: 'AuditWorkbench',
    component: () => import('@/views/specialEquipment/audit/index.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
