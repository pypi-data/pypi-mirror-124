#######################################
# IMPORTS
#######################################

from strings_with_arrows import *

import string
import os
import math
import re
import time

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

lreg = re.compile("^[a-zA-Z0-9ㄱ-ㅎㅏ-ㅣ가-힣_\$]+$")
def lregm(text):
    return True if lreg.match(str(text)) else False

#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result    = f'{self.error_name}: {self.details}\n'
        result += f'{self.pos_start.fn} 파일, {self.pos_start.ln + 1}번 줄'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '사용할 수 없는 문자', details)

class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '필요한 문자', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, '잘못된 구문', details)

class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, '런타임 오류', details)
        self.context = context

    def as_string(self):
        result    = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  {pos.fn} 파일, {ctx.display_name} 중 {str(pos.ln + 1)}번 줄\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return '오류가 난 부분을 역추적한 결과:\n' + result

#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENS
#######################################

TT_INT			= 'INT'
TT_FLOAT        = 'FLOAT'
TT_STRING		= 'STRING'
TT_IDENTIFIER	= 'IDENTIFIER'
TT_KEYWORD		= 'KEYWORD'
TT_PLUS         = 'PLUS'
TT_MINUS        = 'MINUS'
TT_MUL          = 'MUL'
TT_DIV          = 'DIV'
TT_POW		    = 'POW'
TT_EQ			= 'EQ'
TT_LPAREN     	= 'LPAREN'
TT_RPAREN     	= 'RPAREN'
TT_LLSQUARE     = 'LLSQUARE'
TT_LISQUARE     = 'LISQUARE'
TT_RSQUARE      = 'RSQUARE'
TT_LBRACE       = 'LBRACE'
TT_RBRACE       = 'RBRACE'
TT_EE			= 'EE'
TT_NE			= 'NE'
TT_LT			= 'LT'
TT_GT			= 'GT'
TT_LTE			= 'LTE'
TT_GTE			= 'GTE'
TT_AND          = 'AND'
TT_OR           = 'OR'
TT_NOT          = 'NOT'
TT_COMMA		= 'COMMA'
TT_ARROW		= 'ARROW'
TT_NEWLINE		= 'NEWLINE'
TT_EOF			= 'EOF'

KEYWORDS = [
    '만약',
    '아니면서',
    '아니면',
    '라면',
    '이라면',
    '반복하기',
    '함수',
    '끝',
    '리턴',
    '반복',
    '그만'
]

