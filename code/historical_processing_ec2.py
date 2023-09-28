"""
    Moving Big Data Predict:
    Data Processing script to execute - takes input data and combines and transforms
    to single output csv file.

"""

# Import packages
import pandas as pd

UBUNTU_HOME = "/home/ubuntu"
S3_BUCKET_HOME = f"{UBUNTU_HOME}/s3-drive"

AIRFLOW_HOME = "/opt/airflow"
AIRFLOW_BUCKET_HOME = f"{AIRFLOW_HOME}/s3-drive"

# # Airflow file directories
# source_path = f"{AIRFLOW_BUCKET_HOME}/Stocks/"
# save_path = f"{AIRFLOW_BUCKET_HOME}/utput/"
# index_file_path = f"{AIRFLOW_BUCKET_HOME}/CompanyNames/top_companies.txt"

# # Local file directories
# # These paths can be updated to meet your testing environment needs.
# source_path = "../../Stocks/"
# save_path = "../../Output/"
# index_file_path = '../data/top_companies.txt'

# # EC2 instance file directories
source_path = f"{S3_BUCKET_HOME}/Stocks/"
save_path = f"{S3_BUCKET_HOME}/Output/"
index_file_path = f"{S3_BUCKET_HOME}/CompanyNames/top_companies.txt"

# Helper function to extract companies to etl
def extract_companies_from_index(index_file_path):
    """Generate a list of company files that need to be processed.

    Args:
        index_file_path (str): path to index file

    Returns:
        list: Names of company names.
    """
    company_file = open(index_file_path, "r")
    contents = company_file.read()
    contents = contents.replace("'","")
    contents_list = contents.split(",")
    cleaned_contents_list = [item.strip() for item in contents_list]
    company_file.close()
    return cleaned_contents_list

# Helper function to extract companie raw file paths
def get_path_to_company_data(list_of_companies, source_data_path):
    """Creates a list of the paths to the company data
       that will be processed

    Args:
        list_of_companies (list): Extracted `.csv` file names of companies whose data needs to be processed.
        source_data_path (str): Path to where the company `.csv` files are stored.

    Returns:
        [type]: [description]
    """
    path_to_company_data = []
    for file_name in list_of_companies:
        path_to_company_data.append(source_data_path + file_name)
    return path_to_company_data

# Helper function to output etl data
def save_table(dataframe, output_path, file_name, header):
    """Saves an input pandas dataframe as a CSV file according to input parameters.

    Args:
        dataframe (pandas.dataframe): Input dataframe.
        output_path (str): Path to which the resulting `.csv` file should be saved.
        file_name (str): The name of the output `.csv` file.
        header (boolean): Whether to include column headings in the output file.
    """
    print(f"Path = {output_path}, file = {file_name}")
    dataframe.to_csv(output_path + file_name + ".csv", index=False, header=header)

# Main data processing function
def data_processing(file_paths, output_path):
    """Process and collate company csv file data for use within the data processing component of the formed data pipeline.

    Args:
        file_paths (list[str]): A list of paths to the company csv files that need to be processed.
        output_path (str): The path to save the resulting csv file to.
    """

    # Create a lookup dictionary mapping column names between
    # the input and output files.
    new_names = {
            'Date':'stock_date',
            'Open':'open_value',
            'High':'high_value',
            'Low':'low_value',
            'Close':'close_value',
            'Volume':'volume_traded'
        }

    df = pd.DataFrame()
    count = 0

    # Iterate through indexed csv files, extracting relevant data
    # and forming new columns through simple calculations.
    for file_path in file_paths:
        count += 1
        print(count)
        try:
            print(file_path)
            historical_data_df = pd.read_csv(file_path)
            historical_data_df['Date'] = pd.to_datetime(historical_data_df['Date'], format='%Y-%m-%d')
            historical_data_df['daily_percent_change'] \
                = ((historical_data_df['Close'] - historical_data_df['Open'])/historical_data_df['Open']*100)
            historical_data_df['value_change'] = historical_data_df['Close']-historical_data_df['Open']
            historical_data_df.drop('OpenInt', inplace=True, axis=1)
            company_name = file_path.split('/')[-1].split('.')[0]
            historical_data_df['company_name'] = company_name
            df = df.append(historical_data_df)
        except:
            print(f"This file {file_path} cannot be read")

    master_df = df.rename(columns=new_names, inplace=False)
    save_table(master_df, output_path, "historical_stock_data", False)

if __name__ == "__main__":

    # Get all file names in source data directory of companies whose data needs to be processed,
    # This information is specified within the `top_companies.txt` file.
    file_names = extract_companies_from_index(index_file_path)

    # Update the company file names to include path information.
    path_to_company_data = get_path_to_company_data(file_names, source_path)

    # Process company data and create full data output
    data_processing(path_to_company_data, save_path)
