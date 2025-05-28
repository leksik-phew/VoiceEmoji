document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
});

window.addEventListener('scroll', function() {
    const nav = document.querySelector('.nav-container');
    if (nav) {
        nav.style.background = window.scrollY > 100 
            ? 'rgba(139, 0, 0, 0.95)' 
            : 'var(--primary)';
    }
});

const overlay = document.querySelector('.image-overlay');
const galleryItems = document.querySelectorAll('.gallery-item');

galleryItems.forEach(item => {
    item.addEventListener('mouseenter', function() {
        const title = this.querySelector('img').alt;
        const overlayContent = overlay.querySelector('.overlay-content');
        overlayContent.querySelector('h3').textContent = title;
        
        switch(title) {
            case 'Emotion Analysis Visualization':
                overlayContent.querySelector('p').textContent = 'Multidimensional mapping of vocal emotional signatures';
                overlayContent.querySelector('.tech-tags').innerHTML = '<span>t-SNE</span><span>PCA</span>';
                break;
            case 'Cognitive State Visualization':
                overlayContent.querySelector('p').textContent = 'Neural network interpretation of mental states';
                overlayContent.querySelector('.tech-tags').innerHTML = '<span>BERT</span><span>LSTM</span>';
                break;
            case 'Dimensionality Reduction Visualization':
                overlayContent.querySelector('p').textContent = 'Non-linear dimensionality reduction analysis';
                overlayContent.querySelector('.tech-tags').innerHTML = '<span>UMAP</span><span>Clustering</span>';
                break;
            case 'Temporal Emotion Tracking':
                overlayContent.querySelector('p').textContent = 'Time-series emotion intensity tracking';
                overlayContent.querySelector('.tech-tags').innerHTML = '<span>LSTM</span><span>Attention</span>';
                break;
            case 'Feature Correlation Analysis':
                overlayContent.querySelector('p').textContent = 'Acoustic feature importance analysis';
                overlayContent.querySelector('.tech-tags').innerHTML = '<span>Librosa</span><span>SHAP</span>';
                break;
        }
        
        overlay.style.display = 'block';
    });

    item.addEventListener('mouseleave', function() {
        overlay.style.display = 'none';
    });
});