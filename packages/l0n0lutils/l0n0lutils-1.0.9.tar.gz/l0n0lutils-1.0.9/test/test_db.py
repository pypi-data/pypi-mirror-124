import sys

sys.path.insert(0, ".")


from l0n0lutils.dbmysql import DbMysqlHelper

helper = DbMysqlHelper('192.168.3.2', 3306, 'root', '123', 'ttat')
helper.add_table("t1", """
`id` int not null auto_increment,
`data` varchar(123),
primary key (`id`)
""")
helper.create_tables()
helper.db.insert("t1", ['data'], ['aaab'])
ret = helper.db.select("t1", ['id', 'data'])
print(ret)
