from pathlib import Path    
import shutil
import zipfile

# Define paths
SOURCE_DIR = Path("C:/Users/brian/Downloads") #Folder where ZIP files are downloaded
TARGET_DIR = Path("C:/Users/brian/WaveMind/NAMU/Amps/Guitar/Tone3000") #Folder where unzipped files will be installed
TEMP_DIR = Path ("C:/Users/brian/Documents/TEMPZipFiles") #Temporary area to unzip files to avoid collision



def extract_and_consolidate(source, target, temp):
    #ensure target and temporary directories exist
    target.mkdir(parents=True, exist_ok=True)
    temp.mkdir(parents=True, exist_ok=True)
    #Find and loop through all ZIP files in the download folder
    zip_files = list(source.glob("*.zip"))
    print(f"Found {len(zip_files)} ZIP archives to process.")
    for zip_path in zip_files:
            print(f"Processing: {zip_path.name}")
            try:
                # Extract zip contents to the temporary files
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(temp)
                    # Search for the temporary and move files to target files
                    for item in temp.rglob ("*"):
                        if item.is_file():
                             #Handle file name collisions
                             destination =  target / item.name
                             if destination.exists():
                                  #Add a suffix if the file already exists in target folder
                                  destination = target / f"{item.stem}_{zip_path.stem}{item.suffix}"

                                #Move the file to the final destination
                             shutil.move(str(item), str(destination))
                            #Clean up individual ZIP after successful migration
            except Exception as error:
                print(f"Error processing {zip_path.name}: {error}")
            #Clean out temporary folder structure before processing the next ZIP file
            finally:
                for item in temp.rglob("*"):
                    if item.is_file():
                        item.unlink()
                    else:
                        shutil.rmtree(item, ignore_errors=True)
        #Final Cleaup of temp directory after all ZIP files have been processed
    if temp.exists():
        shutil.rmtree(temp)

    print(f"Success! All files have been extracted and consolidated into {target}.")
extract_and_consolidate(SOURCE_DIR, TARGET_DIR, TEMP_DIR)