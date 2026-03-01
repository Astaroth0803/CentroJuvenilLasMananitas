<template>
  <div class="min-h-screen bg-gray-50">

    <!-- Main Content -->
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 space-y-6">

     <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
       <h1 class="text-3xl font-bold text-gray-800">Manejo de Usuarios</h1>
       <div class="flex flex-col sm:flex-row w-full sm:w-auto gap-3">
          <div class="relative w-full sm:w-64">
             <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
                </svg>
             </div>
             <input v-model="searchQuery" type="text" placeholder="Buscar por nombre o cédula..." class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-orange-500 focus:border-orange-500 sm:text-sm shadow-sm transition-colors">
          </div>
          <div class="flex gap-2">
            <button @click="exportToExcel" :disabled="!filteredAndSortedBeneficiaries.length" class="flex flex-row items-center justify-center gap-2 px-4 py-2 bg-green-50 text-green-700 rounded-md hover:bg-green-100 font-medium disabled:opacity-50 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m5.231 13.481L15 17.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Zm3.75 11.625a1.125 1.125 0 1 1-2.25 0 1.125 1.125 0 0 1 2.25 0Zm-8.25 4.125c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v.75c0 .621-.504 1.125-1.125 1.125H6.375a1.125 1.125 0 0 1-1.125-1.125v-.75Z" />
                </svg>
                Excel
            </button>
            <button @click="exportToPDF" :disabled="!filteredAndSortedBeneficiaries.length" class="flex flex-row items-center justify-center gap-2 px-4 py-2 bg-red-50 text-red-600 rounded-md hover:bg-red-100 font-medium disabled:opacity-50 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>
                PDF
            </button>
          </div>
       </div>
     </div>

    <!-- Active List -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th @click="sortBy('first_name')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 group select-none">
                <div class="flex items-center gap-1">
                    Nombre Completo
                    <span v-if="sortKey === 'first_name'" class="text-orange-500">{{ sortOrder === 1 ? '↑' : '↓' }}</span>
                    <span v-else class="text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity">↕</span>
                </div>
            </th>
            <th @click="sortBy('ci')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 group select-none">
                <div class="flex items-center gap-1">
                    Cédula
                    <span v-if="sortKey === 'ci'" class="text-orange-500">{{ sortOrder === 1 ? '↑' : '↓' }}</span>
                    <span v-else class="text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity">↕</span>
                </div>
            </th>
            <th @click="sortBy('sector')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 group select-none">
                <div class="flex items-center gap-1">
                    Sector
                    <span v-if="sortKey === 'sector'" class="text-orange-500">{{ sortOrder === 1 ? '↑' : '↓' }}</span>
                    <span v-else class="text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity">↕</span>
                </div>
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="b in filteredAndSortedBeneficiaries" :key="b.id">
            <td class="px-6 py-4 whitespace-nowrap">{{ b.first_name }} {{ b.last_name }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ b.ci }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ b.sector }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <router-link :to="`/beneficiaries/${b.id}`" class="text-green-600 hover:text-green-900 font-bold mr-4">Ver Perfil</router-link>
              <button class="text-indigo-600 hover:text-indigo-900 mr-4">Editar</button>
              <button @click="deleteItem(b.id)" class="text-red-600 hover:text-red-900">Eliminar</button>
            </td>
          </tr>
          <tr v-if="filteredAndSortedBeneficiaries.length === 0">
              <td colspan="4" class="px-6 py-8 text-center text-gray-500">
                <div v-if="searchQuery">
                    No se encontraron resultados para "<span class="font-semibold">{{ searchQuery }}</span>".
                </div>
                <div v-else>
                    No hay beneficiarios registrados.
                </div>
              </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Simple Add Form Modal -->

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import apiClient from '../plugins/axios'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import * as XLSX from 'xlsx'
const beneficiaries = ref([])
const showForm = ref(false)
const form = ref({
    ci: '',
    first_name: '',
    last_name: '',
    dob: '',
    sex: 'M',
    sector: ''
})

const fetchItems = async () => {
    try {
        const res = await apiClient.get('beneficiaries/')
        beneficiaries.value = res.data
    } catch (e) { console.error(e) }
}

