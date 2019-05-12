from ply import *
import robotlex

tokens = robotlex.tokens

# Precedence & associative rules for the arithmetic operators
# 1. Unary, right-associative minus.
# 2. Binary, left-associative comparison
# 3. Binary, left-associative addition and subtraction
# Parenthesis precedence defined through the grammar


precedence = (
    ('right', 'UMINUS'),
    ('left', 'COMPARE'),
    ('left', 'PLUS', 'MINUS')
)


# We represent the program as a dictionary of tuples indexed by line number.

def p_application(p):
    '''application : application statement
                   | statement'''
    if len(p) == 2 and p[1]:
        p.counter = 0
        p[0] = {}
        p[0][p.counter] = p[1]
        p.counter += 1
    elif len(p) == 3:
        p[0] = p[1]
        if not p[0]:
            p[0] = {}
        if p[2]:
            stat = p[2]
            p[0][p.counter] = stat
            p.counter += 1


# This catch-all rule is used for any catastrophic errors.  In this case,
# we simply return nothing

def p_application_error(p):             					
    '''application : error'''
    p[0] = None
    p.parser.error = 1
    print("PROGRAM ERROR")

# Format of all statements.						

def p_statement(p):
    '''statement : command NEWLINE
                 | command statement '''
    if isinstance(p[1], str):
        print("%s %s %s" % (p[1], "AT LINE", p[1]))
        p[0] = None
        p.parser.error = 1
    else:
        p[0] = p[1]

def p_one_statement(p):
    '''one_statement : command'''
    p[0] = p[1]

def p_stategroup(p):				# for if-else statement to make big groups of statements
    '''stategroup : stategroup command
                  | command'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[2])


# Error handling for wrong statements

def p_statement_bad(p):
    '''statement : error NEWLINE'''
    print("WRONG STATEMENT AT LINE ")
    p[0] = None
    p.parser.error = 1


# Blank line

def p_statement_newline(p):
    '''statement : NEWLINE'''
    p[0] = None


# DATA statement

def p_command_data(p):
    '''command : DATA variable_array'''
    p[0] = ('DATA', p[2])


def p_command_data_bad(p):
    '''command : DATA error'''
    p[0] = "MALFORMED NUMBER LIST IN DATA"


# PRINT statement


def p_command_print(p):
    '''command : PRINT variable_array'''
    p[0] = ('PRINT', p[2])


def p_command_print_bad(p):
    '''command : PRINT error'''
    p[0] = "MALFORMED PRINT STATEMENT"


# PRINT statement with no arguments


def p_command_print_empty(p):
    '''command : PRINT'''
    p[0] = ('PRINT', [])


# END statement


def p_command_end(p):
    '''command : FINISH'''
    p[0] = ('FINISH',)

# For a robot

def p_command_robot(p):
    '''command : ROBOT NUMERIC_VAR NUMERIC_VAR '''
    p[0] = ('ROBOT', eval(p[2]), eval(p[3]))


# VARIABLE statement

def p_command_bool(p):
    '''command : BOOLEAN variable_group'''
    p[0] = ('BOOLEAN', p[2])

def p_command_int(p):
    '''command : INTEGER variable_group'''
    p[0] = ('INTEGER', p[2])

def p_command_str(p):
    '''command : STRING variable_group'''
    p[0] = ('STRING', p[2])

def p_command_vect(p):				
    '''command : VECTOR OF type variable_group'''
    p[0] = ('VECTOR', p[3], p[4])

def p_command_vect_bad(p):
    '''command : VECTOR OF error'''
    p[0] = "WRONG NUMBER LIST IN VECTOR"

# Type

def p_type(p):
    '''type : BOOLEAN
	        | INTEGER
 	        | STRING'''
    p[0] = p[1]

# Type conversing operator

def p_command_conv(p):
    '''command : expression TO type
	           | expression TO expression'''
    p[0] = ('TO', p[1], p[3])

# Assignment operator

def p_command_assign(p):
    '''command : variable EQUAL expression'''
    p[0] = ('ASSIGN', p[1], p[3])

def p_command_bad(p):
    '''command : variable EQUAL error'''
    p[0] = "BAD EXPRESSION IN ASSIGN"


# Arithmetic expressions

def p_expression_arith(p):
    '''expression : expression PLUS expression
	              | expression MINUS expression'''
    p[0] = ('BINOP', p[2], p[1], p[3])


# Relational expressions


def p_logical_expression(p):
    '''logical_expression : expression LT expression
               		  | expression GT expression
               		  | expression EQUALS expression
               		  | expression NE expression'''
    p[0] = ('RELOP', p[2], p[1], p[3])


# Variables

def p_expression_number(p):
     '''expression : NUMERIC_VAR'''
     p[0] = ('NUM', eval(p[1]))

def p_expression_string(p):
     '''expression : STRING_VAR'''
     p[0] = ('STR', eval(p[1]))


def p_expression_bool(p):
     '''expression : TRUE
                   | FALSE
                   | UNDEFINED'''
     p[0] = ('BOOL', p[1])

def p_expression_unary(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = ('UNARY', '-', p[2])

# VARIABLE statement

def p_variable(p):
    '''variable : ID'''
    if len(p) == 2:
        p[0] = p[1]

def p_several_ID(p):
    '''several_ID : several_ID COMMA ID
  		  | ID
		  | several_ID COMMA ELLIPSIS
		  | ELLIPSIS'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])


