<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">

    <!-- Main Content -->
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 space-y-6">

     <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
       <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100">Administradores del Sistema</h1>
       <div class="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <button @click="openCreateForm" class="px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 shadow-sm font-medium whitespace-nowrap">
            + Nuevo Administrador
          </button>
       </div>
     </div>

    <!-- Active List -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden transition-colors">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-700/50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Nombre</th>
            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Usuario</th>
            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Correo</th>
            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Acciones</th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-gray-900 dark:text-gray-100 font-medium">{{ user.first_name }} {{ user.last_name }}</td>
            <td class="px-6 py-4 whitespace-nowrap font-bold text-orange-600 dark:text-orange-400">{{ user.username }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-700 dark:text-gray-300">{{ user.email }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <button @click="openEditForm(user)" class="text-indigo-600 dark:text-indigo-400 hover:text-indigo-900 dark:hover:text-indigo-300 mr-4 transition-colors">Editar</button>
              <button @click="deleteItem(user.id)" class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300 transition-colors">Eliminar</button>
            </td>
          </tr>
          <tr v-if="users.length === 0">
              <td colspan="4" class="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                  No hay administradores registrados o cargando...
              </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Form -->
    <div v-if="showForm" class="fixed inset-0 bg-gray-600 bg-opacity-50 dark:bg-gray-900/70 overflow-y-auto h-full w-full z-50 flex justify-center items-center">
        <div class="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-xl w-full max-w-lg border border-gray-100 dark:border-gray-700">
            <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">{{ isEditing ? 'Editar Administrador' : 'Nuevo Administrador' }}</h2>
            <form @submit.prevent="saveUser" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-bold text-gray-700 dark:text-gray-300">Nombre</label>
                        <input v-model="form.first_name" required type="text" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 shadow-sm p-2 border focus:ring-orange-500 focus:border-orange-500">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-gray-700 dark:text-gray-300">Apellido</label>
                        <input v-model="form.last_name" required type="text" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 shadow-sm p-2 border focus:ring-orange-500 focus:border-orange-500">
                    </div>
                </div>
                <div>
                   <label class="block text-sm font-bold text-gray-700 dark:text-gray-300">Usuario (Login)</label>
                   <input v-model="form.username" required type="text" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm p-2 border bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-orange-500 focus:border-orange-500">
                </div>
                <div>
                   <label class="block text-sm font-bold text-gray-700 dark:text-gray-300">Correo Electrónico</label>
                   <input v-model="form.email" required type="email" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm p-2 border bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-orange-500 focus:border-orange-500">
                </div>
                <div v-if="!isEditing || form.password">
                   <label class="block text-sm font-bold text-gray-700 dark:text-gray-300">
                       Contraseña <span v-if="isEditing" class="text-xs font-normal text-gray-400 dark:text-gray-500">(Déjalo en blanco para mantener la actual)</span>
                   </label>
                   <input v-model="form.password" :required="!isEditing" type="password" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm p-2 border bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-orange-500 focus:border-orange-500">
                </div>
                <div class="flex justify-end gap-3 mt-6">
                    <button type="button" @click="showForm = false" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300">Cancelar</button>
                    <button type="submit" class="px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 shadow-sm">Guardar</button>
                </div>
            </form>
        </div>
    </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../plugins/axios'


const users = ref([])
const showForm = ref(false)
const isEditing = ref(false)
const editingId = ref(null)

const form = ref({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: ''
})

const fetchItems = async () => {
    try {
        const res = await apiClient.get('users/')
        users.value = res.data
    } catch (e) { console.error(e) }
}

const openCreateForm = () => {
    isEditing.value = false
    editingId.value = null
    form.value = { username: '', email: '', first_name: '', last_name: '', password: '' }
    showForm.value = true
}

const openEditForm = (user) => {
    isEditing.value = true
    editingId.value = user.id
    form.value = {
        username: user.username,
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name,
        password: '' // empty so we don't change if not typed
    }
    showForm.value = true
}

const saveUser = async () => {
    try {
        const payload = { ...form.value }
        if (isEditing.value && !payload.password) {
            delete payload.password // don't send empty password if editing
        }

        if (isEditing.value) {
            await apiClient.patch(`users/${editingId.value}/`, payload)
        } else {
            await apiClient.post('users/', payload)
        }
        
        showForm.value = false
        fetchItems()
    } catch (e) {
        alert("Error al guardar usuario. Revisa que el usuario no exista previamente.")
        console.error(e)
    }
}

const deleteItem = async (id) => {
    if(confirm('¿Seguro que deseas eliminar este administrador?')) {
        try {
            await apiClient.delete(`users/${id}/`)
            fetchItems()
        } catch (e) {
            console.error(e)
            alert("No se pudo eliminar el administrador.")
        }
    }
}

onMounted(() => fetchItems())
</script>
