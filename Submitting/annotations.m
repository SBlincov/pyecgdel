clear all;

origin_path = '../Data/UNNCyberHeartDatabase';

fn = sprintf('%s/delineated_by_doc_ids.txt', origin_path);
records_ids = importdata(fn);
num_records = size(records_ids, 1);

num_points = 5000;

freq = 500.0;

leads = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};
num_leads = size(leads, 2);

for record_id = 1:num_records 
    
    record = records_ids(record_id)
    record_name = sprintf('record_%d', record);
    
    signals = zeros(num_points, num_leads);
    leads_names = {};
    
    for lead_id = 1:num_leads
        
        indexes = [];
        markers = {};
        
        lead = leads{lead_id};
        lead_name = lead(6:end);
        
        fn = sprintf('%s/%s/%s/qrs_delineation_doc.txt', origin_path, record_name, lead);
        data = importdata(fn);
        for del_id = 1:size(data, 1)
            for col = 1:3
                indexes = vertcat(indexes, data(del_id, col));
                if col == 1
                    markers = vertcat(markers, '(');
                elseif col == 2
                    markers = vertcat(markers, 'N');
                elseif col == 3
                    markers = vertcat(markers, ')');
                end
            end
        end
        
        fn = sprintf('%s/%s/%s/t_delineation_doc.txt', origin_path, record_name, lead);
        data = importdata(fn); 
        for del_id = 1:size(data, 1)
            for col = 1:3
                indexes = vertcat(indexes, data(del_id, col));
                if col == 1
                    markers = vertcat(markers, '(');
                elseif col == 2
                    markers = vertcat(markers, 't');
                elseif col == 3
                    markers = vertcat(markers, ')');
                end
            end
        end
        
        fn = sprintf('%s/%s/%s/p_delineation_doc.txt', origin_path, record_name, lead);
        data = importdata(fn);
        for del_id = 1:size(data, 1)
            for col = 1:3
                indexes = vertcat(indexes, data(del_id, col));
                if col == 1
                    markers = vertcat(markers, '(');
                elseif col == 2
                    markers = vertcat(markers, 'p');
                elseif col == 3
                    markers = vertcat(markers, ')');
                end
            end
        end
        
        [indexes_sorted, order] = sort(indexes);
        markers_sorted = '';
        for point_id = 1:size(markers, 1)
            tmp = markers{order(point_id)};
            markers_sorted(point_id) = tmp;
        end
        markers_sorted = markers_sorted';
        name = int2str(record_id);
        wrann(name, sprintf('atr_%s', lead_name), indexes_sorted, markers_sorted, [], [], []);
    end
end

