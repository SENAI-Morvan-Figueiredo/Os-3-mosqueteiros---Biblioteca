const editarBtns = document.querySelectorAll('.editarBtn');
const salvarBtn = document.getElementById('salvarBtn');

// Desativa todos os inputs no início
const inputs = document.querySelectorAll('.campo-perfil input');
const labels = document.querySelectorAll('.campo-perfil label');

inputs.forEach(input => input.disabled = true);
labels.forEach(l => l.style.color = '#00000075');

editarBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const currentBtn = e.currentTarget;

        // pega o wrapper do campo
        const wrapper = currentBtn.closest('.campo-perfil') || currentBtn.parentElement;

        // agora só o input desse wrapper
        const input = wrapper ? wrapper.querySelector('input') : currentBtn.previousElementSibling;

        if (!input){
            console.warn('Input não encontrado para botão', currentBtn);
            return;
        }

        // desativa todos
        inputs.forEach(i => i.disabled = true);
        labels.forEach(l => l.style.color = '#00000075');

        // ativa apenas o input clicado
        input.disabled = false;

        // pega o label correspondente e destaca
        const label = wrapper ? wrapper.querySelector('label') : input.previousElementSibling;
        if (label){
            label.style.color = "#000";
        }

        // mostra o botão salvar
        if (salvarBtn){
            salvarBtn.style.display = 'inline';
        }

        // foca no campo ativado
        input.focus();

        const length = input.value.length;
        input.setSelectionRange(length, length);

    });
});

// Confirmação antes de enviar
document.getElementById('perfilForm').addEventListener('submit', (e) => {
    inputs.forEach(i => i.disabled = false);

    if (!confirm("Tem certeza que quer alterar este campo?")) {
        e.preventDefault();
    }
    
});

const animacaoCpf = document.getElementById('animacao-cpf');

// Quando passar o mouse
animacaoCpf.addEventListener('mouseenter', () => {
    document.getElementById('aviso-cpf').classList.add('mover');
    document.getElementById('exclamacao').classList.add('apagar');
});

// Quando tirar o mouse (se quiser voltar ao normal)
animacaoCpf.addEventListener('mouseleave', () => {
    document.getElementById('aviso-cpf').classList.remove('mover');
    document.getElementById('exclamacao').classList.remove('apagar');
});


