clear all;

freq = 250.0;
window_limit = 15;

base_name = 'qtdb';
db_path = sprintf('../Data/%s/', base_name);

for record = 1:20
    record_path = sprintf('record_%d/', record);
    
    leads = {'lead_ii', 'lead_v5'};
    
    for lead_id = 1:2
        
        lead = leads{lead_id};
        lead_path = sprintf('%s/', lead);
        
        file_name_qrs_del = sprintf('%s%s%sqrs_delineation.txt', db_path, record_path, lead_path);
        qrs_del_data = importdata(file_name_qrs_del);
        qrs_del_candidate = horzcat(qrs_del_data(:,1), qrs_del_data(:,3));
        
        file_name_qrs_del = sprintf('%s%s%sqrs_original_delineation.txt', db_path, record_path, lead_path);
        delimiter = '\t';
        formatSpec = '%s%s%s%s%[^\n\r]';
        fileID = fopen(file_name_qrs_del,'r');
        dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter,  'ReturnOnError', false);
        fclose(fileID);
        raw = repmat({''},length(dataArray{1}),length(dataArray)-1);
        for col=1:length(dataArray)-1
            raw(1:length(dataArray{col}),col) = dataArray{col};
        end
        numericData = NaN(size(dataArray{1},1),size(dataArray,2));
        for col=[1,2,3]
            % Converts text in the input cell array to numbers. Replaced non-numeric
            % text with NaN.
            rawData = dataArray{col};
            for row=1:size(rawData, 1);
                % Create a regular expression to detect and remove non-numeric prefixes and
                % suffixes.
                regexstr = '(?<prefix>.*?)(?<numbers>([-]*(\d+[\,]*)+[\.]{0,1}\d*[eEdD]{0,1}[-+]*\d*[i]{0,1})|([-]*(\d+[\,]*)*[\.]{1,1}\d+[eEdD]{0,1}[-+]*\d*[i]{0,1}))(?<suffix>.*)';
                try
                    result = regexp(rawData{row}, regexstr, 'names');
                    numbers = result.numbers;
                    
                    % Detected commas in non-thousand locations.
                    invalidThousandsSeparator = false;
                    if any(numbers==',');
                        thousandsRegExp = '^\d+?(\,\d{3})*\.{0,1}\d*$';
                        if isempty(regexp(numbers, thousandsRegExp, 'once'));
                            numbers = NaN;
                            invalidThousandsSeparator = true;
                        end
                    end
                    % Convert numeric text to numbers.
                    if ~invalidThousandsSeparator;
                        numbers = textscan(strrep(numbers, ',', ''), '%f');
                        numericData(row, col) = numbers{1};
                        raw{row, col} = numbers{1};
                    end
                catch me
                end
            end
        end
        rawNumericColumns = raw(:, [1,2,3]);
        rawCellColumns = raw(:, 4);
        R = cellfun(@(x) ~isnumeric(x) && ~islogical(x),rawNumericColumns); % Find non-numeric cells
        rawNumericColumns(R) = {NaN}; % Replace non-numeric cells
        onset = cell2mat(rawNumericColumns(:, 1));
        peak = cell2mat(rawNumericColumns(:, 2));
        offset = cell2mat(rawNumericColumns(:, 3));
        ssssssss = rawCellColumns(:, 1);
        clearvars filename delimiter formatSpec fileID dataArray ans raw col numericData rawData row regexstr result numbers invalidThousandsSeparator thousandsRegExp me rawNumericColumns rawCellColumns R;
        
        primary_size_del_origin = size(peak, 1);
        
        qrs_del_origin = zeros(primary_size_del_origin, 2);
        
        for i = 1:primary_size_del_origin
            if offset(i, 1) > 0
                qrs_del_origin(i,1) = onset(i, 1);
                qrs_del_origin(i,2) = offset(i, 1);
            else
                qrs_del_origin(i,1) = 0;
                qrs_del_origin(i,2) = 0;
            end
            
            if onset(i, 1) < qrs_del_candidate(1,1)
                qrs_del_origin(i,1) = 0;
                qrs_del_origin(i,2) = 0;
            end
            
            if offset(i, 1) > qrs_del_candidate(size(qrs_del_candidate, 1),2)
                qrs_del_origin(i,1) = 0;
                qrs_del_origin(i,2) = 0;
            end
            
        end
        
        qrs_del_origin( ~any(qrs_del_origin,2), : ) = [];
        
        qrs_del_diffs = zeros(size(qrs_del_origin, 1) - 1, 2);
        
        candidate_del_id_tmp = 1;
        for original_del_id = 1:size(qrs_del_diffs, 1)
            
            current_diff_onset = abs(qrs_del_candidate(candidate_del_id_tmp, 1) - qrs_del_origin(original_del_id, 1));
            next_diff_onset = abs(qrs_del_candidate(candidate_del_id_tmp + 1, 1) - qrs_del_origin(original_del_id, 1));
            current_diff_offset = abs(qrs_del_candidate(candidate_del_id_tmp, 2) - qrs_del_origin(original_del_id, 2));
            next_diff_offset = abs(qrs_del_candidate(candidate_del_id_tmp + 1, 2) - qrs_del_origin(original_del_id, 2));
            
            
            
            while ((next_diff_onset < current_diff_onset) && (candidate_del_id_tmp + 1 < size(qrs_del_candidate, 1)))
                candidate_del_id_tmp = candidate_del_id_tmp + 1;
                
                current_diff_onset = abs(qrs_del_candidate(candidate_del_id_tmp, 1) - qrs_del_origin(original_del_id, 1));
                next_diff_onset = abs(qrs_del_candidate(candidate_del_id_tmp + 1, 1) - qrs_del_origin(original_del_id, 1));
                
                current_diff_offset = abs(qrs_del_candidate(candidate_del_id_tmp, 2) - qrs_del_origin(original_del_id, 2));
                next_diff_offset = abs(qrs_del_candidate(candidate_del_id_tmp + 1, 2) - qrs_del_origin(original_del_id, 2));
            end
            
            qrs_del_diffs(original_del_id, 1) = current_diff_onset;
            qrs_del_diffs(original_del_id, 2) = current_diff_offset;
            
        end
        
        correct_count = 0;
        non_correct_count = 0;
        for diff_id = 1:size(qrs_del_diffs, 1)
            
            if qrs_del_diffs(diff_id, 1) > window_limit || qrs_del_diffs(diff_id, 2) > window_limit
                non_correct_count = non_correct_count + 1;
                non_corect_dels(non_correct_count, 1) = qrs_del_origin(diff_id, 1);
                non_corect_dels(non_correct_count, 2) = qrs_del_origin(diff_id, 2);
                non_corect_dels(non_correct_count, 3) = max(qrs_del_diffs(diff_id, 2), qrs_del_diffs(diff_id, 1));
            else
                correct_count = correct_count + 1;
            end
            
        end
        
        if (non_correct_count > 0)
            file_name = sprintf('record_%d_%s.txt', record, leads{lead_id});
            file_id = fopen(file_name, 'w');
            for dump_id = 1:size(non_corect_dels, 1)
                fprintf(file_id, '%d %d %d\n', non_corect_dels(dump_id, 1), non_corect_dels(dump_id, 2), non_corect_dels(dump_id, 3));
            end
            fclose(file_id);
        end
        
        non_corect_dels = 0;
        
        
    end
    
end
