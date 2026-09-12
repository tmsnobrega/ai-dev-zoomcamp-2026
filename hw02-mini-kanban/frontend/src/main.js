import { api } from './api.js';
import './style.css';

const columns = [
  ['todo', 'To do'],
  ['doing', 'In progress'],
  ['done', 'Done'],
];
const app = document.querySelector('#app');
let tasks = [];
let error = '';
let busy = false;

function element(tag, text, className) {
  const node = document.createElement(tag);
  node.textContent = text;
  if (className) node.className = className;
  return node;
}

// Rebuild the small board after each successful change or error.
function render() {
  app.replaceChildren();
  const header = element('header', '', 'header');
  header.append(element('h1', 'TaskLane'), element('p', 'A clear view of what is next, underway, and finished.'));
  app.append(header);

  const form = document.createElement('form');
  form.className = 'new-task';
  const title = document.createElement('input');
  title.name = 'title';
  title.placeholder = 'Task title';
  title.maxLength = 100;
  title.required = true;
  title.setAttribute('aria-label', 'Task title');
  const description = document.createElement('input');
  description.name = 'description';
  description.placeholder = 'Details (optional)';
  description.maxLength = 500;
  description.setAttribute('aria-label', 'Task details');
  const add = element('button', busy ? 'Working…' : 'Add task');
  add.disabled = busy;
  form.append(title, description, add);
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const value = title.value.trim();
    if (!value) return;
    await change(() => api.create({ title: value, description: description.value.trim() }));
  });
  app.append(form);
  if (error) app.append(element('p', error, 'error'));

  const board = element('section', '', 'board');
  board.setAttribute('aria-label', 'Task board');
  for (const [status, label] of columns) {
    const column = element('section', '', 'column');
    const items = tasks.filter((task) => task.status === status);
    column.append(element('h2', `${label} · ${items.length}`));
    if (items.length === 0) column.append(element('p', 'No tasks here yet.', 'empty'));
    for (const task of items) {
      const card = element('article', '', 'card');
      card.append(element('h3', task.title));
      if (task.description) card.append(element('p', task.description));
      const actions = element('div', '', 'actions');
      const select = document.createElement('select');
      select.setAttribute('aria-label', `Status for ${task.title}`);
      select.disabled = busy;
      for (const [value, name] of columns) {
        const option = new Option(name, value);
        select.add(option);
      }
      select.value = task.status;
      select.addEventListener('change', () => change(() => api.move(task.id, select.value)));
      const remove = element('button', 'Delete', 'delete');
      remove.type = 'button';
      remove.disabled = busy;
      remove.setAttribute('aria-label', `Delete ${task.title}`);
      remove.addEventListener('click', () => {
        if (window.confirm(`Delete “${task.title}”?`)) change(() => api.remove(task.id));
      });
      actions.append(select, remove);
      card.append(actions);
      column.append(card);
    }
    board.append(column);
  }
  app.append(board);
}

async function change(operation) {
  busy = true;
  error = '';
  render();
  try {
    await operation();
    tasks = await api.list();
  } catch (cause) {
    error = cause.message;
  } finally {
    busy = false;
    render();
  }
}

render();
api.list().then((items) => { tasks = items; render(); }).catch((cause) => { error = cause.message; render(); });

