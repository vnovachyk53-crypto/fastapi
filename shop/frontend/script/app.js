const API = '';
const bookGrid = document.querySelector('#bookGrid');
const searchInput = document.querySelector('#searchInput');
const authModal = document.querySelector('#authModal');
const bookModal = document.querySelector('#bookModal');
const detailModal = document.querySelector('#detailModal');
let books = [];
let currentUser = null;
let authMode = 'login';
let editingBookId = null;

async function api(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    credentials: 'same-origin',
    ...options,
    headers: { ...(options.body && !(options.body instanceof URLSearchParams) ? { 'Content-Type': 'application/json' } : {}), ...(options.headers || {}) }
  });
  const data = response.status === 204 ? null : await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || `Помилка ${response.status}`);
  return data;
}

function showMessage(text, isError = false) {
  const box = document.querySelector('#message');
  box.textContent = text;
  box.classList.remove('hidden', 'error');
  if (isError) box.classList.add('error');
  window.clearTimeout(showMessage.timer);
  showMessage.timer = window.setTimeout(() => box.classList.add('hidden'), 4000);
}

function setAuthUI() {
  document.querySelector('#authButton').classList.toggle('hidden', !!currentUser);
  document.querySelector('#logoutButton').classList.toggle('hidden', !currentUser);
  document.querySelector('#userLabel').textContent = currentUser ? `Привіт, ${currentUser.username}` : '';
  document.querySelector('#adminPanel').classList.toggle('hidden', !currentUser);
  renderBooks();
}

async function loadUser() {
  try { currentUser = await api('/auth/me'); }
  catch { currentUser = null; }
  setAuthUI();
}

async function loadBooks() {
  bookGrid.innerHTML = '<div class="loading">Завантажуємо каталог...</div>';
  try {
    books = await api('/books');
    renderBooks();
  } catch (error) {
    bookGrid.innerHTML = `<div class="empty">Не вдалося завантажити каталог: ${escapeHTML(error.message)}</div>`;
  }
}

function escapeHTML(value) {
  return String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
}

function renderBooks() {
  const query = searchInput.value.trim().toLocaleLowerCase('uk');
  const filtered = books.filter(book => `${book.title} ${book.author} ${book.genre || ''}`.toLocaleLowerCase('uk').includes(query));
  document.querySelector('#bookCount').textContent = `${filtered.length} ${wordForBooks(filtered.length)}`;
  if (!filtered.length) {
    bookGrid.innerHTML = '<div class="empty">Нічого не знайдено. Спробуй інший запит.</div>';
    return;
  }
  bookGrid.innerHTML = filtered.map((book, index) => `
    <article class="book-card">
      <div class="book-cover cover-${(index % 6) + 1}"><span class="cover-symbol">${escapeHTML((book.title || 'К').trim().charAt(0).toUpperCase())}</span></div>
      <div class="book-info">
        <span class="book-genre">${escapeHTML(book.genre || 'Без жанру')}</span>
        <h3>${escapeHTML(book.title)}</h3><div class="book-author">${escapeHTML(book.author)}</div>
        <div class="card-bottom"><button class="text-link" data-view="${book.id}">ДЕТАЛЬНІШЕ ↗</button>
          ${currentUser ? `<div class="admin-actions"><button class="text-link" data-edit="${book.id}">Змінити</button><button class="text-link delete-link" data-delete="${book.id}">Видалити</button></div>` : ''}
        </div>
      </div>
    </article>`).join('');
}

function wordForBooks(count) {
  const n = count % 100;
  if (n >= 11 && n <= 14) return 'книг';
  if (count % 10 === 1) return 'книга';
  if (count % 10 >= 2 && count % 10 <= 4) return 'книги';
  return 'книг';
}

function openAuth(mode = 'login') {
  setAuthMode(mode);
  authModal.classList.remove('hidden');
}
function setAuthMode(mode) {
  authMode = mode;
  const register = mode === 'register';
  document.querySelector('#authTitle').textContent = register ? 'Створи акаунт' : 'Увійти в акаунт';
  document.querySelector('#authDescription').textContent = register ? 'Зареєструйся, щоб керувати каталогом.' : 'Увійди, щоб керувати каталогом.';
  document.querySelector('#authSubmit').textContent = register ? 'Зареєструватися' : 'Увійти';
  document.querySelectorAll('[data-auth-mode]').forEach(tab => tab.classList.toggle('active', tab.dataset.authMode === mode));
  document.querySelector('#authError').textContent = '';
}

