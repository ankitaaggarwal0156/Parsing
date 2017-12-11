# Parsing
Viterbi algorithm implementation for parsing sentences

## Data prepping
The file train.trees contains a sequence of trees, one per line, each in the following format:

(TOP (S (VP (VB Book) (NP (DT that) (NN flight)))) (PUNC .))

Run train.trees through preprocess.py and save the output to train.trees.pre. This script makes the trees strictly binary branching. When it binarizes, it inserts nodes with labels of the form X*, and when it removes unary nodes, it fuses labels so they look like X_Y . Run train.post through postprocess.py and verify that the output is identical to the original train.trees. This script reverses all the modifications made by preprocess.py.
Run train.trees.pre through unknown.py and save the output to train.trees.pre.unk. This script replaces all words that occurred only once with the special symbol <unk>.
  
## Learning Grammar
We learn the grammar from the train.trees.pre.unk and create a probabilisitic CFG in the following format:
       NP -> DT NN # 0.5
       NP -> DT NNS # 0.5
       DT -> the # 1.0
       NN -> boy # 0.5
       NN -> girl # 0.5
       NNS -> boys # 0.5
       NNS -> girls # 0.5

The rules are stored as a Dictionary.

## Parsing 
Using Viterbi algorithm, a parser is constructed that takes in the above created grammar and one sentence, and produces the most probable parse for it.
We use <strong> log probabilities </strong> here to avoid any underflow errors.

## Evaluation
Run your parser output through postprocess.py and save the output to dev.parses.post. Evaluate your parser output against the correct trees in dev.trees using the command:

python evalb.py dev.parses.post dev.trees

## Output:
matching	396 brackets
precision	0.91454965358
recall	  0.84076433121
F1	      0.87610619469
