start:
	@echo "starting local server... 🦄⚡️"
	uvicorn src.app.main:app --reload --port 8000

black:
	@echo "Black formatting files...✅ 🤩"
	python -m black ./src