function openBookForm(book = null) {
  editingBookId = book ? book.id : null;
  document.querySelector('#bookModalTitle').textContent = book ? 'Редагувати книгу' : 'Нова книга';
  const form = document.querySelector('#bookForm');
  form.elements.title.value = book?.title || '';
  form.elements.author.value = book?.author || '';
  form.elements.genre.value = book?.genre || '';
  document.querySelector('#bookError').textContent = '';
  bookModal.classList.remove('hidden');
}

function openDetails(book) {
  document.querySelector('#detailContent').innerHTML = `
    <div class="detail-content"><div class="book-cover cover-${(book.id % 6) + 1}"><span class="cover-symbol">${escapeHTML(book.title.charAt(0).toUpperCase())}</span></div>
    <div><span class="book-genre">${escapeHTML(book.genre || 'Без жанру')}</span><h2 id="detailTitle">${escapeHTML(book.title)}</h2><p>Автор: ${escapeHTML(book.author)}</p><p>ID книги: ${book.id}</p></div></div>`;
  detailModal.classList.remove('hidden');
}

document.querySelector('#authButton').addEventListener('click', () => openAuth('login'));
document.querySelector('#logoutButton').addEventListener('click', async () => {
  try { await api('/auth/logout', { method: 'POST' }); } catch (error) { showMessage(error.message, true); }
  currentUser = null;
  setAuthUI();
  showMessage('Ти вийшов з акаунта. Каталог залишається доступним.');
});
document.querySelector('#addBookButton').addEventListener('click', () => openBookForm());
searchInput.addEventListener('input', renderBooks);
document.querySelectorAll('[data-auth-mode]').forEach(tab => tab.addEventListener('click', () => setAuthMode(tab.dataset.authMode)));
document.querySelectorAll('[data-close]').forEach(button => button.addEventListener('click', () => {
  ({ auth: authModal, book: bookModal, detail: detailModal })[button.dataset.close].classList.add('hidden');
}));

bookGrid.addEventListener('click', async event => {
  const viewButton = event.target.closest('[data-view]');
  const editButton = event.target.closest('[data-edit]');
  const deleteButton = event.target.closest('[data-delete]');
  if (viewButton) {
    const book = books.find(item => item.id === Number(viewButton.dataset.view));
    if (book) openDetails(book);
  }
  if (editButton) {
    const book = books.find(item => item.id === Number(editButton.dataset.edit));
    if (book) openBookForm(book);
  }
  if (deleteButton) {
    const id = Number(deleteButton.dataset.delete);
    const book = books.find(item => item.id === id);
    if (!book || !confirm(`Видалити книгу «${book.title}»?`)) return;
    try {
      await api(`/books/${id}`, { method: 'DELETE' });
      await loadBooks();
      showMessage('Книгу видалено.');
    } catch (error) { showMessage(error.message, true); }
  }
});

document.querySelector('#authForm').addEventListener('submit', async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const body = new URLSearchParams(new FormData(form));
  const errorBox = document.querySelector('#authError');
  errorBox.textContent = '';
  try {
    if (authMode === 'register') await api('/auth/register', { method: 'POST', body });
    await api('/auth/login', { method: 'POST', body });
    currentUser = await api('/auth/me');
    authModal.classList.add('hidden');
    form.reset();
    setAuthUI();
    showMessage(authMode === 'register' ? 'Акаунт створено. Ти увійшов!' : 'Вхід успішний! Тепер можна керувати каталогом.');
  } catch (error) { errorBox.textContent = error.message; }
});

document.querySelector('#bookForm').addEventListener('submit', async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form));
  const errorBox = document.querySelector('#bookError');
  errorBox.textContent = '';
  try {
    if (editingBookId) await api(`/books/${editingBookId}`, { method: 'PUT', body: JSON.stringify(payload) });
    else await api('/books', { method: 'POST', body: JSON.stringify(payload) });
    bookModal.classList.add('hidden');
    form.reset();
    await loadBooks();
    showMessage(editingBookId ? 'Зміни збережено.' : 'Книгу додано до каталогу.');
  } catch (error) { errorBox.textContent = error.message; }
});

(async function init() {
  await Promise.all([loadUser(), loadBooks()]);
})();
