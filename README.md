🛡️ CyberShield SIEM
Mini SIEM Profissional com Detecção de Ameaças em Tempo Real
<br> <p align="center"> <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow" /> <img src="https://img.shields.io/badge/python-3.10%2B-blue" /> <img src="https://img.shields.io/badge/fastapi-modern-green" /> <img src="https://img.shields.io/badge/security-SIEM-red" /> </p> <br> <p align="center"> <a href="#-sobre-o-projeto">📖 Sobre</a> &nbsp;&nbsp;•&nbsp;&nbsp; <a href="#-objetivos">🎯 Objetivos</a> &nbsp;&nbsp;•&nbsp;&nbsp; <a href="#-tecnologias-utilizadas">⚙️ Tecnologias</a> &nbsp;&nbsp;•&nbsp;&nbsp; <a href="#-como-executar-o-projeto">🚀 Executar</a> &nbsp;&nbsp;•&nbsp;&nbsp; <a href="#-autor">👨‍💻 Autor</a> </p>
<br>
📖 Sobre o Projeto

O CyberShield SIEM é um sistema de Security Information and Event Management (SIEM) desenvolvido com foco educacional e profissional, simulando um ambiente real de monitoramento de segurança cibernética.

<br>
🔍 A aplicação permite:
📊 Monitorar eventos de segurança em tempo real
🚨 Detectar ataques automaticamente (ex: brute force)
🧠 Mapear ameaças com base no framework MITRE ATT&CK
📈 Visualizar dados através de dashboards interativos
🧪 Simular ataques para fins de teste
<br>
💡 Este projeto demonstra:
Backend moderno
Segurança da informação
Arquitetura de software
Análise de eventos
<br>
🎯 Objetivos
Criar um SIEM funcional simplificado
Demonstrar conceitos de:
Detecção de intrusão
Correlação de eventos
Inteligência de ameaças
Construir um projeto forte para portfólio
Simular cenários reais de segurança
Permitir expansão futura (IA, Machine Learning, etc.)
<br>
⚙️ Tecnologias Utilizadas
🧠 Backend
FastAPI → API moderna e performática
SQLModel → ORM simples e eficiente
SQLite → Banco leve e fácil de usar
JWT + bcrypt → Autenticação segura
<br>
🎨 Frontend
Jinja2 → Templates dinâmicos
Tailwind CSS + DaisyUI → Interface moderna
HTMX → Interatividade sem complexidade
Chart.js → Gráficos interativos
<br>
🔐 Segurança
Rule-based detection engine
Mapeamento MITRE ATT&CK
Simulação de ataques
<br>
🏗️ Arquitetura do Projeto
cybershield-siem/
├── app/
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── templates/
│   └── main.py
├── logs/
├── tests/
├── Dockerfile
├── docker-compose.yml
└── README.md
<br>

Arquitetura baseada em:

Separação de responsabilidades
Clean Code
Escalabilidade
<br>
🚀 Como Executar o Projeto
🔧 1. Clone o repositório
git clone https://github.com/Adriano-Dev22/cybershield.git
cd cybershield
<br>
🐍 2. Crie e ative o ambiente virtual
Linux/Mac:
python -m venv venv
source venv/bin/activate
Windows:
python -m venv venv
venv\Scripts\activate
<br>
📦 3. Instale as dependências
pip install -r requirements.txt
<br>
▶️ 4. Execute o projeto
uvicorn app.main:app --reload
<br>
🌐 5. Acesse no navegador
Sistema: http://localhost:8000
Documentação: http://localhost:8000/docs
<br>
🧪 Funcionalidades
✅ Autenticação de usuários (JWT)
✅ Dashboard interativo
✅ Detecção de brute force
✅ Geração de logs fake
✅ Upload de logs
✅ Alertas automáticos
✅ Mapeamento MITRE ATT&CK
✅ API documentada (Swagger)
<br>
📊 Roadmap Futuro
 Integração com Machine Learning 🤖
 WebSockets para tempo real 🔴
 Banco PostgreSQL 🐘
 Deploy em cloud (AWS/GCP) ☁️
 Sistema de usuários avançado 👥
<br>
👨‍💻 Autor

Claudemir Adriano de Albuquerque Silva

🎓 Sistemas de Informação – CESAR School
🚀 Focado em tecnologia, segurança e inovação

<br>
⭐ Contribuição

Sinta-se à vontade para contribuir:

git checkout -b feature/minha-feature
git commit -m "feat: minha melhoria"
git push origin feature/minha-feature
<br>
📜 Licença

Este projeto está sob a licença MIT.

<br>
💡 Inspiração

Inspirado em sistemas reais de SIEM utilizados para:

Monitoramento de ameaças
Resposta a incidentes
Segurança corporativa
