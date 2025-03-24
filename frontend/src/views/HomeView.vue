<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import Skeleton from "primevue/skeleton";
import Dialog from "primevue/dialog";
import Checkbox from "primevue/checkbox";
import InputText from "primevue/inputtext";

const skeletons = ref(new Array(20));

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

const formatDate = (_d) => {
  var d = new Date(_d);
  return d.getDate() + "/" + (d.getMonth() + 1) + "/" + d.getFullYear();
};

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
  newUser.value.created_ts = Date.now();

  console.log(newUser.value);

  await axios.post("http://localhost:5000/users", newUser.value);

  users.value.push({ ...newUser.value });

  showAddModal.value = false;
};

const openEditModal = (user) => {
  editedUser.value = {
    ...user,
    preferences: { timezone: user.preferences.timezone },
    roles: [...user.roles],
  }; // Clona roles para evitar edição direta no objeto original
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
    <Button class="add-user-button" @click="openAddModal"
      >Adicionar Usuário</Button
    >

    <DataTable v-if="loading" :value="skeletons">
      <Column field="username" header="Name">
        <template #body>
          <Skeleton></Skeleton>
        </template>
      </Column>
      <Column field="roles" header="Roles">
        <template #body>
          <Skeleton></Skeleton>
        </template>
      </Column>
      <Column field="preferences.timezone" header="Timezone">
        <template #body> <Skeleton></Skeleton> </template
      ></Column>
      <Column field="created_ts" header="Timestamp">
        <template #body>
          <Skeleton></Skeleton>
        </template>
      </Column>
      <Column field="active" header="Active">
        <template #body>
          <Skeleton></Skeleton>
        </template>
      </Column>
      <Column header="Actions">
        <template #body>
          <Skeleton></Skeleton>
        </template>
      </Column>
      <Column header="Detalhes">
        <template #body>
          <Skeleton></Skeleton>
        </template>
      </Column>
    </DataTable>
    <div v-else-if="error" class="error">{{ error }}</div>
    <DataTable v-else :value="users">
      <Column field="username" header="Name"> </Column>
      <Column field="roles" header="Roles">
        <template #body="slotProps">
          {{ slotProps.data.roles.join(", ") }}
        </template>
      </Column>
      <Column field="preferences.timezone" header="Timezone"></Column>
      <Column field="created_ts" header="Timestamp">
        <template #body="slotProps">
          {{ formatDate(slotProps.data.created_ts) }}
        </template>
      </Column>
      <Column field="active" header="Active">
        <template #body="slotProps">
          <span
            :class="{
              active: slotProps.data.active,
              inactive: !slotProps.data.active,
            }"
          >
            {{ slotProps.data.active ? "Sim" : "Não" }}
          </span>
        </template>
      </Column>
      <Column header="Actions">
        <template #body="slotProps">
          <div class="actions-column-cell">
            <Button @click="openEditModal(slotProps.data)" severity="secondary"
              >Editar</Button
            >
            <Button @click="confirmDelete(slotProps.data)" severity="secondary">
              Excluir
            </Button>
          </div>
        </template>
      </Column>
      <Column header="Detalhes">
        <template #body="slotProps">
          <router-link :to="`/user/${slotProps.data.username}`">
            <Button severity="secondary">Detalhes</Button>
          </router-link>
        </template>
      </Column>
    </DataTable>

    <!-- Modal de Adicionar Usuário -->
    <Dialog
      v-model:visible="showAddModal"
      modal
      header="Confirm Deletion"
      :style="{ width: '25rem' }"
    >
      <template #header>
        <h2>Adicionar Usuário</h2>
      </template>

      <div class="text-field">
        <label>Usuário:</label>
        <InputText v-model="newUser.username" />
      </div>

      <div class="text-field">
        <label>Senha:</label>
        <InputText v-model="newUser.password" type="password" />
      </div>

      <div class="text-field">
        <label>Fuso Horário:</label>
        <InputText v-model="newUser.preferences.timezone" />
      </div>

      <label>Funções:</label>
      <div class="edit-dialog-checkboxes">
        <label v-for="role in availableRoles" :key="role">
          <Checkbox
            type="checkbox"
            :value="role"
            :checked="newUser.roles.includes(role)"
            @change="toggleRole(role, newUser)"
          />
          <span>{{ role }}</span>
        </label>
      </div>

      <template #footer>
        <Button @click="addUser">Criar</Button>
        <Button @click="showAddModal = false" severity="secondary"
          >Cancelar</Button
        >
      </template>
    </Dialog>

    <!-- Modal de Edição -->
    <Dialog
      v-model:visible="showEditModal"
      modal
      header="Confirm Deletion"
      :style="{ width: '25rem' }"
    >
      <template #header>
        <h2>Editar Usuário</h2>
      </template>

      <div class="text-field">
        <label>Usuário:</label>
        <InputText v-model="editedUser.username" disabled />
      </div>

      <div class="text-field">
        <label>Fuso Horário:</label>
        <InputText v-model="editedUser.preferences.timezone" />
      </div>

      <label>Funções:</label>
      <div class="edit-dialog-checkboxes">
        <label v-for="role in availableRoles" :key="role">
          <Checkbox
            type="checkbox"
            :value="role"
            :checked="editedUser.roles.includes(role)"
            @change="toggleRole(role)"
          />
          <span>{{ role }}</span>
        </label>
      </div>

      <template #footer>
        <Button @click="updateUser">Salvar</Button>
        <Button @click="showEditModal = false" severity="secondary"
          >Cancelar</Button
        >
      </template>
    </Dialog>

    <!-- Modal de Exclusão -->
    <Dialog
      v-model:visible="showModal"
      modal
      header="Confirm Deletion"
      :style="{ width: '25rem' }"
    >
      <p>
        Tem certeza de que deseja excluir o usuário
        <strong>{{ selectedUser?.username }}</strong
        >?
      </p>
      <template #footer>
        <Button @click="deleteUser" severity="danger">Confirmar</Button>
        <Button @click="showModal = false" severity="secondary"
          >Cancelar</Button
        >
      </template>
    </Dialog>
  </div>
</template>

<style scoped>
.container {
  margin: auto;
  text-align: center;
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
  padding: 1.25rem;
  border-radius: 0.5rem;
  text-align: center;
}

input {
  width: 100%;
  margin-bottom: 0.5rem;
}

.actions-column-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.add-user-button {
  margin: 0.5rem 0;
}

.text-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.text-field label {
  font-size: 0.75rem;
}

.edit-dialog-checkboxes {
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.edit-dialog-checkboxes label {
  display: inline-flex;
  gap: 0.5rem;
}
</style>