NKEYWORDS = [
    '참',
    '거짓',
    '없음',
    '원주율'
]

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        self.back_char = self.text[self.pos.idx-1] if self.pos.idx-1 < len(self.text) and self.pos.idx > 0 else None
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '#':
                self.skip_comment()
            elif self.current_char in ';\n':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif lregm(self.current_char):
                tokens.append(self.make_identifier())
            elif self.current_char == '"' or self.current_char == "'":
                tokens.append(self.make_string())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '[':
                tokens.append(self.make_square())
            elif self.current_char == ']':
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LBRACE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RBRACE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                tokens.append(self.make_not_equals())
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == '&':
                tokens.append(Token(TT_AND, pos_start=self.pos))
                self.advance()
            elif self.current_char == '|':
                tokens.append(Token(TT_OR, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        quote = self.current_char
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != quote or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
                    escape_character = False
            self.advance()
        
        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()
        
        while self.current_char != None and lregm(self.current_char):
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_square(self):
        tok_type = TT_LLSQUARE
        pos_start = self.pos.copy()
        
        if self.back_char != None and (lregm(self.back_char) or self.back_char in ')}]'):
            tok_type = TT_LISQUARE

        self.advance()
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_not_equals(self):
        tok_type = TT_NOT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_NE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_equals(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_EE
        elif self.current_char == '>':
            self.advance()
            tok_type = TT_ARROW

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def skip_comment(self):
        self.advance()

        while self.current_char != '\n' and self.current_char != None:
            self.advance()

        self.advance()

#######################################
# NODES
#######################################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

class StringNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class ElemNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end

class WhileNode:
    def __init__(self, body_node, should_return_null):
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.body_node.pos_start
        self.pos_end = self.body_node.pos_end

class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_auto_return = should_auto_return

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

class ReturnNode:
    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return

        self.pos_start = pos_start
        self.pos_end = pos_end

class BreakNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self

#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        if self.tok_idx+1 >= 0 and self.tok_idx+1 < len(self.tokens):
            self.next_tok = self.tokens[self.tok_idx+1]
        if self.tok_idx-1 >= 0 and self.tok_idx-1 < len(self.tokens):
            self.back_tok = self.tokens[self.tok_idx-1]
        
    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "이전 토큰 뒤에 토큰을 표시할 수 없습니다."
            ))
        return res

    ###################################

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False
            
            if not more_statements: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, '리턴'):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))
        
        if self.current_tok.matches(TT_KEYWORD, '반복'):
            res.register_advancement()
            self.advance()
            if self.current_tok.matches(TT_KEYWORD, '그만'):
                res.register_advancement()
                self.advance()
                return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "'반복' 뒤에 '그만'이 필요합니다."
                ))
                
        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "'리턴', '반복 그만', '만약', '반복하기', '함수', 정수, 실수, 식별자, '+', '-', '(', '[', 또는 '!'가 필요합니다."
            ))
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        if hasattr(self, 'next_tok') and self.next_tok.type == TT_EQ:
            if self.current_tok.type != TT_IDENTIFIER or self.current_tok.value in NKEYWORDS:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "변수명을 지정하지 않았거나 사용할 수 없는 변수명입니다."
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "'='가 필요합니다."
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, (TT_AND, TT_OR)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "'만약', '반복하기', '함수', 정수, 실수, 식별자, '+', '-', '(', '[', 또는 '!'가 필요합니다."
            ))

        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.type == TT_NOT:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))
        
        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "정수, 실수, 식별자, '+', '-', '(', '[', '만약, '반복하기', '함수', 또는 '!'가 필요합니다."
            ))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.elem_expr, (TT_POW, ), self.factor)
    
    def elem_expr(self):
        return self.get_elem(self.call, (TT_LISQUARE, ), self.expr)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res

        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "')', '만약', '반복하기', '함수', 정수, 실수, 식별자, '+', '-', '(', '[', 또는 '!'가 필요합니다."
                    ))

                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"',', 또는 ')'가 필요합니다."
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "')'가 필요합니다."
                ))

        elif tok.type == TT_LLSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)
        
        elif tok.matches(TT_KEYWORD, '만약'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, '반복하기'):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, '함수'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "정수, 실수, 식별자, '+', '-', '(', '[', '만약', '반복하기', '함수'가 필요합니다."
        ))

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LLSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "'['가 필요합니다."
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "']', '만약', '반복하기', '함수', 정수, 실수, 식별자, '+', '-', '(', '[', 또는 '!'가 필요합니다."
                ))

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "',', 또는 ']'가 필요합니다."
                ))

            res.register_advancement()
            self.advance()

        return res.success(ListNode(
            element_nodes,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('만약'))
        if res.error: return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_b(self):
        return self.if_expr_cases('아니면서')
        
    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.current_tok.matches(TT_KEYWORD, '아니면'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements, True)

                if self.current_tok.matches(TT_KEYWORD, '끝'):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "'끝'이 필요합니다."
                    ))
            else:
                expr = res.register(self.statement())
                if res.error: return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TT_KEYWORD, '아니면서'):
            all_cases = res.register(self.if_expr_b())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error: return res
        
        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'{case_keyword}'(이)가 필요합니다."
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if (not self.current_tok.matches(TT_KEYWORD, '라면')) and (not self.current_tok.matches(TT_KEYWORD, '이라면')):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'(이)라면'이 필요합니다."
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.current_tok.matches(TT_KEYWORD, '끝'):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, '반복하기'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'반복하기'가 필요합니다."
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, '끝'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"'끝'이 필요합니다."
                ))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(body, True))
        
        body = res.register(self.statement())
        if res.error: return res

        return res.success(WhileNode(body, False))

    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, '함수'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'함수'가 필요합니다."
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"'('가 필요합니다."
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "함수명이나 '('가 필요합니다."
                ))
        
        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()
            
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"사용할 수 있는 매개변수명이 필요합니다."
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()
            
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"',', 또는 ')'가 필요합니다."
                ))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"사용할 수 있는 매개변수명이나 ')'가 필요합니다."
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_ARROW:
            res.register_advancement()
            self.advance()

            body = res.register(self.expr())
            if res.error: return res

            return res.success(FuncDefNode(
                var_name_tok,
                arg_name_toks,
                body,
                True
            ))
        
        if self.current_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'=>', ';', 또는 새 줄이 필요합니다."
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, '끝'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'끝'이 필요합니다."
            ))

        res.register_advancement()
        self.advance()
        
        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            body,
            False
        ))

    ###################################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a
        
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def get_elem(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a
        
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"']'가 필요합니다."
                ))
            res.register_advancement()
            self.advance()
            left = ElemNode(left, op_tok, right)

        return res.success(left)

#######################################
# RUNTIME RESULT
#######################################

class RTResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_break = False

    def register(self, res):
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_break = res.loop_should_break
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.func_return_value = value
        return self
    
    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        return (
            self.error or
            self.func_return_value or
            self.loop_should_break
        )

#######################################
# VALUES
#######################################

