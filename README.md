## Run Docker
```bash
docker build -t discord_bot .
docker run --name robot_game_bot --detach -v $PWD/discord_bot/data:/discord_bot/data discord_bot
```

## Run Python script
```bash
python3.9 -m discord_bot.main
```

## Tests
Run tests:
```bash
python3.9 -m pytest -v tests
```