from expression import Expression

class Function:
  def __init__ (function_string, function_arg):
    pass

class column:
  def __init__(self, func, col):
    pass
  def _sum(self):
    return sum(self)
  def _avg(self):
    return avg(self)


class query:
  class select_line:
    pass
  class group_by_line:
    pass
  class order_by_line:
    pass

def sum(col):
  pass

def avg(col):
  pass

if __name__ == "__main__":
  expres = Expression("""select sum(a   and b) from table1""")
  print(expres.toList())
  print(expres)
  print(expres)[1]