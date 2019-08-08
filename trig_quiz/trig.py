import random
import re

def texify(input_string):
	''' Converts specific substrings of given string into valid latex symbols.
	Important!!! - This will probably break outside of the specific use cases 
	here (particularly replacement or parentheses with brackets) and does not 
	necessarily return fully valid latex code'''
	d = {
		'sin': '\\sin', 'cos': '\\cos', 'tan': '\\tan', 'csc': '\\csc', 'sec': '\\sec',
		'cot': '\\cot', 'pi' : '\\pi', 'sqrt': '\\sqrt',  '(': '{', ')': '}'
		}
	
	res = input_string
	for key in d:
		res = res.replace(key, d[key])

	return res


def tex_frac(input_string):
	''' Converts a fraction-like string into valid latex code for a fraction.  Numerator and 
	denominator should be delimited by a /'''
	if input_string.find('/') == -1:
		return input_string
	
	temp = input_string.split('/')    		#output: [numerator, denominator]
	temp = ''.join(['{' + x + '}' for x in temp])	#output: '{numerator}{denominator}'
	return '\\frac{}'.format(temp)

def value_dict(val_order): 								
		'''Returns a dictionary of angle -> value mappings for a specific trig
		function.
		
		Arguments: val_order is a list of values particular to the trig function'''
		
		angles = ['pi/6', 'pi/3', 'pi/4', '5pi/6', '2pi/3', '3pi/4',
				'7pi/6', '4pi/3', '5pi/4', '11pi/6', '5pi/3', '7pi/4']
		
		return dict(zip(angles, val_order))

class TrigFunction:
	def __init__(self):		
		pass

	def __str__(self):
		return self.name + '({})'.format(self.angle)

	def tex_repr(self):
		'''Return a string representing corresponding LaTeX representation of the 
		object's trig expression. Ex) sin()
		
		"name" and "angle" are attributes of the subclasses which inherit this
		method'''
		
		return '$' + texify(self.name) + tex_frac(texify(self.angle)) + '$'
	
	def tex_value(self):
		'''Return a string representing corresponding LaTeX representation of the
		object's value attribute'''
		
		return '$' + tex_frac(texify(self.value)) + '$'

class Sin(TrigFunction): 	
	name = 'sin'
	
	def __init__(self, angle):
		
		# Build {angle: value, ...} dictionary
		pos = ['1/2', 'sqrt(3)/2', 'sqrt(2)/2']
		neg = ['-1/2', '-sqrt(3)/2', '-sqrt(2)/2']
		val_order = pos + pos + neg + neg
		dict_ = value_dict(val_order)
		
		self.angle = angle
		self.value = dict_[angle]

class Csc(TrigFunction):
	name = 'csc'
	
	def __init__(self, angle):
		pos = ['2', '2/sqrt(3)', '2/sqrt(2)']
		neg = ['-2', '-2/sqrt(3)', '-2/sqrt(2)']
		val_order = pos + pos + neg + neg
		dict_ = value_dict(val_order)

		self.angle = angle
		self.value = dict_[angle]

class Cos(TrigFunction):
	name = 'cos'
	
	def __init__(self, angle):
		pos = ['sqrt(3)/2' , '1/2', 'sqrt(2)/2']
		neg = ['-sqrt(3)/2', '-1/2' , '-sqrt(2)/2']
		val_order = pos + neg + neg + pos
		dict_ = value_dict(val_order)

		self.angle = angle
		self.value = dict_[angle]

class Sec(TrigFunction):
	name = 'sec'

	def __init__(self, angle):
		pos = ['2/sqrt(3)' , '2', '2/sqrt(2)']
		neg = ['-2/sqrt(3)' , '-2', '-2/sqrt(2)']
		val_order = pos + neg + neg + pos
		dict_ = value_dict(val_order)

		self.angle = angle
		self.value = dict_[angle]
	
class Tan(TrigFunction):
	name = 'tan'
	
	def __init__(self, angle):
		pos = ['1/sqrt(3)' , 'sqrt(3)', '1']
		neg = ['-1/sqrt(3)' , '-sqrt(3)', '-1']
		val_order = pos + neg + pos + neg
		dict_ = value_dict(val_order)

		self.angle = angle
		self.value = dict_[angle]

class Cot(TrigFunction):	
	name = 'cot'
	
	def __init__(self, angle):
		pos = ['sqrt(3)' , '1/sqrt(3)', '1']
		neg = ['-sqrt(3)' , '-1/sqrt(3)', '-1']
		val_order = pos + neg + pos + neg
		dict_ = value_dict(val_order)

		self.angle = angle
		self.value = dict_[angle]

class TrigQuiz:
	'''An object representing a new trig quiz'''

	def __init__(self, *, weights):
		'''Arguments: 
		weights(required) is a dictionary of form {'sin': #, 'cos': #, ...} for the six trig functions
		representing how many questions of each type'''
		
		angles = ['pi/6', 'pi/3', 'pi/4', '5pi/6', '2pi/3', '3pi/4',
				'7pi/6', '4pi/3', '5pi/4', '11pi/6', '5pi/3', '7pi/4']
		trig_functions = [Sin, Cos, Tan, Csc, Sec, Cot]
		
		# Iterate through each trig function class and create a pool of n random objects 
		# specified by weights dictionary, then append those objects to object list
		self.obj_list = []
		for TrigClass in trig_functions:
			pool = [TrigClass(a) for a in angles]
			random.shuffle(pool)
			self.obj_list += random.sample(pool, weights[TrigClass.name])
			random.shuffle(self.obj_list)

		# Convert each object into its latex representation
		self.questions = [obj.tex_repr() for obj in self.obj_list]
		
		# Iterate through each trig object in questions and call the tex_value method
		self.answers = [obj.tex_value() for obj in self.obj_list]
		
	def create_quiz(self, template, output):
		with open(template) as f:
			code = ''.join(f.readlines())
	
		# Build the LaTeX code block of questions
		question_block = ''.join(['\\item {}\n'.format(q) for q in self.questions])
		answer_block = ''.join(['\\item {}\n'.format(a) for a in self.answers])

		code = code.replace('%Questions%', question_block)
		code = code.replace('%Answers%', answer_block)

		self.code = code
		
		with open(output, 'w+') as f_out:
			f_out.write(code)


if __name__ == '__main__':
	# import os

	# weights = {'sin': 6, 'cos': 6, 'tan': 6, 'csc': 2, 'sec': 2, 'cot': 2}

	# quiz = TrigQuiz(weights = weights)
	# template = r"E:\Desktop2\Python Projects\quiz_generator\trig_quiz\template.txt"
	# output = r"E:\Desktop2\Python Projects\quiz_generator\trig_quiz\quiz.tex"
	# quiz.create_quiz(template, output)

	n = [1, 2, 3]
	L = [(i, j, k) for i in n for j in n for k in n]

	print(L)
	









