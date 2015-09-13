#!/usr/bin/env python
"""
factoid.py - Phenny/Sopal Fact Module
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import random, sqlite3, os;

stock_answers = [
    """I don't know.""",
    """Er...""",
    """shrug"""
]

def setup(self):
    homedir = self.config.homedir or '~/.bot'
    self.factoiddb = os.path.join(homedir, 'factoids.db')
    conn = sqlite3.connect(self.factoiddb)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS factoids (word varchar PRIMARY KEY, fact varchar)""")
    conn.commit()

def get_fact(conn, subject):
    c = conn.cursor()
    c.execute("""SELECT fact FROM factoids WHERE word=?""", (subject,))
    answer = c.fetchone()
    if answer:
        return answer[0]
    return


def question(bot, input): 
    """Answers a question."""
    question = input.group(1)
    conn = sqlite3.connect(bot.factoiddb)
    word = get_fact(conn, question)
    if word:
        bot.say(question + " is " + word)
    else:
        bot.say(random.choice(stock_answers))
question.rule = '$nick\s*(.*)\?\s*$'
question.example = '$nickname: grass?'
question.priority = 'medium'

def factoid(bot, input):
    """A database of facts"""

    no      = input.group(1)
    subject = input.group(2)
    also    = input.group(3)
    factoid = input.group(4)

    conn = sqlite3.connect(bot.factoiddb)

    oldfactoid = get_fact(conn, subject)

    c = conn.cursor()

    if no:
        c.execute("""INSERT OR REPLACE INTO factoids values(?,?)""", (subject,factoid))
        conn.commit()
    elif also:
        if not oldfactoid:
            bot.say("I'm not familiar with ".append(subject))
            return
        newfactoid = " or ".join((oldfactoid, factoid))
        c.execute("""REPLACE INTO factoids values(?,?)""",(subject, newfactoid))
        conn.commit()
    elif oldfactoid:
        bot.say("But %s is %s..." % (subject, oldfactoid))
        return
    else:
        c.execute("""INSERT INTO factoids values(?, ?)""", (subject, factoid))
        conn.commit()
    bot.say('ok')
factoid.rule = '$nick\s*(no, )?(.+?) is (also )?(.*[^?])$'
factoid.example = '$nickname: grass is green'
factoid.priority = 'medium'

def forget(bot, input):
    """Forget a fact"""
    subject = input.group(2)
    conn = sqlite3.connect(bot.factoiddb)
    c = conn.cursor()
    try:
        c.execute("""DELETE FROM factoids WHERE word=?""", (subject,))
        conn.commit()
        bot.say("I don't remember what %s is" % (subject,))
    except:
        bot.say('err...')
forget.commands = ['forget']
forget.priority = 'medium'
# forget.example = 'forget grass'


if __name__ == '__main__': 
   print __doc__.strip()
