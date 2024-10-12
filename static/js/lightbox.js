let currentImageIndex = 0;
let images = [];

function openLightbox(imageElement) {
    var lightbox = document.getElementById("lightbox");
    var lightboxImage = document.getElementById("lightbox-image");
    
    // Znajdź indeks klikniętego zdjęcia w liście wszystkich zdjęć
    images = Array.from(document.querySelectorAll('.post-image'));
    currentImageIndex = images.indexOf(imageElement);

    // Wyświetl kliknięte zdjęcie w lightboxie
    lightboxImage.src = imageElement.src;
    lightbox.style.display = "flex";  // Pokaż lightbox
}

function closeLightbox() {
    var lightbox = document.getElementById("lightbox");
    lightbox.style.display = "none";  // Ukryj lightbox
}

function nextImage(event) {
    event.stopPropagation();  // Zapobiega zamknięciu lightboxa
    currentImageIndex = (currentImageIndex + 1) % images.length;  // Cykl przez zdjęcia
    document.getElementById("lightbox-image").src = images[currentImageIndex].src;
}

function prevImage(event) {
    event.stopPropagation();  // Zapobiega zamknięciu lightboxa
    currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;  // Cykl w tył
    document.getElementById("lightbox-image").src = images[currentImageIndex].src;
}