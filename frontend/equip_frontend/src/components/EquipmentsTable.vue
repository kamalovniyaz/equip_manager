<template>
  <div class="wrapper">
    <router-link
        :class="{ 'active-link': $route.path === '/' }"
        class="btn btn-outline-success"
        to="/"
    >
      Меню
    </router-link>
    <router-link
        :class="{ 'active-link': $route.path === '/equipment_add' }"
        class="btn btn-outline-success"
        to="/equipment_add"
    >
      Добавить
    </router-link>
    <input class="search-input" v-model="serialNumberFilter" placeholder="Для поиска введите серийный номер">
    <table class="table">
      <thead>
      <tr>
        <th>Тип оборудования</th>
        <th>Серийный номер</th>
        <th>Активно</th>
        <th>Примечание</th>
        <th>Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="equipment in filteredEquipments" :key="equipment.id">
        <td>{{ equipment.equipment_type }}</td>
        <td>{{ equipment.serial_number }}</td>
        <td>
          <span v-if="equipment.is_active">✅</span>
          <span v-else>❌</span>
        </td>
        <td>{{ equipment.note }}</td>
        <td>
          <div class="image-container">
            <img
                data-bs-target="#exampleModal"
                data-bs-toggle="modal"
                src="@/assets/images/trash.png"
                @click="openModal(equipment.id)"
            />
            <div
                id="exampleModal"
                aria-hidden="true"
                aria-labelledby="exampleModalLabel"
                class="modal fade"
                tabindex="-1"
            >
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 id="exampleModalLabel" class="modal-title">
                      Вы уверены что хотите удалить оборудование?
                    </h5>
                    <button
                        aria-label="Close"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        type="button"
                    ></button>
                  </div>
                  <div class="modal-footer">
                    <button class="btn btn-secondary" data-bs-dismiss="modal" type="button">
                      Отмена
                    </button>
                    <button
                        class="btn btn-primary"
                        data-bs-dismiss="modal"
                        type="button"
                        @click="deleteEquipment(equipment.id)"
                    >
                      Удалить
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <router-link :to="`/equipment_edit/${equipment.id}`">
              <img src="@/assets/images/settings.png"/>
            </router-link>
          </div>
        </td>
      </tr>
      </tbody>
    </table>

    <nav aria-label="Навигация по страницам">
      <ul class="pagination justify-content-center">
        <li :class="{ disabled: currentPage === 1 }" class="page-item">
          <a aria-disabled="true" class="page-link" href="#" tabindex="-1" @click="goToFirstPage"
          >1</a
          >
        </li>
        <li v-if="currentPage > 11" class="page-item">
          <a class="page-link" href="#" @click="lastTenPages">{{ currentPage - 10 }}</a>
        </li>
        <li :class="{ disabled: currentPage === 1 }" class="page-item">
          <a aria-disabled="true" class="page-link" href="#" tabindex="-1" @click="previousPage"
          >Предыдущая</a
          >
        </li>
        <li v-if="showPageRange" :class="{ active: page === currentPage }" class="page-item">
          <a aria-disabled="true" class="page-link" href="#" tabindex="-1">{{ currentPage }}</a>
        </li>
        <li
            v-for="page in getPageRange"
            :key="page"
            :class="{ active: page === currentPage }"
            class="page-item"
        >
          <a class="page-link" href="#" @click="selectPage(page)">{{ page }}</a>
        </li>
        <li :class="{ disabled: currentPage === totalPages }" class="page-item">
          <a class="page-link" href="#" @click="nextPage">Следующая</a>
        </li>
        <li v-if="currentPage < totalPages - 10" class="page-item">
          <a class="page-link" href="#" @click="nextTenPages">{{ currentPage + 10 }}</a>
        </li>
        <li :class="{ disabled: currentPage === totalPages }" class="page-item">
          <a class="page-link" href="#" @click="goToLastPage">{{ totalPages }}</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'vue3-toastify'

export default {
  data() {
    return {
      equipmentIdToDelete: null,
      equipments: [],
      currentPage: 1,
      totalPages: null,
      serialNumberFilter: '',
    }
  },
  computed: {
    showPageRange() {
      return this.currentPage > 1 && this.currentPage < this.totalPages
    },
    filteredEquipments() {
      if (!this.serialNumberFilter) {
        return this.equipments;
      } else {
        return this.equipments.filter(equipment =>
            equipment.serial_number.toLowerCase().includes(this.serialNumberFilter.toLowerCase())
        );
      }
    }
  },
  watch: {
    currentPage(page) {
      this.fetchData(page)
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
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
    openModal(equipmentId) {
      this.equipmentIdToDelete = equipmentId
    },
    fetchData(page = 1) {
      axios
          .get(`/api/equipment/?page=${page}`)
          .then((response) => {
            console.log(response.data)
            this.equipments = response.data.equipments
            this.totalPages = response.data.total_pages
          })
          .catch(() => {
            this.errorToast('Ошибка получения данных по оборудованию.')
          })


    },
    deleteEquipment() {
      axios
          .delete(`/api/equipment?id=${this.equipmentIdToDelete}`)
          .then(() => {
            this.successToast('Оборудование успешно удалено.')
            this.equipmentIdToDelete = null
            this.fetchData(this.currentPage)
          })
          .catch(() => {
            this.errorToast('Ошибка удаления оборудования.')
          })
    },
    lastTenPages() {
      if (this.currentPage > 10) {
        this.currentPage -= 10
      }
    },

    nextTenPages() {
      if (this.currentPage < this.totalPages - 10) {
        this.currentPage += 10
      }
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },
    selectPage(page) {
      this.currentPage = page
    },
    goToFirstPage() {
      this.currentPage = 1
    },
    goToLastPage() {
      this.currentPage = this.totalPages
    },
    getPageRange() {
      const range = []
      const minRange = Math.max(1, this.currentPage - 1)
      const maxRange = Math.min(this.totalPages, this.currentPage + 1)

      for (let i = minRange; i <= maxRange; i++) {
        range.push(i)
      }

      return range
    }
  }
}
</script>

<style scoped>
.wrapper {
  margin-top: 10px;
  padding: 20px;
}

.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 20px;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.table th:last-child,
.table td:last-child {
  border-right: none;
}

.table th {
  font-weight: normal;
  background-color: #ffc107;
  color: black;
}

.table tr:hover {
  background-color: #f2f2f2;
}

.table tr:after {
  transition: background-color 0.3s ease;
}

.table tr:hover::after {
  background-color: transparent;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.page-item {
  display: inline-block;
  margin: 2px;
}

.page-link {
  display: block;
  padding: 6px 12px;
  background-color: #f9f9f9;
  border: 1px solid rgba(0, 0, 0, 0.1);
  color: #333;
  cursor: pointer;
  text-decoration: none;
}

.page-link:hover {
  background-color: #e9e9e9;
}

.page-item.active .page-link {
  background-color: orange;
  border-color: orange;
  color: white;
}

.page-item.disabled .page-link {
  opacity: 0.5;
  pointer-events: none;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-outline-success {
  margin: 5px;
}
.search-input {
  width: 300px;
  height: 37px;
  margin-left: 5px;
  padding: 10px;
  border: 1px solid black;
  border-radius: 4px;
}
</style>

