
const editarBtns = document.querySelectorAll('.editarBtn');
const salvarBtn = document.getElementById('salvarBtn');

// Desativa todos os inputs no início
const inputs = document.querySelectorAll('.campo-perfil input');
inputs.forEach(input => input.disabled = true);

editarBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const input = e.target.previousElementSibling;

        // Desativa todos os outros inputs
        inputs.forEach(i => i.disabled = true);

        // Ativa apenas o input clicado
        input.disabled = false;
        input.focus();

        // Mostra o botão salvar
        salvarBtn.style.display = 'inline';
    });
});

// Confirmação antes de enviar
document.getElementById('perfilForm').addEventListener('submit', (e) => {
    if (!confirm("Tem certeza que quer alterar este campo?")) {
        e.preventDefault();
    }
});

