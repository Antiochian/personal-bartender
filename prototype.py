# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 11:24:59 2021

@author: Hal


Table Of Contents:
------------------
A) DISPLAY FUNCTIONS
    i) print_splash_screen
        -displays ASCII butler image
    ii) print_recipe
        - Formats and prints a given cocktail's recipe
        
B) UTILITY FUNCTIONS
    i) read_file
        -reads input recipe datafile
    ii) parse_ingredient
        -places a list of ingredients into the substitutions dictionary
    iii) get_category
        -assigns an ingredient a category of ingredient "type"
    iv) gen_subs
        -initialises empty substitutions dictionary
    v) eval_cocktail
        -given available ingredients, check if a given cocktail can be made
    vi) get_valid_cocktail
        -given available ingredients, find all possible cocktails that can be made
    
C) PRIMARY DRIVER FUNCTIONS
    i) search
        -search for specific recipe and print it
    ii) query
        -take user input on available ingredients and return matching recipes
    iii) get_random
        -print random recipe
D) MAIN
    i) main
        -its the main function. nuff said.
                   
"""
import difflib
import random

#####################
# DISPLAY FUNCTIONS #
#####################
    
def print_splash_screen(text = ''):   
    #prints cute ASCII butler saying something ('text')
    butler = ["        .--.",
              "       /    \            ",
              "      ## a  a       _    "+text,
              "      (   '._)     |_|",
              "       |'-- |      | |", 
              "     _.\___/_   ___|_|___",
              "   .'\> \Y/|<'.  '._.-'",
              "  /  \ \_\/ /  '-' /",
              "  | --'\_/|/ |   _/",
              "  |___.-' |  |`'`",
              "    |     |  |",
              "    |    / './",
              "   /__./` | |",
              "      \   | |",
              "       \  | |",
              "       ;  | |",
              "      /  | |",
              "     |___\_.\_",
              "     `-'--'---'  "]
    [print(i) for i in butler]
    return


def print_recipe(name, cocktails, partial=False,):
    #print pretty recipe for a given cocktail name
    name = name.lower()
    if name not in cocktails:
        print("\nSearching...\n")
        print('Cocktail "',name,'" not found in recipe book\n')
        #attempt to fix mis-spellings (eg: "gin and tonic" vs "gin & tonic")
        best_match = difflib.get_close_matches(name, cocktails.keys(),1)
        if best_match:
            print('Perhaps you meant: ')
            print_recipe( best_match[0],cocktails, partial)
        return False
    spacer = '--------------'
    print(spacer+'\n', name.upper(),'\n'+spacer)
    print('Ingredients:')
    for idx, item in enumerate(cocktails[name]['ingredients']):
        if item[2] == 'Build':
            tag = ''
        else:
            tag = ' ('+item[2]+')' #display if ingredient is not essential "build" ingredient
            
        printstr = item[0]+' - '+item[1]+ tag
        if partial and partial[idx][1].lower() != item[0].lower():
            print('\t',printstr.ljust(40),'----> YOU HAVE: ', partial[idx][1])
        else:
            print('\t', printstr)
    print('\t Serve in: ', cocktails[name]['glass'])
    print('Instructions:')
    print('\t',cocktails[name]['method'])
    return True

#####################
# UTILITY FUNCTIONS #
#####################

def read_file(filename='recipe_data.tsv'):
    #read data file
    cocktails = {}
    all_ingredients = set()
    with open(filename) as inpfile:
        for line in inpfile:
            if line[0] == '\n' or line[0] == '#': #ignore blank/commented out lines
                continue
            name, ingredient, amount, ingredient_type, glass, method = line.split('\t')
            all_ingredients.add(ingredient)
            name = name.lower()
            if name not in cocktails:
                cocktails[name] = {'ingredients' : [], 'glass' : glass, 'method': method}
            cocktails[name]['ingredients'].append( [ingredient, amount, ingredient_type] )
    del cocktails['drink'] #remove header line fudge
    return cocktails, all_ingredients

def get_category(item, subs, lossy=False):
    # Convert name of item into category of item
    # For example: 
    # "12-Year Aged Scotch Whisky" --> whiskey
    # "Belvedere Smooth Vodka --> vodka
    # "Lemon Slice" --> lemon
    # "Cynar" --> misc
    parsed = item.lower().split()
    #manual fudges for idosyncratic edge cases
    if 'bitters' in parsed:
        return 'bitters'
    elif 'coke' in parsed:
        return 'coca-cola'
    elif 'whisky' in parsed:
        return 'whiskey'
    elif 'beer' in parsed or parsed == ['fever-tree', 'ginger', 'ale']:
        return 'ginger beer'
    elif 'rhum' in parsed:
        return 'rum'
    elif 'lillet' in parsed:
        return 'vermouth'
    else:
        for key in subs:
            if key in parsed:
                return key
    if lossy:
        best_guess = difflib.get_close_matches(item, subs.keys(), cutoff=0.5)
        #print("lossily guessed", best_guess, "for ", item)
        if best_guess:
            return best_guess[0]
    return 'misc'

def parse_ingredient(ingredient_names, subs):
    #add ingredient/list of ingredients to subs (substitution) dictionary
    if type(ingredient_names) == set:
        ingredient_names = list(ingredient_names)
    elif type(ingredient_names) != list:
        ingredient_names = [ingredient_names]
        
    for item in ingredient_names:
        cat = get_category(item, subs)
        subs[cat].add(item)     
    return

def gen_subs():
    #Create empty dict of handpicked categories for "types" of ingredient
    #These categories help searching be faster, but even ingredients that
    #dont fit into a category should work fine, they just get shunted into 
    #the 'misc' section
    subs = {'misc' : set()}
    category_list =  ['whiskey',
                     'bourbon', 
                     'soju',
                     'wine',
                     'vodka',
                     'gin',
                     'port',
                     'brandy',
                     'rum',
                     'tequila',
                     'champagne',
                     'prosecco',
                     'absinthe',
                     'ale',
                     'cognac',
                     'sake',
                     'sherry',
                     'pisco',
                     'suze',
                     'syrup',
                     'vermouth',
                     'chartreuse',
                     'tonic', 
                     'soda',
                     'coca-cola',
                     'water',
                     'bitters',
                     'preserves',
                     'egg',
                     'cucumber',
                     'lemon',
                     'lime',
                     'orange',
                     'strawberry',
                     'grapefruit',
                     'cinnamon',
                     'mint',
                     'salt',
                     'sugar',
                     'ginger beer',
                     'tea']
    for category in category_list:
        subs[category] = set([category])
    return subs

def eval_cocktail(my_ingredients, my_cat, name, cocktails, subs):
    # given available resources and a specific cocktail recipe, return
    # if it is possible (return 2), almost-possible (return 1) or impossible 
    # (return 0) to make
    required = [ i for i in cocktails[name]['ingredients'] ]
    partial = False
    recipe = []
    for ingred in required:
        req = ingred[0]
        reqcat = get_category(req, subs)
        if reqcat in my_cat: 
            #makes search faster by checking just category instead of indiv. ingredients
            best_match = difflib.get_close_matches(req, [my_cat[reqcat]],2, cutoff=0)
            if best_match:
                recipe.append( (req, best_match[-1]) ) 
            else:
                if ingred[2] == 'Build':
                    return 0, None #failed match
                else:
                    partial = True
                    recipe.append( (req, '(Missing garnish)') )

        else:
            if ingred[2] == 'Build':
                return 0, None #failed match
            else:
                partial = True
                recipe.append( (req, '(Missing garnish)') )
    if partial:
        return 1, recipe #partial match
    else:
        return 2, recipe #perfect match

def get_valid_cocktails(my_ingredients,cocktails, subs):
    #given list of options my_ingredients, return all cocktails that can be made
    #also return recipes that are only missing garnishes (I judge these as non-essential)
    my_cat = {get_category(i, subs, True) : i for i in my_ingredients}
    partial_matches, perfect_matches = {}, {}
    for name in cocktails:
        res, recipe = eval_cocktail(my_ingredients, my_cat, name, cocktails, subs)
        if res == 2: #perfect match
            perfect_matches[name] = recipe
        elif res == 1: #partial match
            partial_matches[name] = recipe
        else: #failed
            pass 
    return partial_matches, perfect_matches


############################
# PRIMARY DRIVER FUNCTIONS #
############################

def search(cocktails):
    name = input('Enter drink name: ')
    print_recipe(name, cocktails)
    input("Press any key to return to menu: ")
    return

def query(cocktails, subs):
    ing = input("Simply write all your ingredients, seperated by commas: ")
    defaults = ['water', 'sugar']
    ing = [i.rstrip().lstrip() for i in ing.split(",")] + defaults    
    partial, perfect = get_valid_cocktails(ing, cocktails, subs) 
    if not perfect:
        print('--------------')
        print("No cocktails found matching those ingredients")
    else:
        for name in perfect:
            print_recipe(name, cocktails, perfect[name])
        print('--------------')
        print(len(perfect), 'cocktails found.')
    if partial:
        choice = input(str(len(partial))+' almost-matches (only missing garnishes) also found. Show? [Y/n]: ')
        if choice.lower() == 'y':
            for name in partial:
                print_recipe(name, cocktails, partial[name])
    input("Press any key to return to menu: ")
    return

def get_random(cocktails):
    name = random.choice(list(cocktails.keys()))
    print_recipe(name, cocktails)
    input("Press any key to return to menu: ")
    return
    
#############
# MAIN      #
#############

def main():
    #read recipes in from datafile
    cocktails, all_ingredients = read_file()
    #read all ingredients
    all_ingredients = set()
    #generate subs dict
    subs = gen_subs()
    parse_ingredient(all_ingredients, subs)
    while True:
        #MENU loop
        print('\n'*20)
        print_splash_screen('Welcome to the bar. Can I recommend you a drink?')
        print("\n")
        print('\t1: Search for specific drink')
        print('\t2: Input available ingredients')
        print('\t3: Get random cocktail')
        print('q to quit')
        choice = input(">: ")
        if choice == '1':
            search(cocktails)
        elif choice == '2':
            query(cocktails, subs)
        elif choice == '3':
            get_random(cocktails)
        elif choice == 'q':
            return
        else:
            print("Unrecognised input:", choice)
    return


if __name__ == '__main__':
    main()
    pass
    
#DEMO/DEBUG LINES
#------------------------------
# cocktails = read_file()
# #read all ingredients
# all_ingredients = set()
# for drink in cocktails:
#     all_ingredients |= set( [ i[0] for i in cocktails[drink]['ingredients'] ])
    
# #generate subs dict
# subs = gen_subs()
# parse_ingredient(all_ingredients, subs)
# ing = ['vodka', 'coke']
# results = get_valid_cocktails(ing, cocktails, subs)
# print(results)
