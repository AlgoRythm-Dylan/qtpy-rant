from datetime import datetime

TOKEN_TYPE_STR = "str"
TOKEN_TYPE_INSTRUCTION = "instr"

class Token:

    def __init__(self, token_type, text=None):
        self.token_type = token_type
        self.text = text

    def continue_token(self, text=None):
        if not text == None:
            if self.text == None:
                self.text = text
            else:
                self.text += text

class Prompt:

    def __init__(self, client, src=""):
        self.source = src
        self.tokens = None
        self.client = client

    def is_compiled(self):
        return self.tokens != None

    def compile(self, src=None):
        if src == None:
            src = self.source
            if src == None:
                src = ""
        else:
            self.source = src
        # tokenize
        self.tokens = []
        i = 0
        is_in_instruction = False
        for character in self.source:
            last_token = None
            if len(self.tokens) != 0:
                last_token = self.tokens[len(self.tokens) - 1]
            if character == "[" or character == "]" or is_in_instruction:
                if character == "[":
                    if i > 0 and src[i-1] == "\\":
                        if last_token != None:
                            last_token.continue_token(text=character)
                        else:
                            self.tokens.append(Token(TOKEN_TYPE_STR, text=character))
                        continue
                    else:
                        is_in_instruction = True
                        self.tokens.append(Token(TOKEN_TYPE_INSTRUCTION, text=character))
                        
                elif character == "]": # You cannot escape an end instruction token
                    is_in_instruction = False
                    last_token.continue_token(text=character)
                else:
                    # We are not starting or ending an instruction, so we can just continue the token
                    last_token.continue_token(text=character)
            elif character == "\\" and i != len(src) - 1 and not (not i == 0 and src[i - 1] == "\\"):
                pass # The next character is meant to be taken literally as text and not interpreted
            else:
                if last_token and last_token.token_type == "str":
                    last_token.continue_token(text=character)
                else:
                    self.tokens.append(Token(TOKEN_TYPE_STR, text=character))
            i += 1

    def print(self):
        if not self.is_compiled():
            self.compile()
        now = datetime.now()
        for token in self.tokens:
            if token.token_type == TOKEN_TYPE_STR:
                print(token.text, end="")
            elif token.token_type == TOKEN_TYPE_INSTRUCTION:
                if token.text == "[user]":
                    # Find user
                    user = self.client.qtpy.auth_service.current_user().username
                    if user == None:
                        user = "Guest"
                    print(user, end="")
                elif token.text == "[time12]":
                    # Print HH:MM:AM
                    print(now.strftime("%I:%M %p"), end="")
                elif token.text == "[time]" or token.text == "[time24]":
                    # Print HH:MM
                    print(now.strftime("%H:%M"), end="")
                elif token.text == "[hour12]":
                    print(now.strftime("%I"), end="")
                elif token.text == "[hour]" or token.text == "[hour24]":
                    print(now.strftime("%H"), end="")
                elif token.text == "[minute]":
                    print(now.strftime("%M"), end="")
                elif token.text == "[second]":
                    print(now.strftime("%S"), end="")
                elif token.text == "[am]":
                    print(now.strftime("%p"))
                elif token.text == "[user_id]":
                    print(self.client.qtpy.auth_service.current_user().user_id, end="")
                elif token.text == "[app_version]":
                    print(self.client.qtpy.version, end="")
                elif token.text == "[client_version]":
                    print(self.client.version, end="")
                elif token.text == "[command_count]":
                    print(self.client.command_count, end="")
                elif token.text == "[date]":
                    print(now.strftime("%A, %b %d, %Y"), end="")
                elif token.text == "[date_short]":
                    print(now.strftime("%d-%b-%Y"), end="")
                elif token.text == "[day]" or token.text == "[day_name]":
                    print(now.strftime("%A"), end="")
                elif token.text == "[day_name_short]":
                    print(now.strftime("%a"), end="")
                elif token.text == "[day_of_week_number]":
                    print(now.strftime("%w"), end="")
                elif token.text == "[day_number]":
                    print(now.strftime("%d"), end="")
                elif token.text == "[year]":
                    print(now.strftime("%Y"), end="")
                elif token.text == "[year_short]":
                    print(now.strftime("%y"), end="")
                elif token.text == "[month]" or token.text == "[month_name]":
                    print(now.strftime("%B"), end="")
                elif token.text == "[month_name_short]":
                    print(now.strftime("%b"), end="")
                elif token.text == "[month_number]":
                    print(now.strftime("%m"), end="")
                elif token.text == "[timezone]":
                    print(now.strftime("%Z"), end="")
