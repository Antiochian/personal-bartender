# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 11:24:59 2021

@author: Hal


substitute[ingredient] = [ideal1, ideal2, ... etc]
eg:
substitute['Elijah Craig 12-Year-Old Bourbon'] = {Bourbon, Maker's Mark bourbon, ... etc}'

                                                  
OR:
    categorize:
        
subs['bourbon'] = {'Elijah Craig 12-Year-Old Bourbon', 'Maker's Mark bourbon', etc... }
"""
import difflib

def read_file(filename='recipe_data.tsv'):
    cocktails = {}
    with open(filename) as inpfile:
        for line in inpfile:
            name, ingredient, amount, ingredient_type, glass, method = line.split('\t')
            name = name.lower()
            if name not in cocktails:
                cocktails[name] = {'ingredients' : [], 'glass' : glass, 'method': method}
            cocktails[name]['ingredients'].append( [ingredient, amount, ingredient_type] )
    return cocktails
      
def get_category(item, subs, lossy=False):
    parsed = item.lower().split()
    if 'bitters' in parsed:
            return 'bitters'
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
    if type(ingredient_names) == set:
        ingredient_names = list(ingredient_names)
    elif type(ingredient_names) != list:
        ingredient_names = [ingredient_names]
        
    
    for item in ingredient_names:
        cat = get_category(item, subs)
        subs[cat].add(item)     
    return

def gen_subs():
    subs = {'misc' : set()}
    category_list =  ['whiskey',
                     'bourbon', 
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
    

def get_valid_cocktails(my_ingredients,cocktails, subs):
    tol = 0.2
    #start with list of valid cocktails and delete them one by one (slow but who cares)
    valid = set(cocktails.keys())
    mycat = {get_category(i, subs, True) : i for i in my_ingredients}
    output = {}
    for name in cocktails:
        required = [ i[0] for i in cocktails[name]['ingredients'] ]
        valid = True
        recipe = []
        for req in required:
            if not valid:
                break
            reqcat = get_category(req, subs)
            if reqcat in mycat:
                best_match = difflib.get_close_matches(req, [mycat[reqcat]],2, cutoff=tol)
                #print(name,"wanted", req, "from category",reqcat,"best match:",best_match)
                if len(best_match) == 0:
                    valid = False
                    #print("\tFailed to find", req)
                elif len(best_match) == 1:
                    recipe.append( (req, best_match[0]) )
                    #print("wanted: ",req," matched with", best_match[0])
                else:
                    recipe.append( (req, best_match[1]) )
                    #add first brand name
                    #print("wanted: ",req," matched with", best_match[1])        
            else:
                #print("\tFailed to find", req)
                valid = False
        if valid:
            output[name] = recipe
    return output


def print_recipe(name, cocktails, partial=False,):
    name = name.lower()
    if name not in cocktails:
        print("Searching...")
        print('Cocktail "',name,'" not found in recipe book')
        print('Perhaps you meant: ')
        print_recipe( difflib.get_close_matches(name, cocktails.keys(),1)[0], partial)
        return False
    spacer = '--------------'
    print(spacer+'\n', name.upper(),'\n'+spacer)
    print('Ingredients:')
    for idx, item in enumerate(cocktails[name]['ingredients']):
        if item[2] == 'Build':
            tag = ''
        else:
            tag = ' ('+item[2]+')'
            
        printstr = item[0]+' - '+item[1]+ tag
        if partial and partial[idx][1].lower() != item[0].lower():
            print('\t',printstr.ljust(40),'----> REPLACE WITH: ', partial[idx][1])
        else:
            print('\t', printstr)
    print('\t Serve in: ', cocktails[name]['glass'])
    print('Instructions:')
    print('\t',cocktails[name]['method'])
    return True
    

def main():
    cocktails = read_file()
    #read all ingredients
    all_ingredients = set()
    for drink in cocktails:
        all_ingredients |= set( [ i[0] for i in cocktails[drink]['ingredients'] ])
        
    #generate subs dict
    subs = gen_subs()
    parse_ingredient(all_ingredients, subs)
    while True:
        #MENU loop
        print("\nWelcome to the bar. Can I recommend you a drink?")
        print('\t1: Search for specific drink')
        print('\t2: Input available ingredients')
        print('q to quit')
        choice = input(">: ")
        if choice == '1':
            search(cocktails)
        elif choice == '2':
            query(cocktails, subs)
        elif choice == 'q':
            return
        else:
            print("Unrecognised input:", choice)
    return

def query(cocktails, subs):
    ing = input("Simply write all your ingredients, seperated by commas: ")
    defaults = ['water', 'sugar']
    ing = [i.rstrip().lstrip() for i in ing.split(",")] + defaults
    
    results = get_valid_cocktails(ing, cocktails, subs)
    
    if not results:
        print("No cocktails found matching those ingredients")
    else:
        for name in results:
            print_recipe(name, cocktails, results[name])
    
def search(cocktails):
    term = input('Enter drink name: ')
    print_recipe(term, cocktails)
    return


if __name__ == '__main__':
    main()
    
#DEMO/DEBUG LINES:
#print subs

#print some recipe


