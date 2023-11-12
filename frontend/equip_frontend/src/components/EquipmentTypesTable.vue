<template>
  <div class="wrapper">
    <router-link
        :class="{ 'active-link': $route.path === '/' }"
        class="btn btn-outline-success"
        to="/"
    >
      Меню
    </router-link>
    <table class="table">
      <thead>
      <tr>
        <th>Наименование типа</th>
        <th>Маска серийного номера</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="type in equipmentTypes" :key="type.id">
        <td>{{ type.name }}</td>
        <td>{{ type.serial_number_mask }}</td>

      </tr>
      </tbody>
    </table>
    <div class="mask-description">
    <span> N – цифра от 0 до 9 | A – прописная буква латинского алфавита | a – строчная буква латинского алфавита |	X – прописная буква латинского алфавита либо цифра от 0 до 9 | Z – символ из списка: “-“, “_”, “@”
</span>
    </div>
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
      equipmentTypes: [],
      currentPage: 1,
      totalPages: null,
    }
  },
  computed: {
    showPageRange() {
      return this.currentPage > 1 && this.currentPage < this.totalPages
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
    fetchData(page = 1) {
      axios
          .get(`/api/equipment-type/?page=${page}`)
          .then((response) => {
            console.log(response.data)
            this.equipmentTypes = response.data.equipment_types
            this.totalPages = response.data.total_pages
          })
          .catch(() => {
            this.errorToast('Ошибка получения данных по типам оборудования.')
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

.btn-outline-success {
  margin: 5px;
}

.mask-description {
  padding: 10px;
  margin: 20px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

.mask-description span {
  font-family: Arial, sans-serif;
  font-size: 14px;
  color: #555;
}

</style>

