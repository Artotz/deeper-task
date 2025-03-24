<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const users = ref([]);
const loading = ref(true);
const error = ref(null);

const showAddModal = ref(false);
const newUser = ref({
  username: "",
  password: "",
  roles: [],
  preferences: { timezone: "" },
});

const showEditModal = ref(false);
const editedUser = ref({
  username: "",
  roles: [],
  preferences: { timezone: "" },
});
const availableRoles = ["admin", "manager", "tester"];

const selectedUser = ref(null);
const showModal = ref(false);

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

const openAddModal = () => {
  newUser.value = {
    username: "",
    password: "",
    roles: [],
    preferences: { timezone: "" },
  };
  showAddModal.value = true;
};

const addUser = async () => {
  if (!newUser.value.username || !newUser.value.password) return;

  newUser.value.active = true;
  newUser.value.created_ts = 0;

  console.log(newUser.value);

  await axios.post("http://localhost:5000/users", newUser.value);

  users.value.push({ ...newUser.value });

  showAddModal.value = false;
};

const openEditModal = (user) => {
  editedUser.value = { ...user, roles: [...user.roles] }; // Clona roles para evitar edição direta no objeto original
  showEditModal.value = true;
};

const toggleRole = (role) => {
  const index = editedUser.value.roles.indexOf(role);
  if (index === -1) {
    editedUser.value.roles.push(role);
  } else {
    editedUser.value.roles.splice(index, 1);
  }
};

const updateUser = async () => {
  if (!editedUser.value.username) return;

  await axios.put(
    `http://localhost:5000/users/${editedUser.value.username}`,
    editedUser.value
  );

  // Atualiza a lista localmente
  const index = users.value.findIndex(
    (u) => u.username === editedUser.value.username
  );
  if (index !== -1) users.value[index] = { ...editedUser.value };

  showEditModal.value = false;
};

const confirmDelete = (user) => {
  selectedUser.value = user;
  showModal.value = true;
};

const deleteUser = async () => {
  if (!selectedUser.value) return;

  await axios.delete(
    `http://localhost:5000/users/${selectedUser.value.username}`
  );
  users.value = users.value.filter(
    (u) => u.username !== selectedUser.value.username
  );

  showModal.value = false;
  selectedUser.value = null;
};

onMounted(fetchUsers);
</script>

<template>
  <div class="container">
    <h1>Lista de Usuários</h1>
    <button @click="openAddModal">Adicionar Usuário</button>

    <div v-if="loading" class="loading">Carregando...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <table v-else class="user-table">
      <thead class="user-table-head">
        <tr>
          <th>Nome</th>
          <th>Funções</th>
          <th>Fuso Horário</th>
          <th>Ativo</th>
          <th>Ações</th>
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
          <td>
            <button @click="openEditModal(user)">Editar</button>
            <button @click="confirmDelete(user)">Excluir</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal de Adicionar Usuário -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <h2>Adicionar Usuário</h2>

        <label>Usuário:</label>
        <input v-model="newUser.username" />

        <label>Senha:</label>
        <input v-model="newUser.password" type="password" />

        <label>Fuso Horário:</label>
        <input v-model="newUser.preferences.timezone" />

        <label>Funções:</label>
        <div>
          <label v-for="role in availableRoles" :key="role">
            {{ role }}
            <input
              type="checkbox"
              :value="role"
              :checked="newUser.roles.includes(role)"
              @change="toggleRole(role, newUser)"
            />
          </label>
        </div>

        <button @click="addUser">Criar</button>
        <button @click="showAddModal = false">Cancelar</button>
      </div>
    </div>

    <!-- Modal de Edição -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h2>Editar Usuário</h2>

        <label>Usuário:</label>
        <input v-model="editedUser.username" disabled />

        <label>Fuso Horário:</label>
        <input v-model="editedUser.preferences.timezone" />

        <label>Funções:</label>
        <div>
          <label v-for="role in availableRoles" :key="role">
            {{ role }}
            <input
              type="checkbox"
              :value="role"
              :checked="editedUser.roles.includes(role)"
              @change="toggleRole(role)"
            />
          </label>
        </div>

        <button @click="updateUser">Salvar</button>
        <button @click="showEditModal = false">Cancelar</button>
      </div>
    </div>

    <!-- Modal de Exclusão -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>Confirmar Exclusão</h2>
        <p>
          Tem certeza de que deseja excluir o usuário
          <strong>{{ selectedUser?.username }}</strong
          >?
        </p>
        <button @click="deleteUser">Confirmar</button>
        <button @click="showModal = false">Cancelar</button>
      </div>
    </div>
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

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

input {
  width: 100%;
  padding: 5px;
  margin-bottom: 10px;
}
</style>
