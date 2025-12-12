import pandas as pd

def keep_leaf_rows(
    df: pd.DataFrame,
    level_cols: list[str],
    min_levels: int = 4,
) -> pd.DataFrame:
    """
    Given a DataFrame with hierarchical columns in `level_cols`,
    keep only the deepest row (leaf) for each branch.

    - Assumes rows are already ordered from top to bottom in tree order.
    - Only keeps leaf rows whose path length >= min_levels.
    """

    leaf_indices: list[int] = []

    prev_path = None
    prev_idx = None
    prev_len = 0

    for idx, row in df[level_cols].iterrows():
        # extract levels from the row
        values = [row[col] for col in level_cols]

        # clean: drop NaN / empty, strip spaces
        cleaned = [
            str(v).strip()
            for v in values
            if pd.notna(v) and str(v).strip() != ""
        ]

        curr_path = tuple(cleaned)

        if not curr_path:
            # no hierarchy info in this row
            continue

        curr_len = len(curr_path)

        if prev_path is None:
            # first valid row
            prev_path = curr_path
            prev_idx = idx
            prev_len = curr_len
            continue

        # is current path a deeper extension of previous branch?
        is_extension = (
            len(prev_path) <= curr_len
            and prev_path == curr_path[:len(prev_path)]
        )

        if is_extension:
            # still in same branch, but deeper -> update leaf candidate
            prev_path = curr_path
            prev_idx = idx
            prev_len = curr_len
        else:
            # branch changed -> previous row was the leaf for its branch
            # only keep it if it has at least min_levels
            if prev_len >= min_levels:
                leaf_indices.append(prev_idx)

            # start tracking new branch (even if curr_len < min_levels)
            prev_path = curr_path
            prev_idx = idx
            prev_len = curr_len

    # after loop, add the last branch's leaf (if deep enough)
    if prev_idx is not None and prev_len >= min_levels:
        leaf_indices.append(prev_idx)

    leaf_df = df.loc[leaf_indices].reset_index(drop=True)
    return leaf_df

def build_leaf_from_products(
    df: pd.DataFrame,
    level_names: list[str],
) -> pd.DataFrame:
    """
    1) Read file with a 'Products' tree column
    2) Split into hierarchy columns in `level_names`
    3) Keep only leaf rows
    4) Save to `out_path`
    """

    products_col = df.columns[0]

    # --- split Products into levels ---
    split = df[products_col].astype(str).str.split("|", expand=True)
    split = split.apply(lambda col: col.str.strip())  # clean spaces

    # in case there are fewer levels than names, only use what exists
    n_cols = split.shape[1]
    use_levels = level_names[:n_cols]

    split.columns = use_levels
    df[use_levels] = split

    # --- keep leaf rows based on the levels we actually have ---
    leaf_df = keep_leaf_rows(df, use_levels)

    # --- save & return ---
    return leaf_df

file = r"C:\Users\Chris Teo\OneDrive\Documents\Internship\hierarchical dataset.xlsx"
df = pd.read_excel(file, header = 0, sheet_name='Sheet1')

print(df.head())  # show original data

level_names = [
    "Category",
    "Function",
    "Brand",
    "Product",
    "SubCategory",
]

leaf_df = build_leaf_from_products(df, level_names)

print(leaf_df.head())   # show the filtered leaf rows
leaf_df.to_excel(r"C:\Users\Chris Teo\OneDrive\Documents\Internship\hierarchical_leaf_only.xlsx", index=False)
