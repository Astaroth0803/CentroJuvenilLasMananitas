<template>
  <div class="flex min-h-screen bg-gray-50">

    <!-- Mobile Sidebar Backdrop -->
    <div v-show="isSidebarOpen" @click="isSidebarOpen = false" class="fixed inset-0 bg-gray-900/50 z-40 md:hidden transition-opacity"></div>

    <!-- Sidebar -->
    <aside :class="['fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-100 shadow-xl md:shadow-sm flex flex-col transition-transform duration-300 md:relative md:translate-x-0', isSidebarOpen ? 'translate-x-0' : '-translate-x-full']">

      <!-- Logo / Brand -->
      <div class="flex items-center gap-3 px-5 py-5 border-b border-gray-100">
        <img src="/logo.png" alt="Logo CJLM" class="h-10 w-auto object-contain shrink-0" />
        <div class="leading-tight">
          <p class="text-sm font-extrabold text-gray-800 tracking-tight leading-none">Centro Juvenil</p>
          <p class="text-sm font-extrabold text-orange-600 tracking-tight leading-none">y Biblioteca</p>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-3 py-5 space-y-1 overflow-y-auto">

        <!-- Main nav label -->
        <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-3 mb-3">Menú Principal</p>

        <router-link to="/dashboard" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Dashboard icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Panel
        </router-link>

        <router-link to="/beneficiaries" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Users icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          Usuarios
        </router-link>

        <router-link to="/activities" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Activities icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z" />
          </svg>
          Actividades
        </router-link>

        <router-link to="/reports" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Reports icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Reportes
        </router-link>

        <router-link to="/admins" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Admin icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Admin
        </router-link>

        <!-- Divider -->
        <div class="pt-4 pb-2">
          <div class="border-t border-gray-100"></div>
        </div>

        <!-- CTA: Register Attendance -->
        <router-link to="/attendance" class="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-orange-600 text-white font-semibold text-sm hover:bg-orange-700 transition-all shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
          Registrar Asistencia
        </router-link>
      </nav>

      <!-- Bottom: Logout -->
      <div class="px-3 py-4 border-t border-gray-100">
        <button @click="logout" class="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-gray-500 hover:bg-red-50 hover:text-red-600 font-semibold text-sm transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Salir
        </button>
      </div>
    </aside>

    <!-- Main content area -->
    <main class="flex-1 min-w-0 overflow-y-auto flex flex-col">

      <!-- Topbar -->
      <header class="sticky top-0 z-10 bg-white border-b border-gray-100 shadow-sm px-6 py-3 flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3">
          <!-- Mobile menu button -->
          <button @click="isSidebarOpen = true" class="md:hidden p-2 -ml-2 text-gray-500 rounded-md hover:bg-gray-100 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <!-- Page title -->
          <h2 class="text-base font-bold text-gray-700 tracking-tight">{{ pageTitle }}</h2>
        </div>

        <!-- Right: date + avatar -->
        <div class="flex items-center gap-4">
          <span class="text-sm text-gray-400 hidden sm:block">{{ currentDate }}</span>
          <!-- Profile avatar -->
          <div class="flex items-center gap-2 cursor-pointer group">
            <div class="w-8 h-8 rounded-full bg-orange-100 border-2 border-orange-200 flex items-center justify-center shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-orange-600" viewBox="0 0 24 24" fill="currentColor">
                <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 1 1 9 0 4.5 4.5 0 0 1-9 0ZM3.751 20.105a8.25 8.25 0 0 1 16.498 0 .75.75 0 0 1-.437.695A18.683 18.683 0 0 1 12 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 0 1-.437-.695Z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="text-sm font-semibold text-gray-600 hidden sm:block">Admin</span>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <div class="flex-1">
        <router-view />
      </div>
    </main>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const isSidebarOpen = ref(false)

watch(() => route.path, () => {
    isSidebarOpen.value = false
})

const pageTitles = {
  Dashboard: 'Panel de Control',
  Beneficiaries: 'Manejo de Usuarios',
  Activities: 'Manejo de Actividades',
  BeneficiaryProfile: 'Perfil de Usuario',
  ActivityProfile: 'Perfil de Actividad',
  Reports: 'Reportes',
  Admins: 'Administradores',
}

const pageTitle = computed(() => pageTitles[route.name] ?? 'CJLM')

const currentDate = computed(() => {
  return new Date().toLocaleDateString('es-PA', { weekday: 'long', day: 'numeric', month: 'long' })
})

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
}
</script>

<style scoped>
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563; /* gray-600 */
  transition: background-color 0.15s, color 0.15s;
}

.sidebar-link:hover {
  background-color: #fff7ed; /* orange-50 */
  color: #ea580c; /* orange-600 */
}

.sidebar-link-active {
  background-color: #fff7ed !important;
  color: #ea580c !important;
  font-weight: 700;
}

.sidebar-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}
</style>
