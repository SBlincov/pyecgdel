clear all;

origin_path = '../Data/UNNCyberHeartDatabase';
save_path = '../Data/unndb';

fn = sprintf('%s/delineated_by_doc_ids.txt', origin_path);
records_ids = importdata(fn);
num_records = size(records_ids, 1);

ages = zeros(num_records, 1);
genders = zeros(num_records, 1);

for record_id = 1:num_records 
    
    record = records_ids(record_id);
    record_name = sprintf('record_%d', record);
    
    fn = sprintf('%s/%s/age.txt', origin_path, record_name);
    age = importdata(fn);
    ages(record_id) = age;
    
    fn = sprintf('%s/%s/gender.txt', origin_path, record_name);
    gender = char(importdata(fn));
    if gender == 'F'
        genders(record_id) = 1;
    else
        genders(record_id) = 0;
    end
end

