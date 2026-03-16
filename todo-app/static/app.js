document.addEventListener('DOMContentLoaded', () => {
    const todoForm = document.getElementById('todo-form');
    const todoInput = document.getElementById('todo-input');
    const todoList = document.getElementById('todo-list');
    const emptyState = document.getElementById('empty-state');
    const filterBtns = document.querySelectorAll('.filter-btn');

    let currentFilter = 'all';

    // Fetch and render todos initially
    fetchTodos();

    todoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = todoInput.value.trim();
        if (text) {
            await addTodo(text);
            todoInput.value = '';
            todoInput.focus();
        }
    });

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            fetchTodos();
        });
    });

    async function fetchTodos() {
        try {
            const res = await fetch('/api/todos');
            const todos = await res.json();
            renderTodos(todos);
        } catch (error) {
            console.error('Error fetching todos:', error);
        }
    }

    async function addTodo(text) {
        try {
            await fetch('/api/todos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            fetchTodos();
        } catch (error) {
            console.error('Error adding todo:', error);
        }
    }

    async function toggleTodo(id, completed) {
        try {
            await fetch(`/api/todos/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ completed })
            });
            fetchTodos();
        } catch (error) {
            console.error('Error updating todo:', error);
        }
    }

    async function deleteTodo(id, listItemElement) {
        try {
            // Apply delete animation
            listItemElement.classList.add('deleting');
            
            // Wait for animation to finish before deleting and refetching
            setTimeout(async () => {
                await fetch(`/api/todos/${id}`, {
                    method: 'DELETE'
                });
                fetchTodos();
            }, 200);
        } catch (error) {
            console.error('Error deleting todo:', error);
        }
    }

    function renderTodos(todos) {
        todoList.innerHTML = '';
        
        let filteredTodos = todos;
        if (currentFilter === 'active') {
            filteredTodos = todos.filter(t => !t.completed);
        } else if (currentFilter === 'completed') {
            filteredTodos = todos.filter(t => t.completed);
        }

        if (filteredTodos.length === 0) {
            emptyState.style.display = 'flex';
        } else {
            emptyState.style.display = 'none';
            filteredTodos.forEach(todo => {
                const li = document.createElement('li');
                li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
                
                li.innerHTML = `
                    <input type="checkbox" class="checkbox" ${todo.completed ? 'checked' : ''} aria-label="Toggle task">
                    <span class="todo-text">${escapeHTML(todo.text)}</span>
                    <button class="delete-btn" aria-label="Delete">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                    </button>
                `;

                const checkbox = li.querySelector('.checkbox');
                checkbox.addEventListener('change', () => {
                    toggleTodo(todo.id, checkbox.checked);
                });

                const deleteBtn = li.querySelector('.delete-btn');
                deleteBtn.addEventListener('click', () => {
                    deleteTodo(todo.id, li);
                });

                todoList.appendChild(li);
            });
        }
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag])
        );
    }
});
