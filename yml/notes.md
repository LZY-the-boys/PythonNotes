dict

```
merge_config: 
  task_arithmetic:
    scaling: 1.0
  fisher:
    normalize_fisher_weight: true
    minimal_fisher_weight: 1e-6
    fisher_scaling_coefficients: 
    nums_fisher_examples:
  regmean:
    trainers:
    nums_regmean_examples: 
    reduce_non_diagonal_ratio: 1.0
  average_merging:
  ties_merging:
    param_value_mask_rate: 0.8
    scaling: 1.0
```


a list of dict

```
merge_config: 
  - task_arithmetic:
      scaling: 1.0
  - fisher:
      normalize_fisher_weight: true
      minimal_fisher_weight: 1e-6
      fisher_scaling_coefficients: 
      nums_fisher_examples:
  - regmean:
      trainers:
      nums_regmean_examples: 
      reduce_non_diagonal_ratio: 1.0
  - average_merging:
  - ties_merging:
      param_value_mask_rate: 0.8
      scaling: 1.0
```

