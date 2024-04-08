<template>
  <div class="flex flex-col justify-center items-center w-full">
    <Toast/>
    <div>
      <div>
        <label for="first_name" class="block mb-2 text-sm font-medium text-gray-900 ">Имя</label>
        <input v-model="userName" type="text" id="first_name"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
               placeholder="John" required/>
      </div>

      <div>
        <label for="first_name" class="block mb-2 text-sm font-medium text-gray-900 ">Телефон</label>
        <input v-model="userContact" type="text" id="first_name"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
               placeholder="John" required/>
      </div>

      <div>
        <label for="first_name" class="block mb-2 text-sm font-medium text-gray-900 ">Возраст</label>
        <input v-model="userAge" type="number" id="first_name"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
               placeholder="John" required/>
      </div>

      <button @click="createUser" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full">
        Создать
      </button>
    </div>

    <div v-if="isLoading">
      <div role="status">
        <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
             viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
              d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
              fill="currentColor"/>
          <path
              d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
              fill="currentFill"/>
        </svg>
        <span class="sr-only">Loading...</span>
      </div>
    </div>


    <div v-else v-for="user in userData" :key="user.id" class="flex justify-between w-[600px] border-2 mb-2">

      <div>
        <p v-if="!user.isEditable">{{ user.firstname }}</p>
        <input
            v-if="user.isEditable"
            v-model="user.firstname" type="text" id="first_name"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            placeholder="John" required/>
      </div>
      <div>
        <p v-if="!user.isEditable">{{ user.fullname }}</p>
        <input
            v-if="user.isEditable"
            v-model="user.fullname" type="text" id="first_name"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            placeholder="John" required/>
      </div>
      <div>
        <p v-if="!user.isEditable">{{ user.age }}</p>

        <input
            v-if="user.isEditable"
            v-model="user.age" type="text" id="first_name"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            placeholder="John" required/>
      </div>
      <div>
        <button v-if="user.isEditable" @click="updateUser(user.id, user)"
                class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-full">
          Обновить
        </button>

        <button v-if="!user.isEditable" @click="resetEdit(user.id)"
                class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded-full">
          Изменить
        </button>
      </div>


      <div class="card flex justify-content-center">
        <Button class="text-black" label="Удалить" @click="confirmVisible = true"/>
        <Dialog v-model:visible="confirmVisible" modal header="Edit Profile" :style="{ width: '25rem', color: 'white' }">
          <span class="p-text-secondary text-white block mb-5">Вы точно хотите удалить это?</span>
          <div class="flex justify-content-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="confirmVisible = false"></Button>
            <button @click="deleteUser(user.id)"
                    class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-full">
              Удалить
            </button>
          </div>
        </Dialog>
      </div>

    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import axios from 'axios'

const userData = ref()
const userName = ref()
const userContact = ref()
const userAge = ref()
const isLoading = ref(false)
const confirmVisible = ref(false)

import {useToast} from 'primevue/usetoast'

const toast = useToast()

const show = () => {
  toast.add({severity: 'error', summary: 'Ошибка', detail: 'Нечего отправлять', life: 2000})
}

const resetEdit = (id) => {
  userData.value.forEach(user => {
    user.isEditable = user.id === id
  })
}

const getUserData = async () => {
  isLoading.value = true
  try {
    const {data} = await axios.get('http://127.0.0.1:8000/api/users')
    data.data.forEach(user => {
      user.isEditable = false
    })
    userData.value = data.data
    isLoading.value = false
  } catch (e) {
    console.error(e)
    isLoading.value = false
  }
}

const createUser = async () => {
  isLoading.value = true
  const data = {
    firstname: userName.value,
    lastname: userContact.value,
    age: parseInt(userAge.value)
  }
  if (!data.firstname && !data.lastname && !data.age) {
    isLoading.value = false
    return show()
  }
  try {
    await axios.post('http://127.0.0.1:8000/api/users', data)
    await getUserData()
    userName.value = ''
    userContact.value = ''
    userAge.value = null
    isLoading.value = false
  } catch (e) {
    console.error(e)
    isLoading.value = false
  }
}

const updateUser = async (id, person) => {
  isLoading.value = true
  try {
    const data = {
      firstname: person.firstname,
      fullname: person.fullname,
      age: parseInt(person.age)
    }
    console.log(data)
    await axios.put(`http://127.0.0.1:8000/api/users/${id}`, data)
    person.isEditable = !person.isEditable
    await getUserData()
    isLoading.value = false
  } catch (e) {
    console.log(e)
    isLoading.value = false
  }
}

const deleteUser = async (id) => {
  confirmVisible.value = true
  isLoading.value = true
  try {
    await axios.delete(`http://127.0.0.1:8000/api/users/${id}`)
    await getUserData()
    isLoading.value = false
    confirmVisible.value = false
  } catch (e) {
    console.error(e)
    isLoading.value = false
  }
}

onMounted(() => {
  getUserData()
})
</script>
