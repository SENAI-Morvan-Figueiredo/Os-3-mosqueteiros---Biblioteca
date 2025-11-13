# Os-3-mosqueteiros---Biblioteca

Código para gerar uma multa pelo 'py manage.py shell':

from Biblioteca.models import Emprestimos
from User.models import Usuario
from django.utils import timezone
import datetime

usuario = Usuario.objects.first()
hoje = timezone.now().date()
data_atrasada = hoje - datetime.timedelta(days=20)

# Cria um novo empréstimo atrasado
emprestimo_teste = Emprestimos.objects.create(
    id_user=usuario,
    id_livro_id=1,  # ajuste o ID conforme um livro existente
    status="Retirado"
)

# Força a data de empréstimo antiga
Emprestimos.objects.filter(id=emprestimo_teste.id).update(data_emprestimo=data_atrasada)

print("Empréstimo de teste criado com sucesso!")
