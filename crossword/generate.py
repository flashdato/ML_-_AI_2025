import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            cp = self.domains[v].copy()
            for x in cp:
                if len(x) != int(v.length):
                    self.domains[v].remove(x)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if not self.crossword.overlaps[x, y]:
            return False

        overlap = self.crossword.overlaps[x, y]
        dx = self.domains[x].copy()

        temp = False
        for w in dx:
            char = w[overlap[0]]
            count = 0
            for w1 in self.domains[y]:
                if w1[overlap[1]] == char:
                    count += 1
            if count == 0:
                self.domains[x].remove(w)
                temp = True
        return temp

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            queue = []
            for a in self.crossword.variables:
                for b in self.crossword.variables:
                    if a != b:
                        try:
                            if self.crossword.overlaps[a, b]:
                                queue.append((a, b))
                        except:
                            pass
        else:
            queue = arcs

        while len(queue) != 0:
            tupple = queue[0]
            x, y = tupple
            queue.remove(tupple)
            change = self.revise(x, y) 
            if change:
                if len(self.domains[x]) == 0:
                    return False 
                for m in self.crossword.variables:
                    if x != m and y != m:
                        try:
                            if self.crossword.overlaps[m, x]:
                                queue.append((m, x))
                        except:
                            pass
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for v in self.crossword.variables:
            try:
                if assignment[v]:
                    pass
                else:
                    return False
            except:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for v1 in assignment:
            for v2 in assignment:
                if v1 != v2 and assignment[v1] == assignment[v2] and assignment[v2] != None:
                    return False
        
    
        for v in assignment:
            if assignment[v]:
                if len(assignment[v]) != int(v.length):
                    return False
        
        
        for a in assignment:
            for b in assignment:
                if a != b:
                    try:
                        if overlap := self.crossword.overlaps[a, b]:
                            if assignment[a][overlap[0]] == assignment[b][overlap[1]]:
                                pass
                            else:
                                return False
                    except:
                        pass
        
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        def count_ruled_out(var, value):

             n = 0
             for x in self.crossword.neighbors(var):
                if var not in assignment: 
                    overlap = self.crossword.overlaps[x, var]
                    char = value[overlap[1]]
                    for w in self.domains[x]:
                        if w[overlap[0]] != char:
                            n += 1
                        elif value == w:
                            n += 1
             return n 
             
                

        domains = []
        for a in self.domains[var]:
            domains.append(a)
        
        return sorted(domains, key=lambda value: count_ruled_out(var, value))

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = []
        for m in self.crossword.variables:
            try: 
                if assignment[m]:
                    pass
                else:
                    unassigned.append(m)
            except:
                unassigned.append(m)
        
        choise = []
        
        lowest = 1000000
        for variable in unassigned:
             if len(self.domains[variable]) < lowest:
                lowest = len(self.domains[variable])

        for variable in unassigned:
            if len(self.domains[variable]) == lowest:
                choise.append(variable)
        
        if len(choise) == 1:
            return choise[0]
        
        sorted_choise = sorted(choise, key=lambda value: self.crossword.neighbors(value)) 
        return sorted_choise[-1]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            assignment[var] = None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