const saveBeneficiary = async () => {
    try {
        await apiClient.post('beneficiaries/', form.value)
        showForm.value = false
        form.value = { ci: '', first_name: '', last_name: '', dob: '', sex: 'M', sector: '' }
        fetchItems()
    } catch (e) {
        alert("Error al guardar")
        console.error(e)
    }
}

const deleteItem = async (id) => {
    if(confirm('¿Seguro que deseas eliminarlo?')) {
        await apiClient.delete(`beneficiaries/${id}/`)
        fetchItems()
    }
}

// Search and Sorting Logic
const searchQuery = ref('')
const sortKey = ref('')
const sortOrder = ref(1) // 1 asc, -1 desc

const sortBy = (key) => {
    if (sortKey.value === key) {
        sortOrder.value = sortOrder.value * -1
    } else {
        sortKey.value = key
        sortOrder.value = 1
    }
}

const filteredAndSortedBeneficiaries = computed(() => {
    let result = beneficiaries.value

    // 1. Filter
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(b => {
            const fullName = `${b.first_name || ''} ${b.last_name || ''}`.toLowerCase()
            const ci = (b.ci || '').toLowerCase()
            return fullName.includes(query) || ci.includes(query)
        })
    }

    // 2. Sort
    if (sortKey.value) {
        result = [...result].sort((a, b) => {
            let valA = a[sortKey.value] || ''
            let valB = b[sortKey.value] || ''
            
            if (sortKey.value === 'first_name') {
                valA = `${a.first_name || ''} ${a.last_name || ''}`.toLowerCase()
                valB = `${b.first_name || ''} ${b.last_name || ''}`.toLowerCase()
            } else {
                valA = valA.toString().toLowerCase()
                valB = valB.toString().toLowerCase()
            }

            if (valA < valB) return -1 * sortOrder.value
            if (valA > valB) return 1 * sortOrder.value
            return 0
        })
    }

    return result
})

const getLocalISODateStr = (d) => {
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const h = String(d.getHours()).padStart(2, '0')
    const min = String(d.getMinutes()).padStart(2, '0')
    return `${y}-${m}-${day}_${h}${min}`
}

const exportToPDF = () => {
    if (!filteredAndSortedBeneficiaries.value.length) return
    
    const doc = new jsPDF()
    doc.text("Listado de Usuarios", 14, 15)
    
    const head = [['Nombre Completo', 'Cédula', 'Fecha Nacimiento', 'Sector']]
    const bodyDate = filteredAndSortedBeneficiaries.value.map(b => [
        `${b.first_name} ${b.last_name}`,
        b.ci,
        b.dob || 'N/A',
        b.sector || 'N/A'
    ])
    
    autoTable(doc, {
        head: head,
        body: bodyDate,
        startY: 25,
        theme: 'grid',
        headStyles: { fillColor: [234, 88, 12] } // Orange-600
    })
    
    doc.save(`Usuarios_${getLocalISODateStr(new Date())}.pdf`)
}

const exportToExcel = () => {
    if (!filteredAndSortedBeneficiaries.value.length) return
    
    const data = filteredAndSortedBeneficiaries.value.map(b => ({
        'Nombre Completo': `${b.first_name} ${b.last_name}`,
        'Cédula': b.ci,
        'Fecha Nacimiento': b.dob || 'N/A',
        'Sector': b.sector || 'N/A'
    }))
    
    const ws = XLSX.utils.json_to_sheet(data)
    
    // Auto-size columns slightly
    const colWidths = [
      { wch: 35 }, // Nombre
      { wch: 20 }, // Cédula
      { wch: 20 }, // Fecha Nacimiento
      { wch: 30 }, // Sector
    ];
    ws['!cols'] = colWidths;
    
    // Hacer la cabecera en negrita
    const range = XLSX.utils.decode_range(ws['!ref'])
    for (let c = range.s.c; c <= range.e.c; c++) {
        const cellAddress = XLSX.utils.encode_cell({ r: 0, c: c })
        if (!ws[cellAddress]) continue
        ws[cellAddress].s = { font: { bold: true } }
    }
    
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, "Usuarios")
    
    XLSX.writeFile(wb, `Usuarios_${getLocalISODateStr(new Date())}.xlsx`)
}

onMounted(() => fetchItems())
</script>
