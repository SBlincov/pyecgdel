data_path = '../Data/';

database_name = 'shiller/';
new_database_name = 'shiller_long/';

record_name = 'record_2319/';
record_name_long = record_name;

concat_number = 30;

lead_names = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};

new_database_path = strcat(data_path, new_database_name);
if ~exist(new_database_path, 'dir')
    mkdir(new_database_path);
    copyfile(strcat(data_path, database_name, 'properties.txt'), new_database_path);
    copyfile(strcat(data_path, database_name, 'filter_params.txt'), new_database_path);
    copyfile(strcat(data_path, database_name, 'flutter_params.txt'), new_database_path);
    copyfile(strcat(data_path, database_name, 'qrs_params.txt'), new_database_path);
    copyfile(strcat(data_path, database_name, 'p_params.txt'), new_database_path);
    copyfile(strcat(data_path, database_name, 't_params.txt'), new_database_path);
end

for lead_id = 1:length(lead_names)
    
    lead_name = lead_names{lead_id};
    signal_path = strcat(data_path, database_name, record_name, lead_name, '/original.txt');
    signal = importdata(signal_path);
    signal_long = repmat(signal, concat_number, 1);
    
        new_record_path = strcat(data_path, new_database_name, record_name_long);
    if ~exist(new_record_path, 'dir')
        mkdir(new_record_path);
    end
    
    new_lead_path = strcat(new_record_path, lead_name);
    if ~exist(new_lead_path, 'dir')
        mkdir(new_lead_path);
    end
    signal_path_long = strcat(data_path, new_database_name, record_name_long, lead_name, '/original.txt');
    dlmwrite(signal_path_long, signal_long);
end
