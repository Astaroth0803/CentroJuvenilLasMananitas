<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">

    <!-- Main Content -->
    <div class="max-w-[1200px] mx-auto p-6 md:p-8 space-y-6">
      <div class="flex justify-between items-center mb-6">
        <div>
          <router-link to="/activities" class="text-[13px] font-medium text-[#8e98a8] hover:text-[#f05100] mb-2 inline-flex items-center transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 mr-1">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
              </svg>
              Volver a Actividades
          </router-link>
          <h1 class="text-[28px] font-extrabold text-gray-900 dark:text-gray-100 tracking-tight">Perfil de Actividad</h1>
        </div>
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-500 dark:text-gray-400">
        Cargando perfil...
      </div>

      <div v-else-if="profile" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Left Column: Activity Details -->
        <div class="col-span-1 space-y-6">
            <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden pb-4">
                <div class="bg-[#1e9d8e] h-24 relative">
                    <!-- Image upload trigger: click on the banner or the avatar -->
                    <input ref="imageInput" type="file" accept="image/*" class="hidden" @change="onImageSelected" />
                </div>
                <div class="px-6 relative">
                    <!-- Avatar: shows image or default icon, click to upload -->
                    <div
                      @click="imageInput?.click()"
                      class="w-20 h-20 rounded-2xl bg-white dark:bg-gray-700 shadow-sm mx-auto -mt-10 flex items-center justify-center overflow-hidden border-4 border-white dark:border-gray-800 cursor-pointer group relative"
                      title="Haz clic para cambiar la imagen"
                    >
                      <!-- Uploaded image -->
                      <img v-if="profile.image" :src="profile.image" alt="Imagen de actividad" class="w-full h-full object-cover" />
                      <!-- Default icon -->
                      <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-10 h-10 text-[#1e9d8e]">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 17.25v1.007a3 3 0 0 1-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0 1 15 18.257V17.25m6-12V15a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 15V5.25m18 0A2.25 2.25 0 0 0 18.75 3H5.25A2.25 2.25 0 0 0 3 5.25m18 0V12a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 12V5.25" />
                      </svg>
                      <!-- Hover overlay -->
                      <div class="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity rounded-xl">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M12 9a3.75 3.75 0 1 0 0 7.5A3.75 3.75 0 0 0 12 9Z" />
                          <path fill-rule="evenodd" d="M9.344 3.071a49.52 49.52 0 0 1 5.312 0c.967.052 1.83.586 2.332 1.39l.821 1.317c.24.383.645.643 1.11.71.386.054.77.113 1.152.177 1.432.239 2.429 1.493 2.429 2.909V18a3 3 0 0 1-3 3h-15a3 3 0 0 1-3-3V9.574c0-1.416.997-2.67 2.429-2.909.382-.064.766-.123 1.151-.178a1.56 1.56 0 0 0 1.11-.71l.822-1.315a2.942 2.942 0 0 1 2.332-1.39ZM6.75 12.75a5.25 5.25 0 1 1 10.5 0 5.25 5.25 0 0 1-10.5 0Zm12-1.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z" clip-rule="evenodd" />
                        </svg>
                      </div>
                    </div>
                    <h2 class="text-2xl font-extrabold text-center text-gray-900 dark:text-gray-100 mt-4 tracking-tight">{{ profile.name }}</h2>
                    <div class="flex justify-center flex-wrap gap-2 mt-2 mb-6 items-center">
                        <span class="inline-block px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wider" 
                              :class="profile.category === 'PERMANENT' ? 'bg-[#e8f7f5] text-[#1e9d8e]' : 'bg-[#feefe6] text-[#f05100]'">
                            {{ profile.category === 'PERMANENT' ? 'Permanente' : 'Eventual' }}
                        </span>
                        
                        <span v-if="profile.category === 'EVENTUAL' && profile.deadline_date" 
                              class="text-xs font-bold text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full">
                           Límite: {{ profile.deadline_date }}
                        </span>
                        
                        <span v-if="!profile.is_active" class="inline-block px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wider bg-red-100 text-red-600">
                            ARCHIVADA
                        </span>
                    </div>
                    
                    <div class="space-y-4 px-2">
                        <div class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed text-center mb-6">
                            {{ profile.description || 'Sin descripción disponible para esta actividad.' }}
                        </div>

                        <div class="bg-gradient-to-br from-[#2ab1a6] to-[#259b91] rounded-2xl shadow-sm p-5 text-white flex items-center justify-between">
                            <div>
                                <p class="text-[#b1e8e3] text-xs font-bold uppercase tracking-wider mb-1">Total Asistencias</p>
                                <h3 class="text-3xl font-extrabold">{{ profile.total_attendance }}</h3>
                            </div>
                            <div class="p-2 bg-white/20 rounded-xl">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-6 text-white">
                                   <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Right Column: Events & Breakdown -->
        <div class="col-span-1 md:col-span-2 space-y-6">
            
            <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6 relative">
                <div class="flex items-center justify-between mb-6">
                    <h3 class="text-[17px] font-extrabold text-gray-900 dark:text-gray-100 flex items-center gap-2">
                        Eventos Asociados
                        <span class="text-[10px] py-1 px-2.5 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 rounded-full font-bold uppercase tracking-wider">{{ profile.events.length }}</span>
                    </h3>
                    <button @click="openEventForm" class="text-sm font-bold text-orange-600 dark:text-orange-400 hover:text-orange-700 bg-orange-50 dark:bg-orange-900/20 px-3 py-1.5 rounded-lg transition-colors">
                        + Agregar Evento
                    </button>
                </div>
                
                <div v-if="profile.events.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div v-for="ev in profile.events" :key="ev.id" class="flex flex-col justify-between bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl p-4 hover:shadow-md transition-shadow relative group">
                        <button @click="deleteEvent(ev.id)" class="absolute top-2 right-2 text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity" title="Eliminar evento">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                            </svg>
                        </button>
                        <div>
                            <h4 class="font-extrabold text-gray-900 dark:text-gray-100 pr-6">{{ ev.name }}</h4>
                            <p class="text-xs font-semibold text-gray-400 dark:text-gray-500 mt-0.5">{{ ev.date || 'Evento general' }}</p>
                        </div>
                        <div class="mt-4 flex items-center justify-between border-t border-gray-100 dark:border-gray-600 pt-3">
                            <span class="text-xs text-gray-500 dark:text-gray-400 font-medium uppercase tracking-wide">Asistencias</span>
                            <div class="inline-flex items-center gap-1.5 bg-[#e8f7f5] text-[#1e9d8e] px-3.5 py-1 rounded-full font-extrabold text-sm">
                                {{ ev.attendance_count }}
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="text-center py-12 text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/30 rounded-xl border border-dashed border-gray-200 dark:border-gray-600">
                    Aún no hay eventos registrados para esta actividad.
                </div>
            </div>

        </div>
      </div>
    </div>

    <!-- Event Form Modal -->
    <div v-if="showEventForm" class="fixed inset-0 bg-gray-600 bg-opacity-50 dark:bg-gray-900/70 overflow-y-auto h-full w-full z-50 flex justify-center items-center">
        <div class="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100 dark:border-gray-700">
            <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">Crear Evento</h2>
            <form @submit.prevent="saveEvent" class="space-y-4">
                <div>
                   <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Nombre del Evento</label>
                   <input v-model="eventForm.name" required type="text" placeholder="Ej: -default- o Torneo" class="block w-full rounded-xl border-gray-300 dark:border-gray-600 shadow-sm p-3 border bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-orange-500 focus:border-orange-500">
                </div>
                <div>
                   <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Fecha (Opcional)</label>
                   <input v-model="eventForm.date" type="date" class="block w-full rounded-xl border-gray-300 dark:border-gray-600 shadow-sm p-3 border bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-orange-500 focus:border-orange-500">
                </div>
                
                <div class="flex justify-end gap-3 mt-8">
                    <button type="button" @click="showEventForm = false" class="px-5 py-2.5 font-semibold text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-colors">Cancelar</button>
                    <button type="submit" class="px-5 py-2.5 bg-orange-600 font-semibold text-white rounded-xl hover:bg-orange-700 shadow-sm transition-colors">Guardar Evento</button>
                </div>
            </form>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '../plugins/axios'

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const profile = ref(null)
const showEventForm = ref(false)
const imageInput = ref(null)

const activityId = route.params.id

const eventForm = ref({
    activity: activityId,
    name: '-default-',
    date: ''
})

const fetchProfile = async () => {
    try {
        const res = await apiClient.get(`reports/activity-profile/${activityId}/`)
        profile.value = res.data
    } catch (e) {
        console.error("Error fetching activity profile", e)
        alert("Actividad no encontrada")
        router.push('/activities')
    } finally {
        loading.value = false
    }
}

const openEventForm = () => {
    eventForm.value.name = '-default-'
    eventForm.value.date = ''
    showEventForm.value = true
}

const saveEvent = async () => {
    try {
        const payload = { ...eventForm.value };
        if (!payload.date) delete payload.date; // DRF fails if empty string is sent as Date

        await apiClient.post('events/', payload)
        showEventForm.value = false
        fetchProfile() // refresh the profile to show the new event
    } catch (e) {
        alert("Error al guardar el evento")
        console.error(e)
    }
}

const deleteEvent = async (id) => {
    if(confirm('¿Seguro que deseas eliminar este evento? También se borrará su historial de asistencia.')) {
        try {
            await apiClient.delete(`events/${id}/`)
            fetchProfile()
        } catch (e) {
            console.error(e)
            alert("Error al eliminar el evento.")
        }
    }
}

const onImageSelected = (e) => {
    const file = e.target.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = async (evt) => {
        const base64 = evt.target.result
        try {
            await apiClient.patch(`activities/${activityId}/`, { image: base64 })
            profile.value.image = base64
        } catch (err) {
            alert('Error al guardar la imagen.')
            console.error(err)
        }
    }
    reader.readAsDataURL(file)
}

onMounted(() => {
    fetchProfile()
})
</script>
