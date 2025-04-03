# S3 Bucket Size and Folder Details Script

## Overview
This Python script uses **boto3** to analyze and report the storage usage of AWS S3 buckets. It calculates the total size of each bucket, the number of folders, the size of each folder, and the number of files per folder. Additionally, it includes keyword-based filtering to analyze only specific buckets based on their names.

## Features
- Retrieves and calculates total storage size per bucket.
- Counts the number of folders and files within each bucket.
- Displays the storage usage of individual folders.
- Filters buckets based on predefined keywords.
- Saves results to a text file (**s3_sizes.txt**).

## Installation
Ensure you have **boto3** installed before running the script:
```sh
pip install boto3
```

## Usage
Run the script with:
```sh
python script.py
```

## Output Format
The script outputs details in the following structure:
```
Bucket: <bucket_name>
  Total bucket size: <size>
  Total folders: <count>
  Total files: <count>
  Folder sizes:
    <folder_name>: <size>
  Number of files in each folder:
    <folder_name>: <count> files
```

### Example Output:
```
Bucket: data-subha-123
  Total bucket size: 0.48 GB
  Total folders: 1
  Total files: 5
  Folder sizes:
    root: 0.48 GB
  Number of files in each folder:
    root: 5 files
```

## Filtering Buckets by Keywords
You can modify the `keywords` list in the script to include specific terms for filtering S3 buckets.
```python
keywords = ["data", "log"]  # Only buckets with 'data' or 'log' in their names will be processed
```

## Notes
- The script uses **AWS credentials** configured with `boto3`. Ensure you have valid credentials set up via:
  ```sh
  aws configure
  ```
- If a bucket has no files, it will still be listed with zero size.
- Modify the script to include additional filtering criteria as needed.

## Author
Developed by Subham Behera.

