# hierarchical-path-leaf-extractor

A Python utility that turns hierarchical path rows into a clean table, keeping only the deepest (leaf) row of each branch. Built during my data analyst internship to clean product hierarchy data for reporting.

**Example:** from rows like

```
Cat1 | Function1
Cat1 | Function1 | Brand1
Cat1 | Function1 | Brand1 | Product1
Cat1 | Function1 | Brand1 | Product1 | SubCat1
```

it keeps only `Cat1 | Function1 | Brand1 | Product1 | SubCat1`, split into `Category`, `Function`, `Brand`, `Product` and `SubCategory` columns.

## Run it

```bash
pip install pandas openpyxl
python keep_leaf_rows.py                                  # uses the sample files in this repo
python keep_leaf_rows.py input.xlsx output.xlsx --sheet Sheet1
```

- **Input:** an Excel file with one `A | B | C` path per row in the first column, and no header row
- **Output:** the leaf rows only, with one column per level

The sample data (`hierarchical dataset.xlsx`) is anonymised. Its result is in `hierarchical_leaf_only.xlsx`.
