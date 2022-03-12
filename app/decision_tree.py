'''
Decision Tree Classification Analysis

Liz Colavita
'''

import sys
import pandas as pd
import math
from random import seed
from random import choice

def go():
    '''
    Function for data processing, building model, and testing model
    '''

    #data processing
    training_set, testing_set = process_data()

    #build classification model from training data
    training_set_copy = training_set.copy()
    root = Node(training_set_copy)
    decision_tree = build_model(root)

    #classify testing data - all variables
    testing_set_copy = testing_set.copy()
    result_lst = [None] * testing_set_copy.shape[0]
    result_lst_all = classify_data(decision_tree, testing_set_copy, result_lst)
    match_rate_all = calculate_match(testing_set_copy['crime_rate'], result_lst_all)

    #build results dict
    results_dict = {}
    results_dict["all variables"] = match_rate_all

    #classify testing data - excluding one variable each iteration
    column_list = create_col_list(training_set)
    for col in column_list:
        training_set_copy_tmp = training_set.copy()
        training_set_copy = training_set_copy_tmp.drop(col, axis = 1)
        root = Node(training_set_copy)
        decision_tree = build_model(root)
        testing_set_copy = testing_set.copy()
        result_lst = [None] * testing_set_copy.shape[0]
        result_lst2 = classify_data(decision_tree, testing_set_copy, result_lst)
        results_dict[col] = calculate_match(testing_set_copy['crime_rate'], result_lst2)
        
    return results_dict

def process_data():
    '''
    Loads and processes data creating a dataframe with categorized variables, training data, and testing data
    
    Returns:
        df_cat: (Pandas dataframe) dataframe with categorized variables
        training_set: (Pandas dataframe) dataframe for building classification model
        testing_set: (Pandas dataframe) dataframe for testing classification model
    '''
    ## load and process data

    df = pd.read_csv("../data/food_data.csv")

    # categorize variables
    cat_series = []
    community_id = df["community_area"]
    cat_series.append(community_id)
    for column in df.columns:
        if column != "community_area":
            cat = pd.cut(df[column], 5, labels = ['Very Low', 'Low', 'Medium', ' High', 'Very High'])
            cat_series.append(cat)
    
    df_cat = pd.concat(cat_series, axis =1)

    # create training and testing sets
    seed(31020)
    training_indices = []
    sequence = [i for i in range(72)]
    for _ in range(32):
        ind = choice(sequence)
        training_indices.append(ind)

    df_cat_copy = df_cat.copy()
    training_set = df_cat_copy.sample(frac=0.7,random_state=200)

    testing_set = df_cat_copy.drop(training_set.index)
    testing_set1 = testing_set.reset_index()
    testing_set2 = testing_set1.drop('index', axis = 1)

    return training_set, testing_set2

    
def build_model(node):
    '''
    Recursive model to build out decisions tree using training set
    Inputs:
        node: Node object for further splitting
        column_set: set of attribute column names
    Output:
        decision_tree: Node object
    '''
    df = node.dataframe
    column_list = create_col_list(df)
    target_col = df['crime_rate']
    node.label = determine_label(target_col)

    #first stopping condition: target class attribute is the same
    # for all entries in S
    if target_col.nunique == 1:
        return node

    #second stopping condition: remaining observations share the same values
    # for the attributes in column_set
    one_unique_val =[]
    for col in column_list:
        if df[col].nunique() == 1:
            one_unique_val.append(1)

    if len(one_unique_val) == len(column_list):
        return node

    #third stopping condition: only target column left
    if not column_list:
        return node

    #further splitting
    max_gain_ratio = -1
    split_col = None

    #find split_col
    for col in column_list:
        attribute = df[col]
        attr_dict = {}
        attr_values = attribute.unique()
        gini_T = compute_gini(target_col)
        for val in attr_values:
            p = attribute[attribute == val].size / attribute.size
            temp_subset = df[df[attribute.name] == val]
            temp_col = temp_subset.iloc[:,-1]
            gini_T_subset = compute_gini(temp_col)
            attr_dict[val] = (p, gini_T_subset)

        #compute gain_ratio for given attribute
        gain_ratio_attr = compute_gain_ratio(gini_T, attr_dict)

        #update max_gain_ratio is applicable
        if gain_ratio_attr > max_gain_ratio:
            max_gain_ratio = gain_ratio_attr
            node.split_col = attribute.name
            split_col = attribute

        elif gain_ratio_attr == max_gain_ratio:
            if attribute.name < split_col.name:
                max_gain_ratio = gain_ratio_attr
                node.split_col = attribute.name
                split_col = attribute

    # stop recursion if largest gain ratio is zero
    if max_gain_ratio == 0:
        return node

    #generate children based on the splitting column
    column_list.remove(split_col.name)

    splits = list(split_col.unique())

    for split in splits:
        node.add_out_edge(split)
        subset1 = df[df[split_col.name] == split]
        subset2 = subset1[[col for col in subset1.columns
            if col in column_list or col == target_col.name]]
        child_node = Node(subset2, in_edge = split)
        node.add_child(child_node)

    for child in node.children:
        build_model(child)

    return node

