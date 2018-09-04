clear all;

origin_path = '../Data/UNNCyberHeartDatabase';
save_path = '../Data/unndb';

fn = sprintf('%s/delineated_by_doc_ids.txt', origin_path);
records_ids = importdata(fn);
num_records = size(records_ids, 1);

num_points = 5000;

freq = 500.0;

leads = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};
num_leads = size(leads, 2);

for record_id = 1:num_records 
    
    record = records_ids(record_id)
    record_name = sprintf('record_%d', record);
    
    ss = zeros(num_points, num_leads);
    leads_names = {};
    
    for lead_id = 1:num_leads

        lead = leads{lead_id};
        lead_name = lead(6:end);
        
        fn = sprintf('%s/%s/%s/original.txt', origin_path, record_name, lead);
        data = importdata(fn);
        
        ss(:, lead_id) = data;
        leads_names{lead_id} = lead_name;
    end
    
    name = int2str(record_id);
    physical_units = 'mV';
    
    fn = sprintf('%s/%s/age.txt', origin_path, record_name);
    age = importdata(fn);
    
    fn = sprintf('%s/%s/gender.txt', origin_path, record_name);
    gender = char(importdata(fn));
    
    header_comment = {sprintf('<age>: %d', age),  sprintf('<sex>: %s', gender),  '<diagnoses>:'}';
    
    fn = sprintf('%s/%s/diagnosis.txt', origin_path, record_name);
    fid = fopen(fn);
    tline = fgetl(fid);
    while ischar(tline)
        tline = fgetl(fid);
        if tline ~= -1
            header_comment = vertcat(header_comment, tline);
        end
    end
    fclose(fid);
    
    mat2wfdb(ss, name, freq, [], physical_units, header_comment, [], leads_names);
    
end

