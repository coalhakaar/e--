import threading

class SimpleInterpreter:
    def __init__(self):
        self.commands = {
            'FLUFF': self.printnew,
            'NOFLUFF': self.print,
            'MEMORIZE': self.set_variable,
            'RECALL': self.check_variable
        }
        self.variables = {}
        self.if_block = False
        self.labels = {}

    def interpret(self, code):
        self.current_line = 0
        lines = code.split('\n')
        while self.current_line < len(lines):
            line = lines[self.current_line].strip()
            if line:
                parts = line.split(' ')
                command = parts[0]
                args = parts[1:]

                # Check for variable references and replace them with values
                args_with_values = []
                for arg in args:
                    if arg.startswith('$'):
                        arg_name = arg[1:]
                        if arg_name in self.variables:
                            args_with_values.append(str(self.variables[arg_name]))
                        else:
                            print(f"Variable '{arg_name}' not found")
                    else:
                        args_with_values.append(arg)

                if command in self.commands:
                    self.commands[command](*args_with_values)
                else:
                    print(f"Invalid command: {command}")
            self.current_line += 1

    def interpret_ifs(self, code):
        lines = code.split(',')
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(' ')
                command = parts[0]
                if command in self.commands:
                    self.commands[command](*parts[1:])
                else:
                    print(f"Invalid command: {command}")

    def run_interpreter(self, code):
        self.interpret(code)

    def run(self, code):
        interpreter_thread = threading.Thread(target=self.run_interpreter, args=(code,))
        interpreter_thread.start()

    def check_end_if(self):
        if 'ENDIF' in self.variables and self.if_block:
            self.if_block = False
            del self.variables['ENDIF']

    def printnew(self, *args):
        print(" ".join(args))

    def print(self, *args):
        print(" ".join(args), end="")

    def set_variable(self, var_name, value, input_type):
        if input_type == 'TEXT':
            self.variables[var_name] = value
        if input_type == 'NUM':
            self.variables[var_name] = int(value)

    def check_variable(self, var_name, var_type, condition, *code_block):
        if var_type == 'TEXT':
            if var_name in self.variables and self.variables[var_name] == condition:
                self.if_block = True
                sub_code = " ".join(code_block)
                self.interpret_ifs(sub_code)
        if var_type == 'NUM':
            if var_name in self.variables and self.variables[var_name] == int(condition):
                self.if_block = True
                sub_code = " ".join(code_block)
                self.interpret_ifs(sub_code)


# Example usage:
interpreter = SimpleInterpreter()
with open('code.txt', 'r') as file:
    code = file.read()
interpreter.run(code)
