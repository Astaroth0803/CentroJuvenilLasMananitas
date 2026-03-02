<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">

    <!-- Main Content -->
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 space-y-8">

      <!-- Loading State -->
      <div v-if="loading" class="text-center p-12 text-gray-500 dark:text-gray-400">
          Cargando estadísticas...
      </div>

      <template v-else>
          <!-- Stats Grid -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm flex items-center justify-between border-l-4 border-orange-500 transition-colors">
                <div>
                    <p class="text-gray-500 dark:text-gray-400 text-sm font-medium">Asistencias Hoy</p>
                    <p class="text-3xl font-bold text-gray-900 dark:text-gray-100"><AnimatedCounter :value="stats.attendances_today" /></p>
                </div>
                <div class="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 rounded-full flex items-center justify-center text-xl">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
                </div>
            </div>
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm flex items-center justify-between border-l-4 border-blue-500 transition-colors">
                <div>
                    <p class="text-gray-500 dark:text-gray-400 text-sm font-medium">Usuarios Activos</p>
                    <p class="text-3xl font-bold text-gray-900 dark:text-gray-100"><AnimatedCounter :value="stats.active_users" /></p>
                </div>
                <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center text-xl">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                </div>
            </div>
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm flex items-center justify-between border-l-4 border-green-500 transition-colors">
                <div>
                    <p class="text-gray-500 dark:text-gray-400 text-sm font-medium">Actividad Principal</p>
                    <p class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ stats.top_activity_name }}</p>
                </div>
                <div class="w-12 h-12 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-full flex items-center justify-center text-xl">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z" /></svg>
                </div>
            </div>
          </div>

          <!-- Bottom Section: Chart and Top Users -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
            
            <!-- Charts Area -->
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm flex-1 transition-colors">
              <h3 class="text-lg font-bold text-gray-800 dark:text-gray-100 mb-4">Asistencia Anual</h3>
              <transition name="fade-slide" appear>
                <div v-show="!loading">
                  <apexchart type="area" height="320" :options="chartOptions" :series="chartSeries"></apexchart>
                </div>
              </transition>
            </div>

            <!-- Top 5 Attendees Table -->
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm flex-1 transition-colors">
              <h3 class="text-lg font-bold text-gray-800 dark:text-gray-100 mb-4">Top 5 Usuarios Destacados</h3>
              <transition name="fade-slide" appear>
              <div v-show="!loading" class="overflow-x-auto rounded-lg border border-gray-100 dark:border-gray-700">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead class="bg-gray-50 dark:bg-gray-700/50">
                    <tr>
                      <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Nombre</th>
                      <th class="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Cédula</th>
                      <th class="px-4 py-3 text-center text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Asistencias</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    <tr v-for="(user, index) in stats.top_attendees" :key="user.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                      <td class="px-4 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                          <span class="w-6 h-6 rounded-full flex items-center justify-center bg-gray-100 dark:bg-gray-600 text-gray-500 dark:text-gray-300 font-bold text-xs mr-3">
                              {{ index + 1 }}
                          </span>
                          <span class="font-medium text-gray-900 dark:text-gray-100">{{ user.name }}</span>
                        </div>
                      </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ user.ci }}</td>
                      <td class="px-4 py-4 whitespace-nowrap text-center">
                        <span class="px-2.5 py-1 bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300 text-xs font-bold rounded-full">
                          {{ user.attendance_count }}
                        </span>
                      </td>
                    </tr>
                    <tr v-if="!stats.top_attendees || stats.top_attendees.length === 0">
                      <td colspan="3" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400 text-sm">
                        Aún no hay suficientes asistencias registradas.
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              </transition>
            </div>

          </div>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../plugins/axios'
import AnimatedCounter from '../components/AnimatedCounter.vue'

const loading = ref(true)
const stats = ref({
    attendances_today: 0,
    active_users: 0,
    top_activity_name: 'N/A',
    chart_data: [],
    top_attendees: []
})

const chartOptions = ref({
    chart: { type: 'area', toolbar: { show: false } },
    colors: ['#ea580c', '#6366f1', '#eab308'], // Naranja, Indigo, Amarillo
    stroke: { curve: 'smooth', width: 3 },
    markers: { size: 4 },
    dataLabels: { enabled: false },
    xaxis: {
      categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
      labels: {
        style: {
          colors: Array(12).fill('#9ca3af'), // gray-400 - light enough for dark mode
          fontSize: '11px',
        }
      }
    },
    yaxis: {
      labels: {
        style: {
          colors: ['#9ca3af'], // gray-400
        }
      }
    },
    grid: { borderColor: '#374151' }, // gray-700 - works in dark
    tooltip: { y: { formatter: val => `${val} asistencias` } },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.4,
            opacityTo: 0.05,
            stops: [0, 90, 100]
        }
    }
})

const chartSeries = ref([{ name: 'Asistencias', data: [] }])

const fetchStats = async () => {
    try {
        const res = await apiClient.get('dashboard-stats/')
        stats.value = res.data
        if (res.data.chart_data) {
            chartSeries.value = res.data.chart_data
        }
    } catch (e) {
        console.error("Error fetching stats:", e)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchStats()
})
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
