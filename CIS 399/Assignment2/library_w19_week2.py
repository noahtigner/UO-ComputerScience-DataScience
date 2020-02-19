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
