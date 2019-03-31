# junction-march-bot
The bot was written for the first March Online Challenge by Junction. Its purpose is to cheer people up with randomly generated motivational images and games to play with.
It was written completely in Python using the framework Bottle, and some libraries like NumPy and PIL.
The quote database comes from https://github.com/mubaris/motivate.

The bot works in Telegram, and it has the following commands:

    /motivate - Motivational image with a real quote (random pick from database)
    /bullshit - Motivational image with one of the bot's wise thoughts. (Markov-chain based text generation from the quote database)
    /games - List the available games with the bot to cheer you up.
    /flipacoin {heads|tails}* - Play "Flip a Coin" with the bot!
    /guess {number} - THe bot will think of a random number, you have to guess it.
    /rps {rock|paper|scissors} - Play "Rock, Paper, Scissors" with the bot!

You can contact me at rabigabor@gmail.com

The bot's telegram link: https://web.telegram.org/#/im?p=@BotivatorBot
