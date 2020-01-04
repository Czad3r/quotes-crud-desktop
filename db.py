import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY, text text, author CHAR(50), source CHAR(50), date DATE)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM quotes")
        rows = self.cur.fetchall()
        return rows

    def insert(self, text, author, source, date):
        self.cur.execute("INSERT INTO quotes VALUES (NULL, ?, ?, ?, ?)",
                         (text, author, source, date))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM quotes WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, text, author, source, date):
        self.cur.execute("UPDATE quotes SET text = ?, author = ?, source = ?, date = ? WHERE id = ?",
                         (text, author, source, date, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


#db = Database('store.db')
#db.insert("Lepiej zaliczać się do niektórych, niż do wszystkich.", "Andrzej Sapkowski", "Krew elfów", None)
#db.insert("Nigdy nie ma się drugiej okazji, żeby zrobić pierwsze wrażenie.", "Andrzej Sapkowski", "Miecz przeznaczenia", None)
#db.insert("Lepiej bez celu iść naprzód niż bez celu stać w miejscu, a z pewnością o niebo lepiej, niż bez celu się cofać.", "Andrzej Sapkowski", "Wieża jaskółki", None)
#db.insert("Ludzie (...) lubią wymyślać potwory i potworności. Sami sobie wydają się wtedy mniej potworni (...) Wtedy jakoś lżej im się robi na sercu. I łatwiej im żyć.", "Andrzej Sapkowski", "Ostatnie życzenie", None)
#db.insert("Zło to zło. Mniejsze, większe, średnie, wszystko jedno, proporcje są umowne a granice zatarte (…), jeżeli mam wybierać pomiędzy jednym złem a drugim, to wolę nie wybierać wcale.", "Andrzej Sapkowski", "Mniejsze zło", None)

