FROM python:3.9

COPY discord_bot ./discord_bot
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

CMD [ "python", "-m", "discord_bot.main"]