def p_variable_group(p):
    '''variable_group : variable_group COMMA variable
                      | variable '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])


def p_variable_group_as(p):
    '''variable_assign : variable_assign COMMA command
		       | command'''
    if len(p) == 2:
	p[0] = [p[1]]
    else:
	p[0] = p[1]
	p[0].append(p[3])

#Several assigning variables

def p_command_several_expression(p):		
    '''expression : expression COMMA command   
                  | command'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2:
        p[0] = [p[1]]




# Building a list of variable targets as a Python list

def p_variable_array(p):
    '''variable_array : variable_array COMMA variable
                      | variable'''
    if len(p) > 2:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]


def p_variable_ar(p):
    'variable  : NUMERIC_VAR'
    p[0] = eval(p[1])

def p_variable_signed_ar(p):
    'variable  : MINUS NUMERIC_VAR'
    p[0] = eval("-" + p[2])

def p_variabel_str_ar(p):
    '''variable : STRING_VAR'''
    p[0] = eval(p[1][-1:-1])

def p_variable_bool_ar(p):
    '''variable : TRUE
		| FALSE
 		| UNDEFINED'''
    P[0] = eval(p[1])


# ARRAY statement

def p_command_array(p):
    '''command : VECTOR OF variable_array'''
    p[0] = ('VECTOR', p[3])


# Accessing to an element in array

def p_array_index(p):
    '''command : variable_array INDEX '''
    p[0] = ('INDEX', p[1], p[2])
    

# Commands for an array

def p_command_vector(p):
   '''command : variable PUSH FRONT expression
	      | variable PUSH BACK expression
  	      | variable POP FRONT expression
	      | variable POP BACK expression'''
   p[0] = ('VECTOPER', p[4], p[2], p[3], p[1])


	# ROBOT commands
# LEFT statement

def p_command_left(p):
    '''command : LEFT'''
    p[0] = ('LEFT',)

# RIGHT statement

def p_command_right(p):
    '''command : RIGHT'''
    p[0] = ('RIGHT',)

# FORWARD statement

def p_command_forward(p):
    '''command : FORWARD'''
    p[0] = ('FORWARD',)

# BACK statement 

def p_command_back(p):
    '''command : BACK'''
    p[0] = ('BACK',) 

# ROTATE_RIGHT statement

def p_command_rotate_right(p):
    '''command : ROTATE_RIGHT'''
    p[0] = ('ROTATE_RIGHT',)

# ROTATE_LEFT statement

def p_command_rotate_left(p):
    '''command : ROTATE_LEFT'''
    p[0] = ('ROTATE_LEFT',)

# LMS statement

def p_command_lms(p):
    '''command : LMS'''
    p[0] = ('LMS',)

# REFLECT statement

def p_command_reflect(p):
    '''command : REFLECT'''
    p[0] = ('REFLECT',)

# DRILL statement

def p_command_drill(p):
    '''command : DRILL'''
    p[0] = ('DRILL', )

# DO-UNTIL statement

def p_command_do_while(p):
    '''command : DO one_statement UNTIL logical_expression
	       | DO BEGIN stategroup END UNTIL logical_expression'''
    if len(p) == 5:
	p[0] = ('DO-UNTIL', p[2], p[4])
    elif len(p) == 7:
	p[0] = ('DO-UNTIL', p[3], p[6])
    else:
	pass

# IF-THEN-ELSE statement

def p_command_if_then(p):    					
    '''command : IF logical_expression THEN statement
	       | IF logical_expression THEN BEGIN stategroup END
	       | IF logical_expression THEN statement ELSE statement
	       | IF logical_expression THEN statement ELSE BEGIN stategroup END
	       | IF logical_expression THEN BEGIN stategroup END ELSE statement
 	       | IF logical_expression THEN BEGIN stategroup END ELSE BEGIN stategroup END'''
    if len(p) == 5:
	p[0] = ('IF', p[2], p[4])
    elif len(p) == 7 and p[4] == 'BEGIN' and p[6] == 'END':
	p[0] = ('IF-LOTS', p[2], p[5])
    elif len(p) == 7 and p[5] == 'ELSE':
	p[0] = ('IF-ELSE', p[2], p[4], p[6])
    elif len(p) == 9 and p[6] == 'BEGIN' and p[8] == 'END':
	p[0] = ('IF-ELSE-LOTS', p[2], p[4], p[7])
    elif len(p) == 9 and p[7] == 'ELSE':
	p[0] = ('IF-ELSE', p[2], p[5], p[8])
    elif len(p) == 11:
	p[0] = ('IF-ELSE-MANY', p[2], p[5], p[9])

# FUNCTION statement

def p_command_function(p):
    '''command : FUNCTION OF type ID OPEN_SC several_ID CLOSE_SC one_statement
	       | FUNCTION OF type ID OPEN_SC several_ID CLOSE_SC BEGIN stategroup END
	       | ID OPEN_SC ID CLOSE_SC '''
    if len(p) == 9:
	p[0] = ('FUNCTION', p[3], p[4], p[6], p[8])
    elif len(p) == 11:
	p[0] = ('FUNCTION', p[3], p[4], p[6], p[9])
    elif len(p) == 5:
	p[0] = ('PROCEDURE', p[1], p[3])

# Return command

def p_command_return(p):
    '''command : RETURN expression
	       | RETURN logical_expression'''
    p[0] = ('RETURN', p[2])


# Catastrophic error handler

def p_error(p):
    if not p:
        print("SYNTAX ERROR AT EOF")


bparser = yacc.yacc()

def parse(data, debug=1):

    bparser.error = 0
    p = bparser.parse(data, debug=debug)
    print p 
    if bparser.error:
        return None
    return p