class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self, other):
        return None, self.illegal_operation(other)

    def execute(self, args):
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            '잘못된 작업',
            self.context
        )

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    '0으로 나눌 수 없습니다.',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'"{self.value}"'

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    '인덱스가 범위를 벗어났기 때문에 이 인덱스의 요소를 배열에서 제거할 수 없습니다.',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def get_elem(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    '인덱스가 범위를 벗어났기 때문에 이 인덱스의 요소를 배열에서 검색할 수 없습니다.',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)
    
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return ", ".join([str(x) for x in self.elements])

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<익명 함수>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)}보다 많은 양의 매개변수가 {self}에 들어갔습니다.",
                self.context
            ))
        
        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)}보다 적은 양의 매개변수가 {self}에 들어갔습니다.",
                self.context
            ))

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value == None: return res

        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
        return res.success(ret_value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<함수 {self.name}>"

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return(): return res

        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<내장 함수 {self.name}>"

    #####################################

    def execute_콘솔에_보여주기(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('내용')))
        return RTResult().success(Number.null)
    execute_콘솔에_보여주기.arg_names = ['내용']
    
    def execute_콘솔_지우기(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'clear') 
        return RTResult().success(Number.null)
    execute_콘솔_지우기.arg_names = []

    def execute_숫자인가(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("값"), Number)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_숫자인가.arg_names = ["값"]

    def execute_문자열인가(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("값"), String)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_문자열인가.arg_names = ["값"]

    def execute_배열인가(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("값"), List)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_배열인가.arg_names = ["값"]

    def execute_함수인가(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("값"), BaseFunction)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_함수인가.arg_names = ["값"]

    def execute_기다리기(self, exec_ctx):
        time.sleep(exec_ctx.symbol_table.get("초").value)
        return RTResult().success(Number.null)
    execute_기다리기.arg_names = ["초"]

    def execute_문자열로(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get("숫자").value)))
    execute_문자열로.arg_names = ["숫자"]

    def execute_실행하기(self, exec_ctx):
        fn = exec_ctx.symbol_table.get("파일명")

        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "파일명은 문자열로 입력해주세요.",
                exec_ctx
            ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"파일 \"{fn}\"(을)를 로딩하는 데 실패했습니다.\n" + str(e),
                exec_ctx
            ))

        _, error = run(fn, script)
        
        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"파일 \"{fn}\"(을)를 실행하는 데 실패했습니다.\n" +
                error.as_string(),
                exec_ctx
            ))

        return RTResult().success(Number.null)
    execute_실행하기.arg_names = ["파일명"]

BuiltInFunction.콘솔에_보여주기 = BuiltInFunction("콘솔에_보여주기")
BuiltInFunction.콘솔_지우기    = BuiltInFunction("콘솔_지우기")
BuiltInFunction.숫자인가      = BuiltInFunction("숫자인가")
BuiltInFunction.문자열인가     = BuiltInFunction("문자열인가")
BuiltInFunction.배열인가      = BuiltInFunction("배열인가")
BuiltInFunction.함수인가      = BuiltInFunction("함수인가")
BuiltInFunction.기다리기      = BuiltInFunction("기다리기")
BuiltInFunction.문자열로      = BuiltInFunction("문자열로")
BuiltInFunction.실행하기	    = BuiltInFunction("실행하기")

#######################################
# CONTEXT
#######################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

#######################################
# SYMBOL TABLE
#######################################

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

#######################################
# INTERPRETER
#######################################

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}'(이)가 없습니다.",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return(): return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.type == TT_AND:
            result, error = left.anded_by(right)
        elif node.op_tok.type == TT_OR:
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return(): return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.type == TT_NOT:
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_ElemNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return(): return res

        if node.op_tok.type == TT_LISQUARE:
            if hasattr(left, 'get_elem'):
                result, error = left.get_elem(right)
            else:
                return res.failure(RTError(
                    node.pos_start, node.pos_end,
                    f"배열, 또는 객체가 아닙니다.",
                    context
                ))

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(Number.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return(): return res
            return res.success(Number.null if should_return_null else expr_value)

        return res.success(Number.null)

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []
        

        while True:
            if res.should_return(): return res

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_break == False: return res

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return(): return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = Number.null
        
        return res.success_return(value)

    def visit_BreakNode(self, node, context):
        return RTResult().success_break()

#######################################
# RUN
#######################################

global_symbol_table = SymbolTable()
global_symbol_table.set("없음", Number.null)
global_symbol_table.set("거짓", Number.false)
global_symbol_table.set("참", Number.true)
global_symbol_table.set("원주율", Number.math_PI)
global_symbol_table.set("콘솔에_보여주기", BuiltInFunction.콘솔에_보여주기)
global_symbol_table.set("콘솔_지우기", BuiltInFunction.콘솔_지우기)
global_symbol_table.set("숫자인가", BuiltInFunction.숫자인가)
global_symbol_table.set("문자열인가", BuiltInFunction.문자열인가)
global_symbol_table.set("배열인가", BuiltInFunction.배열인가)
global_symbol_table.set("함수인가", BuiltInFunction.함수인가)
global_symbol_table.set("기다리기", BuiltInFunction.기다리기)
global_symbol_table.set("문자열로", BuiltInFunction.문자열로)
global_symbol_table.set("실행하기", BuiltInFunction.실행하기)

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error
    #return tokens, None
    
    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error
    #return ast.node, None
    
    # Run program
    interpreter = Interpreter()
    context = Context('<프로그램>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error