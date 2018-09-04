clear all;

fid = fopen('info.txt');
tline = fgetl(fid);
all_lines = {tline};
while ischar(tline)
    tline = fgetl(fid);
    all_lines = vertcat(all_lines, tline);
end
fclose(fid);

fn = sprintf('delineated_by_doc_ids.txt');
records_ids = importdata(fn);
num_records = size(records_ids, 1);

for record_id = 1:num_records
    
    record = records_ids(record_id);
    record_name = sprintf('record_%d', record);
    
    age_id = 2 + (record_id-1) * 5;
    gender_id = 3 + (record_id-1) * 5;
    
    age_raw = char(all_lines(age_id));
    age = age_raw(14:end-1);
    fn = sprintf('%s/age.txt', record_name);
    file_id = fopen(fn, 'w');
    fprintf(file_id, '%s', age);
    fclose(file_id);
    
    gender_raw = char(all_lines(gender_id));
     gender = gender_raw(17:end-1);
    fn = sprintf('%s/gender.txt', record_name);
    file_id = fopen(fn, 'w');
    fprintf(file_id, '%s', gender);
    fclose(file_id);
end