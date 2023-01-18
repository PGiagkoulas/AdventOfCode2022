from enum import Enum


class Shapes(Enum):
    ROCK = "ROCK"
    PAPER = "PAPER"
    SCISSORS = "SCISSORS"


class OutcomeScores(Enum):
    WIN = 6
    LOSS = 0
    DRAW = 3


shape_scores = {
    Shapes.ROCK: 1,
    Shapes.PAPER: 2,
    Shapes.SCISSORS: 3
}


shape_scores_list = [Shapes.ROCK, Shapes.PAPER, Shapes.SCISSORS]


choice_to_shape = {
    "A": Shapes.ROCK,
    "B": Shapes.PAPER,
    "C": Shapes.SCISSORS,
    "X": Shapes.ROCK,
    "Y": Shapes.PAPER,
    "Z": Shapes.SCISSORS
}


guide_results = {
    "X": OutcomeScores.LOSS,
    "Y": OutcomeScores.DRAW,
    "Z": OutcomeScores.WIN
}


result_factor = {
    OutcomeScores.LOSS: -1,
    OutcomeScores.DRAW: 0,
    OutcomeScores.WIN: 1
}


Rules = {
    (Shapes.ROCK, Shapes.ROCK): OutcomeScores.DRAW,
    (Shapes.PAPER, Shapes.PAPER): OutcomeScores.DRAW,
    (Shapes.SCISSORS, Shapes.SCISSORS): OutcomeScores.DRAW,
    (Shapes.ROCK, Shapes.SCISSORS): OutcomeScores.WIN,
    (Shapes.SCISSORS, Shapes.PAPER): OutcomeScores.WIN,
    (Shapes.PAPER, Shapes.ROCK): OutcomeScores.WIN,
}


def __calculate_result(opp_choice, my_choice):
    if (my_choice, opp_choice) in Rules:
        score =  Rules[(my_choice, opp_choice)]
    else:
        score = OutcomeScores.LOSS
    return score.value + shape_scores[my_choice]


if __name__=='__main__':
    with open('d2-input.txt') as f:
        lines = f.readlines()
    print(f"[>] Guide length: {len(lines)}")
    print(f"[>] Guide's first options: {lines[0]}")

    choices = [(choice[:-1].split(' ')[0], choice[:-1].split(' ')[1]) for choice in lines]
    chosen_shapes = [(choice_to_shape[c[0]], choice_to_shape[c[1]]) for c in choices]

    # score calculation
    results = [__calculate_result(c[0], c[1]) for c in chosen_shapes]

    # total score
    print(sum(results))

    # opponent choice and results mapping
    opp_choices = [choice_to_shape[c[0]] for c in choices]
    guided_results = [guide_results[c[1]] for c in choices]

    score = 0 
    for op_c, res in zip(opp_choices, guided_results):
        my_choice = shape_scores_list[(shape_scores_list.index(op_c) + result_factor[res] * 1) % 3]
        score += res.value + shape_scores[my_choice]
    
    print(score)
    