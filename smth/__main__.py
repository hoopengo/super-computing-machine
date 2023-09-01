import re
from os import getenv

from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.types import PeerChannel, ReactionEmoji

load_dotenv()

api_id = getenv("api_id")
api_hash = getenv("api_hash")
client = TelegramClient("my_account", api_id, api_hash)
client.flood_sleep_threshold = 300

mihail = 1546741872
budda = 5786492862

# Replace offensive words with an empty string
offensive_words = {
    r"\bбля\b": "быб",
    r"\bблять\b": "быбь",
    r"\bблядть\b": "быбдь",
    r"\bблядь\b": "быб",
    r"\bсука\b": "сус",
    r"\bебал\b": "манул",
    r"\bебанулся\b": "манулся",
    r"\bебался\b": "манулался",
    r"\bтрахать\b": "мануловать",
    r"\bпиздец\b": "копец",
    r"\bкурва\b": "корова",
    r"\bдолбоеб\b": "мозгоеб",
    r"\bмудак\b": "мудрец",
    r"\bуебище\b": "улучшение",
    r"\bговно\b": "гречка",
    r"\bгондон\b": "гончар",
    r"\bсрака\b": "сосиска",
    r"\bхерня\b": "хлеб",
    r"\bмочалка\b": "молоко",
    r"\bдрочить\b": "дроздить",
    r"\bзалупа\b": "бебра",
    r"\bговнюк\b": "гонщик",
    r"\bхуй\b": "хух",
    r"\bдрочиться\b": "друзиться",
    r"\bебучий\b": "учебный",
    r"\bгандон\b": "гангстер",
    r"\bпенис\b": "пенсия",
    r"\bсоси\b": "сосиска",
    r"\bхуйня\b": "фигня",
    r"\bхуйню\b": "фигню",
    r"\bАпездал\b": "Дилитант",
    r"\bАпездошенная\b": "Удивлённая",
    r"\bБлядь\b": "Девушка лёгкого поведения",
    r"\bБлядство\b": "Беспредел,неразбериха",
    r"\bВыебон\b": "Хвастовство,показуха",
    r"\bВыебать\b": "Совершить половой акт",
    r"\bВхуюжить\b": "Воткнуть",
    r"\bГомосек\b": "Голубой",
    r"\bДолбоёб\b": "Дурак",
    r"\bЕбло\b": "Лицо",
    r"\bЕблище\b": "Тоже что и ебло",
    r"\bЕбать\b": "Совершать половой акт",
    r"\bЕбическая сила\b": "сверхестественная сила",
    r"\bЕбунок\b": "Ребёнок",
    r"\bЕблан\b": "Дурак",
    r"\bЁбнуть\b": "Ударить",
    r"\bЁболызнуть\b": "Стукнуть",
    r"\bЕбош\b": "Груповой секс",
    r"\bЗаебал\b": "Надоел,достал",
    r"\bЗаебатый\b": "Хороший,отличный",
    r"\bЗлаебучий\b": "Нехороший,плохой",
    r"\bЗаёб\b": "Заскок,сдвиг по фазе",
    r"\bИди на хуй\b": "Отстанть, свободен",
    r"\bКолдоебина\b": "Большая вещь, препятствие",
    r"\bМанда\b": "Женские половые органы",
    r"\bМандовошка\b": "Малолетка",
    r"\bМокрощелка\b": "Девушка легкого поведения",
    r"\bНаебка\b": "Обман",
    r"\bНаебал\b": "Обманул",
    r"\bНаебаловка\b": "Хитрость, уловка",
    r"\bНапиздеть\b": "Соврать, обмануть",
    r"\bОтъебись\b": "Отстань",
    r"\bОхуеть\b": "Удивиться",
    r"\bОтхуевертить\b": "Избить",
    r"\bОпизденеть\b": "Обнаглеть",
    r"\bОхуевший\b": "Обнаглевший",
    r"\bОтебукать\b": "Поколатить",
    r"\bПизда\b": "Женские половые органы",
    r"\bПидарас\b": "Голубой",
    r"\bПиздатый\b": "Хороший",
    r"\bПиздец\b": "Конец, смерть",
    r"\bПизданутый\b": "Дурной",
    r"\bПоебать\b": "Наплевать",
    r"\bПоебустика\b": "Рутина",
    r"\bПроебать\b": "Потерять",
    r"\bПодзалупный\b": "Опущенный",
    r"\bПизденыш\b": "Незначительный человек",
    r"\bПрипиздак\b": "Дуралей",
    r"\bРазъебать\b": "Разбить",
    r"\bРаспиздяй\b": "Развязанный человек, делающий все спустя рукава",
    r"\bРазъебанный\b": "Разбитый",
    r"\bСука\b": "Нехорошая женщина",
    r"\bСучка\b": "Уменьшительно-ласкательное от 'суки'",
    r"\bТрахать\b": "Совершать половой акт",
    r"\bУебок\b": "Отморозок",
    r"\bУебать\b": "Ударить",
    r"\bУгондошить\b": "Избить, убить, уничтожить",
    r"\bУебан\b": "То же что и 'уебок'",
    r"\bХитровыебанный\b": "Скользкий человек",
    r"\bХуй\b": "Мужской половой орган, личность мужского пола",
    r"\bХуйня\b": "Некий предмет, очень плохое",
    r"\bХуета\b": "Заморочка",
    r"\bХуево\b": "Плохо",
    r"\bХуесос\b": "Сосущий мужской член",
    r"\bХуеть\b": "удивляться, балдеть",
    r"\bХуевертить\b": "Бить, избивать",
    r"\bХуеглот\b": "Глотающий мужской член",
    r"\bХуистика\b": "Наука про....",
    r"\bЧленосос\b": "То же что и 'хуесос'",
    r"\bЧленоплет\b": "Балбес",
    r"\bШлюха\b": "Проститутка",
}


def filter_russian_offensive(text: str):
    # Use regular expressions to match complete words
    for word, replaces in offensive_words.items():
        text = re.sub(word, replaces, text, flags=re.IGNORECASE)

    return text


@client.on(events.NewMessage)
async def handle_message(event: events.NewMessage.Event):
    # Check if the message is from a user
    if event.sender_id == 876980354:
        # Filter the message text
        filtered_text = filter_russian_offensive(event.raw_text)

        # Send the filtered text back to the user
        if not filtered_text == event.raw_text:
            await event.edit(filtered_text)


async def spam_reaction():
    i = 0
    valid_messages_ids = []
    channel = PeerChannel(channel_id=1759079503)
    async for message in client.iter_messages(channel, from_user=budda):
        if message.reactions is not None and "🤔" in [
            result.reaction.emoticon for result in message.reactions.results
        ]:
            print("skipping")
            continue

        valid_messages_ids.append(message.id)
        if len(valid_messages_ids) > 100:
            break

    print(valid_messages_ids)

    for message_id in valid_messages_ids:
        i += 1
        await client(
            SendReactionRequest(
                peer=channel,
                msg_id=message_id,
                reaction=[ReactionEmoji(emoticon="🤔")],
            )
        )
        print(f"{i} 🤔")


with client:
    client.run_until_disconnected()
