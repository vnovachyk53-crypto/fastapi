const API_URL = '/api';

        async function fetchProjects() {
            try {
                const res = await fetch(`${API_URL}/projects/`);
                const projects = await res.json();
                const list = document.getElementById('projects-list');
                list.innerHTML = projects.map(p => `
                    <li>
                        <strong>ID: ${p.id}</strong> - ${p.title || p.name}<br>
                        <small>${p.description || ''}</small>
                    </li>
                `).join('');
            } catch (err) {
                console.error('Помилка завантаження проєктів:', err);
            }
        }

  
        async function fetchTasks() {
            try {
                const res = await fetch(`${API_URL}/tasks/`);
                const tasks = await res.json();
                const list = document.getElementById('tasks-list');
                list.innerHTML = tasks.map(t => `
                    <li>
                        <strong>${t.title}</strong> (Проєкт ID: ${t.project_id})<br>
                        <small>Статус: ${t.status || 'В процесі'}</small>
                    </li>
                `).join('');
            } catch (err) {
                console.error('Помилка завантаження завдань:', err);
            }
        }


        document.getElementById('project-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('project-name').value;
            const description = document.getElementById('project-desc').value;

            await fetch(`${API_URL}/projects/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, title: name, description })
            });

            e.target.reset();
            fetchProjects();
        });


        document.getElementById('task-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('task-title').value;
            const project_id = parseInt(document.getElementById('task-project-id').value);

            await fetch(`${API_URL}/tasks/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, project_id })
            });

            e.target.reset();
            fetchTasks();
        });

        fetchProjects();
        fetchTasks();