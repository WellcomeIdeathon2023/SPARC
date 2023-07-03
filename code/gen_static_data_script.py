import numpy as np
from scipy.stats import truncnorm
import pandas as pd
import operator
import json
import argparse

op_map = {'>=':operator.ge,'>':operator.gt,'<=':operator.le,'<':operator.lt,'==':operator.eq}


def simulate_categorical_feature(n_samples, n_categories, probs, seed=None):
    np.random.seed(seed)
    X = np.random.choice(n_categories, size=n_samples, p=probs)
    
    return X

def simulate_float_feature_by_Normal(n_samples, mean, std, seed=None):
    np.random.seed(seed)
    X = np.random.normal(loc=mean, scale=std, size=n_samples)
    return X

def simulate_float_feature_by_Uniform(n_samples, low, high, seed=None):
    np.random.seed(seed)
    X = np.random.uniform(low=low, high=high, size=n_samples)
    return X

def simulate_float_feature_by_truncatedNormal(n_samples, mean, std, low, high, seed=None):
    np.random.seed(seed)
    X = truncnorm.rvs((low - mean) / std, (high - mean) / std, loc=mean, scale=std, size=n_samples)
    return X


def simulate_int_feature_by_Normal(n_samples, mean, std, seed=None):
    np.random.seed(seed)
    X = np.random.normal(loc=mean, scale=std, size=n_samples)
    X = np.rint(X)
    return X

def simulate_int_feature_by_truncatedNormal(n_samples, mean, std, low, high, seed=None):
    np.random.seed(seed)
    X = truncnorm.rvs((low - mean) / std, (high - mean) / std, loc=mean, scale=std, size=n_samples)
    X = np.rint(X)
    return X


def simulate_feature_by_config(feature_type, n_samples, config, seed=None):
    """_summary_

    Args:
        feature_type (str): could be one of category, float, int
        n_samples (int): number of samples
        config (dict): configuration of the feature
        seed (int, optional): random seed.

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        X: simulated feature
    """
    
    X = None
    
    if feature_type == 'category':
        X = simulate_categorical_feature(n_samples, config['n_categories'], config['probs'], seed=seed)
        
    elif feature_type == 'float':
        if config['distribution'] == 'Normal':
            X = simulate_float_feature_by_Normal(n_samples, config['mean'], config['std'], seed=seed)
        elif config['distribution'] == 'Uniform':
            X = simulate_float_feature_by_Uniform(n_samples, config['low'], config['high'], seed=seed)
        elif config['distribution'] == 'truncatedNormal':
            X = simulate_float_feature_by_truncatedNormal(n_samples, config['mean'], config['std'], config['low'], config['high'], seed=seed)
        else:
            raise ValueError('distribution should be one of Normal, Uniform, truncatedNormal')
            
    elif feature_type == 'int':
        if config['distribution'] == 'Normal':
            X = simulate_int_feature_by_Normal(n_samples, config['mean'], config['std'], seed=seed)
        elif config['distribution'] == 'truncatedNormal':
            X = simulate_int_feature_by_truncatedNormal(n_samples, config['mean'], config['std'], config['low'], config['high'], seed=seed)
        else:
            raise ValueError('distribution should be one of Normal, truncatedNormal')
        
    else:       
        raise ValueError('feature_type should be one of categorical, float, int')
    return X


def simulate_static_data_by_config(config, seed=None):
    """_summary_

    Args:
        config (dict): configuration of the dataset
        seed (int, optional): random seed.

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        X: simulated dataset
    """
    
    df = pd.DataFrame()
    n_samples = config['n_samples']
    del config['n_samples']
    
    ### generate independent features first
    ind_config = config['independent']
    for fname, fconfig in ind_config.items():
        df[fname] = simulate_feature_by_config(fconfig['type'], n_samples, fconfig, seed=seed)
        if fconfig['type'] == 'category':
            for i, v in enumerate(fconfig["values"]):
                df[fname] = df[fname].replace(i, v).astype('category')
                
    ### generate dependent features
    cond_config = config['conditional']
    for fname, fconfig in cond_config.items():
        condtions = fconfig['conditions']
        for cond in condtions:
            cond_f = cond['feature_name']
            cond_v = cond['feature_value']
            
            if fconfig['type'] != 'category':
                cond['distribution'] = fconfig['distribution']
            else:
                cond["n_categories"] = fconfig["n_categories"]
            
            if df[cond_f].dtype.name == 'category':
                sids = df[df[cond_f] == cond_v].index
            else:
                sids = df.index
                k = 0
                while k < len(cond_v)-1:
                    op = op_map[cond_v[k]]
                    bound = cond_v[k+1]
                    sids = sids[op(df.loc[sids,cond_f], bound)]
                    k+=2
                
            df.loc[sids, fname] = simulate_feature_by_config(fconfig['type'], len(sids), cond, seed=seed)
        
        if fconfig['type'] == 'category':
            for i, v in enumerate(fconfig["values"]):
                df[fname] = df[fname].replace(i, v).astype('category')
            
    return df




parser = argparse.ArgumentParser()
parser.add_argument('--config_path',default='../data/static_data_config.json', help='Path to config file')
parser.add_argument('--save_path',default='../data/static_data.csv', help='Path to save data')
parser.add_argument('--seed',default=42,type=int, help='Random seed')

args = parser.parse_args()

with open(args.config_path, "r") as infile:
    configs = json.load(infile)
    
sdf = simulate_static_data_by_config(configs, seed=args.seed)
sdf.to_csv(args.save_path, index=False)

