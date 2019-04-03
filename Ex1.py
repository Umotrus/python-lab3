
# Exercise 1

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction


def start(bot, update):
    update.message.reply_text("Hello! Please issue commands in this format:\n")
    update.message.reply_text("1. /showTasks\n"
                              "2. /newTask <task to add>\n"
                              "3. /removeTask <task to remove>\n"
                              "4. /removeAllTasks <substring to use to remove all the tasks that contain it>\n")


def save():
    file = open("task_list.txt", 'w')
    for task in task_list:
        file.write(task)
    file.close()
    return


def unknownMessage(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("I'm sorry I can't do that.")


def showTasks(bot, update):
    """
    Show existing tasks
    :return:
    """
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("To do list:\n")
    for task in sorted(task_list):
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text(task, end="")


def buidString(words):
    ret = ""
    for word in words:
        ret = ret + " " + word
    return ret.strip()


def newTask(bot, update, args):
    """
    Add a new task to the list
    :return:
    """

    if args is not None:
        task_list.append(buidString(args) + "\n")
        save()
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("New task added successfully")


def remove_all(bot, update, args):
    """
    Remove an existing task from the list
    :return:
    """
    if args is None:
        return

    to_be_removed = []

    task = buidString(args)
    for element in task_list:
        if task in element:
            to_be_removed.append(element)

    if to_be_removed.__sizeof__() == 0:
        update.message.reply_text("Task %s is not in the list" % task)
    else:
        for element in to_be_removed:
            task_list.remove(element)
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("Task(s) Removed")
    save()


def remove_task(bot, update, args):

    if args is None:
        return

    task = buidString(args) + "\n"
    if task in task_list:
        task_list.remove(task)
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("Task Removed")
    else:
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("Task is not in the list")


def main():
    """
    The bot will help you manage your tasks
    """

    file = open("task_list.txt")

    for line in file:
        task_list.append(line)

    file.close()

    updater = Updater(token='')

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("showTasks", showTasks))
    dp.add_handler(CommandHandler("newTask", newTask, pass_args=True))
    dp.add_handler(CommandHandler("removeTask", remove_task, pass_args=True))
    dp.add_handler(CommandHandler("removeAllTasks", remove_all, pass_args=True))
    dp.add_handler(MessageHandler(Filters.all, unknownMessage))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    task_list = []
    main()
