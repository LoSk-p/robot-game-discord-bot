FROM python:3.9

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY discord_bot ./discord_bot

CMD [ "python", "-m", "discord_bot.main"]