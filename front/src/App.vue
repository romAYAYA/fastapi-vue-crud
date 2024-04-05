<template>
  <div class="flex flex-col justify-center items-center w-full">
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

    <div v-for="user in userData" :key="user.id" class="flex justify-between w-[600px] border-2 mb-2">
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


      <button @click="deleteUser(user.id)"
              class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-full">
        Удалить
      </button>
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

const resetEdit = (id) => {
  userData.value.forEach(user => {
    user.isEditable = user.id === id
  })
}

const getUserData = async () => {
  try {
    const {data} = await axios.get('http://127.0.0.1:8000/api/users')
    data.data.forEach(user => {
      user.isEditable = false
    })
    userData.value = data.data
  } catch (e) {
    console.error(e)
  }
}

const createUser = async () => {
  const data = {
    firstname: userName.value,
    lastname: userContact.value,
    age: parseInt(userAge.value)
  }
  try {
    await axios.post('http://127.0.0.1:8000/api/users', data)
    await getUserData()
    userName.value = ''
    userContact.value = ''
    userAge.value = null
  } catch (e) {
    console.error(e)
  }
}

const updateUser = async (id, person) => {
  const data = {
    firstname: person.firstname,
    fullname: person.fullname,
    age: parseInt(person.age)
  }
  console.log(data)
  await axios.put(`http://127.0.0.1:8000/api/users/${id}`, data)
  person.isEditable = !person.isEditable
  await getUserData()
}

const deleteUser = async (id) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/users/${id}`)
    await getUserData()
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  getUserData()
})
</script>
