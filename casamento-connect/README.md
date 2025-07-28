# 💍 Casamento Connect — Sistema de Presença e Presentes Online

**Casamento Connect** é uma aplicação web desenvolvida com Django, HTML, CSS e JavaScript, que permite aos noivos gerenciar convidados, confirmar presença, cadastrar acompanhantes e organizar a reserva de presentes — tudo em uma interface prática e responsiva.

---

## 🛠 Tecnologias Utilizadas

- **Django (Python)** — back-end estruturado e seguro
- **HTML & CSS (Tailwind)** — interface moderna e responsiva
- **JavaScript** — interações e ações dinâmicas
- **SQLite/PostgreSQL** — banco de dados relacional
- **Git & GitHub** — versionamento de código
- **Python** — lógica e integrações backend

---

## 🎁 Funcionalidades

- ✅ Cadastro de convidados com número de acompanhantes
- ✅ Geração automática de link exclusivo (via token)
- ✅ Confirmação de presença (Confirmar ou Recusar)
- ✅ Reserva de presentes com prioridade visual
- ✅ Cadastro de acompanhantes vinculados ao convidado
- ✅ Visualização dos presentes reservados e disponíveis

---

## ▶ Como Executar o Projeto Localmente

bash
# Clone o repositório
git clone git@github.com:Roberto-Manuel818/casamento-connect.git
cd casamento-connect

# Crie o ambiente virtual (opcional)
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py makemigrations
python manage.py migrate

# Inicie o servidor
python manage.py runserver


Acesse o projeto no navegador em [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

*👤 Autor*

Desenvolvido por *Roberto Manuel*
📧 [roberto.programadortech@outlook.com.br](mailto:roberto.programadortech@outlook.com.br)

*📌 Observação*

Este sistema foi criado para eventos de casamento, mas pode ser adaptado para aniversários, palestras, formaturas e eventos corporativos. Pronto para evoluir com novos módulos, como envio de convites por WhatsApp e painel administrativo.
