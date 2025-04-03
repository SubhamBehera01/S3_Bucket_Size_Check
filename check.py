import boto3

def format_size(size):
    """
    Convert size to GB, MB, or KB for better readability.
    """
    if size >= 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} GB"
    elif size >= 1024 ** 2:
        return f"{size / (1024 ** 2):.2f} MB"
    else:
        return f"{size / 1024:.2f} KB"

def get_s3_bucket_details(bucket_name):
    """
    Get the total size and file count of an S3 bucket, its folders, total folder count, and the number of files in each folder.
    """
    s3 = boto3.client("s3")
    total_size = 0
    file_count = 0
    folder_sizes = {}
    folder_file_counts = {}
    folders = set()
    
    paginator = s3.get_paginator("list_objects_v2")
    operation_parameters = {"Bucket": bucket_name}
    
    for page in paginator.paginate(**operation_parameters):
        if "Contents" in page:
            for obj in page["Contents"]:
                folder = obj["Key"].split("/")[0] if "/" in obj["Key"] else "root"
                
                total_size += obj["Size"]
                file_count += 1
                folder_sizes[folder] = folder_sizes.get(folder, 0) + obj["Size"]
                folder_file_counts[folder] = folder_file_counts.get(folder, 0) + 1
                folders.add(folder)
    
    return total_size, file_count, folder_sizes, folder_file_counts, len(folders)

def save_to_file(bucket_details):
    """
    Save the bucket details to a file.
    """
    with open("s3_sizes.txt", "w") as file:
        for bucket, details in bucket_details.items():
            file.write(f"Bucket: {bucket}\n")
            file.write(f"  Total bucket size: {format_size(details['total_size'])}\n")
            file.write(f"  Total folders: {details['total_folders']}\n")
            file.write(f"  Total files: {details['file_count']}\n")
            file.write("  Folder sizes:\n")
            for folder, size in details['folder_sizes'].items():
                file.write(f"    {folder}: {format_size(size)}\n")
            file.write("  Number of files in each folder:\n")
            for folder, count in details['folder_file_counts'].items():
                file.write(f"    {folder}: {count} files\n")
            file.write("\n")

if __name__ == "__main__":
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    bucket_details = {}
    
    keywords = ["my"]  # Change this to filter bucket names by multiple keywords // # An empty list will disable filtering and include all buckets
    
    for bucket in response.get("Buckets", []):
        bucket_name = bucket["Name"]
        
        # Apply filtering only to bucket names
        if keywords and not any(keyword in bucket_name for keyword in keywords):
            continue
        
        total_size, file_count, folder_sizes, folder_file_counts, total_folders = get_s3_bucket_details(bucket_name)
        bucket_details[bucket_name] = {
            "total_size": total_size,
            "file_count": file_count,
            "folder_sizes": folder_sizes,
            "folder_file_counts": folder_file_counts,
            "total_folders": total_folders
        }
        
        print(f"Bucket: {bucket_name}")
        print(f"  Total bucket size: {format_size(total_size)}")
        print(f"  Total folders: {total_folders}")
        print(f"  Total files: {file_count}")
        print("  Folder sizes:")
        for folder, size in folder_sizes.items():
            print(f"    {folder}: {format_size(size)}")
        print("  Number of files in each folder:")
        for folder, count in folder_file_counts.items():
            print(f"    {folder}: {count} files")
        print()
    
    save_to_file(bucket_details)


