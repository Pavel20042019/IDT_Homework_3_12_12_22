from multiprocessing import Process, Queue
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler
from time import perf_counter
from roots import *
ids = {}
with open('messages.txt') as f:
    messages = f.read().split(';')
queue = Queue()
errors = Queue()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global ids, messages
    ids[context._user_id] = 0
    await update.message.reply_text(messages[0])


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global ids, messages
    await update.message.reply_text(messages[1])


async def reply_roots(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global ids, messages
    ids[context._user_id] = 1
    await update.message.reply_text(messages[2] + 'корней.')


async def reply_min(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global ids, messages
    ids[context._user_id] = 2
    await update.message.reply_text(messages[2] + 'локальных минимумов.')


async def reply_max(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global ids, messages
    ids[context._user_id] = 3
    await update.message.reply_text(messages[2] + 'локальных максимумов.')


def process(q: Queue, e: Queue, f) -> None:
    args = q.get()
    try:
        q.put(f(args[0], float(args[1]), float(args[2])))
        e.put(False)
    except:
        e.put(True)
        pass


def work(args: list[str], f) -> Process:
    global queue, errors
    queue.put(args)
    p = Process(target=process, args=(queue, errors, f))
    p.start()
    s = perf_counter()
    while perf_counter() < s + 10.0 and p.is_alive():
        pass
    return p


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global ids, messages, queue, errors
    if context._user_id in ids:
        args = update.message.text.split('\n')
        match ids[context._user_id]:
            case 0:
                answer = messages[3]
            case 1:
                p = work(args, answer_roots)
                if p.is_alive():
                    p.kill()
                    answer = messages[4]
                else:
                    if errors.get():
                        answer = messages[5]
                    else:
                        ans = queue.get()
                        answer = messages[6] if len(
                            ans) > 10 else 'Корни: {' + ', '.join(map(str, ans)) + '}.'
            case 2:
                p = work(args, answer_min)
                if p.is_alive():
                    p.kill()
                    answer = messages[4]
                else:
                    if errors.get():
                        answer = messages[5]
                    else:
                        ans = queue.get()
                        answer = messages[6] if len(ans) > 10 else 'Локальные минимумы: {' + ', '.join(
                            '(' + str(m[0]) + '; ' + str(m[1]) + ')' for m in ans) + '}.'
            case 3:
                p = work(args, answer_max)
                if p.is_alive():
                    p.kill()
                    answer = messages[4]
                else:
                    if errors.get():
                        answer = messages[5]
                    else:
                        ans = queue.get()
                        answer = messages[6] if len(ans) > 10 else 'Локальные максимумы: {' + ', '.join(
                            '(' + str(m[0]) + '; ' + str(m[1]) + ')' for m in ans) + '}.'
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text(messages[3])
with open('token.txt') as f:
    token = str(*f)
application = Application.builder().token(token).build()
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('help', help))
application.add_handler(CommandHandler('roots', reply_roots))
application.add_handler(CommandHandler('min', reply_min))
application.add_handler(CommandHandler('max', reply_max))
application.add_handler(MessageHandler(
    filters.TEXT & ~ filters.COMMAND, reply))
application.run_polling()
