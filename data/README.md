
# Configuration of the static data generator


1. The number of samples to generate ("n_samples") must be included in the config file
2. The rest of the config file is optional, each field starts with the feature name, the feature name must be unique and cannot be "n_samples".
3. All features must be under either "independent" or "conditional" feild.
4. "type" is a mandatory feild of each feature in the config file, the type can be "category", "float", "int". Mandatory feilds for each file is as in below table:

    | Type       | Mandatory Field |
    |------------|-----------------|
    | category   | n_categories, probs, values    |
    | float      | distribution    |
    | int        | distribution    |


8. "distribution" can be "uniform", "normal", "truncatedNormal". Mandatory fields for each distribution is as in below table:

    | Distribution      | Mandatory Field |
    |------------|-----------------|
    | Normal   | mean, std    |
    | Uniform      | low, high    |
    | truncatedNormal        | mean, std, low, high    |
    | Dirichlet   | alpha    |
    | Beta   | alpha, beta    |

9. For conditional features, "conditions" is a mandatory feild and it includes all condtional distributions in a list. For conditioning on float or int features, the "feature_value" in a condition is in the form of ["operator1",boundary_value1,"operator2",boundary_value2], which should at least has one operator and one boundary value. For example:
```
        "dummy_int_feature":{
            "type": "int",
            "distribution": "truncatedNormal",
            "conditions":[
                {"feature_name": "dummy_float_feature",
                "feature_value": [">",0.5],
                "mean": 5,
                "std": 2,
                "low": 0,
                "high": 10},
                {"feature_name": "dummy_float_feature",
                "feature_value": ["<=",0.5,">",0],
                "mean": 3,
                "std": 1,
                "low": 0,
                "high": 10},
                {"feature_name": "dummy_float_feature",
                "feature_value": ["<=",0],
                "mean": 1,
                "std": 1,
                "low": 0,
                "high": 10}
            ]
        }
```

10. "condition_conjunction" is a mandatory feild for conditioning on multiple variables, which can be: "linear","and","or". For example, we want to generate "weight" condtioned on "sex":
```
    "conditional":{
        "retention_rate":{
            "type": "float",
            "distribution": "Beta",
            "conditions":[
                {
                    "condition_conjunction": "linear",
                    "feature_names": ["duration","age>65","support_sessions"],
                    "feature_values": [-0.001,0.05,[0.05,"yes"]],
                    "bias":0.9
                }
            ]
        }
    },
    "white":{
            "type": "float",
            "distribution": "Beta",
        "conditions":[
                {
                    "condition_conjunction": "and",
                    "feature_names": ["use_technology","duration","follow_up_considered","support_sessions"],
                    "feature_values": ["yes",["<", 200],"yes","yes"],
                    "feature_names": ["duration","support_sessions"],
                    "feature_values": [["<", 200],"yes"],
                    "alpha": 9,
                    "beta": 1
                }
        ]
    }
```
