const links = document.querySelectorAll('.sub-header a');
const urlAtual = window.location.pathname;


links.forEach(link => {
    if (urlAtual.includes(link.getAttribute('href'))){
        link.classList.add('sub-header-btn-ativo');
    }
    });
