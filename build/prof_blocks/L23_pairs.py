P = [
 ("You must write IS NULL.",
  "You must write IS NULL. NULLs also catch people in aggregates. COUNT star counts every row, but COUNT of a column skips the NULLs, and AVG ignores them too. So if three of ten employees have no bonus recorded, COUNT star is ten, COUNT bonus is seven, and the average bonus is over those seven only."),
]
