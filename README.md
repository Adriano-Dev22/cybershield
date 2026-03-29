# 🛡️ CyberShield SIEM

**SIEM Profissional com Detecção de Ameaças em Tempo Real**

<p align="center">
  <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow" alt="Status" />
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python" />
  <img src="https://img.shields.io/badge/fastapi-modern-green" alt="FastAPI" />
  <img src="https://img.shields.io/badge/security-SIEM-red" alt="SIEM" />
</p>

<p align="center">
  <a href="#-sobre-o-projeto">📖 Sobre</a> • 
  <a href="#-objetivos">🎯 Objetivos</a> • 
  <a href="#-tecnologias-utilizadas">⚙️ Tecnologias</a> • 
  <a href="#-como-executar">🚀 Como Executar</a> • 
  <a href="#-funcionalidades">🧪 Funcionalidades</a> • 
  <a href="#-roadmap-futuro">📊 Roadmap</a> • 
  <a href="#-autor">👨‍💻 Autor</a>
</p>

---

## 📖 Sobre o Projeto

O **CyberShield SIEM** é um sistema de *Security Information and Event Management* (SIEM) desenvolvido com foco educacional e profissional. Ele simula um ambiente real de monitoramento e resposta a ameaças cibernéticas.

A aplicação permite monitorar eventos de segurança em tempo real, detectar ataques automaticamente e visualizar tudo através de dashboards interativos.

---

## 🎯 Objetivos

- Criar um SIEM funcional e simplificado
- Demonstrar conceitos avançados de segurança cibernética
- Praticar **detecção de intrusão**, **correlação de eventos** e **inteligência de ameaças**
- Construir um projeto robusto para portfólio
- Servir como base para expansões futuras (Machine Learning, WebSockets, etc.)

---

## ⚙️ Tecnologias Utilizadas

### 🧠 Backend
- **FastAPI** — API moderna, rápida e com excelente documentação
- **SQLModel** — ORM simples e tipado
- **SQLite** — Banco de dados leve (fácil de usar em desenvolvimento)
- **JWT + bcrypt** — Autenticação segura

### 🎨 Frontend
- **Jinja2** — Templates dinâmicos
- **Tailwind CSS + DaisyUI** — Interface moderna e responsiva
- **HTMX** — Interatividade sem JavaScript pesado
- **Chart.js** — Gráficos interativos

### 🔐 Segurança
- Motor de detecção baseado em regras
- Mapeamento com framework **MITRE ATT&CK**
- Simulação de ataques para testes

---

## 🏗️ Arquitetura do Projeto

```bash
cybershield-siem/
├── app/
│   ├── models/          # Modelos de dados
│   ├── routers/         # Rotas da API
│   ├── services/        # Lógica de negócio e detecção
│   ├── templates/       # Templates Jinja2
│   └── main.py
├── logs/                # Armazenamento de logs
├── tests/               # Testes automatizados
├── Dockerfile
├── docker-compose.yml
└── README.md
Princípios adotados:

Separação clara de responsabilidades
Clean Code
Facilidade de manutenção e escalabilidade


🚀 Como Executar o Projeto
1. Clone o repositório
Bashgit clone https://github.com/Adriano-Dev22/cybershield.git
cd cybershield
2. Crie e ative o ambiente virtual
Linux / macOS:
Bashpython -m venv venv
source venv/bin/activate
Windows:
Bashpython -m venv venv
venv\Scripts\activate
3. Instale as dependências
Bashpip install -r requirements.txt
4. Execute o servidor
Bashuvicorn app.main:app --reload
5. Acesse a aplicação

Sistema:http://localhost:8000
Documentação Swagger:http://localhost:8000/docs


🧪 Funcionalidades
✅ Autenticação de usuários com JWT
✅ Dashboard interativo com gráficos
✅ Detecção automática de brute force
✅ Geração de logs falsos para testes
✅ Upload de logs
✅ Alertas em tempo real
✅ Mapeamento de ameaças com MITRE ATT&CK
✅ API totalmente documentada (Swagger)

📊 Roadmap Futuro

Integração com Machine Learning 🤖
Suporte a WebSockets para monitoramento em tempo real 🔴
Migração para PostgreSQL 🐘
Deploy em nuvem (AWS / GCP / Docker) ☁️
Sistema de usuários com roles e permissões 👥
Relatórios avançados em PDF


👨‍💻 Autor
Claudemir Adriano de Albuquerque Silva

🎓 Sistemas de Informação – CESAR School
🚀 Apaixonado por tecnologia, segurança cibernética e inovação


⭐ Contribuição
Contribuições são bem-vindas!

Faça um fork do projeto
Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade)
Commit suas mudanças (git commit -m 'feat: adiciona nova funcionalidade')
Push para a branch (git push origin feature/nova-funcionalidade)
Abra um Pull Request


📜 Licença
Este projeto está sob a licença MIT.

💡 Inspiração
Inspirado em sistemas profissionais de SIEM utilizados em:

Monitoramento contínuo de ameaças
Resposta a incidentes de segurança
Ambientes corporativos de alta segurança
