globalPath = ('../Data/ptbdb/');

numPatients = 549;
numLeads = 15;
leadNames = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6', 'lead_vx', 'lead_vy', 'lead_vz'};

% numPatients = 75;
% numLeads = 12;
% leadNames = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};

numCharacteristics = 31;

missingNumber = -10000;
missingCharacter = 'n';

dataArray = zeros(1, numCharacteristics * numLeads);
diagnosisArray = cell(1);

for patientID = 1:numPatients
    fprintf('patient %d \n', patientID);
    leadDataArray = zeros;
    leadNamesArray = zeros;
    for leadID = 1:numLeads
        localPath = sprintf('patient_%d/%s/characteristics.txt', patientID, leadNames{leadID});
        fullPath = strcat(globalPath, localPath);
        delimiter = ' ';
        data = readtable(fullPath, 'ReadRowNames', 0, 'ReadVariableNames', 0, 'Delimiter', delimiter, 'FileType', 'text', 'TreatAsEmpty',{missingCharacter});
        names = table2array(data(:, 1));
        values = table2array(data(:, end));
        for nameID = 1:length(names)
            names{nameID} = strcat(leadNames{leadID}, '_', names{nameID});
        end
        values(isnan(values)) = missingNumber;
        leadNamesArray = horzcat(leadNamesArray, (names)');
        leadDataArray = horzcat(leadDataArray, (values)');
        clearvars values names
    end
    
    diagnosisPath = sprintf('patient_%d/diagnosis.txt', patientID);
    fullPath = strcat(globalPath, diagnosisPath);
    diagnosisFile = fopen(fullPath);
    diagnosis = fgets(diagnosisFile);
    fclose(diagnosisFile);
    
    diagnosisArray{patientID} = char(strtrim(diagnosis));
    
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
writetable(dataArray, strcat(globalPath, 'characteristics.txt'), 'Delimiter', '\t');