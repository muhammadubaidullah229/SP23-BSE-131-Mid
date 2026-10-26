// Interactive Tasks & Kanban Board Script
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('taskModal');
  const openModalBtn = document.getElementById('openTaskModalBtn');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const cancelModalBtn = document.getElementById('cancelModalBtn');
  const searchInput = document.getElementById('taskSearchInput');

  // Modal handlers
  if (openModalBtn && modal) {
    openModalBtn.addEventListener('click', () => {
      modal.classList.add('active');
      document.getElementById('taskTitleInput')?.focus();
    });
  }

  const hideModal = () => {
    if (modal) modal.classList.remove('active');
  };

  if (closeModalBtn) closeModalBtn.addEventListener('click', hideModal);
  if (cancelModalBtn) cancelModalBtn.addEventListener('click', hideModal);

  // Close modal when clicking on backdrop
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) hideModal();
    });
  }

  // Live Task Search & Filter
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      const taskCards = document.querySelectorAll('.task-card');

      taskCards.forEach(card => {
        const title = card.querySelector('.task-title')?.textContent.toLowerCase() || '';
        const desc = card.querySelector('.task-desc')?.textContent.toLowerCase() || '';

        if (title.includes(query) || desc.includes(query)) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }
});

// Interactive AJAX status changer (without page reload)
function updateTaskStatusAjax(taskId, newStatus) {
  fetch(`/tasks/${taskId}/update-status`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: JSON.stringify({ status: newStatus })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      window.location.reload();
    } else {
      alert('Error updating status: ' + data.message);
    }
  })
  .catch(err => console.error('Error updating task:', err));
}
