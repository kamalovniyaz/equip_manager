<template>
  <div class="centered-container">
    <h2>Изменения данных оборудования</h2>
  </div>
  <div class="new-equipment-add">
    <div class="form-columns">
      <div class="form-column">
        <div class="form-group">
          <input
              id="equipmentType"
              v-model="equipmentType"
              class="form-input"
              placeholder="Тип оборудования"
              required
              type="text"
          />
        </div>
        <div class="form-group">
          <input id="serialNumber" v-model="serialNumber" class="form-input" placeholder="Серийный номер" required
                 type="text"/>
        </div>
        <div class="form-group">
          <input id="note" v-model="note" class="form-input" placeholder="Примечание"
                 type="text"/>
        </div>
        <div class="form-group">
          <input id="isActive" v-model="isActive" type="checkbox"/>
          <label for="isActive">Активное оборудование</label>
        </div>
      </div>
      <button class="form-button" @click="updateEquipment()">Сохранить</button>
      <button class="form-button" @click="goBack">Назад</button>
      <br/>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'vue3-toastify'
import router from '@/router'

export default {
  data() {
    return {
      id: '',
      equipmentType: '',
      serialNumber: '',
      isActive: false,
      note: '',
      equipmentTypes: ''

    }
  },
  mounted() {
    this.getEquipment()
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    successToast(text) {
      toast(text, {
        theme: 'colored',
        type: 'success',
        position: toast.POSITION.BOTTOM_RIGHT
      })
    },
    errorToast(text) {
      toast(text, {
        theme: 'colored',
        type: 'error',
        position: toast.POSITION.BOTTOM_RIGHT
      })
    },
    getEquipment() {
      this.id = this.$route.params.equipmentId
      axios.get(`/api/equipment?id=${this.id}`)
          .then((response) => {
                const res = response.data['equipment']
                this.equipmentType = res['equipment_type']
                this.serialNumber = res['serial_number']
                this.isActive = res['is_active']
                this.note = res['note']
              }
          )
          .catch((error) => {
            this.errorToast('Ошибка получения типов оборудования')
          })
    },
    updateEquipment() {
      const data = {
        equipment_type: this.equipmentType,
        serial_number: this.serialNumber,
        is_active: this.isActive,
        note: this.note,
      }
      if (this.validateFields()) {
        axios
            .put(`/api/equipment/?id=${this.id}`, data)
            .then(() => {
              this.successToast('Данные об оборудовании успешно обновлены.')
              setTimeout(() => {
                this.clearForm()
                router.push('/equipments_table')
              }, 5000)
            })
            .catch((error) => {
              this.errorToast(error.response.data)
            })
      } else {
        return false
      }
    },
    validateFields() {
      if (this.serialNumber.length !== 10) {
        this.errorToast("Длина маски должна быть равна 10!")
      }
      return true
    },
    clearForm() {
      // Очистка полей формы
      this.equipmentType = ''
      this.serialNumber = ''
      this.isActive = ''
      this.note = ''
    }
  }
}
</script>

<style>
.centered-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 30vh;
}

.new-equipment-add {
  width: 600px;
  padding: 20px;
  margin: auto;
  background-color: #f3f3f3;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-input {
  padding: 0.7rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: calc(100% - 20px);
  box-sizing: border-box;
}

.form-checkbox {
  display: flex;
  align-items: center;
  font-size: 1rem;
}

.form-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  display: block;
  margin-bottom: 10px;
}

.form-button:hover {
  background-color: #2980b9;
}

label {
  font-size: 1rem;
}
</style>


