// Real-time Student Directory Search & Modal Handler
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('addStudentModal');
  const openModalBtn = document.getElementById('openAddStudentModalBtn');
  const closeModalBtn = document.getElementById('closeAddModalBtn');
  const cancelModalBtn = document.getElementById('cancelAddModalBtn');
  const searchInput = document.getElementById('studentSearchInput');
  const deptSelect = document.getElementById('deptFilterSelect');

  // Modal toggle handlers
  if (openModalBtn && modal) {
    openModalBtn.addEventListener('click', () => {
      modal.classList.add('active');
      document.getElementById('inputStudentName')?.focus();
    });
  }

  const hideModal = () => {
    if (modal) modal.classList.remove('active');
  };

  if (closeModalBtn) closeModalBtn.addEventListener('click', hideModal);
  if (cancelModalBtn) cancelModalBtn.addEventListener('click', hideModal);

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) hideModal();
    });
  }

  // Combined Live Search and Department Filter
  const applyFilters = () => {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const selectedDept = deptSelect ? deptSelect.value.toLowerCase() : '';
    const cards = document.querySelectorAll('.student-card');

    cards.forEach(card => {
      const name = card.querySelector('.student-full-name')?.textContent.toLowerCase() || '';
      const reg = card.querySelector('.student-reg-num')?.textContent.toLowerCase() || '';
      const email = card.querySelector('.email-val')?.textContent.toLowerCase() || '';
      const dept = card.getAttribute('data-department')?.toLowerCase() || '';

      const matchesSearch = !query || name.includes(query) || reg.includes(query) || email.includes(query);
      const matchesDept = !selectedDept || dept === selectedDept;

      if (matchesSearch && matchesDept) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  };

  if (searchInput) searchInput.addEventListener('input', applyFilters);
  if (deptSelect) deptSelect.addEventListener('change', applyFilters);
});
