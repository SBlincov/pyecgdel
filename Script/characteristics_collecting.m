globalPath = ('../Data/physionet2017/');

numRecords = 8528;
numLeads = 1;
leadNames = {'lead'};

numCharacteristics = 38;

missingNumber = -10000;
missingCharacter = 'n';

dataArray = zeros(1, numCharacteristics * numLeads);
diagnosisArray = cell(1);

for recordID = 1:numRecords
    fprintf('patient %d \n', recordID);
    leadDataArray = zeros;
    leadNamesArray = zeros;
    for leadID = 1:numLeads
        localPath = sprintf('record_%d/%s/characteristics.txt', recordID, leadNames{leadID});
        fullPath = strcat(globalPath, localPath);
        delimiter = ' ';
        data = readtable(fullPath, 'ReadRowNames', 0, 'ReadVariableNames', 0, 'Delimiter', delimiter, 'FileType', 'text');
        if isempty(data) 
            continue
        else
            for i=1:height(data(:, end))
                if ~iscell(data{i, end-1})
                    if ~isnan(data{i, end-1})
                        data{i, end} = data{i, end-1};
                    end
                end
            end
            names = table2array(data(:, 1));
            values = table2array(data(:, end));
            for nameID = 1:length(names)
                names{nameID} = strcat(leadNames{leadID}, '_', names{nameID});
            end
            if iscell(values)
                for valueID = 1:length(values)
                    if values{valueID} == missingCharacter
                        values{valueID} = missingNumber;
                    else
                        values{valueID} = str2double(values{valueID});
                    end
                end
                values = cell2mat(values);
            end
            leadNamesArray = horzcat(leadNamesArray, (names)');
            leadDataArray = horzcat(leadDataArray, (values)');
            clearvars values names
        end
    end
    
    diagnosisPath = sprintf('record_%d/diagnosis.txt', recordID);
    fullPath = strcat(globalPath, diagnosisPath);
    diagnosisFile = fopen(fullPath);
    diagnosis = fgets(diagnosisFile);
    fclose(diagnosisFile);
    
    diagnosisArray{recordID} = char(strtrim(diagnosis));
    
    leadDataArray = leadDataArray(2:end);
    leadNamesArray = leadNamesArray(2:end);
    dataArray = vertcat(dataArray, leadDataArray);
end

diagnosisArray = diagnosisArray';
dataArray = dataArray(2:end, :);
dataArray = num2cell(dataArray);
for i = 1:length([dataArray{:, 1}])
    for j = 1:length([dataArray{1, :}])
        if dataArray{i, j} == missingNumber
            dataArray{i, j} = missingCharacter;
        end
    end
end

dataArray = horzcat(dataArray, diagnosisArray);
leadNamesArray = horzcat(leadNamesArray, 'diagnosis');

dataArray = array2table(dataArray, 'VariableNames', leadNamesArray);
writetable(dataArray, strcat(globalPath, 'characteristics'), 'FileType', 'spreadsheet');
%writetable(dataArray, strcat(globalPath, 'characteristics.txt'), 'Delimiter', '\t');