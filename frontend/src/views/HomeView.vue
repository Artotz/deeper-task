<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const users = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchUsers = async () => {
  try {
    const response = await axios.get("http://localhost:5000/users"); // Endpoint Flask
    users.value = response.data; // Supondo que a API retorne uma lista de usuários
    console.log(response.data);
  } catch (err) {
    error.value = "Erro ao carregar usuários!";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchUsers);
</script>

<template>
  <div class="container">
    <h1 class="title">Lista de Usuários</h1>

    <div v-if="loading" class="loading">Carregando...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <table v-else class="user-table">
      <thead class="user-table-head">
        <tr>
          <th>Nome</th>
          <th>Funções</th>
          <th>Fuso Horário</th>
          <th>Ativo</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.username">
          <td>
            <router-link :to="`/user/${user.username}`">{{
              user.username
            }}</router-link>
          </td>
          <td>{{ user.roles.join(", ") }}</td>
          <td>{{ user.preferences.timezone }}</td>
          <td>
            <span :class="{ active: user.active, inactive: !user.active }">
              {{ user.active ? "Sim" : "Não" }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
  text-align: center;
}

.title {
  font-size: 24px;
  margin-bottom: 20px;
}

.loading,
.error {
  font-size: 18px;
  color: red;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.user-table-head {
  color: black;
}

.user-table th,
.user-table td {
  border: 1px solid #ddd;
  padding: 10px;
}

.user-table th {
  background: #f4f4f4;
}

.active {
  color: green;
  font-weight: bold;
}

.inactive {
  color: red;
  font-weight: bold;
}
</style>
