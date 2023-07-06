extract:
	pybabel extract --input-dirs=. -o locales/ApiSwipeBot.pot

update:
	pybabel update -d locales -D API_SWIPE -i locales/ApiSwipeBot.pot

init:
	pybabel init -i locales/ApiSwipeBot.pot -d locales -D ApiSwipeBot -l en

compile:
	pybabel compile -d locales -D ApiSwipeBot

run:
	pybabel compile -d locales -D ApiSwipeBot
	python bot.py