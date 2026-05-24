    const PAGE_SIZE = 5;
    let currentPage = 1;
    let isLoading = false;

    const container = document.getElementById('table-scroll-container');
    const tbody = document.getElementById('user-table-body');
    const allUserRows = Array.from(tbody.querySelectorAll('.user-row'));
    const bottomLoader = document.getElementById('bottom-loader');
    const scrollHint = document.getElementById('scroll-hint');
    const searchInput = document.getElementById('search');

    let filteredRows = [...allUserRows];

    function hideSkeleton() {
        document.querySelectorAll('.skeleton-row').forEach(row => row.remove());
    }

    function showLoader() {
        bottomLoader.classList.remove('hidden');
        container.scrollTop = container.scrollHeight;
    }

    function hideLoader() {
        bottomLoader.classList.add('hidden');
    }

    function showFilteredPage(page) {
        const start = (page - 1) * PAGE_SIZE;
        const end = Math.min(start + PAGE_SIZE, filteredRows.length);

        for (let i = start; i < end; i++) {
            const row = filteredRows[i];
            row.classList.remove('hidden');
            setTimeout(() => {
                row.classList.remove('opacity-0', 'translate-y-4');
            }, (i - start) * 80);
        }

        currentPage = page;

        const totalFilteredPages = Math.ceil(filteredRows.length / PAGE_SIZE);
        if (currentPage >= totalFilteredPages) {
            if (scrollHint) scrollHint.style.display = 'none';
        } else {
            if (scrollHint) scrollHint.style.display = 'flex';
        }
    }

    function applySearch(query) {
        const q = query.trim().toLowerCase();

        filteredRows = allUserRows.filter(row => {
            const nameCell = row.querySelector('td:first-child');
            const name = nameCell ? nameCell.textContent.trim().toLowerCase() : '';
            return q === '' || name.startsWith(q);
        });

        allUserRows.forEach(row => {
            row.classList.add('hidden', 'opacity-0', 'translate-y-4');
        });

        currentPage = 0;
        showFilteredPage(1);

        if (scrollHint) scrollHint.style.display = filteredRows.length > PAGE_SIZE ? 'flex' : 'none';
    }

    function loadNextPage() {
        const totalFilteredPages = Math.ceil(filteredRows.length / PAGE_SIZE);
        if (isLoading || currentPage >= totalFilteredPages) return;
        isLoading = true;

        showLoader();

        setTimeout(() => {
            hideLoader();
            showFilteredPage(currentPage + 1);
            isLoading = false;
        }, 800);
    }

    container.addEventListener('scroll', () => {
        const nearBottom = container.scrollTop + container.clientHeight >= container.scrollHeight - 10;
        if (nearBottom) loadNextPage();
    });

    searchInput.addEventListener('input', (e) => {
        applySearch(e.target.value);
    });

    function init() {
        setTimeout(() => {
            hideSkeleton();
            showFilteredPage(1);
        }, 600);
    }

    init();
    