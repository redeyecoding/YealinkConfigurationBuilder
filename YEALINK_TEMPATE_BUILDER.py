from io import BufferedWriter
import os
import yealink_common_builder

## Grab The Common Files
common_file_config_path = '<COMMON-FILE-DIRECTORY>'
completed_configs_directory = '<DIRECTORY TO HOUSE COMPLETED CONFIG-FILES>'

with open('VOC-DEFAULT-YEALINK-MAC-TEMPLATE.cfg','r') as yealink_configs:
    configs_list  = yealink_configs.readlines()


def mac_config_builder(line_number, buffer = '', new_line = '', variable_line = ''):
    #Create Accounts for mac
    for line in configs_list:
        # Replace BroadSoft Variable line
        if f'-2%' and 'account.line_number' in line:
            #Replace "account" with new number
            variable_line = line.replace(f'-2%',f'-{line_number}%')
            variable_line_2 = variable_line.replace(f'account.line_number',f'account.{line_number}')
            buffer = buffer + variable_line_2

        elif f'-2%' and 'voice_mail.number.line_number' in line: 
            #Replace "account" with new number
            variable_line = line.replace(f'-2%',f'-{line_number}%')
            variable_line_2 = variable_line.replace(f'voice_mail.number.line_number',f'voice_mail.number.{line_number}')
            buffer = buffer + variable_line_2

        elif f'-2%' in line:     
            #Replace "account" with new number
            variable_line = line.replace(f'-2%',f'-{line_number}%')
            buffer = buffer + variable_line 

        elif f'account.line_number' in line:
            #Replace "account" with new number
            new_line = line.replace(f'account.line_number',f'account.{line_number}')
            buffer = buffer + new_line

        else:            
            buffer = buffer + line

    line_number += 1
    return [line_number, buffer]



def looper(line_supported, yealink_line_number = 1, buffer=''):    
    if yealink_line_number > line_supported:
        # All Accounts were added
        return [True, buffer]

    yealink_results = mac_config_builder(yealink_line_number, buffer)
    buffer = yealink_results[1]
    yealink_line_number = yealink_results[0] 

    return looper(line_supported, yealink_line_number, buffer)


def build_yealink_config():
    #YEALINK SUPPORTED NUMBER OF LINES
    YEALINK_2 = 2
    YEALINK_3 = 3
    YEALINK_6 = 6
    YEALINK_12 = 12
    YEALINK_16 = 16


    suported_yealink_lines = {
        
        'VOC-YEALINK-CP960': YEALINK_2, 'VOC-YEALINK-T21P': YEALINK_2,
        'VOC-YEALINK-T23G': YEALINK_3, 'VOC-YEALINK-T40G': YEALINK_3, 
        'VOC-YEALINK-T40P': YEALINK_3, 'VOC-YEALINK-T41P': YEALINK_6 , 
        'VOC-YEALINK-T41S': YEALINK_6, 'VOC-YEALINK-T42G': YEALINK_12,
        'VOC-YEALINK-T42S': YEALINK_12, 'VOC-YEALINK-T43U': YEALINK_12, 
        'VOC-YEALINK-T46G': YEALINK_16, 'VOC-YEALINK-CP920': YEALINK_2,         
        'VOC-YEALINK-T46S': YEALINK_16, 'VOC-YEALINK-T48G': YEALINK_16,
        'VOC-YEALINK-T48S': YEALINK_16, 'VOC-YEALINK-T48U': YEALINK_16, 
        'VOC-YEALINK-T54W': YEALINK_16, 'VOC-YEALINK-T57W': YEALINK_16,
        'VOC-YEALINK-T58A': YEALINK_16, 'VOC-YEALINK-CP930': YEALINK_2, 
        'VOC-YEALINK-T46U': YEALINK_16, 'VOC-YEALINK-T53W': YEALINK_12,
        'VOC-YEALINK-W60P': YEALINK_6

    }
 


    # Get list of yealink configs
    list_of_yealink_configs = os.listdir(common_file_config_path)

    #Find model number in config
    for common_conf_file in list_of_yealink_configs:

        # Open the yealink COMMON config for reading
        with open(common_file_config_path + common_conf_file,'r') as yealink_configs:
            yealink_common_file  = yealink_configs.readlines()
            
        for line in yealink_common_file:
            if 'VOC-YEALINK-' in line:
                stripped_model_number = line.strip()
                model_number = stripped_model_number.replace('#','')
                additional_yealink_accounts = looper(suported_yealink_lines[model_number])

               # new_yealink_file = common_conf_file.replace('.cfg','TEST.cfg')
                with open(completed_configs_directory + model_number+'-TEMPLATE-'+'2021','a') as new_yealink_config_file:
                    for line in yealink_common_file:
                        new_yealink_config_file.write(line)
                    new_yealink_config_file.write(additional_yealink_accounts[1])
                continue 
    return


build_yealink_config()
