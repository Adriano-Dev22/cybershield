# ============================================================
# CyberShield — Makefile
# ============================================================

.PHONY: run dev test lint format install clean help

# Roda o servidor em produção
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

# Roda o servidor em modo desenvolvimento (reload automático)
dev:
	uvicorn app.main:app --reload --port 8000

# Instala as dependências
install:
	pip install -r requirements.txt

# Roda os testes
test:
	pytest tests/ -v

# Roda os testes com cobertura
test-cov:
	pytest tests/ -v --cov=app --cov-report=term-missing

# Lint com ruff
lint:
	ruff check app/

# Formata o código
format:
	ruff format app/

# Limpa arquivos temporários
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache .coverage htmlcov .ruff_cache

# Docker
docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

# Ajuda
help:
	@echo ""
	@echo "CyberShield — Available commands:"
	@echo ""
	@echo "  make run        Run production server"
	@echo "  make dev        Run development server with auto-reload"
	@echo "  make install    Install dependencies"
	@echo "  make test       Run tests"
	@echo "  make test-cov   Run tests with coverage report"
	@echo "  make lint       Lint code with ruff"
	@echo "  make format     Format code with ruff"
	@echo "  make clean      Remove temporary files"
	@echo "  make docker-up  Build and start Docker containers"
	@echo "  make docker-down Stop Docker containers"
	@echo ""
