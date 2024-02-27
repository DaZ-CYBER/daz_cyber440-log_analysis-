import os
import re

def parse_xml(XMLfile, WRITEFILE):
    # Opening file
    content = open(XMLfile, "r")
    # Initializing line inclusion
    print_next_lines = False; count = 0
    lines_to_print=5 #change this and line15 to alter amount of lines written to file
    
    with open(WRITEFILE, 'w') as write_file:
        for line in content:
            if "<EventID>4624" in line:
                print(line, file=write_file, end='')  # Print the line containing the EventID
                print_next_lines = True
                lines_to_print = 5  # Reset lines_to_print for each occurrence of the condition
            elif print_next_lines and lines_to_print > 0:
                print(line, file=write_file, end='')  # Print the next 5 lines
                lines_to_print -= 1
            elif print_next_lines and lines_to_print == 0:
                print_next_lines == False; lines_to_print=5; count+=1
        write_file.close()
        print(f"{count} instances of Event ID")
    return count

# Open write_file in notepad instead of manually printing to screen
def open_file(file_path):
    command = f'start "" "{file_path}"'
    os.system(command)

def time_calc(edited_event_xml, write_to_grep):

    read_file = open(edited_event_xml, "r")
    with open(write_to_grep, "w") as file_c:
        for line in read_file:
            if "2011-04-15T" in line or "2011-04-16T" in line:
                print(line, file=file_c, end='')
    
    file_c.close()

    new_read = open(write_to_grep, "r")
    os.system('powershell "New-Item -ItemType File -Path C:/Users/f3arz/OneDrive/Documents/SP2024/CYBER440/loganalysis/grepped.txt"')
    file_grep = "C:/Users/f3arz/OneDrive/Documents/SP2024/CYBER440/loganalysis/grepped.txt"
    list_initialize=[]
    with open(file_grep, "w") as file:
        for line in new_read:
            # regex to match pattern of 2011-04-XX
            pattern_to_look = r'\d{4}-\d{2}-\d{2}T.*'
            match = re.search(pattern_to_look, line)
            if(match):
                string = match.group(0)
                parsed_string = string[:13]
                list_initialize.append(parsed_string)
        
    sorted_set = sorted(set(list_initialize), key=lambda x: int(x[-2:]), reverse=True)
                    
    with open(edited_event_xml, "r") as file:
        returned_set = set()
        print("Event instances for Event ID - 4624")
        for i in sorted_set:
            count=0
            file.seek(0)
            for line in file:
                if str(i) in line:
                    count+=1
            volume_string = f"{i} - {count} event instances"
            returned_set.add(volume_string)

    # spawn lambda function to split the 
    sorted_returned = sorted(returned_set, key=lambda x: x.split("T")[1])
    
    for i in sorted_returned:
        print(i)
        

    open_file(write_to_grep)

# variable initialization
PATH = "C:/Users/f3arz/OneDrive/Documents/SP2024/CYBER440/loganalysis/" #CHANGEME TO DESIRED PATH
XML_File = PATH + "SecurityLog-rev2.xml"
WRITE_File = PATH + "write_file.txt"
if os.path.exists(WRITE_File): # if file exists, remove it and create new file
    os.remove(WRITE_File)
    with open(os.path.join(PATH, WRITE_File), 'w') as fp:
        pass
    WRITE_File = PATH + "write_file.txt" # update write_file to new path
parse_xml(XML_File, WRITE_File)
open_file(WRITE_File)

os.remove(PATH + "file_to_grep.txt")
os.system('powershell "New-Item -ItemType File -Path C:/Users/f3arz/OneDrive/Documents/SP2024/CYBER440/loganalysis/file_to_grep.txt"')
file_to_grep = PATH + "file_to_grep.txt"
time_calc(WRITE_File, file_to_grep)

os.remove(PATH + "grepped.txt")
#file_content = open(WRITE_File, "r")
#for line in file_content:
    #print(line)

