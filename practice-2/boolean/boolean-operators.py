array = [[True, True], [True, False], [False, True], [False, False]]

# I decided to construct truth table for NOT, AND, OR, XOR
for i in range(0, 5):
    if i == 0:
        print(f" \033[4m{' ' * 55}\033[0m ")
        print("|\033[1;4m   P   \033[0m|\033[1;4m   Q   \033[0m|\033[1;4m  ¬ P  \033[0m|\033[1;4m  ¬ Q  \033[0m|\033[1;4m P ∧ Q \033[0m|\033[1;4m P ∨ Q \033[0m|\033[1;4m P ⊕ Q \033[0m|")
        continue
    for j in range(0, 7):
        match j:
            case 0:
                print("|\033[4m {:<5} \033[0m".format(f"{array[i - 1][0]}"), end="")
            case 1:
                print("|\033[4m {:<5} \033[0m".format(f"{array[i - 1][1]}"), end="")
            case 2:
                print("|\033[4m {:<5} \033[0m".format(f"{not array[i - 1][0]}"), end="")
            case 3:
                print("|\033[4m {:<5} \033[0m".format(f"{not array[i - 1][1]}"), end="")
            case 4:
                print("|\033[4m {:<5} \033[0m".format(f"{array[i - 1][0] and array[i - 1][1]}"), end="")
            case 5:
                print("|\033[4m {:<5} \033[0m".format(f"{array[i - 1][0] or array[i - 1][1]}"), end="")
            case 6:
                print("|\033[4m {:<5} \033[0m|".format(f"{array[i - 1][0] ^ array[i - 1][1]}"))
 