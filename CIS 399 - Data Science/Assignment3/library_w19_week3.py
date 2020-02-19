def predictor_case(row, pred, target):
  case_dict = {(0,0): 'true_negative', (1,1): 'true_positive', (0,1): 'false_negative', (1,0): 'false_positive'}
  actual = row[target]
  prediction = row[pred]
  case = case_dict[(prediction, actual)]
  return case

def accuracy(cases):
    tp = cases['true_positive']
    tn = cases['true_negative']
    fp = cases['false_positive']
    fn = cases['false_negative']
    return (tp + tn)/(tp+tn+fp+fn)

def f1(cases):
    
    #the heart of the matrix
    tp = cases['true_positive']
    fn = cases['false_negative']
    tn = cases['true_negative']
    fp = cases['false_positive']
    
    #other measures we can derive
    recall = 1.0*tp/(tp+fn)  # positive correct divided by total positive in the table
    precision = 1.0*tp/(tp+fp) # positive correct divided by all positive predictions made
    
    #now for the one we want
    f1 = 2/(1/recall + 1/precision)
    
    return f1

def informedness(cases):
    tp = cases['true_positive']
    fn = cases['false_negative']
    tn = cases['true_negative']
    fp = cases['false_positive']
    recall = 1.0*tp/(tp+fn)  # positive correct divided by total positive in the table
    specificty = 1.0*tn/(tn+fp) # negative correct divided by total negative in the table
    J = (recall + specificty) - 1
    return J

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
