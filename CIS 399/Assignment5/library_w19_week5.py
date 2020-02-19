from functools import reduce
from operator import itemgetter
import numpy as np
import pandas as pd
from types import SimpleNamespace
import random

def predictor_case(row, pred, target):
  case_dict = {(0,0): 'true_negative', (1,1): 'true_positive', (0,1): 'false_negative', (1,0): 'false_positive'}
  actual = row[target]
  prediction = row[pred]
  case = case_dict[(prediction, actual)]
  return case

def accuracy(cases):
    if len(cases) == 0:
        return 0
    
    tp = 0
    tn = 0
    fp = 0
    fn = 0
   
    if 'true_positive' in cases:
        tp = cases['true_positive']
    if 'true_negative' in cases:
        tn = cases['true_negative']
    if 'false_positive' in cases:
        fp = cases['false_positive']
    if 'false_negative' in cases:
        fn = cases['false_negative']

    if tp+tn+fp+fn != 0:
        return (tp+tn)/(tp+tn+fp+fn)
    return 0

def f1(cases):
    if len(cases) == 0:
        return 0
    
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    recall = 0
    precision = 0
   
    if 'true_positive' in cases:
        tp = cases['true_positive']
    if 'true_negative' in cases:
        tn = cases['true_negative']
    if 'false_positive' in cases:
        fp = cases['false_positive']
    if 'false_negative' in cases:
        fn = cases['false_negative']
    
    if tp+fn != 0:
        recall = 1.0*tp/(tp+fn)  # positive correct divided by total positive in the table
    if tp+fp != 0:
        precision = 1.0*tp/(tp+fp) # positive correct divided by all positive predictions made
    if recall != 0 and precision != 0:
        return 2/(1/recall + 1/precision)
    return 0

def informedness(cases):
    if len(cases) == 0:
        return -1
    
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    recall = 0.0
    specificity = 0.0
   
    if 'true_positive' in cases:
        tp = cases['true_positive']
    if 'true_negative' in cases:
        tn = cases['true_negative']
    if 'false_positive' in cases:
        fp = cases['false_positive']
    if 'false_negative' in cases:
        fn = cases['false_negative']
        
    if tp+fn != 0:    
        recall = 1.0*tp/(tp+fn)  # positive correct divided by total positive in the table
    if tn+fp != 0:
        specificty = 1.0*tn/(tn+fp) # negative correct divided by total negative in the table
    return (recall + specificty) - 1.0

def probabilities(counts):
    count_0 = 0 if 0 not in counts else counts[0]  #could have no 0 values
    count_1 = 0 if 1 not in counts else counts[1]
    total = count_0 + count_1
    probs = (0,0) if total == 0 else (count_0/total, count_1/total)  #build 2-tuple
    return probs

def gini(counts):
    (p0,p1) = probabilities(counts)
    sum_probs = p0**2 + p1**2
    gini = 1 - sum_probs
    return gini

def gig(starting_table, split_column, target_column):
    
    #split into two branches, i.e., two sub-tables
    true_table = starting_table.loc[starting_table[split_column] == 1]
    false_table = starting_table.loc[starting_table[split_column] == 0]
    
    #Now see how the target column is divided up in each sub-table (and the starting table)
    true_counts = true_table[target_column].value_counts()  # Note using true_table and not starting_table
    false_counts = false_table[target_column].value_counts()  # Note using false_table and not starting_table
    starting_counts = starting_table[target_column].value_counts() 
    
    #compute the gini impurity for the 3 tables
    starting_gini = gini(starting_counts)
    true_gini = gini(true_counts)
    false_gini = gini(false_counts)

    #compute the weights
    starting_size = len(starting_table.index)
    true_weight = 0.0 if starting_size == 0 else len(true_table.index)/starting_size
    false_weight = 0.0 if starting_size == 0 else len(false_table.index)/starting_size
    
    #wrap it up and put on a bow
    gig = starting_gini - (true_weight * true_gini + false_weight * false_gini)
    
    return gig

def build_pred(column, branch):
    return lambda row: row[column] == branch

def find_best_splitter(table, choice_list, target):
  
    assert (len(table)>0),"Cannot split empty table"
    assert (target in table),"Target must be column in table"
    
    gig_scores = map(lambda col: (col, gig(table, col, target)), choice_list)  #compute tuple (col, gig) for each column
    gig_sorted = sorted(gig_scores, key=lambda item: item[1], reverse=True)  # sort on gig
    return gig_sorted

def generate_table(table, conjunction):
  
    assert (len(table)>0),"Cannot generate from empty table"

    sub_table = reduce(lambda subtable, pair: subtable.loc[pair[1]], conjunction, table)
    return sub_table

def compute_prediction(table, target):
  
    assert (len(table)>0),"Cannot predict from empty table"
    assert (target in table),"Target must be column in table"
    
    counts = table[target].value_counts()  # counts looks like {0: v1, 1: v2}

    if 0 not in counts:
        prediction = 1
    elif 1 not in counts:
        prediction = 0
    elif counts[1] > counts[0]:  # ties go to 0 (negative)
        prediction = 1
    else:
        prediction = 0

    return prediction

