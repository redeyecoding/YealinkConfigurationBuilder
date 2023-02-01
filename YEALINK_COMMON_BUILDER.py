import glob
import os

## Grab The Common Files
common_file_config_path = '<COMMON-FILE-DIRECTORY>'
completed_common_files_path='<COMPLETED-COMMON-FILE-DIRECTORY>'

with open(f'{common_file_config_path}<NAME OF FILES CREATED>','r') as yealink_configs:
    yealink_common_template  = yealink_configs.readlines()



def common_config_builder(year=2022, common_path=completed_common_files_path):
    yealink_model_list = [
        'COMPANY-NAME-YEALINK-CP960', 'COMPANY-NAME-YEALINK-T21P',
        'COMPANY-NAME-YEALINK-T23G',  'COMPANY-NAME-YEALINK-T40G', 
        'COMPANY-NAME-YEALINK-T40P',  'COMPANY-NAME-YEALINK-T41P',  
        'COMPANY-NAME-YEALINK-T41S',  'COMPANY-NAME-YEALINK-T42G', 
        'COMPANY-NAME-YEALINK-T42S',  'COMPANY-NAME-YEALINK-T43U',  
        'COMPANY-NAME-YEALINK-T46G',  'COMPANY-NAME-YEALINK-CP920',
        'COMPANY-NAME-YEALINK-T46S',  'COMPANY-NAME-YEALINK-T48G', 
        'COMPANY-NAME-YEALINK-T48S',  'COMPANY-NAME-YEALINK-T48U',  
        'COMPANY-NAME-YEALINK-T54W',  'COMPANY-NAME-YEALINK-T57W', 
        'COMPANY-NAME-YEALINK-T58A',  'COMPANY-NAME-YEALINK-CP930', 
        'COMPANY-NAME-YEALINK-T46U',  'COMPANY-NAME-YEALINK-T53W',
        'COMPANY-NAME-YEALINK-W60P',  'COMPANY-NAME-YEALINK-T31G',
        'COMPANY-NAME-YEALINK-935W'
    ]

   
    for yealink_model_number in yealink_model_list:
        #Strip down the model-number
        model_number = yealink_common_template[1].replace(yealink_common_template[1], f'#{yealink_model_number}'.strip('COMPANY-NAME-')+'\n')
        base_model_number = model_number.replace('#COMPANY-NAME-YEALINK-', '').strip()

        #Set up naming convention for output file
        file_name_convention = model_number.replace('#COMPANY-NAME-', '').strip('\n')
        current_firmware_url = yealink_common_template[310]

        #Setup Firmware URL
        new_firmware_url = yealink_common_template[310].replace(f'{current_firmware_url}',f'static.firmware.url = tftp://%PROV_SERVER%/Yealink/%{base_model_number}_FIRMWARE%')
        
        #Update config with new values
        yealink_common_template[1] = model_number
        yealink_common_template[310] = new_firmware_url
        
        #Create Common.cfg template for model
        with open(f'{common_path}{file_name_convention}-COMMON-TEMPLATE-{year}.cfg','a') as yealink_config_file:
            for line in yealink_common_template:
                yealink_config_file.write(line)
    return {
        'common_file_path': common_path
    }
#Delete existing files in directory ; if any
def delete_existing_files(file_path):
    files = glob.glob(f'{file_path}/*.cfg', recursive=True)

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))    
    return 

delete_existing_files(completed_common_files_path)
common_config_builder()
