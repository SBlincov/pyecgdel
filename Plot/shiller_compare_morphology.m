data_path_stable = '../Data/';
data_path_unstable = 'C:/Users/user/Desktop/pyecgdel/Data/';

database_name = 'shiller/';

record_name = 'record_50436612/';

lead_names = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};

complex_name = 't';

difference = {};
difference_id = 1;

for lead_id = 1:length(lead_names)
    
    lead_name = lead_names{lead_id};
    
    morph_path_stable = strcat(data_path_stable, database_name, record_name, lead_name, '/', complex_name, '_morphology.txt');
    morph_stable = importdata(morph_path_stable);
    
    morph_path_unstable = strcat(data_path_unstable, database_name, record_name, lead_name, '/', complex_name, '_morphology.txt');
    morph_unstable = importdata(morph_path_unstable);
    
    for morph_id = 1:size(morph_stable, 1)
        if ~strcmp(morph_stable.textdata{morph_id, 1}, morph_unstable.textdata{morph_id, 1}) || ~strcmp(morph_stable.textdata{morph_id, 2}, morph_unstable.textdata{morph_id, 2}) ||...
                morph_stable.data(morph_id, 1) ~= morph_unstable.data(morph_id, 1) || morph_stable.data(morph_id, 2) ~= morph_unstable.data(morph_id, 2) ||...
                morph_stable.data(morph_id, 3) ~= morph_unstable.data(morph_id, 3) || morph_stable.data(morph_id, 4) ~= morph_unstable.data(morph_id, 4) ||...
                morph_stable.data(morph_id, 5) ~= morph_unstable.data(morph_id, 5) || morph_stable.data(morph_id, 6) ~= morph_unstable.data(morph_id, 6)
            difference{difference_id, 1} = lead_name;
            difference{difference_id, 2} = morph_stable.textdata(morph_id, 1);
            difference{difference_id, 3} = morph_stable.textdata(morph_id, 2);
            for j = 1:6
                ind = 3+j;
                difference{difference_id, ind} = morph_stable.data(morph_id, j);
            end
            difference{difference_id, 10} = morph_unstable.textdata(morph_id, 1);
            difference{difference_id, 11} = morph_unstable.textdata(morph_id, 2);
            for j = 1:6
                ind = 11+j;
                difference{difference_id, ind} = morph_unstable.data(morph_id, j);
            end
            difference_id = difference_id + 1;
        end
    end
end