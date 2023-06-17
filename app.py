import pandas as pd
import os
import fnmatch
import watchdog.events
import watchdog.observers
import time
import shutil
from turtle import textinput, numinput

os.chdir('C:/Users/Lenovo/Desktop/MGI7000')


### function that fills in the empty cells in the TubeID column.
### take df as a variable, assigned to it in hte last section of this script. 
### the purpose of this function is to disallow null inputs.
### if null is entered a recursive function is then called and loops over the empty cells again filling in the nulls.

def fillEmpty(df):
    for file in fnmatch.filter(os.listdir("."), 
            '?????????????? Output Position? ?????????.csv') :
        emptyCellsNum = df[df.columns[4]].count() - df[df.columns[9]].count()
        plateID = file.split(' ')
        plateID = plateID[3].split('.')
        for i in range(emptyCellsNum) :
            emptyBar =  df.iloc[:,9].isna()
            blank_row_index =  [i for i, x in enumerate(emptyBar) if x][0]
            barcode = textinput("Barcode", 
                                    "Please enter the barcode of " + df.iloc[blank_row_index, 4] +
                                        " from plate " + plateID[0] + " :")
            if barcode : 
                df.iloc[blank_row_index, 9] = barcode
                df.to_csv(file, index=False)
        

        if df[df.columns[9]].count() == df[df.columns[8]].count() and emptyCellsNum == 0 :
            
                ### move the file to elab and backup
                try :
                    shutil.copy(file, '../BackupWorklist/' + file)
                    shutil.move(file, '../X/' + file)
                except OSError as e:
                    print(f"{type(e)}: {e} ")
            
        else :
            fillEmpty(df) 


## Watchdog for checking if a file is updated or created in a set folder. 
class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.csv'],
                                                             ignore_directories=True, case_sensitive=False)
  
    def on_created(self, event):
 
        


        for file in fnmatch.filter(os.listdir("."), '*.csv'):
            # remove input files
            time.sleep(2)
            if fnmatch.fnmatch(file, '?????????????? Input.csv'):
                try :
                    os.replace(file, '../inputfiles/' + file)
                except OSError as e:
                    print(f"{type(e)}: {e}")

            if fnmatch.fnmatch(file, '?????????????? Output Position? 0.csv') or fnmatch.fnmatch(file, '?????????????? Output Position?? 0 .csv'): 
                

                try :
                    os.replace(file, '../outputnoworklist/' + file)
                except OSError as e:
                    print(f"{type(e)}: {e}")

            if fnmatch.fnmatch(file, '?????????????? Output Position?.csv') :

                df = pd.read_csv(file, dtype=str)
                
                if df[df.columns[0]].count() < 2 : 

                    time.sleep(2)

                    ### move the file to output no worklist folder
                    try :
                        os.replace(file, '../outputnoworklist/' + file)
                    except OSError as e:
                        print(f"{type(e)}: {e}")
                
                else :
                    for file in fnmatch.filter(os.listdir("."), '?????????????? Output Position?.csv') :
                        fileName = os.path.basename(file)
                        fileName = fileName.split('Position')
                        fileName = fileName[1].split('.')
                        worklistID = numinput("Worklist ID", "Please enter Worklist ID from Position " + fileName[0] + " :", minval = 0)
                        ### get rid of .0 of the float input
                        if worklistID % 1 == 0:
                            worklistID =  int(worklistID)
                        if len(str(worklistID)) == 9 or worklistID == 0 :
                            
                            newFileName = file.split('.')
                            newFileName = str(newFileName[0] + ' ' + worklistID + '.csv')
                            
                            ### change the filename to the new filename
                            try :
                                    os.replace(file, newFileName)
                            except OSError as e:
                                    print(f"{type(e)}: {e}")
                            
                            if worklistID == 0 : 
                                
                                ### move the file to worklist no number folder
                                try :
                                    os.replace(newFileName, '../outputnoworklist/' + newFileName)
                                except OSError as e:
                                    print(f"{type(e)}: {e}")

            time.sleep(2)
            if fnmatch.fnmatch(file, '?????????????? Output Position? .csv') :

                df = pd.read_csv(file, dtype=str)

                if df[df.columns[0]].count() < 2 : 

                    time.sleep(2)

                    ### move the file to output no worklist folder
                    try :
                        os.replace(file, '../outputnoworklist/' + file)
                    except OSError as e:
                        print(f"{type(e)}: {e}")
                
                else :
                    for file in fnmatch.filter(os.listdir("."), '?????????????? Output Position? .csv') :
                        fileName = os.path.basename(file)
                        fileName = fileName.split('Position')
                        fileName = fileName[1].split('.')
                        worklistID = numinput("Worklist ID", "Please enter Worklist ID from Position " + fileName[0] + " :", minval= 0)
                        ### get rid of .0 of the float input
                        if worklistID % 1 == 0:
                            worklistID =  int(worklistID)
                        if len(str(worklistID)) == 9 or worklistID == 0 :
                            newFileName = file.split('.')
                            newFileName = str(newFileName[0] + str(worklistID) + '.csv')
                            
                            ### change the filename to the new filename
                            try :
                                    os.replace(file, newFileName)
                            except OSError as e:
                                    print(f"{type(e)}: {e}")
                            
                            if worklistID == 0 : 
                                
                                ### move the file to worklist no number folder
                                try :
                                    os.replace(newFileName, '../outputnoworklist/' + newFileName)
                                except OSError as e:
                                    print(f"{type(e)}: {e}")

            time.sleep(2)
            for file in fnmatch.filter(os.listdir("."), 
                             '?????????????? Output Position? ?????????.csv') :
                
                df = pd.read_csv(file, dtype=str)

                if df[df.columns[4]].count() ==  df[df.columns[9]].count():
                    
                    ### move the file to elab and backup
                    try :
                        shutil.copy(file, '../BackupWorklist/' + file)
                        shutil.move(file, '../X/' + file)
                    except OSError as e:
                        print(f"{type(e)}: {e} ")
                else :
                    fillEmpty(df)
                    
                    






if __name__ == "__main__":
    src_path = "."
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(30)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
