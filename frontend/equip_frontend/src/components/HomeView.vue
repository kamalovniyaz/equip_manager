<template>
  <div class="menu">
    <h1>Меню</h1>
    <button @click="goToEquipmentsTable">Просмотреть оборудование</button>
    <button @click="goToEquipmentTypesTable">Просмотреть типы оборудования</button>
  </div>
</template>

<script>
import router from "@/router/index.js";

export default {
  methods: {
    goToEquipmentsTable() {
      router.push('/equipments_table');
    },
    goToEquipmentTypesTable() {
      router.push('/equipment_types_table');
    }
  }
}
</script>

<style scoped>
.menu {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 400px;
}

button:hover {
  background-color: #2980b9;
}
</style>
