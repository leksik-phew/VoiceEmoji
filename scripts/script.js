// Smooth scroll для якорных ссылок
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
});

// Динамический фон навигации
window.addEventListener('scroll', function() {
    const nav = document.querySelector('.nav-container');
    nav.style.background = window.scrollY > 100 
        ? 'rgba(139, 0, 0, 0.95)' 
        : 'var(--primary)';
});

// Модальное окно
const modal = document.getElementById('galleryModal');
const modalImg = document.getElementById('modalImage');
const captionText = document.querySelector('.caption');

document.querySelectorAll('.gallery img').forEach(img => {
    img.addEventListener('click', function(e) {
        const imgRect = this.getBoundingClientRect();
        
        // Позиционирование модалки
        modal.style.display = 'block';
        modal.style.position = 'absolute';
        modal.style.left = `${imgRect.right + 20}px`;
        modal.style.top = `${imgRect.top}px`;

        // Контент
        modalImg.src = this.src;
        captionText.innerHTML = this.alt;

        // Адаптация для мобилок
        if(window.innerWidth <= 768) {
            modal.style.left = '10px';
            modal.style.right = '10px';
            modal.style.top = 'auto';
            modal.style.bottom = '20px';
        }
    });
});

// Закрытие модалки
document.querySelector('.close').addEventListener('click', closeModal);
document.addEventListener('click', function(e) {
    if(!modal.contains(e.target)) closeModal();
});

function closeModal() {
    modal.style.display = 'none';
}

// Ресайз и скролл
window.addEventListener('resize', closeModal);
window.addEventListener('scroll', closeModal);