def build_tree_iter(table, choices, target, hypers={} ):

    assert (len(choices)>0),"Must have at least one column in choices"
    assert (target in table), "Target column not in table"
    assert (len(table) > 1), "Table must have more than 1 row"
    
    k = hypers['max-depth'] if 'max-depth' in hypers else min(4, len(choices))
    gig_cutoff = hypers['gig-cutoff'] if 'gig-cutoff' in hypers else 0.0
    
    def iterative_build(k):
        columns_sorted = find_best_splitter(table, choices, target)
        (best_column, gig_value) = columns_sorted[0]
        
        #Note I add _1 or _0 to make it more readable for debugging
        current_paths = [{'conjunction': [(best_column+'_1', build_pred(best_column, 1))],
                          'prediction': None,
                          'gig_score': gig_value},
                         {'conjunction': [(best_column+'_0', build_pred(best_column, 0))],
                          'prediction': None,
                          'gig_score': gig_value}
                        ]
        k -= 1  # we just built a level as seed so subtract 1 from k
        tree_paths = []  # add completed paths here
        
        while k>0:
            new_paths = []
            for path in current_paths:
                old_conjunction = path['conjunction']  # a list of (name, lambda)
                before_table = generate_table(table, old_conjunction)  #the subtable the current conjunct leads to
                columns_sorted = find_best_splitter(before_table, choices, target)
                (best_column, gig_value) = columns_sorted[0]
                if gig_value > gig_cutoff:
                    new_path_1 = {'conjunction': old_conjunction + [(best_column+'_1', build_pred(best_column, 1))],
                                'prediction': None,
                                 'gig_score': gig_value}
                    new_paths.append( new_path_1 ) #true
                    new_path_0 = {'conjunction': old_conjunction + [(best_column+'_0', build_pred(best_column, 0))],
                                'prediction': None,
                                 'gig_score': gig_value}
                    new_paths.append( new_path_0 ) #false
                else:
                    #not worth splitting so complete the path with a prediction
                    path['prediction'] = compute_prediction(before_table, target)
                    tree_paths.append(path)
            #end for loop
            
            current_paths = new_paths
            if current_paths != []:
                k -= 1
            else:
                break  # nothing left to extend so have copied all paths to tree_paths
        #end while loop

        #Generate predictions for all paths that have None
        for path in current_paths:
            conjunction = path['conjunction']
            before_table = generate_table(table, conjunction)
            path['prediction'] = compute_prediction(before_table, target)
            tree_paths.append(path)
        return tree_paths

    return {'paths': iterative_build(k), 'weight': None}

def tree_predictor(row, tree):
    
    #go through each path, one by one (could use a map instead of for loop?)
    for path in tree['paths']:
        conjuncts = path['conjunction']
        result = map(lambda tuple: tuple[1](row), conjuncts)  # potential to be parallelized
        if all(result):
            return path['prediction']
    raise LookupError('No true paths found for row: ' + str(row))
    
def path_id(row, tree):
  
    assert (len(tree['paths']) > 0), "Tree must have at least one path"
    i = 0
    for path in tree["paths"]:
        conjuncts = path['conjunction']
        result = map(lambda tuple: tuple[1](row), conjuncts)
        if all(result):
            return i
        i+=1

def reorder_paths(table, tree):
    pcounts = loan_table.apply(lambda row: path_id(row, tree), axis=1)
    pdict = dict(pcounts.value_counts())
    plist = list(pdict.items())
    plist = list(reversed(sorted(plist,key=itemgetter(1))))
    print(plist)
    new_paths = []
    for path in plist:
        new_paths.append(tree["paths"][path[0]])
    return new_paths

def produce_scores(table, tree, target):
    scratch_table = pd.DataFrame(columns=['prediction', 'actual'])
    scratch_table['prediction'] = table.apply(lambda row: tree_predictor(row, tree), axis=1)
    scratch_table['actual'] = table[target]  # just copy the target column
    cases = scratch_table.apply(lambda row: predictor_case(row, pred='prediction', target='actual'), axis=1)
    vc = cases.value_counts()
    return [accuracy(vc), f1(vc), informedness(vc)]

def compute_training(slices, left_out):
    training_slices = []
    for i,slice in enumerate(slices):
        if i == left_out:
            continue
        training_slices.append(slices[i])
    return pd.concat(training_slices)  # note we are returning a table (DataFrame)

def k_fold(table, k, target, hypers, candidate_columns):
  
    #set up the table where we will record fold results
    result_columns = ['name',  'accuracy', 'f1', 'informedness']
    k_fold_results_table = pd.DataFrame(columns=result_columns)
    
    #generate the slices
    total_len = len(table.index)
    slice_size = int(total_len/(1.0*k))
    slices = []
    for i in range(k-1):
        a_slice =  table[i*slice_size:(i+1)*slice_size]
        slices.append( a_slice )
    slices.append( table[(k-1)*slice_size:] )  # whatever is left
    
    #generate test results
    all_scores = []  #keep track of all k results
    for i in range(k):
        test_table = slices[i]
        train_table = compute_training(slices, i)
        fold_tree = build_tree_iter(train_table, candidate_columns, target, hypers)  # train
        scores = produce_scores(test_table, fold_tree, target)  # test
        results_row = {'name': 'fold_'+str(i), 'accuracy': scores[0], 'f1': scores[1], 'informedness': scores[2]}
        k_fold_results_table = k_fold_results_table.append(results_row,ignore_index=True)
        all_scores.append(scores)
    
    #compute average of all folds
    avg_scores = tuple(reduce(lambda total, triple: np.add(triple, total), all_scores)/k)
    results_row = {'name': 'average', 'accuracy': avg_scores[0], 'f1': avg_scores[1], 'informedness': avg_scores[2]}
    k_fold_results_table = k_fold_results_table.append(results_row,ignore_index=True)
    
    #note that I add the meta comment as last step to avoid it being wiped out
    k_fold_results_table.meta = SimpleNamespace()
    k_fold_results_table.meta.hypers  = hypers # adds comment to remind me of hyper params used
    
    return k_fold_results_table



