clear all;

base_name = 'qtdb';
freq = 250.0;

record = 12;

leads = {'lead_ii', 'lead_v5'};

for lead_id = 1:2
    
    fig_ecg = figure;
    propertyeditor(fig_ecg)
    lead = leads{lead_id};
    
    wdc_scale = 1;
    markerWidth = 12;
    is_filtered = 1;
    
    db_path = sprintf('../Data/%s/', base_name);
    record_path = sprintf('record_%d/', record);
    lead_path = sprintf('%s/', lead);
    
    if is_filtered
        file_name_ecg = sprintf('%s%s%sfiltrated.txt', db_path, record_path, lead_path);
    else
        file_name_ecg = sprintf('%s%s%soriginal.txt', db_path, record_path, lead_path);
    end
    
    ecg_lead = importdata(file_name_ecg);
    
    for i = 1:size(ecg_lead)
        times(i) = (i - 1);
        %times(i) = (i - 1) / freq;
    end
    
    hLine = plot(times, ecg_lead, 'k', 'LineWidth', 2);
    legend(hLine, 'ECG');
    set(gca, 'FontSize', 18);
    grid on;
    hold all;
    
    file_name_qrs_del = sprintf('%s%s%sqrs_delineation.txt', db_path, record_path, lead_path);
    qrs_del = importdata(file_name_qrs_del);
    
    times_qrs_onset = zeros(size(qrs_del, 1), 1);
    times_qrs_peak = zeros(size(qrs_del, 1), 1);
    times_qrs_offset = zeros(size(qrs_del, 1), 1);
    vals_qrs_onset = zeros(size(qrs_del, 1), 1);
    vals_qrs_peak = zeros(size(qrs_del, 1), 1);
    vals_qrs_offset = zeros(size(qrs_del, 1), 1);
    
    for i = 1:size(qrs_del, 1)
        times_qrs_onset(i) = times(qrs_del(i, 1) + 1);
        times_qrs_peak(i) = times(qrs_del(i, 2) + 1);
        times_qrs_offset(i) = times(qrs_del(i, 3) + 1);
        
        vals_qrs_onset(i) = ecg_lead(qrs_del(i, 1) + 1);
        vals_qrs_peak(i) = ecg_lead(qrs_del(i, 2) + 1);
        vals_qrs_offset(i) = ecg_lead(qrs_del(i, 3) + 1);
    end
    
    hLine = plot(times_qrs_onset, vals_qrs_onset,  '>', 'MarkerSize', markerWidth, 'Color', 'r', 'MarkerFaceColor', 'r');
    legend(hLine, sprintf('onset qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_qrs_peak, vals_qrs_peak,  'o', 'MarkerSize', markerWidth, 'Color', 'r', 'MarkerFaceColor', 'r');
    legend(hLine, sprintf('peak qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_qrs_offset, vals_qrs_offset, '<', 'MarkerSize', markerWidth, 'Color', 'r', 'MarkerFaceColor', 'r');
    legend(hLine, sprintf('offset qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    file_name_p_del = sprintf('%s%s%sp_delineation.txt', db_path, record_path, lead_path);
    p_del = importdata(file_name_p_del);
    
    times_p_onset = zeros(size(p_del, 1), 1);
    times_p_peak = zeros(size(p_del, 1), 1);
    times_p_offset = zeros(size(p_del, 1), 1);
    vals_p_onset = zeros(size(p_del, 1), 1);
    vals_p_peak = zeros(size(p_del, 1), 1);
    vals_p_offset = zeros(size(p_del, 1), 1);
    
    for i = 1:size(p_del, 1)
        times_p_onset(i) = times(p_del(i, 1) + 1);
        times_p_peak(i) = times(p_del(i, 2) + 1);
        times_p_offset(i) = times(p_del(i, 3) + 1);
        
        vals_p_onset(i) = ecg_lead(p_del(i, 1) + 1);
        vals_p_peak(i) = ecg_lead(p_del(i, 2) + 1);
        vals_p_offset(i) = ecg_lead(p_del(i, 3) + 1);
    end
    
    hLine = plot(times_p_onset, vals_p_onset,  '>', 'MarkerSize', markerWidth, 'Color', [0 0.5 0], 'MarkerFaceColor',  [0 0.5 0]);
    legend(hLine, sprintf('onset p'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_p_peak, vals_p_peak,  'o', 'MarkerSize', markerWidth, 'Color', [0 0.5 0], 'MarkerFaceColor',  [0 0.5 0]);
    legend(hLine, sprintf('peak p'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_p_offset, vals_p_offset, '<', 'MarkerSize', markerWidth, 'Color', [0 0.5 0], 'MarkerFaceColor',  [0 0.5 0]);
    legend(hLine, sprintf('offset p'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    file_name_t_del = sprintf('%s%s%st_delineation.txt', db_path, record_path, lead_path);
    t_del = importdata(file_name_t_del);
    
    times_t_onset = zeros(size(t_del, 1), 1);
    times_t_peak = zeros(size(t_del, 1), 1);
    times_t_offset = zeros(size(t_del, 1), 1);
    vals_t_onset = zeros(size(t_del, 1), 1);
    vals_t_peak = zeros(size(t_del, 1), 1);
    vals_t_offset = zeros(size(t_del, 1), 1);
    
    for i = 1:size(t_del, 1)
        times_t_onset(i) = times(t_del(i, 1) + 1);
        times_t_peak(i) = times(t_del(i, 2) + 1);
        times_t_offset(i) = times(t_del(i, 3) + 1);
        
        vals_t_onset(i) = ecg_lead(t_del(i, 1) + 1);
        vals_t_peak(i) = ecg_lead(t_del(i, 2) + 1);
        vals_t_offset(i) = ecg_lead(t_del(i, 3) + 1);
    end
    
    hLine = plot(times_t_onset, vals_t_onset,  '>', 'MarkerSize', markerWidth, 'Color', [0 0.45 0.74], 'MarkerFaceColor',  [0 0.45 0.74]);
    legend(hLine, sprintf('onset t'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_t_peak, vals_t_peak,  'o', 'MarkerSize', markerWidth, 'Color', [0 0.45 0.74], 'MarkerFaceColor',  [0 0.45 0.74]);
    legend(hLine, sprintf('peak t'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_t_offset, vals_t_offset, '<', 'MarkerSize', markerWidth, 'Color', [0 0.45 0.74], 'MarkerFaceColor',  [0 0.45 0.74]);
    legend(hLine, sprintf('offset t'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    
    
    
    
    
    
    
    
    
    
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
    
    times_qrs_onset = zeros(size(peak, 1), 1);
    times_qrs_peak = zeros(size(peak, 1), 1);
    times_qrs_offset = zeros(size(peak, 1), 1);
    vals_qrs_onset = zeros(size(peak, 1), 1);
    vals_qrs_peak = zeros(size(peak, 1), 1);
    vals_qrs_offset = zeros(size(peak, 1), 1);
    
    for i = 1:size(peak, 1)
        
        if offset(i, 1) > 0
            times_qrs_onset(i) = times(onset(i, 1) + 1);
            vals_qrs_onset(i) = ecg_lead(onset(i, 1) + 1);
            times_qrs_peak(i) = times(peak(i, 1) + 1);
            vals_qrs_peak(i) = ecg_lead(peak(i, 1) + 1);
            times_qrs_offset(i) = times(offset(i, 1) + 1);
            vals_qrs_offset(i) = ecg_lead(offset(i, 1) + 1);
        else
            times_qrs_onset(i) = times(onset(i, 1) + 1);
            vals_qrs_onset(i) = ecg_lead(onset(i, 1) + 1);
            times_qrs_peak(i) = times(onset(i, 1) + 1);
            vals_qrs_peak(i) = ecg_lead(onset(i, 1) + 1);
            times_qrs_offset(i) = times(peak(i, 1) + 1);
            vals_qrs_offset(i) = ecg_lead(peak(i, 1) + 1);
        end
    end
    
    clearvars onset peak offset;
    
    hLine = plot(times_qrs_onset, vals_qrs_onset,  '>', 'MarkerSize', 8, 'Color', 'y', 'MarkerFaceColor', [1 0.84 0]);
    legend(hLine, sprintf('onset qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_qrs_peak, vals_qrs_peak,  'o', 'MarkerSize', 8, 'Color', 'y', 'MarkerFaceColor', [1 0.84 0]);
    legend(hLine, sprintf('peak qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_qrs_offset, vals_qrs_offset, '<', 'MarkerSize', 8, 'Color', 'y', 'MarkerFaceColor', [1 0.84 0]);
    legend(hLine, sprintf('offset qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    file_name_p_del = sprintf('%s%s%sp_original_delineation.txt', db_path, record_path, lead_path);
    delimiter = '\t';
    formatSpec = '%s%s%s%s%[^\n\r]';
    fileID = fopen(file_name_p_del,'r');
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
    pp = rawCellColumns(:, 1);
    clearvars filename delimiter formatSpec fileID dataArray ans raw col numericData rawData row regexstr result numbers invalidThousandsSeparator thousandsRegExp me rawNumericColumns rawCellColumns R;
    
    times_p_onset = zeros(size(peak, 1), 1);
    times_p_peak = zeros(size(peak, 1), 1);
    times_p_offset = zeros(size(peak, 1), 1);
    vals_p_onset = zeros(size(peak, 1), 1);
    vals_p_peak = zeros(size(peak, 1), 1);
    vals_p_offset = zeros(size(peak, 1), 1);
    
    for i = 1:size(peak, 1)
        
        if offset(i, 1) > 0
            times_p_onset(i) = times(onset(i, 1) + 1);
            times_p_peak(i) = times(peak(i, 1) + 1);
            times_p_offset(i) = times(offset(i, 1) + 1);
            vals_p_onset(i) = ecg_lead(onset(i, 1) + 1);
            vals_p_peak(i) = ecg_lead(peak(i, 1) + 1);
            vals_p_offset(i) = ecg_lead(offset(i, 1) + 1);
        else
            times_p_onset(i) = times(onset(i, 1) + 1);
            times_p_peak(i) = times(onset(i, 1) + 1);
            times_p_offset(i) = times(peak(i, 1) + 1);
            vals_p_onset(i) = ecg_lead(onset(i, 1) + 1);
            vals_p_peak(i) = ecg_lead(onset(i, 1) + 1);
            vals_p_offset(i) = ecg_lead(peak(i, 1) + 1);
        end
        
    end
    
    clearvars onset peak offset;
    
    hLine = plot(times_p_onset, vals_p_onset,  '>', 'MarkerSize', 8, 'Color', [0 1.0 0], 'MarkerFaceColor',  [0.47 0.67 0.19]);
    legend(hLine, sprintf('onset p'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_p_peak, vals_p_peak,  'o', 'MarkerSize', 8, 'Color', [0 1.0 0], 'MarkerFaceColor',  [0.47 0.67 0.19]);
    legend(hLine, sprintf('peak p'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_p_offset, vals_p_offset, '<', 'MarkerSize', 8, 'Color', [0 1.0 0], 'MarkerFaceColor',  [0.47 0.67 0.19]);
    legend(hLine, sprintf('offset p'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    file_name_t_del = sprintf('%s%s%st_original_delineation.txt', db_path, record_path, lead_path);
    delimiter = '\t';
    formatSpec = '%s%s%s%s%s%[^\n\r]';
    fileID = fopen(file_name_t_del,'r');
    dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter,  'ReturnOnError', false);
    fclose(fileID);
    raw = repmat({''},length(dataArray{1}),length(dataArray)-1);
    for col=1:length(dataArray)-1
        raw(1:length(dataArray{col}),col) = dataArray{col};
    end
    numericData = NaN(size(dataArray{1},1),size(dataArray,2));
    for col=[1,2,3,4]
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
    rawNumericColumns = raw(:, [1,2,3,4]);
    rawCellColumns = raw(:, 5);
    R = cellfun(@(x) ~isnumeric(x) && ~islogical(x),rawNumericColumns); % Find non-numeric cells
    rawNumericColumns(R) = {NaN}; % Replace non-numeric cells
    onset = cell2mat(rawNumericColumns(:, 1));
    peak = cell2mat(rawNumericColumns(:, 2));
    offset_1 = cell2mat(rawNumericColumns(:, 3));
    offset_2 = cell2mat(rawNumericColumns(:, 4));
    tt = rawCellColumns(:, 1);
    clearvars filename delimiter formatSpec fileID dataArray ans raw col numericData rawData row regexstr result numbers invalidThousandsSeparator thousandsRegExp me rawNumericColumns rawCellColumns R;
    
    times_t_onset = zeros(size(peak, 1), 1);
    times_t_peak = zeros(size(peak, 1), 1);
    times_t_offset = zeros(size(peak, 1), 1);
    vals_t_onset = zeros(size(peak, 1), 1);
    vals_t_peak = zeros(size(peak, 1), 1);
    vals_t_offset = zeros(size(peak, 1), 1);
    
    for i = 1:size(peak, 1)
        if offset_2(i, 1) > 0
            times_t_onset(i) = times(onset(i, 1) + 1);
            vals_t_onset(i) = ecg_lead(onset(i, 1) + 1);
            times_t_peak(i) = times(peak(i, 1) + 1);
            vals_t_peak(i) = ecg_lead(peak(i, 1) + 1);
            times_t_offset(i) = times(offset_2(i, 1) + 1);
            vals_t_offset(i) = ecg_lead(offset_2(i, 1) + 1);
        elseif offset_1(i, 1) > 0
            times_t_onset(i) = times(onset(i, 1) + 1);
            vals_t_onset(i) = ecg_lead(onset(i, 1) + 1);
            times_t_peak(i) = times(peak(i, 1) + 1);
            vals_t_peak(i) = ecg_lead(peak(i, 1) + 1);
            times_t_offset(i) = times(offset_1(i, 1) + 1);
            vals_t_offset(i) = ecg_lead(offset_1(i, 1) + 1);
        else
            times_t_onset(i) = times(onset(i, 1) + 1);
            vals_t_onset(i) = ecg_lead(onset(i, 1) + 1);
            times_t_peak(i) = times(onset(i, 1) + 1);
            vals_t_peak(i) = ecg_lead(onset(i, 1) + 1);
            times_t_offset(i) = times(peak(i, 1) + 1);
            vals_t_offset(i) = ecg_lead(peak(i, 1) + 1);
        end
    end
    
    hLine = plot(times_t_onset, vals_t_onset,  '>', 'MarkerSize', 8, 'Color', [0 0.1 1.0], 'MarkerFaceColor',  [0.3 0.75 0.93]);
    legend(hLine, sprintf('onset t'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_t_peak, vals_t_peak,  'o', 'MarkerSize', 8, 'Color', [0 0.1 1.0], 'MarkerFaceColor',  [0.3 0.75 0.93]);
    legend(hLine, sprintf('peak t'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_t_offset, vals_t_offset, '<', 'MarkerSize', 8, 'Color', [0 0.1 1.0], 'MarkerFaceColor',  [0.3 0.75 0.93]);
    legend(hLine, sprintf('offset t'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    
    
    
    
    
    
    
    
    
    file_name_wdc = sprintf('%s%s%swdc.txt', db_path, record_path, lead_path);
    wdc = importdata(file_name_wdc);
    
    wdc_num = size(wdc, 2);
    
    wdc_shifts = [0 1 3 7 15 31 65];
    
    for wdc_scale = 1:wdc_num
        
        curr_wdc = wdc(:,wdc_scale);
        title(lead);
        hLine = plot(times(1:size(wdc, 1)), curr_wdc, 'LineWidth', 1);
        legend(hLine, sprintf('wdc %d', wdc_scale));
        set(gca, 'FontSize', 18);
        hold all;
    end
    
    grid on;
    
    propertyeditor(fig_ecg)
    
end
