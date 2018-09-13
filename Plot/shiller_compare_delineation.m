data_path_stable = '../Data/';
data_path_unstable = 'C:/Users/user/Desktop/pyecgdel/Data/';

database_name = 'shiller/';

record_name = 'record_50436612/';

lead_names = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};

complex_name = 'p';

difference = {};
difference_id = 1;

for lead_id = 1:length(lead_names)
    
    lead_name = lead_names{lead_id};
    
    del_path_stable = strcat(data_path_stable, database_name, record_name, lead_name, '/', complex_name, '_delineation.txt');
    del_stable = importdata(del_path_stable);
    
    del_path_unstable = strcat(data_path_unstable, database_name, record_name, lead_name, '/', complex_name, '_delineation.txt');
    del_unstable = importdata(del_path_unstable);
    
    for del_id = 1:size(del_stable, 1)
        if del_stable(del_id, 1) ~= del_unstable(del_id, 1) || del_stable(del_id, 2) ~= del_unstable(del_id, 2) || ...
                del_stable(del_id, 3) ~= del_unstable(del_id, 3) || del_stable(del_id, 4) ~= del_unstable(del_id, 4)
            difference{difference_id, 1} = lead_name;
            for j = 1:4
                ind = 1+j;
                difference{difference_id, ind} = del_stable(del_id, j);
            end
            for j = 1:4
                ind = 5+j;
                difference{difference_id, ind} = del_unstable(del_id, j);
            end
            difference_id = difference_id + 1;
        end
    end
end