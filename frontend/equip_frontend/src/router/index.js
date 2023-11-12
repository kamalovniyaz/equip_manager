import {createRouter, createWebHistory} from 'vue-router'
import EquipmentsTable from "../components/EquipmentsTable.vue";
import UserLogin from "@/components/UserLogin.vue";
import HomeView from "@/components/HomeView.vue";
import EquipmentTypesTable from "@/components/EquipmentTypesTable.vue";
import EquipmentAdd from "@/components/EquipmentAdd.vue";
import EquipmentEdit from "@/components/EquipmentEdit.vue";

const routes = [
    {
        path: '/auth',
        name: 'auth',
        component: UserLogin
    },
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/equipments_table',
        name: 'equipments_table',
        component: EquipmentsTable
    },
    {
        path: '/equipment_types_table',
        name: 'equipment_types_table',
        component: EquipmentTypesTable
    },
    {
        path: '/equipment_add',
        name: 'equipment_add',
        component: EquipmentAdd
    },
    {
    path: '/equipment_edit/:equipmentId',
    name: 'equipment_edit',
    component: EquipmentEdit
  },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router


