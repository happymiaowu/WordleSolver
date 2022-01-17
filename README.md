# Wordle Solver

### Algorithm
Construct a search tree and minimize the max of depth of each subtree.  

### HowTo
#### Search Tree
search_tree.txt is the json format file for search tree. 
You can analysis the file content like this:
{word_to_guess -> {guess_result -> {next_word_to_guess -> ...}}}

##### Guess Result Desc
The guess result is a 5 length string which only contains 3 characters: 0, 1, 2.
0 means gray(this letter is not in the word in any spot)
1 means yellow(this letter is in the word but wrong spot)
2 means green(this letter is in the word and correct spot)

#### Play
Run main.py, the agent will begin guessing and getting feedback for gaming engine automaically.

### Comments
#### Wordle
[Wordle](https://www.powerlanguage.co.uk/wordle/)
Thanks [this article](https://bert.org/2021/11/24/the-best-starting-word-in-wordle/) for providing the method to extract candidate words list.



