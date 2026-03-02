<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">

    <!-- Main Content -->
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 space-y-6">

     <div class="flex justify-between items-center mb-6">
       <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100">Manejo de Actividades</h1>
       <div class="flex gap-4">
          <button @click="showForm = true" class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 font-medium shadow-sm">
            + Nueva Actividad
          </button>
       </div>
     </div>

     <!-- Toggle Tabs -->
     <div class="flex border-b border-gray-200 dark:border-gray-700 mb-6">
        <button @click="activeTab = 'ACTIVE'" 
                class="px-6 py-3 font-semibold text-sm transition-colors border-b-2"
                :class="activeTab === 'ACTIVE' ? 'border-orange-600 text-orange-600' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:border-gray-300'">
            Activas
        </button>
        <button @click="activeTab = 'ARCHIVED'" 
                class="px-6 py-3 font-semibold text-sm transition-colors border-b-2"
                :class="activeTab === 'ARCHIVED' ? 'border-red-600 text-red-600' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:border-gray-300'">
            Archivadas
        </button>
     </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6">
       <!-- Active Activities -->
       <div v-for="act in displayedActivities" :key="act.id" 
            @click="goToProfile(act.id)"
            class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:border-orange-200 dark:hover:border-orange-700 cursor-pointer transition-all group flex flex-col justify-between h-full">
          
          <div>
              <div class="flex justify-between items-start mb-4">
                  <div class="w-12 h-12 bg-gray-50 dark:bg-gray-700 rounded-xl flex items-center justify-center text-gray-500 dark:text-gray-400 group-hover:bg-orange-50 dark:group-hover:bg-orange-900/30 group-hover:text-orange-600 dark:group-hover:text-orange-400 transition-colors">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
                      </svg>
                  </div>
                  <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button v-if="activeTab === 'ACTIVE'" @click.stop="archiveActivity(act.id, $event)" class="text-gray-300 hover:text-orange-500 px-2 py-1" title="Archivar Actividad">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
                          </svg>
                      </button>
                      <button v-else @click.stop="openReactivate(act, $event)" class="text-gray-300 hover:text-green-500 px-2 py-1" title="Reactivar Actividad">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                          </svg>
                      </button>
                      
                      <button @click.stop="deleteActivity(act.id)" class="text-gray-300 hover:text-red-500 px-2 py-1" title="Eliminar Permanentemente">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                          </svg>
                      </button>
                  </div>
              </div>
              
              <h2 class="text-[17px] font-extrabold text-gray-900 dark:text-gray-100">{{ act.name }}</h2>
              <span class="inline-block mt-2 px-2.5 py-1 text-[10px] uppercase font-bold tracking-wider rounded-full"
                    :class="act.category === 'PERMANENT' ? 'bg-[#e8f7f5] text-[#1e9d8e]' : 'bg-[#feefe6] text-[#f05100]'">
                 {{ act.category === 'PERMANENT' ? 'Permanente' : 'Eventual' }}
              </span>
              <p v-if="act.category === 'EVENTUAL' && act.deadline_date" class="text-xs text-red-500 font-bold mt-2">
                 Límite: {{ act.deadline_date }}
              </p>
              
              <p class="text-gray-500 text-sm mt-4 line-clamp-3 leading-relaxed">{{ act.description || 'Sin descripción' }}</p>
          </div>

          <div class="mt-6 pt-4 border-t border-gray-100 flex justify-between items-center text-sm font-semibold text-orange-600 group-hover:text-orange-700">
              Ver perfil de actividad
              <span>&rarr;</span>
          </div>
       </div>

       <div v-if="activities.length === 0" class="col-span-full text-center text-gray-500 p-12 bg-white rounded-2xl shadow-sm border border-gray-100">
           No hay actividades creadas. Haz clic en "Nueva Actividad" para comenzar.
       </div>
       <div v-else-if="displayedActivities.length === 0" class="col-span-full text-center text-gray-500 p-12 bg-white rounded-2xl shadow-sm border border-gray-100">
           No hay actividades {{ activeTab === 'ACTIVE' ? 'activas' : 'archivadas' }}.
       </div>
    </div>

    <!-- Activity Form Modal -->
    <div v-if="showForm" class="fixed inset-0 bg-gray-600 bg-opacity-50 dark:bg-gray-900/70 overflow-y-auto h-full w-full z-50 flex justify-center items-center">
        <div class="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100 dark:border-gray-700">
            <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">Crear Actividad</h2>
            <form @submit.prevent="saveActivity" class="space-y-4">
                <div>
                   <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Nombre</label>
                   <input v-model="form.name" required type="text" class="block w-full rounded-xl border-gray-300 dark:border-gray-600 shadow-sm p-3 border bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-orange-500">
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Categoría</label>
                    <select v-model="form.category" required class="block w-full rounded-xl border-gray-300 dark:border-gray-600 shadow-sm p-3 border focus:ring-orange-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                        <option value="PERMANENT">Permanente</option>
                        <option value="EVENTUAL">Eventual</option>
                    </select>
                </div>
                <div v-if="form.category === 'EVENTUAL'">
                   <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Fecha Límite</label>
                   <input v-model="form.deadline_date" required type="date" class="block w-full rounded-xl border-gray-300 dark:border-gray-600 shadow-sm p-3 border bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-orange-500">
                </div>
                <div>
                   <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Descripción</label>
                   <textarea v-model="form.description" rows="3" class="block w-full rounded-xl border-gray-300 dark:border-gray-600 shadow-sm p-3 border bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-orange-500"></textarea>
                </div>
                
                <div class="flex justify-end gap-3 mt-8">
                    <button type="button" @click="showForm = false" class="px-5 py-2.5 font-semibold text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-colors">Cancelar</button>
                    <button type="submit" class="px-5 py-2.5 bg-[#1e9d8e] text-white font-semibold rounded-xl hover:bg-[#1a8b7e] shadow-sm transition-colors">Guardar</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Reactivate Form Modal -->
    <div v-if="showReactivateForm" class="fixed inset-0 bg-gray-600 bg-opacity-50 dark:bg-gray-900/70 overflow-y-auto h-full w-full z-50 flex justify-center items-center">
        <div class="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100 dark:border-gray-700">
            <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">Reactivar Actividad Eventual</h2>
            <form @submit.prevent="submitReactivate" class="space-y-4">
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">Para reactivar esta actividad, debes establecer una nueva fecha límite obligatoria.</p>
                <div>
                   <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Nueva Fecha Límite</label>
                   <input v-model="reactivateForm.deadline_date" required type="date" class="block w-full rounded-xl border-gray-300 dark:border-gray-600 shadow-sm p-3 border bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-orange-500">
                </div>
                <div class="flex justify-end gap-3 mt-8">
                    <button type="button" @click="showReactivateForm = false" class="px-5 py-2.5 font-semibold text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-colors">Cancelar</button>
                    <button type="submit" class="px-5 py-2.5 bg-green-600 text-white font-semibold rounded-xl hover:bg-green-700 shadow-sm transition-colors">Activar</button>
                </div>
            </form>
        </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../plugins/axios'

