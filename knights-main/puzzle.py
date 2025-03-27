from logic import *

# Define symbols
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

knowledge = And(
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Or(CKnight,CKnave),
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave)),
    Not(And(CKnight,CKnave)),
)

knowledge0 = And(
    knowledge,
    Implication(AKnight, And(AKnight,AKnave)),
    Implication(AKnave, Not(And(AKnight,AKnave)))
)


knowledge1 = And(
    knowledge,
    Implication(AKnight, And(AKnave,BKnave)),
    Implication(AKnave, Not(And(AKnave,BKnave)))
)



knowledge2 = And(
    knowledge,
    Implication(AKnight, Or(And(AKnave,BKnave),And(AKnight,BKnight))),
    Implication(AKnave, Not(Or(And(AKnave,BKnave),And(AKnight,BKnight)))),
    Implication(BKnight, Or(And(AKnave,BKnight),And(AKnight,BKnave))),
    Implication(BKnave, Not(Or(And(AKnave,BKnight),And(AKnight,BKnave)))),
)


knowledge3 = And(
    knowledge,
    Implication(AKnight, Or(AKnight,AKnave)),
    Implication(AKnave, Not(Or(AKnight,AKnave))),
    Or(Implication(BKnight,Or(Implication(AKnight,AKnave),Implication(AKnave,Not(AKnave)))),Implication(BKnave,Not(Or(Implication(AKnight,AKnave),Implication(AKnave,Not(AKnave)))))),
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),
)



# Main function to check models
def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]

    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
