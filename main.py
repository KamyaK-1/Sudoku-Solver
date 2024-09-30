import random
import copy 

holes = 20
k = False
def check_valid(puzzle):
    for i in range(9):
        vals = set()
        for j in range(9):
            if puzzle[i][j]!='' and puzzle[i][j] in vals:
                return False
            vals.add(puzzle[i][j])
    for i in range(9):
        vals = set()
        for j in range(9):
            if puzzle[i][j]!='' and puzzle[j][i] in vals:
                return False
            vals.add(puzzle[j][i])
    
    for i in range(3):
        for j in range(3):
            vals = set()
            for k in range(3):
                for l in range(3):
                    if puzzle[3*i+k][3*j+l]!='':
                        ...
                    else:
                        if (puzzle[3*i+k][3*j+l] in vals):
                            return False
                        vals.add(puzzle[3*i+k][3*j+l])
                        ...
    return solver(puzzle)
def display(puzzle):
    for i in puzzle:
        print(i)
    print()
def shuffle_rows(puzzle):
    for i in range(3):
        L = [puzzle[3*i],puzzle[3*i+1],puzzle[3*i+2]]
        random.shuffle(L)
        puzzle[3*i],puzzle[3*i+1],puzzle[3*i+2]=L
    return puzzle
def shuffle_columns(puzzle):
    # Transpose the puzzle, shuffle rows and then transpose it again

    puzzle = list(map(list,zip(*puzzle)))
    puzzle = shuffle_rows(puzzle)
    puzzle = list(map(list,zip(*puzzle)))
    return puzzle

def shuffle_row_blocks(puzzle):
    #row blocks means blocks of 3*9
    L = [puzzle[:3],puzzle[3:6],puzzle[6:]]
    random.shuffle(L)
    puzzle[:3],puzzle[3:6],puzzle[6:] = L
    return puzzle
def shuffle_column_blocks(puzzle):
    # Transpose the puzzle, shuffle row blocks and then transpose it again
    puzzle = list(map(list,zip(*puzzle)))
    puzzle = shuffle_row_blocks(puzzle)
    puzzle = list(map(list,zip(*puzzle)))
    return puzzle

def generate_puzzle():
    initial_puzzle = [
        [1,2,3,4,5,6,7,8,9],
        [4,5,6,7,8,9,1,2,3],
        [7,8,9,1,2,3,4,5,6],
        [2,3,4,5,6,7,8,9,1],
        [5,6,7,8,9,1,2,3,4],
        [8,9,1,2,3,4,5,6,7],
        [3,4,5,6,7,8,9,1,2],
        [6,7,8,9,1,2,3,4,5],
        [9,1,2,3,4,5,6,7,8]
    ]
    initial_puzzle = shuffle_rows(initial_puzzle)
    initial_puzzle  = shuffle_columns(initial_puzzle)
    initial_puzzle = shuffle_row_blocks(initial_puzzle)
    initial_puzzle = shuffle_column_blocks(initial_puzzle)

    map_numbers = [i for i in range(1,10)]
    random.shuffle(map_numbers)

    map_to_nums = lambda L:list(map(lambda y:map_numbers[y-1],L))
    initial_puzzle = list(map(lambda x:map_to_nums(x),initial_puzzle))

    trial = copy.deepcopy(initial_puzzle)
    unsolved_puzzle = give_unsolved(trial,0,0)
    return initial_puzzle,unsolved_puzzle



def give_unsolved(puzzle,row,column):
    global holes
    global k
    if holes == 0:
        return puzzle
    if column == 9:
        row = row+1
        column = 0
        if not k:
            k  = True
    if row == 9:
        return False
    val = puzzle[row][column]
    found_another = 0

        
    puzzle[row][column] = ''
    if not solver(copy.deepcopy(puzzle)):
        found_another = 1    

    if found_another !=0:
        puzzle[row][column] = val
        if row ==0 and column == 0:
            print(puzzle[0][0])
    else:
        holes-=1
        puzzle[row][column] = ''

    temp = give_unsolved(puzzle,row,column+1)
    if temp == False:
        return give_unsolved(puzzle,row,column+1)
    return temp

