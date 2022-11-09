

class State:
    def __init__(self, num, main_left, main_right):
        self.num = num
        self.main_left = main_left
        self.main_right = main_right
        self.sub_left = []
        self.sub_right = []
        self.generate_subs()
        self.connections = []

    def generate_subs(self):
        for production in productions:
            if self.main_right[-1] != '.':
                if production.left == self.main_right[self.main_right.index('.')+1]:
                    self.sub_left.append(production.left)
                    self.sub_right.append(f'.{production.right}')
        for production in productions:
            if production.right not in self.sub_right:
                for sub in self.sub_right:
                    if sub[-1] != '.':
                        if production.left == sub[sub.index('.')+1]:
                            self.sub_left.append(production.left)
                            self.sub_right.append(f'.{production.right}')
        # print(self.sub_left, self.sub_right)

    def generate_new_states(self):
        cur_right = self.main_right
        if cur_right[-1] != '.':
            period_index = cur_right.index('.')
            cur_right = cur_right.replace('.', '')
            new_right = cur_right[:period_index+1] + \
                '.' + cur_right[period_index+1:]
            is_new_state = True
            for state in states:
                if state.main_right == new_right:
                    is_new_state = False
            if is_new_state:
                states.append(
                    State(len(states), self.main_left, new_right))
        for index in range(len(self.sub_left)):
            cur_right = self.sub_right[index]
            if cur_right[-1] != '.':
                period_index = cur_right.index('.')
                cur_right = cur_right.replace('.', '')
                new_right = cur_right[:period_index+1] + \
                    '.' + cur_right[period_index+1:]
                is_new_state = True
                for state in states:
                    if state.main_right == new_right:
                        is_new_state = False
                if is_new_state:
                    states.append(
                        State(len(states), self.sub_left[index], new_right))

    def __str__(self):
        out = ''
        max_len = len(self.main_right)
        for sub in self.sub_right:
            max_len = max(max_len, len(sub))
        max_len += 5

        sep = f'+{"-"*(max_len+2)}+'
        out += f'{sep}\n'
        out += f'| {f"{self.main_left} -> {self.main_right}":<{max_len}} |\n'
        out += f'{sep}'
        for index in range(len(self.sub_left)):
            out += f'\n| {f"{self.sub_left[index]} -> {self.sub_right[index]}":<{max_len}} |'
        if len(self.sub_left) != 0:
            out += f'\n{sep}'
        return out


class Production:
    def __init__(self, input):
        split_input = input.split()
        self.left = split_input[0]
        self.right = split_input[2]
        self.follow = split_input[3][1:-1].split(',')

    def __str__(self):
        return f'{self.left} -> {self.right} {{{", ".join(self.follow)}}}'


with open('test3.txt') as f:
    lines = f.readlines()
    f.close()

for index in range(len(lines)):
    lines[index] = lines[index].strip()
# print(lines)

productions = []
for line in lines:
    productions.append(Production(line))

for production in productions:
    print(production)

states = []
states.append(State(0, productions[0].left, f'.{productions[0].right}'))

# print(states[0])

for state in states:
    print(state, end='\n\n')
    state.generate_new_states()
