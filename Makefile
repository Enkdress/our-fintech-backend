UV = uv

.PHONY: install dev test add

install:
	$(UV) sync

dev:
	$(UV) run uvicorn app.main:app --reload

test:
	$(UV) run pytest

add:
	$(UV) add $(pkg)

add-dev:
	$(UV) add --dev $(pkg)