def solver(puzzle):
    possibilities = dict()
    Possibilities = []
    rows = [{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)}]
    columns = [{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)}]
    squares = [{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)},{i for i in range(1,10)}]

    empty_squares = []
    for i in range(9):
        for j in range(9):
            if puzzle[i][j]!='':
                rows[i].discard(puzzle[i][j])
                columns[j].discard(puzzle[i][j])
                squares[3*(i//3)+j//3].discard(puzzle[i][j])
            else:
                
                empty_squares.append((i,j))
    for coordinate in empty_squares:
        possibilities[coordinate] =  rows[coordinate[0]].intersection(columns[coordinate[1]]).intersection(squares[3*(coordinate[0]//3)+coordinate[1]//3])
    for i in range(9):
        for j in range(9):
            if (i,j) in empty_squares:
                coordinate = (i,j)
                possibilities[coordinate] =  rows[coordinate[0]].intersection(columns[coordinate[1]]).intersection(squares[3*(coordinate[0]//3)+coordinate[1]//3])
                Possibilities.append(possibilities[coordinate])
            else:
                Possibilities.append(set())
    possibilities = sorted(possibilities.items(),key = lambda item:len(item[1]))
    
    if (len(possibilities)==0):
        return False
    _index = 0
    
    while _index < len(possibilities) and len(possibilities[_index][1]) == 1:
        puzzle[possibilities[_index][0][0]][possibilities[_index][0][1]] = possibilities[_index][1].pop()
        _index+=1
    
    possibilities = possibilities[_index:]
    answers = [0]
    
    solve(puzzle,possibilities,answers,Possibilities)
    if (answers[0] > 1) :
        return False
    assert(answers[0]==1)
    return True

def solve(puzzle,possibilities,answers,Possibilities,index=0):
    if index == len(possibilities):
        answers[0]+=1
        return 
    if answers[0] > 1:
        return 
    Row = possibilities[index][0][0]
    Column = possibilities[index][0][1] 

    index_in_Possibilities = 9*Row+Column
    
    chances = list(Possibilities[index_in_Possibilities])
    for i in chances:
            puzzle[possibilities[index][0][0]][possibilities[index][0][1]] = i

            indices = []
            for temp in range(9):
                if i in Possibilities[9*Row+temp]:
                    indices.append(9*Row+temp)
                    Possibilities[9*Row+temp].remove(i)
                if i in Possibilities[9*temp+Column]:
                    indices.append(9*temp+Column)      
                    Possibilities[9*temp+Column].remove(i)      
            index1 = Row//3
            index2 = Column//3

            for box_ka_row in range(3*index1,3*index1+3):
                for box_ka_column in range(3*index2,3*index2+3):
                    if i in Possibilities[9*box_ka_row+box_ka_column]:
                        indices.append(9*box_ka_row+box_ka_column)
                        Possibilities[9*box_ka_row+box_ka_column].remove(i)
            solve(puzzle,possibilities,answers,Possibilities,index+1)

            puzzle[possibilities[index][0][0]][possibilities[index][0][1]] = ''

            for _index in indices:
                Possibilities[_index].add(i)




sudoku_puzzle = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
[6, 7, 2, 1, 9, 5, 3, 4, 8],
[1, 9, 8, 3, 4, 2, 5, 6, 7],
[8, 5, 9, 7, 6, 1, 4, 2, 3],
[4, 2, 6, 8, 5, 3, 7, 9, 1],
[7, 1, 3, 9, 2, 4, 8, 5, 6],
[9, 6, 1, 5, 3, 7, 2, 8, 4],
[2, 8, 7, 4, 1, 9, 6, 3, 5],
[3, 4, 5, 2, 8, 6, 1, 7, 9],
]




solved , unsolved = generate_puzzle()
display(solved)
print("\n")
display(unsolved)

