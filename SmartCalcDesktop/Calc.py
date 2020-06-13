from sympy import symbols, Eq, solve, sympify


class Calc:
    equation = ""
    result = 0
    char = '0'

    def __init__(self, _stringEquation):
        self.equation = _stringEquation

    def IsSymbolIn(self):

        i = 0
        while i < len(self.equation):
            if "a" <= self.equation[i] <= "e":
                self.char = self.equation[i]
                return True
            i += 1

        return False

    def ConvertToNormalEquation(self):

        i = 0
        convertedString = ""

        minus = False
        while i <= len(self.equation) - 1:
            if self.equation[i] == "-" and self.equation[i + 1] == "-":
                minus = True
                i += 2
                continue
            elif self.equation[i] == '=':
                minus = True
                i += 1
                continue

            if minus is True:
                c = self.equation[i]
                if self.equation[i] == '-':
                    convertedString += "+"
                    convertedString, i = self.CollectNumbers(i+1, convertedString)
                    continue
                elif self.equation[i] == '+':
                    convertedString += "-"
                    convertedString, i = self.CollectNumbers(i+1, convertedString)
                    continue
                elif self.equation[i] == '*' or self.equation[i] == '/' or self.equation[i] == '(' or self.equation[i] == ')':
                    convertedString += self.equation[i]
                    convertedString, i = self.CollectNumbers(i+1, convertedString)
                    continue
                else:
                    convertedString += "-"
                    convertedString, i = self.CollectNumbers(i, convertedString)
                    continue
            else:
                convertedString += self.equation[i]

            i += 1
        return convertedString

    def CollectNumbers(self, i, convertedString):
        while i < len(self.equation) and '9' >= self.equation[i] >= '0':
            convertedString += self.equation[i]
            i += 1
        return convertedString, i


    def Calculate(self):

        # one symbol solving is implemented, but now it is not problem to extend implementation
        array = []
        evalString = ""

        if self.IsSymbolIn() is False:
            i = len(self.equation) - 1
            newEqu = self.equation
            while self.equation[i] > '9' or self.equation[i] < '0':
                newEqu = self.equation[:i]
                i -= 1
            self.result = eval(newEqu)

        else:
            newEqu = self.ConvertToNormalEquation()
            e = sympify(newEqu)
            x = symbols(self.char)

            r = solve(e, x)
            self.result = r[0]
