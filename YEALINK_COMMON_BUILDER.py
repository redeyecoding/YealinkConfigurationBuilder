# %T40P_FIRMWARE%
# VOC-DEFAULT-YEALINK-COMMON-TEMPLATE

## Grab The Common Files
common_file_config_path = '<COMMON-FILE-DIRECTORY>'
completed_common_files_path='<COMPLETED-COMMON-FILE-DIRECTORY>'

with open(f'{common_file_config_path}<NAME OF FILES CREATED>','r') as yealink_configs:
    yealink_common_template  = yealink_configs.readlines()



def common_config_builder(year=2022, common_path=completed_common_files_path):
    yealink_model_list = [
        'VOC-YEALINK-CP960', 'VOC-YEALINK-T21P',
        'VOC-YEALINK-T23G',  'VOC-YEALINK-T40G', 
        'VOC-YEALINK-T40P',  'VOC-YEALINK-T41P',  
        'VOC-YEALINK-T41S',  'VOC-YEALINK-T42G', 
        'VOC-YEALINK-T42S',  'VOC-YEALINK-T43U',  
        'VOC-YEALINK-T46G',  'VOC-YEALINK-CP920',
        'VOC-YEALINK-T46S',  'VOC-YEALINK-T48G', 
        'VOC-YEALINK-T48S',  'VOC-YEALINK-T48U',  
        'VOC-YEALINK-T54W',  'VOC-YEALINK-T57W', 
        'VOC-YEALINK-T58A',  'VOC-YEALINK-CP930', 
        'VOC-YEALINK-T46U',  'VOC-YEALINK-T53W',
        'VOC-YEALINK-W60P',  'VOC-YEALINK-T31G',
        'VOC-YEALINK-935W'
    ]

   
    for yealink_model_number in yealink_model_list:
        #Strip down the model-number
        model_number = yealink_common_template[1].replace(yealink_common_template[1], f'#{yealink_model_number}'.strip('VOC-')+'\n')
        base_model_number = model_number.replace('#VOC-YEALINK-', '').strip()

        #Set up naming convention for output file
        file_name_convention = model_number.replace('#VOC-', '').strip('\n')
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
