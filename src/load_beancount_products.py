import yaml
import pandas as pd

def load_beancount_products(yaml_path):
    """
    Load product data from a YAML file and expand the 'payback' dictionary into separate columns.

    Parameters:
    - yaml_path (str): Path to the YAML file containing product information.

    Returns:
    - pd.DataFrame: DataFrame with product details and expanded 'payback' fields.
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        price_data = yaml.safe_load(f)
    
    df_products = pd.DataFrame(price_data)

    # Expand the 'payback' dictionary into its own columns
    if 'payback' in df_products.columns:
        payback_df = df_products['payback'].apply(
            lambda x: x if isinstance(x, dict) else {}
        ).apply(pd.Series)
        payback_df.columns = [f'payback_{col}' for col in payback_df.columns]
        df_products = pd.concat([df_products.drop(columns=['payback']), payback_df], axis=1)
    
    # Rename 'currency' to 'item'
    df_products.rename(columns={'currency': 'item'}, inplace=True)
    return df_products