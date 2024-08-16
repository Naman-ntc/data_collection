import os
import dropbox
import requests

from live_code_bench.config import atcoder_contest_ids

ACCESS_TOKEN = "YOUR_DROPBOX_ACCESS_TOKEN"

LOCAL_DOWNLOAD_PATH = 'data/0.0.1/atcoder/tests'

SHARED_LINK = 'https://www.dropbox.com/sh/nx3tnilzqz7df8a/AAAYlTq2tiEHl5hsESw6-yfLa'

def download_folder(dbx, folder_path, shared_link_object, local_path, level=0):
    try:
        has_more = True
        cursor = None

        while has_more:
            if cursor is None:
                folder_metadata = dbx.files_list_folder(folder_path, shared_link=shared_link_object)
            else:
                folder_metadata = dbx.files_list_folder_continue(cursor)

            print(f"Listing folder: {folder_path}")
            # print(folder_metadata)
            for entry in folder_metadata.entries:
                if isinstance(entry, dropbox.files.FolderMetadata) and (level>0 or entry.name.lower() in atcoder_contest_ids):
                    print(f"Downloading folder: {folder_path+'/'+entry.name} {entry.path_lower}")
                    new_local_path = os.path.join(local_path, entry.name)
                    os.makedirs(new_local_path, exist_ok=True)
                    download_folder(dbx, folder_path+"/"+entry.name, shared_link_object, new_local_path, level+1)
                elif isinstance(entry, dropbox.files.FileMetadata):
                    local_file_path = os.path.join(local_path, entry.name)
                    print(f"Downloading file: {folder_path+'/'+entry.name}")
                    # print(dbx.sharing_get_shared_link_file(shared_link_object.url, path=folder_path+'/'+entry.name))
                    # dbx.files_download_to_file(local_file_path, folder_path+'/'+entry.name)
                    file_url = dbx.sharing_get_shared_link_file(shared_link_object.url, path=folder_path+'/'+entry.name)[0].url
                    download_url = file_url.replace('dl=0', 'dl=1')
                    r = requests.get(download_url, stream=True)
                    with open(local_file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                    

            has_more = folder_metadata.has_more
            cursor = folder_metadata.cursor

    except Exception as e:
        print(f"Error downloading folder: {str(e)}")

def download_shared_folder(dbx, shared_link, local_path):
    try:
        shared_link_object = dropbox.files.SharedLink(url=shared_link)
        # print(shared_link_object)
        download_folder(dbx, "", shared_link_object, local_path)

        # shared_folder_metadata = dbx.sharing_get_shared_link_metadata(shared_link)
        if isinstance(shared_folder_metadata, dropbox.sharing.SharedLinkMetadata):
            # shared_folder_path = shared_folder_metadata.path_lower or ''
            print(f"Shared folder path: {shared_link_object}")
            download_folder(dbx, shared_link_object, local_path)
        else:
            print("Shared link metadata is not a folder.")
    except Exception as e:
        print(f"Error downloading shared folder: {str(e)}")

def main():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    
    if not os.path.exists(LOCAL_DOWNLOAD_PATH):
        os.makedirs(LOCAL_DOWNLOAD_PATH)
    
    download_shared_folder(dbx, SHARED_LINK, LOCAL_DOWNLOAD_PATH)

if __name__ == "__main__":
    main()