clear all;

base_name = 'shiller';
freq = 500.0;

%record = 50005192;
record = 2508;

leads = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};
lead_ids = 1:12;
num_leads = size(lead_ids, 2);

qrs_ver_lead_id = num_leads;

qrs_corr_ids = [];

num_qrs_ids = zeros(num_leads,1);
num_t_ids = zeros(num_leads,1);
num_p_ids = zeros(num_leads,1);

least_qrs_ids = [];
least_t_ids = [];
least_p_ids = [];

qrs_lefts = [];
qrs_rights = [];

qrs_lefts_global = [];
qrs_lefts_counts = [];
qrs_rights_global = [];
qrs_rights_counts = [];

mean_qrs = zeros(num_leads);
mean_qrs_global = 0;
mean_qrs_part = 0.75;

for lead_id = 1:num_leads
    
    lead_name_long = lead_ids(lead_id);
    
    lead = leads{lead_name_long};
    lead_name = lead(6:end);
   
    db_path = sprintf('../Data/%s/', base_name);
    record_path = sprintf('record_%d/', record);
    lead_path = sprintf('%s/', lead);
    
    file_name_qrs_del = sprintf('%s%s%sqrs_delineation.txt', db_path, record_path, lead_path);
    qrs_del = importdata(file_name_qrs_del);
    
    num_qrs_ids_curr = size(qrs_del, 1);
    num_qrs_ids(lead_id) = num_qrs_ids_curr;
    least_qrs_ids{lead_id} = linspace(1, num_qrs_ids_curr, num_qrs_ids_curr)';
    qrs_lefts_curr = qrs_del(:, 1);
    qrs_lefts{lead_id} = qrs_lefts_curr;
    qrs_rights_curr = qrs_del(:, 3);
    qrs_rights{lead_id} = qrs_rights_curr;
    
    for del_id = 1:num_qrs_ids_curr
        mean_qrs(lead_id) = mean_qrs(lead_id) + (qrs_rights_curr(del_id) - qrs_lefts_curr(del_id));
    end
    mean_qrs(lead_id) = mean_qrs(lead_id) / num_qrs_ids_curr;
    
end

mean_qrs_global = mean(mean_qrs);

qrs_lefts_global = qrs_lefts{1};
qrs_rights_global = qrs_rights{1};
qrs_borders_counts = ones(num_qrs_ids(1));

for lead_id = 2:num_leads
    
    qrs_lefts_curr = qrs_lefts{lead_id};
    qrs_rights_curr = qrs_rights{lead_id};
    
    curr_num_global = size(qrs_lefts_global, 1);
    
    for del_id = 1:num_qrs_ids(lead_id)
        
        left_diffs = zeros(curr_num_global, 1);
        right_diffs = zeros(curr_num_global, 1);
        for g_del_id = 1:curr_num_global
            left_diffs(g_del_id) = qrs_lefts_curr(del_id) - qrs_lefts_global(g_del_id) / qrs_borders_counts(g_del_id);
            right_diffs(g_del_id) = qrs_rights_curr(del_id) - qrs_rights_global(g_del_id) / qrs_borders_counts(g_del_id);
        end
        
        [left_min_diff, left_argmin_diff] = min(abs(left_diffs));
        [right_min_diff, right_argmin_diff] = min(abs(right_diffs));
        
        if (left_argmin_diff == right_argmin_diff)
            
            argmin_diff = left_argmin_diff;
            
            if ((left_min_diff < mean_qrs_global * mean_qrs_part) || (right_min_diff < mean_qrs_global * mean_qrs_part))
                
                qrs_lefts_global(argmin_diff) = qrs_lefts_global(argmin_diff) + left_diffs(argmin_diff);
                qrs_rights_global(argmin_diff) = qrs_rights_global(argmin_diff) + right_diffs(argmin_diff);
                qrs_borders_counts(argmin_diff) = qrs_borders_counts(argmin_diff) + 1;
                
            else
                if (left_diffs(argmin_diff) < 0 && right_diffs(argmin_diff) < 0)
                    
                    qrs_lefts_global = vertcat(qrs_lefts_global(1:argmin_diff-1), qrs_lefts_curr, qrs_lefts_global(argmin_diff:end));
                    qrs_rights_global = vertcat(qrs_rights_global(1:argmin_diff-1), qrs_rights_curr, qrs_rights_global(argmin_diff:end));
                    qrs_borders_counts(argmin_diff) = vertcat(qrs_borders_counts(1:argmin_diff - 1), 1, qrs_borders_counts(argmin_diff:end));
                    
                elseif ((left_diffs(argmin_diff) > 0 && right_diffs(argmin_diff) > 0))
                        
                    qrs_lefts_global = vertcat(qrs_lefts_global(1:argmin_diff), qrs_lefts_curr, qrs_lefts_global(argmin_diff+1:end));
                    qrs_rights_global = vertcat(qrs_rights_global(1:argmin_diff), qrs_rights_curr, qrs_rights_global(argmin_diff+1:end));
                    qrs_borders_counts(argmin_diff) = vertcat(qrs_borders_counts(1:argmin_diff), 1, qrs_borders_counts(argmin_diff+1:end));
                    
                else
                    
                    disp('wrong left and right diffs');
                    lead_id = lead_id
                    del_id = del_id
                    
                end
            end
            
            qrs_lefts_global = qrs_lefts_global;
            qrs_rights_global = qrs_rights_global;
            
        else
            
            disp('onset and offset out of correspondence');
            lead_id = lead_id
            del_id = del_id
        
        end
        
        
        
    end
    
end




for


