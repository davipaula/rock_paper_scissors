dev:
	cd rock_paper_scissors && python -m uvicorn main:app --reload

run:
	cd rock_paper_scissors && python -m uvicorn main:app