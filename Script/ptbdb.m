clear all;

figure;
subplot(2,1,2);

base_name = 'ptbdb';
freq = 1000.0;
patient_id = 49;
record_id = 1;
lead = 'lead_i';
scale = 1;
markerWidth = 10;

files = dir(sprintf('../Data/%s', base_name));
dir_flags = [files.isdir];
sub_folders = files(dir_flags);
num_folders = 0;
for i = 1:size(sub_folders)
    tmp = strfind(sub_folders(i).name, 'patient');
    if tmp
        num_folders = num_folders + 1;
        patient_folders(num_folders) = sub_folders(i);
    end
end

files = dir(sprintf('../Data/%s/%s', base_name, patient_folders(patient_id).name));
dir_flags = [files.isdir];
sub_folders = files(dir_flags);
num_folders = 0;
for i = 1:size(sub_folders)
    tmp = strfind(sub_folders(i).name, 'record');
    if tmp
        num_folders = num_folders + 1;
        records_folders(num_folders) = sub_folders(i);
    end
end

patient_folders(patient_id).name
records_folders(record_id).name

file_name_ecg = sprintf('../Data/%s/%s/%s/%s/filtrated.txt', base_name, patient_folders(patient_id).name, records_folders(record_id).name, lead);
%file_name_ecg = sprintf('../Data/%s/%s/%s/%s/original.txt', base_name, patient_folders(patient_id).name, records_folders(record_id).name, lead);
ecg_lead = importdata(file_name_ecg);

max_ecg = max(ecg_lead(4000:7000));
min_ecg = min(ecg_lead(4000:7000));

limit = 1.0 / (max_ecg - min_ecg);



for i = 1:size(ecg_lead)
    % times(i) = (i - 1);
    times(i) = (i - 1) / freq; 
end

ecg_lead = ecg_lead * limit;

hLine = plot(times, ecg_lead,'k', 'LineWidth', 1);
legend(hLine, sprintf('ECG', 1));
set(gca, 'FontSize', 18);
grid on;
hold all;


file_name_ecg = sprintf('../Data/%s/%s/%s/%s/wdc.txt', base_name, patient_folders(patient_id).name, records_folders(record_id).name, lead);
dataArray = importdata(file_name_ecg);
ecg = dataArray;
clearvars filename delimiter formatSpec fileID dataArray ans;

wdc_1 = ecg(:, 1);

max_wdc = max(wdc_1(4000:7000));
min_wdc = min(wdc_1(4000:7000));

limit = 0.4 / (max_wdc - min_wdc);

wdc_1 = wdc_1 * limit;

% hLine = plot(times(1:size(wdc_1)), wdc_1, 'LineWidth', 1.0);
% legend(hLine, sprintf('wdc scale %d', scale));
% set(gca, 'FontSize', 18);
% xlabel('time, sec')
% grid on;
% hold all;

wdc_2 = ecg(:, 2);

max_wdc = max(wdc_2(4000:7000));
min_wdc = min(wdc_2(4000:7000));

limit = 0.7 / (max_wdc - min_wdc);

wdc_2 = wdc_2 * limit;

zero_num = 1;
ololo = zeros(zero_num,1);
wdc_shifted = vertcat(ololo, wdc_2(1 : size(wdc_2) - zero_num));
% 
% hLine = plot(times(1:size(wdc_2)), wdc_shifted, 'LineWidth', 1.0);
% legend(hLine, sprintf('wdc scale %d', scale));
% set(gca, 'FontSize', 18);
% xlabel('time, sec')
% grid on;
% hold all;

waveFileName = sprintf('../Data/%s/%s/%s/%s/qrs_delineation.txt', base_name, patient_folders(patient_id).name, records_folders(record_id).name, lead);

