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
overlay.style.display = 'none';

galleryItems.forEach(item => {
    const img = item.querySelector('img');
    
    item.addEventListener('mouseenter', function() {
        const title = img.alt;
        const overlayContent = overlay.querySelector('.overlay-content');
        overlayContent.querySelector('h3').textContent = getTitle(title);
        overlayContent.querySelector('p').textContent = getDescription(title);
        overlayContent.querySelector('.tech-tags').innerHTML = getTechTags(title);
        overlay.style.display = 'block';
    });

    item.addEventListener('mouseleave', function() {
        overlay.style.display = 'none';
    });
});

function getTitle(alt) {
    const titles = {
        'Emotion Analysis Visualization': 'Emotion Spectrum',
        'Cognitive State Visualization': 'Cognitive Landscape',
        'Dimensionality Reduction Visualization': 'Manifold Projection',
        'Temporal Emotion Tracking': 'Temporal Dynamics',
        'Feature Correlation Analysis': 'Feature Correlation'
    };
    return titles[alt] || alt;
}

function getDescription(alt) {
    const descriptions = {
        'Emotion Analysis Visualization': 'Multidimensional mapping of vocal emotional signatures',
        'Cognitive State Visualization': 'Neural network interpretation of mental states',
        'Dimensionality Reduction Visualization': 'Non-linear dimensionality reduction analysis',
        'Temporal Emotion Tracking': 'Time-series emotion intensity tracking',
        'Feature Correlation Analysis': 'Acoustic feature importance analysis'
    };
    return descriptions[alt] || '';
}

function getTechTags(alt) {
    const tags = {
        'Emotion Analysis Visualization': '<span>t-SNE</span><span>PCA</span>',
        'Cognitive State Visualization': '<span>BERT</span><span>LSTM</span>',
        'Dimensionality Reduction Visualization': '<span>UMAP</span><span>Clustering</span>',
        'Temporal Emotion Tracking': '<span>LSTM</span><span>Attention</span>',
        'Feature Correlation Analysis': '<span>Librosa</span><span>SHAP</span>'
    };
    return tags[alt] || '';
}