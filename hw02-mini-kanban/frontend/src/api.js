// Keep all server calls here, so the board never depends on storage details.
const baseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const response = await fetch(`${baseUrl}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options.headers },
  });
  if (!response.ok) {
    throw new Error(`Request failed (${response.status}). Please try again.`);
  }
  return response.status === 204 ? null : response.json();
}

const serverApi = {
  list: () => request('/api/tasks'),
  create: (task) => request('/api/tasks', { method: 'POST', body: JSON.stringify(task) }),
  move: (id, status) => request(`/api/tasks/${id}`, { method: 'PATCH', body: JSON.stringify({ status }) }),
  remove: (id) => request(`/api/tasks/${id}`, { method: 'DELETE' }),
};

// The prototype uses the same interface without a running backend.
let mockTasks = [];
let nextId = 1;
const mockApi = {
  list: async () => [...mockTasks],
  create: async (task) => {
    const saved = { ...task, id: nextId++, status: 'todo', created_at: new Date().toISOString() };
    mockTasks.push(saved);
    return saved;
  },
  move: async (id, status) => {
    const task = mockTasks.find((item) => item.id === id);
    task.status = status;
    return task;
  },
  remove: async (id) => { mockTasks = mockTasks.filter((item) => item.id !== id); },
};

export const api = import.meta.env.VITE_USE_MOCK === 'true' ? mockApi : serverApi;