formatSpec = '%24f%f%f%[^\n\r]';
fileID = fopen(waveFileName,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', '', 'WhiteSpace', '', 'EmptyValue' ,NaN, 'ReturnOnError', false);
fclose(fileID);
onset = dataArray{:, 1};
peak = dataArray{:, 2};
offset = dataArray{:, 3};
clearvars formatSpec fileID dataArray ans;


for i = 1:size(onset)
    times_onset(i) = times((onset(i) + 1));
    vals_onset(i) = ecg_lead(onset(i) + 1);
end

for i = 1:size(peak)
    times_peak(i) = times((peak(i) + 1));
    vals_peak(i) = ecg_lead(peak(i) + 1);
end

for i = 1:size(offset)
    times_offset(i) = times((offset(i) + 1));
    vals_offset(i) = ecg_lead(offset(i) + 1);
end

hLine = plot(times_onset, vals_onset,  '>', 'MarkerSize', markerWidth, 'Color', 'r', 'MarkerFaceColor', 'r');
legend(hLine, sprintf('onset qrs'));
set(gca, 'FontSize', 18);
hold all;
hLine = plot(times_peak, vals_peak,  'o', 'MarkerSize', markerWidth, 'Color', 'r', 'MarkerFaceColor', 'r');
legend(hLine, sprintf('peak qrs'));
set(gca, 'FontSize', 18);
hold all;
hLine = plot(times_offset, vals_offset, '<', 'MarkerSize', markerWidth, 'Color', 'r', 'MarkerFaceColor', 'r');
legend(hLine, sprintf('offset qrs'));
set(gca, 'FontSize', 18);
grid on;
hold all;

clearvars times_onset vals_onset times_peak vals_peak times_offset vals_offset


waveFileName = sprintf('../Data/%s/%s/%s/%s/p_delineation.txt', base_name, patient_folders(patient_id).name, records_folders(record_id).name, lead);


formatSpec = '%24f%f%f%f%f%[^\n\r]';
fileID = fopen(waveFileName,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', '', 'WhiteSpace', '', 'EmptyValue' ,NaN, 'ReturnOnError', false);
fclose(fileID);
onset = dataArray{:, 1};
peak = dataArray{:, 2};
offset = dataArray{:, 3};
clearvars formatSpec fileID dataArray ans;


for i = 1:size(onset)
    times_onset(i) = times((onset(i) + 1));
    vals_onset(i) = ecg_lead(onset(i) + 1);
end

for i = 1:size(peak)
    times_peak(i) = times((peak(i) + 1));
    vals_peak(i) = ecg_lead(peak(i) + 1);
end

for i = 1:size(offset)
    times_offset(i) = times((offset(i) + 1));
    vals_offset(i) = ecg_lead(offset(i) + 1);
end

hLine = plot(times_onset, vals_onset,  '>', 'MarkerSize', markerWidth, 'Color', [0 0.5 0], 'MarkerFaceColor',  [0 0.5 0]);
legend(hLine, sprintf('onset p'));
set(gca, 'FontSize', 18);
hold all;
hLine = plot(times_peak, vals_peak,  'o', 'MarkerSize', markerWidth, 'Color', [0 0.5 0], 'MarkerFaceColor',  [0 0.5 0]);
legend(hLine, sprintf('peak p'));
set(gca, 'FontSize', 18);
hold all;
hLine = plot(times_offset, vals_offset, '<', 'MarkerSize', markerWidth, 'Color', [0 0.5 0], 'MarkerFaceColor',  [0 0.5 0]);
legend(hLine, sprintf('offset p'));
set(gca, 'FontSize', 18);
grid on;
hold all;

clearvars times_onset vals_onset times_peak vals_peak times_offset vals_offset



waveFileName = sprintf('../Data/%s/%s/%s/%s/t_delineation.txt', base_name, patient_folders(patient_id).name, records_folders(record_id).name, lead);


formatSpec = '%24f%f%f%f%f%[^\n\r]';
fileID = fopen(waveFileName,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', '', 'WhiteSpace', '', 'EmptyValue' ,NaN, 'ReturnOnError', false);
fclose(fileID);
onset = dataArray{:, 1};
peak = dataArray{:, 2};
offset = dataArray{:, 3};
clearvars formatSpec fileID dataArray ans;


for i = 1:size(onset)
    times_onset(i) = times((onset(i) + 1));
    vals_onset(i) = ecg_lead(onset(i) + 1);
end

for i = 1:size(peak)
    times_peak(i) = times((peak(i) + 1));
    vals_peak(i) = ecg_lead(peak(i) + 1);
end

for i = 1:size(offset)
    times_offset(i) = times((offset(i) + 1));
    vals_offset(i) = ecg_lead(offset(i) + 1);
end

hLine = plot(times_onset, vals_onset,  '>', 'MarkerSize', markerWidth, 'Color', [0 0.45 0.74], 'MarkerFaceColor',  [0 0.45 0.74]);
legend(hLine, sprintf('onset t'));
set(gca, 'FontSize', 18);
hold all;
hLine = plot(times_peak, vals_peak,  'o', 'MarkerSize', markerWidth, 'Color', [0 0.45 0.74], 'MarkerFaceColor',  [0 0.45 0.74]);
legend(hLine, sprintf('peak t'));
set(gca, 'FontSize', 18);
hold all;
hLine = plot(times_offset, vals_offset, '<', 'MarkerSize', markerWidth, 'Color', [0 0.45 0.74], 'MarkerFaceColor',  [0 0.45 0.74]);
legend(hLine, sprintf('offset t'));
set(gca, 'FontSize', 18);
xlabel('time, sec', 'Interpreter', 'latex');
set(gca, 'FontSize', 18);

set(gca, 'FontSize', 18);
ylabel('Lead I', 'Interpreter', 'latex');

grid on;
hold all;

clearvars times_onset vals_onset times_peak vals_peak times_offset vals_offset





legend off;
