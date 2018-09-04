clear all;

fid = fopen('diagnosis.txt');
tline = fgetl(fid);
rec = horzcat('record_', tline);
fw_name = sprintf('%s/diagnosis.txt', rec);
fw = fopen(fw_name, 'w');

while ischar(tline)
    tline = fgetl(fid);
    disp(tline)
    
    if isempty(tline)
        tline = fgetl(fid);
        rec = horzcat('record_', tline);
        fclose(fw);
        fw_name = sprintf('%s/diagnosis.txt', rec);
        fw = fopen(fw_name, 'w');
    else
       tline = regexprep(tline,'\s+',' '); 
       fprintf(fw, '%s\n', tline(2:end)); 
    end
    
end
fclose(fid);