def calculate_match(expected_values, actual_values):
    '''
    Calculates the proportion of matching classifications between expected and actual values

    Inputs:
        expected_values: (Pandas series) expected (known) classification of crime rate
        actual_values: (Pandas series) actual (predicted) classification of crime rate from
        decision tree model
    Outputs:
        proportion: (float) proportion of correctly classified crime rates
    '''
    n = len(expected_values)
    matches = 0
    for i in range(n):
        if expected_values[i] == actual_values[i]:
            matches += 1
    
    return matches/n


def create_col_list(df):
    '''
    Creates a list of column names (attributes) of a dataframe
    Inputs:
        df: dataframe
    Outputs:
        column_list: set of attribute column names
    '''
    
    col_list = [col for col in df.columns if col != 'crime_rate' and col != 'community_area']

    return col_list


def determine_label(target_col):
    '''
    Determines the label of a node
    Inputs: target_col (pandas Series)
    Outputs: value for the node label
    '''
    value_counts = target_col.value_counts()

    if value_counts.nunique() == 1:
        min_idx = None
        for idx,_ in value_counts.iteritems():
            if not min_idx:
                min_idx = idx
            elif idx < min_idx:
                min_idx = idx
        return min_idx

    return value_counts.idxmax()


def compute_gini(col):
    '''
    Computes the gini score and split info for an attribute column
    Inputs:
        df: (Pandas dataframe) Pandas dataframe representing the multiset
        col: (Pandas Series) Attribute for which we are computing the gini score
    Outputs: gini score
    '''
    proportions = col.value_counts(normalize = True)
    sum1 = 0
    for prop in proportions:
        sum1 += prop ** 2
    gini_score = 1 - sum1

    return gini_score


def compute_gain_ratio(gini_T, attr_dict):
    '''
    Computes gain ratio for a given attribute
    Inputs:
        ginit_T: (float) gini score for parent (gini(S,T))
        attr_dict: (dict) where keys are the values the attribute takes
            and the values are tuple of length two with the p(attr = key) and gini(S, attr = key)
    Outputs:
        gain_ratio_attr: (float) gain ratio for given attribute
    '''
    gini_split = 0
    split_info = 0
    for value in attr_dict.values():
        gini_split += (value[0] * value[1])
        split_info += (value[0] * math.log2(value[0]))

    gain_attr = gini_T - gini_split

    if split_info == 0:
        gain_ratio_attr = 0
    else:
        gain_ratio_attr = gain_attr/ (-1 * split_info)

    return gain_ratio_attr


def classify_data(tree, df, result_lst):
    '''
    Traverses a model (tree) built from training data and
    generates predicted values of a target attribute for testing data
    Inputs:
        tree: Node object
        df: Pandas dataframe
        result_lst: list
    Outputs:
        result_lst: list
    '''
    if not tree.children:
        label = tree.label
        for idx,_ in df.iterrows():
            result_lst[idx] = label

    else:
        attr = tree.split_col
        attr_vals = list(df[attr].unique())

        for child in tree.children:
            split_val = child.in_edge
            subset = df[df[attr] == split_val]
            classify_data(child, subset, result_lst)

        for val in attr_vals:
            if val not in tree.out_edges:
                label = tree.label
                subset = df[df[attr] == val]
                for idx,_ in subset.iterrows():
                    result_lst[idx] = label

    return result_lst


class Node(object):
    '''
    Creates an instance of the Node class to build out the decision tree model
    '''
    def __init__(self, dataframe, in_edge = None):
        '''
        Creates an instance of the node class
        Inputs:
            dataframe: (Pandas df)
            in_edge: (str) attribute value = j for parent's split column attribute
        '''
        self.dataframe = dataframe
        self.label = None
        self.split_col = None
        self.in_edge = in_edge
        self.out_edges = []
        self.children = []


    def add_child(self, obj):
        '''
        Adds a child node to the parent node
        Inputs:
            obj: Node object
        Outputs:
            updates node.children attribute
        '''
        self.children.append(obj)


    def add_out_edge(self, string):
        '''
        Adds an out going edge (specific value found in the node's split column) to a node
        Inputs:
            string: (str) one value (A = j) of the node's split column
        Outputs:
            updates node.out_edges attribute
        '''
        self.out_edges.append(string)


if __name__ == "__main__":
    app.run
   