const router = useRouter()

const activities = ref([])
const showForm = ref(false)
const activeTab = ref('ACTIVE')

const form = ref({
    name: '',
    category: 'PERMANENT',
    deadline_date: '',
    description: ''
})

const displayedActivities = computed(() => {
    const today = new Date();
    today.setHours(0,0,0,0);

    return activities.value.filter(act => {
        let isExpired = false;
        if (act.category === 'EVENTUAL' && act.deadline_date) {
            const parts = act.deadline_date.split('-');
            const deadline = new Date(parts[0], parts[1] - 1, parts[2]);
            if (deadline < today) isExpired = true;
        }

        const isCurrentlyActive = act.is_active && !isExpired;
        return activeTab.value === 'ACTIVE' ? isCurrentlyActive : !isCurrentlyActive;
    })
})

const goToProfile = (id) => {
    router.push(`/activities/${id}`)
}

const fetchActivities = async () => {
    try {
        const res = await apiClient.get('activities/')
        activities.value = res.data
    } catch (e) { console.error(e) }
}

const saveActivity = async () => {
    try {
        const payload = { ...form.value }
        if (payload.category === 'PERMANENT' || !payload.deadline_date) {
            delete payload.deadline_date
        }

        await apiClient.post('activities/', payload)
        showForm.value = false
        form.value = { name: '', category: 'PERMANENT', deadline_date: '', description: '' }
        fetchActivities()
    } catch (e) {
        alert("Error al guardar")
        console.error(e)
    }
}

const deleteActivity = async (id) => {
    if(confirm('¿Seguro que deseas eliminar permanentemente esta actividad? También se borrarán sus eventos.')) {
        await apiClient.delete(`activities/${id}/`)
        fetchActivities()
    }
}

const archiveActivity = async (id, event) => {
    event.stopPropagation();
    if(confirm('¿Seguro que deseas archivar esta actividad? No saldrá en el registro activo.')) {
        await apiClient.patch(`activities/${id}/`, { is_active: false })
        fetchActivities()
    }
}

const showReactivateForm = ref(false)
const reactivateForm = ref({ id: null, deadline_date: '' })

const openReactivate = (act, event) => {
    event.stopPropagation();
    if (act.category === 'EVENTUAL') {
        reactivateForm.value = { id: act.id, deadline_date: '' };
        showReactivateForm.value = true;
    } else {
        reactivateActivity(act.id, { is_active: true });
    }
}

const reactivateActivity = async (id, payload) => {
    try {
        await apiClient.patch(`activities/${id}/`, payload);
        if (showReactivateForm.value) showReactivateForm.value = false;
        fetchActivities();
    } catch (e) {
        alert("Error al reactivar la actividad.");
    }
}

const submitReactivate = () => {
    reactivateActivity(reactivateForm.value.id, { 
        is_active: true, 
        deadline_date: reactivateForm.value.deadline_date 
    })
}

onMounted(() => fetchActivities())
</script>
