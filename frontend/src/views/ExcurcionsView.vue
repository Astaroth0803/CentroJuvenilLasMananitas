<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 space-y-6">
      
      <!-- Back button and title -->
      <div v-if="activeExcursion" class="mb-4">
        <button @click="activeExcursion = null" class="text-orange-600 hover:text-orange-800 flex items-center gap-1 font-medium mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          <span class="hidden sm:inline">Volver</span>
          <span class="sm:hidden">Volver</span>
        </button>
      </div>

      <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 mb-6">
        <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100 break-words max-w-full lg:max-w-[45%]">
          {{ activeExcursion ? `Gestión: ${activeExcursion.nombre}` : 'Eventos Especiales' }}
        </h1>
        
        <div v-if="!activeExcursion">
          <button @click="showCreateModal = true" class="px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 font-medium shadow-sm transition-colors">
            + Nueva Excursión
          </button>
        </div>
      </div>

      <!-- Main LIST View -->
      <div v-if="!activeExcursion" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="exc in excursions" :key="exc.id" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-100 dark:border-gray-700 overflow-hidden flex flex-col">
          <div class="p-6 flex-grow">
            <div class="flex justify-between items-start mb-4">
              <h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 line-clamp-2 leading-tight" :title="exc.nombre">{{ exc.nombre }}</h2>
              <span :class="stateBadgeClass(exc.estado)" class="px-3 py-1 rounded-full text-xs font-bold tracking-wide uppercase shrink-0 ml-2">
                {{ formatState(exc.estado) }}
              </span>
            </div>
            
            <div class="space-y-3 mb-6">
              <div class="flex items-center text-gray-600 dark:text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="text-base font-medium">{{ exc.fecha_evento }}</span>
              </div>
              <div class="flex items-center text-gray-600 dark:text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span class="text-base font-medium">{{ exc.inscritos_count }} Inscritos</span>
              </div>
              <div class="flex items-center text-gray-600 dark:text-gray-400" v-if="exc.edad_min > 0 || exc.edad_max < 99">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-sm font-medium">De {{ exc.edad_min }} a {{ exc.edad_max }} años</span>
              </div>
            </div>
            
            <p v-if="exc.descripcion" class="text-gray-500 text-sm line-clamp-2 mt-4">{{ exc.descripcion }}</p>
          </div>
          
          <div class="px-6 py-4 bg-gray-50 dark:bg-gray-700/50 border-t border-gray-100 dark:border-gray-700">
            <button @click="manageExcursion(exc)" class="w-full flex justify-center items-center py-2.5 px-4 rounded-lg bg-orange-100 text-orange-800 font-bold hover:bg-orange-200 transition-colors text-base shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Gestionar
            </button>
          </div>
        </div>
        
        <!-- Empty State -->
        <div v-if="excursions.length === 0" class="col-span-full bg-white dark:bg-gray-800 p-12 text-center rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9.5a2.5 2.5 0 00-2.5-2.5H15M9 11l3 3m0 0l3-3m-3 3V8" />
          </svg>
          <h3 class="text-xl font-medium text-gray-800 dark:text-gray-100 mb-2">No hay excursiones</h3>
          <p class="text-gray-500 dark:text-gray-400 mb-6 text-base">Crea la primera excursión para empezar a administrar participantes.</p>
          <button @click="showCreateModal = true" class="px-6 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 font-bold shadow-md transition-all duration-200 hover:-translate-y-0.5">
            Crear Primera Excursión
          </button>
        </div>
      </div>

      <!-- DETAIL View -->
      <div v-if="activeExcursion" class="space-y-8 animate-fade-in-up">
        
        <!-- Header Controls & Status -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
          <div class="bg-orange-50/50 dark:bg-orange-900/10 p-6 border-b border-gray-100 dark:border-gray-700">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <p class="text-sm font-bold text-orange-600 uppercase tracking-wider mb-1">Estado General</p>
                <div class="flex items-center gap-3">
                  <span :class="stateBadgeClass(activeExcursion.estado)" class="px-4 py-1.5 rounded-full text-sm font-bold tracking-wide uppercase shadow-sm">
                    {{ formatState(activeExcursion.estado) }}
                  </span>
                </div>
              </div>
              
              <div class="flex flex-wrap gap-3">
                <button v-if="activeExcursion.estado === 'pendiente_registro'" @click="advanceState('registro_cerrado')" class="flex items-center px-5 py-2.5 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 shadow-sm hover:shadow-md transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  Cerrar Registro
                </button>
                <button v-if="activeExcursion.estado === 'registro_cerrado'" @click="advanceState('dia_evento')" class="flex items-center px-5 py-2.5 bg-indigo-600 text-white font-bold rounded-lg hover:bg-indigo-700 shadow-sm hover:shadow-md transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Iniciar Día de Evento
                </button>
                <button v-if="activeExcursion.estado === 'dia_evento'" @click="advanceState('finalizado')" class="flex items-center px-5 py-2.5 bg-gray-800 text-white font-bold rounded-lg hover:bg-gray-900 shadow-sm hover:shadow-md transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Finalizar Excursión
                </button>
                <button v-if="['pendiente_registro', 'registro_cerrado', 'dia_evento'].includes(activeExcursion.estado)" @click="advanceState('cancelado')" class="flex items-center px-4 py-2.5 bg-red-100 text-red-700 font-bold rounded-lg hover:bg-red-200 border border-red-200 transition-all ml-auto">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Cancelar Evento
                </button>
              </div>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 divide-y sm:divide-y-0 sm:divide-x divide-gray-100 dark:divide-gray-700">
            <div class="p-6 flex items-start gap-4">
              <div class="p-3 bg-blue-50 text-blue-600 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Fecha Programada</p>
                <p class="text-lg font-bold text-gray-900 dark:text-gray-100">{{ activeExcursion.fecha_evento }}</p>
              </div>
            </div>
            
            <div class="p-6 flex items-start gap-4">
              <div class="p-3 bg-green-50 text-green-600 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Personas Inscritas</p>
                <p class="text-lg font-bold text-gray-900 dark:text-gray-100">{{ activeExcursion.inscritos_count }} participantes</p>
              </div>
            </div>

            <div class="p-6 flex items-start gap-4">
              <div class="p-3 bg-purple-50 text-purple-600 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Requisitos</p>
                <p class="text-sm font-bold text-gray-900 dark:text-gray-100">Edad: {{ activeExcursion.edad_min }} - {{ activeExcursion.edad_max }} años</p>
                <p class="text-sm text-gray-600 dark:text-gray-400 mt-0.5">Asist. previas necesarias: {{ activeExcursion.min_asistencias }}</p>
              </div>
            </div>
          </div>
          
          <div class="p-6 bg-gray-50 dark:bg-gray-700/30 border-t border-gray-100 dark:border-gray-700" v-if="activeExcursion.descripcion">
            <p class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">Descripción Oficial</p>
            <p class="text-gray-800 dark:text-gray-200 text-base leading-relaxed">{{ activeExcursion.descripcion }}</p>
          </div>
        </div>

        <!-- Add Participant Section (Only in pendiente_registro) -->
        <div v-if="activeExcursion.estado === 'pendiente_registro'" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
          <div class="bg-gray-50 dark:bg-gray-700/50 px-6 py-4 border-b border-gray-100 dark:border-gray-700">
            <h2 class="text-lg font-bold text-gray-800 dark:text-gray-100 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
              Inscribir Nuevos Participantes
            </h2>
          </div>
          <div class="p-6">
            <div class="flex flex-col md:flex-row gap-4">
              <div class="relative flex-grow">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
                  </svg>
                </div>
                <input v-model="userSearchQuery" @input="searchUsers" type="text" placeholder="Escribe el nombre o número de cédula para buscar..." class="block w-full pl-11 pr-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg text-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:bg-white dark:focus:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all shadow-inner">
              </div>
            </div>
            
            <!-- Found Users List -->
            <div v-if="foundUsers.length > 0" class="mt-4 border border-gray-200 rounded-lg divide-y divide-gray-100 overflow-hidden shadow-sm">
              <div v-for="user in foundUsers" :key="user.id" class="p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center hover:bg-orange-50 transition-colors gap-4">
                <div class="flex items-center gap-4">
                  <div class="bg-gray-200 h-10 w-10 rounded-full flex items-center justify-center shrink-0">
                    <span class="text-gray-600 font-bold text-lg">{{ user.first_name.charAt(0) }}</span>
                  </div>
                  <div>
                    <p class="font-bold text-gray-900 text-lg">{{ user.first_name }} {{ user.last_name }}</p>
                    <p class="text-sm text-gray-500 flex items-center gap-2">
                      <span class="font-medium bg-gray-100 px-2 py-0.5 rounded text-gray-700">CI: {{ user.ci }}</span> 
                      <span class="truncate max-w-[200px]" v-if="user.sector">{{ user.sector }}</span>
                    </p>
                  </div>
                </div>
                <button @click="registerParticipant(user.id)" class="w-full sm:w-auto px-5 py-2.5 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 shadow flex items-center justify-center transition-all hover:scale-105" :disabled="isRegistering">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Matricular
                </button>
              </div>
            </div>
            <div v-else-if="userSearchQuery.length > 2" class="bg-yellow-50 text-yellow-800 p-4 rounded-lg mt-4 flex items-center border border-yellow-200">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
               </svg>
               No se encontraron beneficiarios con esa búsqueda, o ya se encuentran matriculados.
            </div>
          </div>
        </div>

        <!-- Participants List -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden w-full">
          <div class="px-6 py-5 bg-gray-50 dark:bg-gray-700/50 border-b border-gray-100 dark:border-gray-700 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              Listado Final de Participantes
            </h2>
            <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
              <button v-if="['registro_cerrado', 'dia_evento', 'finalizado'].includes(activeExcursion.estado) && activeExcursion.registros && activeExcursion.registros.length > 0" @click="exportToExcel" class="w-full sm:w-auto px-4 py-2.5 bg-green-50 text-green-700 border border-green-200 rounded-lg hover:bg-green-100 transition-all font-bold shadow-sm flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Excel
              </button>
              <button v-if="['registro_cerrado', 'dia_evento', 'finalizado'].includes(activeExcursion.estado) && activeExcursion.registros && activeExcursion.registros.length > 0" @click="exportToPDF" class="w-full sm:w-auto px-4 py-2.5 bg-red-50 text-red-700 border border-red-200 rounded-lg hover:bg-red-100 transition-all font-bold shadow-sm flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                PDF
              </button>
              <button v-if="activeExcursion.estado === 'dia_evento'" @click="saveAttendance" class="w-full sm:w-auto px-6 py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all font-bold shadow-md hover:shadow-lg flex items-center justify-center transform hover:-translate-y-0.5" :disabled="isSavingAttendance">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                </svg>
                Guardar Reporte de Asistencia
              </button>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-white dark:bg-gray-800">
                <tr>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Beneficiario</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Registrado el</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Control de Asistencia</th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-100 dark:divide-gray-700">
                <tr v-for="(reg, index) in activeExcursion.registros" :key="reg.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors" :class="{'bg-gray-50/50 dark:bg-gray-700/20': index % 2 === 0}">
                  <td class="px-6 py-4">
                    <div class="flex items-center">
                      <div class="h-10 w-10 shrink-0 bg-orange-100 text-orange-600 rounded-full flex items-center justify-center font-bold text-lg mr-4">
                        {{ reg.beneficiary_details.first_name.charAt(0) }}
                      </div>
                      <div>
                        <div class="font-bold text-gray-900 dark:text-gray-100 text-lg">{{ reg.beneficiary_details.first_name }} {{ reg.beneficiary_details.last_name }}</div>
                        <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mt-0.5">CI: {{ reg.beneficiary_details.ci }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-gray-600 dark:text-gray-400 text-base">
                    {{ new Date(reg.fecha_registro).toLocaleDateString() }} a las {{ new Date(reg.fecha_registro).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}
                  </td>
                  <td class="px-6 py-4">
                    <!-- Day of Event Attendance Controls -->
                    <div v-if="activeExcursion.estado === 'dia_evento'" class="flex items-center gap-6 bg-gray-50 dark:bg-gray-700 p-2 rounded-lg inline-flex border border-gray-100 dark:border-gray-600 shadow-inner">
                         <label class="flex items-center gap-2 cursor-pointer group">
                            <div class="relative flex items-center">
                              <input type="radio" :name="'att_'+reg.usuario" :value="true" v-model="attendanceForm[reg.usuario]" class="peer sr-only">
                              <div class="w-6 h-6 border-2 border-gray-300 rounded-full peer-checked:border-green-600 peer-checked:bg-green-600 transition-all flex items-center justify-center">
                                <svg class="w-4 h-4 text-white opacity-0 peer-checked:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                                </svg>
                              </div>
                            </div>
                            <span class="text-lg font-bold text-gray-600 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-gray-100 peer-checked:text-green-700">Asistió</span>
                         </label>
                         
                         <label class="flex items-center gap-2 cursor-pointer group">
                            <div class="relative flex items-center">
                              <input type="radio" :name="'att_'+reg.usuario" :value="false" v-model="attendanceForm[reg.usuario]" class="peer sr-only">
                              <div class="w-6 h-6 border-2 border-gray-300 rounded-full peer-checked:border-red-600 peer-checked:bg-red-600 transition-all flex items-center justify-center">
                                <svg class="w-4 h-4 text-white opacity-0 peer-checked:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                              </div>
                            </div>
                            <span class="text-lg font-bold text-gray-600 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-gray-100 peer-checked:text-red-700">Faltó</span>
                         </label>
                    </div>
                    <!-- Finished Status Output -->
                    <div v-else class="flex">
                      <span v-if="reg.asistio === true" class="inline-flex items-center px-3 py-1 rounded-full text-base font-bold bg-green-100 text-green-800">
                        <svg class="mr-1.5 h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                        Estuvo Presente
                      </span>
                      <span v-else-if="reg.asistio === false" class="inline-flex items-center px-3 py-1 rounded-full text-base font-bold bg-red-100 text-red-800">
                        <svg class="mr-1.5 h-4 w-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                        </svg>
                        Marcó Falta
                      </span>
                      <span v-else class="inline-flex items-center px-3 py-1 rounded-full text-base font-medium bg-gray-100 text-gray-500">
                        <svg class="mr-1.5 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Aún Pendiente
                      </span>
                    </div>
                  </td>
                </tr>
                <tr v-if="!activeExcursion.registros || activeExcursion.registros.length === 0">
                  <td colspan="3" class="px-6 py-12 text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-300 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                    <p class="text-lg font-medium text-gray-500 dark:text-gray-400">Aún no hay personas inscritas.</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Create Modal -->
      <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition ease-in duration-150" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
        <div v-if="showCreateModal" class="fixed inset-0 flex items-center justify-center p-4 z-50">
          <div class="absolute inset-0 bg-gray-900 bg-opacity-60 backdrop-blur-sm" @click="showCreateModal = false"></div>
          
          <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden relative z-10 flex flex-col max-h-[90vh]">
            <div class="px-8 py-6 border-b border-gray-100 bg-gray-50/80">
              <h3 class="text-2xl font-bold text-gray-900 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-3 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Agendando Evento Nuevo
              </h3>
            </div>
            
            <div class="p-8 space-y-5 overflow-y-auto">
              <div class="bg-blue-50 text-blue-800 p-4 rounded-lg flex items-start text-sm border border-blue-100 mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p>Complete los datos para generar el evento. Podrá inscribir usuarios una vez lo haya guardado.</p>
              </div>
              
              <div>
                <label class="block text-base font-bold text-gray-700 mb-2">Título de la Excursión o Evento</label>
                <input v-model="form.nombre" type="text" placeholder="Ej: Visita al Museo Nacional" class="w-full text-lg border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-500 focus:border-orange-500 px-4 py-3 border transition-all">
              </div>
              <div>
                <label class="block text-base font-bold text-gray-700 mb-2">Descripción General (Opcional)</label>
                <textarea v-model="form.descripcion" rows="2" placeholder="Información útil sobre la excursión..." class="w-full text-base border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-500 focus:border-orange-500 px-4 py-3 border transition-all"></textarea>
              </div>
              <div>
                <label class="block text-base font-bold text-gray-700 mb-2">Fecha Programada</label>
                <input v-model="form.fecha_evento" type="date" class="w-full text-lg border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-500 focus:border-orange-500 px-4 py-3 border transition-all">
              </div>
              
              <div class="pt-4 mt-2 border-t border-gray-100">
                <h4 class="font-bold text-gray-800 mb-4 text-lg">Reglas y Requisitos para Participar</h4>
                <div class="grid grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-bold text-gray-700 mb-2">Edad Mínima permitida</label>
                    <div class="relative">
                      <input v-model="form.edad_min" type="number" class="w-full text-lg border-gray-300 rounded-lg shadow-sm focus:ring-orange-500 focus:border-orange-500 px-4 py-3 border">
                      <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-500">años</div>
                    </div>
                  </div>
                  <div>
                    <label class="block text-sm font-bold text-gray-700 mb-2">Edad Máxima permitida</label>
                    <div class="relative">
                      <input v-model="form.edad_max" type="number" class="w-full text-lg border-gray-300 rounded-lg shadow-sm focus:ring-orange-500 focus:border-orange-500 px-4 py-3 border">
                      <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-500">años</div>
                    </div>
                  </div>
                </div>
                <div class="mt-5">
                  <label class="block text-sm font-bold text-gray-700 mb-2">Asistencias obligatorias previas (0 = Ninguna)</label>
                  <input v-model="form.min_asistencias" type="number" class="w-full text-lg border-gray-300 rounded-lg shadow-sm focus:ring-orange-500 focus:border-orange-500 px-4 py-3 border">
                </div>
              </div>
            </div>
            
            <div class="px-8 py-5 bg-gray-50 border-t border-gray-100 flex justify-end gap-3 rounded-b-2xl">
              <button @click="showCreateModal = false" class="px-6 py-3 text-base font-bold text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 shadow-sm transition-colors">Cerrar y Cancelar</button>
              <button @click="saveExcursion" class="px-8 py-3 text-base font-bold text-white bg-orange-600 border border-transparent rounded-lg hover:bg-orange-700 shadow-md transition-all flex items-center transform hover:-translate-y-0.5" :disabled="isSaving">
                <svg v-if="isSaving" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Guardar Excursión
              </button>
            </div>
          </div>
        </div>
      </transition>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import apiClient from '../plugins/axios'
import * as XLSX from 'xlsx'
import jsPDF from 'jspdf'
import 'jspdf-autotable'

const excursions = ref([])
const activeExcursion = ref(null)
const showCreateModal = ref(false)
const isSaving = ref(false)
const isRegistering = ref(false)
const isSavingAttendance = ref(false)

const form = ref({
    nombre: '',
    descripcion: '',
    fecha_evento: '',
    edad_min: 0,
    edad_max: 99,
    min_asistencias: 0
})

const userSearchQuery = ref('')
const foundUsers = ref([])

// Map to hold temporary attendance marker selections locally before submit
// key: string (usuario_id), value: bool
const attendanceForm = reactive({})

const fetchExcursions = async () => {
    try {
        const res = await apiClient.get('excursions/')
        excursions.value = res.data
    } catch (e) { console.error(e) }
}

const saveExcursion = async () => {
    isSaving.value = true
    try {
        await apiClient.post('excursions/', form.value)
        showCreateModal.value = false
        form.value = { nombre: '', descripcion: '', fecha_evento: '', edad_min: 0, edad_max: 99, min_asistencias: 0 }
        await fetchExcursions()
    } catch (e) {
        alert("Error al crear la excursión.")
        console.error(e)
    } finally {
        isSaving.value = false
    }
}

const manageExcursion = async (exc) => {
    // Fetch full details (although our queryset already brings everything, a refresh is good)
    try {
        const res = await apiClient.get(`excursions/${exc.id}/`)
        activeExcursion.value = res.data
        // prep attendance form state
        if (res.data.estado === 'dia_evento') {
           res.data.registros.forEach(r => {
              if (r.asistio !== null) {
                  attendanceForm[r.usuario] = r.asistio
              }
           })
        }
    } catch (e) {
        console.error(e)
    }
}

const searchTimer = ref(null)
const searchUsers = () => {
    clearTimeout(searchTimer.value)
    if (userSearchQuery.value.length < 3) {
        foundUsers.value = []
        return
    }
    searchTimer.value = setTimeout(async () => {
        try {
            // Reusing existing beneficiaries endpoint to search users
            const res = await apiClient.get(`beneficiaries/`)
            const q = userSearchQuery.value.toLowerCase()
            const allUsers = res.data
            // Filter locally:
            const filtered = allUsers.filter(u => {
                const name = `${u.first_name} ${u.last_name}`.toLowerCase()
                const ci = (u.ci || '').toLowerCase()
                return name.includes(q) || ci.includes(q)
            })
            // Filter out existing participants
            const existingIds = activeExcursion.value.registros.map(r => r.usuario)
            foundUsers.value = filtered.filter(u => !existingIds.includes(u.id)).slice(0, 10)
        } catch (e) {
            console.error(e)
        }
    }, 400)
}

const registerParticipant = async (userId) => {
    isRegistering.value = true
    try {
        await apiClient.post(`excursions/${activeExcursion.value.id}/register/`, {
            usuario_id: userId
        })
        userSearchQuery.value = ''
        foundUsers.value = []
        alert("Participante registrado de forma exitosa.")
        await manageExcursion(activeExcursion.value) // refresh
    } catch (e) {
        alert(e.response?.data?.detail || "Error al registrar participante. Verifica las validaciones de edad, inasistencias previas o límite de edad.")
    } finally {
        isRegistering.value = false
    }
}

const advanceState = async (newState) => {
    if (newState === 'registro_cerrado' || newState === 'dia_evento') {
        if (!activeExcursion.value.registros || activeExcursion.value.registros.length < 2) {
            alert("Atención: No se puede cambiar el estado. Se requieren al menos 2 participantes registrados.");
            return;
        }
    }

    if (!confirm(`¿Actualizar estado a: ${formatState(newState)}?`)) return
    
    try {
        await apiClient.post(`excursions/${activeExcursion.value.id}/change-state/`, {
            estado: newState
        })
        await manageExcursion(activeExcursion.value)
        await fetchExcursions()
    } catch (e) {
        alert(e.response?.data?.detail || "Error al actualizar estado.")
    }
}

const saveAttendance = async () => {
    isSavingAttendance.value = true
    try {
        await apiClient.post(`excursions/${activeExcursion.value.id}/attendance/`, {
            attendance: attendanceForm
        })
        alert("Asistencia guardada con éxito.")
        await manageExcursion(activeExcursion.value)
    } catch (e) {
        alert(e.response?.data?.detail || "Error al guardar la asistencia.")
    } finally {
        isSavingAttendance.value = false
    }
}

const formatState = (state) => {
    const map = {
        'pendiente_registro': 'Pendiente',
        'registro_cerrado': 'Registro Cerrado',
        'dia_evento': 'Día del Evento',
        'finalizado': 'Finalizado',
        'cancelado': 'Cancelado'
    }
    return map[state] || state
}

const stateBadgeClass = (state) => {
    if (state === 'pendiente_registro') return 'bg-yellow-100 text-yellow-800'
    if (state === 'registro_cerrado') return 'bg-blue-100 text-blue-800'
    if (state === 'dia_evento') return 'bg-indigo-100 text-indigo-800'
    if (state === 'finalizado') return 'bg-gray-200 text-gray-800'
    if (state === 'cancelado') return 'bg-red-100 text-red-800'
    return 'bg-gray-100 text-gray-800'
}

// Configuración de exportación
const getExportData = () => {
    return activeExcursion.value.registros.map((r, i) => {
        let asistenciaStr = "Pendiente";
        if (r.asistio === true) asistenciaStr = "Presente";
        if (r.asistio === false) asistenciaStr = "Ausente";

        return {
            'N°': i + 1,
            'Cédula de Identidad': r.beneficiary_details.ci,
            'Nombre Completo': `${r.beneficiary_details.first_name} ${r.beneficiary_details.last_name}`,
            'Fecha de Registro': new Date(r.fecha_registro).toLocaleString(),
            'Estado de Asistencia': asistenciaStr
        }
    });
}

const getReportFilename = (extension) => {
    const rawName = activeExcursion.value.nombre.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const date = new Date().toISOString().split('T')[0];
    return `excursion_${rawName}_${date}.${extension}`;
}

const exportToExcel = () => {
    const data = getExportData();
    const worksheet = XLSX.utils.json_to_sheet(data);

    // Dar estilo negrita a la primera fila (Cabeceras)
    const range = XLSX.utils.decode_range(worksheet['!ref']);
    for (let current_col = range.s.c; current_col <= range.e.c; current_col++) {
        const address = XLSX.utils.encode_cell({r: 0, c: current_col});
        if (!worksheet[address]) continue;
        worksheet[address].s = { font: { bold: true } }; // Required xlsx-style or pro version for native styles, but usually standard export is fine.
    }

    // Auto-adjust column widths
    const colWidths = [
      { wch: 5 },  // N°
      { wch: 15 }, // CI
      { wch: 35 }, // Nombre
      { wch: 25 }, // Fecha Reg
      { wch: 20 }  // Asistencia
    ];
    worksheet['!cols'] = colWidths;

    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Asistentes");
    XLSX.writeFile(workbook, getReportFilename('xlsx'));
}

const exportToPDF = () => {
    const doc = new jsPDF()
    const data = getExportData();
    
    // Header
    doc.setFontSize(18);
    doc.text("Listado Final de Participantes", 14, 22);
    
    doc.setFontSize(11);
    doc.setTextColor(100);
    doc.text(`Excursión: ${activeExcursion.value.nombre}`, 14, 30);
    doc.text(`Fecha del Evento: ${activeExcursion.value.fecha_evento}`, 14, 36);
    doc.text(`Estado: ${formatState(activeExcursion.value.estado)}`, 14, 42);
    doc.text(`Total Inscritos: ${activeExcursion.value.inscritos_count}`, 14, 48);

    const tableColumn = ["N°", "Cédula", "Nombre Completo", "Fecha de Registro", "Asistencia"];
    const tableRows = data.map(row => [
        row['N°'],
        row['Cédula de Identidad'],
        row['Nombre Completo'],
        row['Fecha de Registro'],
        row['Estado de Asistencia']
    ]);

    doc.autoTable({
        head: [tableColumn],
        body: tableRows,
        startY: 55,
        theme: 'striped',
        headStyles: { fillColor: [234, 88, 12] } // Orange 600 color to match app theme
    });

    doc.save(getReportFilename('pdf'));
}

onMounted(() => {
    fetchExcursions()
})
</script>

<style scoped>
/* Custom animations that Tailwind might not have out-of-the-box in this specific setup */
.animate-fade-in-up {
  animation: fadeInUp 0.4s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
