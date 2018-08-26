clear all;

origin_path = '../Data/UNNCyberHeartDatabase';

fn = sprintf('%s/delineated_by_doc_ids.txt', origin_path);
records_ids = importdata(fn);
num_records = size(records_ids, 1);

num_points = 5000;

freq = 500.0;

leads = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};
num_leads = size(leads, 2);

total_num = 0;
qrs_num = 0;
t_num = 0;
p_num = 0;

for record_id = 1:num_records 
    
    record = records_ids(record_id)
    record_name = sprintf('record_%d', record);
    
    signals = zeros(num_points, num_leads);
    leads_names = {};
    
    for lead_id = 1:num_leads
        
        indexes = [];
        markers = {};
        
        lead = leads{lead_id};
        lead_name = lead(6:end);
        
        fn = sprintf('%s/%s/%s/qrs_delineation_doc.txt', origin_path, record_name, lead);
        data = importdata(fn);
        total_num = total_num + size(data, 1);
        qrs_num = qrs_num + size(data, 1);
        
        fn = sprintf('%s/%s/%s/t_delineation_doc.txt', origin_path, record_name, lead);
        data = importdata(fn); 
        total_num = total_num + size(data, 1);
        t_num = t_num + size(data, 1);
        
        fn = sprintf('%s/%s/%s/p_delineation_doc.txt', origin_path, record_name, lead);
        data = importdata(fn);
        total_num = total_num + size(data, 1);
        p_num = p_num + size(data, 1);
        
    end
end

