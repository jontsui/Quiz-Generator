import sqlite3
from tex_tools import *

'''This block is setup code for interfacing with the database'''
conn = sqlite3.connect('C:\\Users\\JT\\Desktop\\SQLite\\math_questions.db')

def dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d

conn.row_factory = dict_factory
cur = conn.cursor()

def get_question_data(id):
	cur.execute('SELECT q_text, a.* from questions q INNER JOIN answers a ON q.id = a.id where q.id = (?);', (str(id),) )
	return cur.fetchone()	#This gets the dictionary out of the cursor object
'''End of setup block'''

class question:
	def __init__(self, id): 
		self.data = get_question_data(id)
		self.q_text = self.data['q_text']	#Makes it slightly easier to reference a specific column


q = question(1)



#Start of test code

def make_question_list(id_list): 
	question_list = [question(id) for id in id_list]

	return question_list

question_list = make_question_list(range(1, 6))

d = document()
d.preamble.add(r'''\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5em}
\usepackage{amsmath})
''')

body_text = ''
for question in question_list:
	body_text += question.q_text + '\n\n'

d.body.add(body_text)

with open(r'tex_output\math_questions.tex', 'w+') as f:
	f.write(str(d))




