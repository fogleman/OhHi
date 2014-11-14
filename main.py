def other(value):
    if value == 1:
        return 2
    if value == 2:
        return 1
    return 0

class Grid(object):
    @staticmethod
    def load(data):
        result = Grid(len(data))
        for y, row in enumerate(data):
            for x, value in enumerate(row):
                if value == '0':
                    result.set(x, y, 1)
                if value == '1':
                    result.set(x, y, 2)
        return result
    def __init__(self, size):
        self.size = size
        self.cells = {}
    def get(self, x, y):
        return self.cells.get((x, y), 0)
    def set(self, x, y, value):
        self.cells[(x, y)] = value
    def set_default(self, x, y, value):
        if not self.get(x, y):
            self.set(x, y, value)
    def update_cell(self, x, y):
        n1 = self.get(x, y - 1)
        n2 = self.get(x, y - 2)
        s1 = self.get(x, y + 1)
        s2 = self.get(x, y + 2)
        e1 = self.get(x + 1, y)
        e2 = self.get(x + 2, y)
        w1 = self.get(x - 1, y)
        w2 = self.get(x - 2, y)
        if n1 and n1 == n2: return other(n1)
        if s1 and s1 == s2: return other(s1)
        if e1 and e1 == e2: return other(e1)
        if w1 and w1 == w2: return other(w1)
        if n1 and n1 == s1: return other(n1)
        if e1 and e1 == w1: return other(e1)
        return 0
    def update_cells(self):
        result = False
        for y in range(self.size):
            for x in range(self.size):
                if self.get(x, y):
                    continue
                value = self.update_cell(x, y)
                if value:
                    result = True
                    self.set(x, y, value)
        return result
    def update_rows_cols(self):
        result = False
        half = self.size / 2
        for y in range(self.size):
            row = [self.get(x, y) for x in range(self.size)]
            n1 = row.count(1)
            n2 = row.count(2)
            if n1 + n2 == self.size:
                continue
            if n1 == half:
                result = True
                for x in range(self.size):
                    self.set_default(x, y, 2)
            if n2 == half:
                result = True
                for x in range(self.size):
                    self.set_default(x, y, 1)
        for x in range(self.size):
            col = [self.get(x, y) for y in range(self.size)]
            n1 = col.count(1)
            n2 = col.count(2)
            if n1 + n2 == self.size:
                continue
            if n1 == half:
                result = True
                for y in range(self.size):
                    self.set_default(x, y, 2)
            if n2 == half:
                result = True
                for y in range(self.size):
                    self.set_default(x, y, 1)
        return result
    def update_duplicate_row(self, y1, y2):
        row1 = [self.get(x, y1) for x in range(self.size)]
        row2 = [self.get(x, y2) for x in range(self.size)]
        n1 = row1.count(0)
        n2 = row2.count(0)
        if n1 == 0 and n2 == 2:
            for x in range(self.size):
                self.set_default(x, y2, other(self.get(x, y1)))
        if n2 == 0 and n1 == 2:
            for x in range(self.size):
                self.set_default(x, y1, other(self.get(x, y2)))
    def update_duplicate_col(self, x1, x2):
        col1 = [self.get(x1, y) for y in range(self.size)]
        col2 = [self.get(x2, y) for y in range(self.size)]
        n1 = col1.count(0)
        n2 = col2.count(0)
        if n1 == 0 and n2 == 2:
            for y in range(self.size):
                self.set_default(x2, y, other(self.get(x1, y)))
        if n2 == 0 and n1 == 2:
            for y in range(self.size):
                self.set_default(x1, y, other(self.get(x2, y)))
    def update_duplicates(self):
        result = False
        for y1 in range(self.size):
            for y2 in range(y1 + 1, self.size):
                row1 = [self.get(x, y1) for x in range(self.size)]
                row2 = [self.get(x, y2) for x in range(self.size)]
                for a, b in zip(row1, row2):
                    if a and b and a != b:
                        break
                else:
                    result = True
                    self.update_duplicate_row(y1, y2)
        for x1 in range(self.size):
            for x2 in range(x1 + 1, self.size):
                col1 = [self.get(x1, y) for y in range(self.size)]
                col2 = [self.get(x2, y) for y in range(self.size)]
                for a, b in zip(col1, col2):
                    if a and b and a != b:
                        break
                else:
                    result = True
                    self.update_duplicate_col(x1, x2)
        return result
    def update(self):
        while True:
            result = False
            result = result or self.update_cells()
            result = result or self.update_rows_cols()
            result = result or self.update_duplicates()
            if not result:
                break
    def __repr__(self):
        rows = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                value = self.get(x, y)
                value = str(value - 1) if value else '.'
                row.append(value)
            rows.append(' '.join(row))
        rows.append('')
        return '\n'.join(rows)

if __name__ == '__main__':
    data = [
        '..11.1...1',
        '0...0.....',
        '..1....11.',
        '.1..01.1..',
        '0.........',
        '.11.1.....',
        '...1...0.0',
        '.00.0..0.0',
        '..........',
        '......0.0.',
    ]
    grid = Grid.load(data)
    print grid
    grid.update()
    print grid
