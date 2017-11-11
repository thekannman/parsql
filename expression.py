from collections import deque

class Expression:
  def __init__(self, expression_string, starting_delim="", depth=0, rel_depth=0, rel_pos=0, break_strings=False,
               is_string=False):
    self.expression_string = expression_string
    self.starting_delim = starting_delim
    self.depth = depth
    self.rel_depth = rel_depth
    self.rel_pos = rel_pos
    self.break_strings = break_strings
    self.is_string = is_string
    self.stop_characters = starting_delim if self.is_string and not self.break_strings else set(
      Expression.delimiters.keys() + Expression.delimiters.values())
    self.closing_delim = Expression.delimiters[starting_delim] if starting_delim else ""
    self.subexpressions = []
    self.ends_with_closing_delim = False
    self.remainder = self.parse()

  # opening delim : closing delim.
  # TODO: Should make param
  delimiters = {'"': '"',
                '\'': '\'',
                '(': ')'}
  string_delimiters = ['"', '\'']

  # Need to split on:
  # paren for inner expression
  # space for commands
  # single and double quotes for strings

  def is_stop(self, chr):
    if self.break_strings or not self.is_string:
      return True if chr in self.stop_characters or chr.isspace() else False
    else:
      return True if chr in self.stop_characters else False

  def parse(self):
    remaining_string = deque(self.expression_string)
    expression = deque()
    if self.rel_depth == 0:
      rel_pos = 0
      while remaining_string:
        self.subexpressions.append(
          Expression(remaining_string, starting_delim=self.starting_delim, depth=self.depth + 1,
                     rel_depth=self.rel_depth + 1, rel_pos=rel_pos))
        rel_pos = rel_pos + 1
        remaining_string = self.subexpressions[-1].remainder
        if self.subexpressions[-1].ends_with_closing_delim:
          return remaining_string
    while remaining_string:
      chr = remaining_string.popleft()
      if chr in self.stop_characters or chr.isspace():
        if expression:
          self.subexpressions.append("".join(expression))
        expression = deque()
        if chr == self.closing_delim:
          self.ends_with_closing_delim = True
          return remaining_string
        elif chr.isspace():
          while chr.isspace():
            chr = remaining_string.popleft()
          remaining_string.appendleft(chr)
          return remaining_string
        elif chr in self.string_delimiters:
          self.subexpressions.append(
            Expression("".join(remaining_string), chr, depth=self.depth + 1, rel_depth=0, rel_pos=0, is_string=True))
          remaining_string = self.subexpressions[-1].remainder
        elif chr in self.delimiters.keys():
          self.subexpressions.append(
            Expression("".join(remaining_string), chr, depth=self.depth + 1, rel_depth=0, rel_pos=0))
          remaining_string = self.subexpressions[-1].remainder
        elif chr in self.delimiters.values():
          raise ValueError("unexpected delimiter. %s expected but %s found." % (self.closing_delim, chr))
        else:
          raise ValueError("unexpected stop character. %s expected but %s found." % (self.closing_delim, chr))
      else:
        expression.append(chr)
    if expression:
      self.subexpressions.append("".join(expression))

  def __str__(self):
    prepender = self.starting_delim if self.rel_depth == 0 else ""
    postpender = self.closing_delim if self.rel_depth == 0 else ""
    return prepender + " ".join([expression.__str__() for expression in self.subexpressions]) + postpender

  def toList(self):
    return [str(expression) for expression in self.subexpressions]

  def __getitem__(self, key):
    return self.subexpressions[key]