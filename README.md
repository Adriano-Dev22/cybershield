🛡️ CyberShield SIEM
Mini SIEM Profissional com Detecção de Ameaças em Tempo Real
<p align="center"> <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow" /> <img src="https://img.shields.io/badge/python-3.10%2B-blue" /> <img src="https://img.shields.io/badge/fastapi-modern-green" /> <img src="https://img.shields.io/badge/security-SIEM-red" /> </p> <p align="center"> <a href="#-sobre-o-projeto"><button>📖 Sobre</button></a> <a href="#-objetivos"><button>🎯 Objetivos</button></a> <a href="#-tecnologias"><button>⚙️ Tecnologias</button></a> <a href="#-como-executar"><button>🚀 Executar</button></a> <a href="#-autor"><button>👨‍💻 Autor</button></a> </p>
📖 Sobre o Projeto

O CyberShield SIEM é um sistema de Security Information and Event Management desenvolvido com foco educacional e profissional, simulando um ambiente real de monitoramento de segurança cibernética.

A aplicação permite:

📊 Monitorar eventos de segurança em tempo real
🚨 Detectar ataques automaticamente (ex: brute force)
🧠 Mapear ameaças com base no framework MITRE ATT&CK
📈 Visualizar dados através de dashboards interativos
🧪 Simular ataques para fins de teste

Este projeto foi projetado para demonstrar habilidades avançadas em:

Backend moderno
Segurança da informação
Arquitetura de software
Análise de dados e eventos
🎯 Objetivos
Criar um SIEM funcional simplificado
Demonstrar conceitos de:
Detecção de intrusão
Correlação de eventos
Inteligência de ameaças
Construir um projeto de alto nível para portfólio
Simular cenários reais de segurança
Facilitar expansão futura (IA, machine learning, etc.)
⚙️ Tecnologias Utilizadas
🧠 Backend
FastAPI → API moderna e performática
SQLModel → ORM simples e eficiente
SQLite → Banco leve (facilmente migrável)
JWT + bcrypt → Autenticação segura
🎨 Frontend
Jinja2 → Templates dinâmicos
Tailwind CSS + DaisyUI → UI moderna
HTMX → Interatividade sem JS pesado
Chart.js → Gráficos interativos
🔐 Segurança
Rule-based detection engine
Mapeamento MITRE ATT&CK
Simulação de ataques
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

Arquitetura baseada em:

Separação de responsabilidades
Clean Code
Escalabilidade
🚀 Como Executar o Projeto
🔧 1. Clone o repositório
git clone https://github.com/seu-usuario/cybershield-siem.git
cd cybershield-siem
🐍 2. Crie e ative o ambiente virtual
Linux/Mac:
python -m venv venv
source venv/bin/activate
Windows:
python -m venv venv
venv\Scripts\activate
📦 3. Instale as dependências
pip install -r requirements.txt
▶️ 4. Execute o projeto
uvicorn app.main:app --reload
🌐 5. Acesse no navegador
Sistema: http://localhost:8000
Documentação da API: http://localhost:8000/docs
🧪 Funcionalidades
✅ Autenticação de usuários (JWT)
✅ Dashboard interativo
✅ Detecção de brute force
✅ Geração de logs fake
✅ Upload de logs
✅ Alertas automáticos
✅ Mapeamento MITRE ATT&CK
✅ API documentada (Swagger)
📊 Roadmap Futuro
 Integração com Machine Learning 🤖
 WebSockets para tempo real real 🔴
 Banco PostgreSQL 🐘
 Deploy em cloud (AWS/GCP) ☁️
 Sistema de usuários avançado 👥
👨‍💻 Autor

Claudemir Adriano de Albuquerque Silva

🎓 Estudante de Sistemas de Informação – CESAR School
🚀 Focado em tecnologia, segurança e inovação

💼 Futuro líder em tecnologia e empreendedorismo

⭐ Contribuição

Sinta-se livre para contribuir com melhorias!

# Fork
# Crie uma branch
git checkout -b feature/minha-feature

# Commit
git commit -m "feat: minha melhoria"

# Push
git push origin feature/minha-feature
📜 Licença

Este projeto está sob a licença MIT.

💡 Inspiração

Projeto inspirado em sistemas reais de SIEM utilizados por empresas para:

Monitoramento de ameaças
Resposta a incidentes
Segurança corporativa
🚀 Destaque

