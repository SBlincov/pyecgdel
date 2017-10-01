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

qrs_lefts_sum = [];
qrs_lefts_counts = [];
qrs_rights_sum = [];
qrs_rights_counts = [];

mean_qrs = zeros(num_leads, 1);
mean_qrs_global = 0;
mean_qrs_part = 0.75;
diff_qrs_part = 0.25;
diff_qrs_corr = 0.20;

%% Reading all leads and calc global avg QRS length
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

%% Creating array with all complexes (with average values and occurancy rate)

[max_complexes, id_with_max] = max(num_qrs_ids);

qrs_lefts_sum = qrs_lefts{id_with_max};
qrs_rights_sum = qrs_rights{id_with_max};
qrs_borders_counts = ones(num_qrs_ids(id_with_max), 1);

for lead_id = 1:num_leads
    
    % For all leads excluding start lead with max num of complexes QRS
    if (lead_id ~= id_with_max)
        
        qrs_lefts_curr = qrs_lefts{lead_id};
        qrs_rights_curr = qrs_rights{lead_id};
        
        for del_id = 1:num_qrs_ids(lead_id)
            
            curr_num_global = size(qrs_lefts_sum, 1);
            
            left_diffs = zeros(curr_num_global, 1);
            right_diffs = zeros(curr_num_global, 1);
            for g_del_id = 1:curr_num_global
                left_diffs(g_del_id) = qrs_lefts_curr(del_id) - qrs_lefts_sum(g_del_id) / qrs_borders_counts(g_del_id);
                right_diffs(g_del_id) = qrs_rights_curr(del_id) - qrs_rights_sum(g_del_id) / qrs_borders_counts(g_del_id);
            end
            
            [left_min_diff_abs, left_argmin_diff] = min(abs(left_diffs));
            [right_min_diff_abs, right_argmin_diff] = min(abs(right_diffs));
            
            % Additional checking of argmins
            if (abs(left_argmin_diff - right_argmin_diff) == 1)
                
                left_diff_own = left_diffs(left_argmin_diff);
                left_diff_der = left_diffs(right_argmin_diff);
                
                right_diff_own = right_diffs(right_argmin_diff);
                right_diff_der = right_diffs(left_argmin_diff);
                
                left_diff_diff_abs = abs(abs(left_diff_own) - abs(left_diff_der));
                right_diff_diff_abs = abs(abs(right_diff_own) - abs(right_diff_der));
                
                if ((left_diff_diff_abs < right_diff_diff_abs) && (left_diff_diff_abs < mean_qrs_global * diff_qrs_part))
                    
                    left_argmin_diff = right_argmin_diff;
                    left_min_diff_abs = abs(left_diffs(left_argmin_diff));
                    
                elseif ((right_diff_diff_abs < left_diff_diff_abs) && (right_diff_diff_abs < mean_qrs_global))
                    
                    right_argmin_diff = left_argmin_diff;
                    right_min_diff_abs = abs(right_diffs(right_argmin_diff));
                    
                end
                
            end
            
            qrs_left_curr = qrs_lefts_sum(left_argmin_diff) / qrs_borders_counts(left_argmin_diff) + left_diffs(left_argmin_diff);
            qrs_right_curr = qrs_rights_sum(right_argmin_diff) / qrs_borders_counts(right_argmin_diff) + right_diffs(right_argmin_diff);
            
            if (left_argmin_diff == right_argmin_diff)
                
                argmin_diff = left_argmin_diff;
                
                if ((left_min_diff_abs < mean_qrs_global * mean_qrs_part) || (right_min_diff_abs < mean_qrs_global * mean_qrs_part))
                    
                    qrs_lefts_sum(argmin_diff) = qrs_lefts_sum(argmin_diff) + qrs_left_curr;
                    qrs_rights_sum(argmin_diff) = qrs_rights_sum(argmin_diff) + qrs_right_curr;
                    qrs_borders_counts(argmin_diff) = qrs_borders_counts(argmin_diff) + 1;
                    
                else
                    if (left_diffs(argmin_diff) < 0 && right_diffs(argmin_diff) < 0)
                        
                        qrs_lefts_sum = vertcat(qrs_lefts_sum(1:argmin_diff-1), qrs_left_curr, qrs_lefts_sum(argmin_diff:end));
                        qrs_rights_sum = vertcat(qrs_rights_sum(1:argmin_diff-1), qrs_right_curr, qrs_rights_sum(argmin_diff:end));
                        qrs_borders_counts = vertcat(qrs_borders_counts(1:argmin_diff - 1), 1, qrs_borders_counts(argmin_diff:end));
                        
                    elseif ((left_diffs(argmin_diff) > 0 && right_diffs(argmin_diff) > 0))
                        
                        qrs_lefts_sum = vertcat(qrs_lefts_sum(1:argmin_diff), qrs_left_curr, qrs_lefts_sum(argmin_diff+1:end));
                        qrs_rights_sum = vertcat(qrs_rights_sum(1:argmin_diff), qrs_right_curr, qrs_rights_sum(argmin_diff+1:end));
                        qrs_borders_counts = vertcat(qrs_borders_counts(1:argmin_diff), 1, qrs_borders_counts(argmin_diff+1:end));
                        
                    else
                        
                        disp('wrong left and right diffs');
                        lead_id = lead_id
                        del_id = del_id
                        
                    end
                end
            else
                
                disp('onset and offset out of correspondence');
                lead_id = lead_id
                del_id = del_id
                
            end
        end
        
    end
end

num_qrs_all = size(qrs_borders_counts, 1);
qrs_lefts_all_avg = zeros(num_qrs_all, 1);
qrs_rights_all_avg = zeros(num_qrs_all, 1);

for cmplx_id = 1:num_qrs_all
    qrs_lefts_all_avg(cmplx_id) = qrs_lefts_sum(cmplx_id) / qrs_borders_counts(cmplx_id);
    qrs_rights_all_avg(cmplx_id) = qrs_rights_sum(cmplx_id) / qrs_borders_counts(cmplx_id);
end

%% Creating the corresponding matrix

corr_matrix = zeros(num_qrs_all, num_leads);

for lead_id = 1:num_leads
    
    qrs_lefts_curr = qrs_lefts{lead_id};
    qrs_rights_curr = qrs_rights{lead_id};
    
    for del_id = 1:num_qrs_ids(lead_id)
        
        left_diffs = zeros(num_qrs_all, 1);
        right_diffs = zeros(num_qrs_all, 1);
        for cmplx_id = 1:num_qrs_all
            left_diffs(cmplx_id) = qrs_lefts_curr(del_id) - qrs_lefts_all_avg(cmplx_id);
            right_diffs(cmplx_id) = qrs_rights_curr(del_id) - qrs_rights_all_avg(cmplx_id);
        end
        
        [left_min_diff_abs, left_argmin_diff] = min(abs(left_diffs));
        [right_min_diff_abs, right_argmin_diff] = min(abs(right_diffs));
        
        % Additional checking of argmins
        if (abs(left_argmin_diff - right_argmin_diff) == 1)
            
            left_diff_own = left_diffs(left_argmin_diff);
            left_diff_der = left_diffs(right_argmin_diff);
            
            right_diff_own = right_diffs(right_argmin_diff);
            right_diff_der = right_diffs(left_argmin_diff);
            
            left_diff_diff_abs = abs(abs(left_diff_own) - abs(left_diff_der));
            right_diff_diff_abs = abs(abs(right_diff_own) - abs(right_diff_der));
            
            if ((left_diff_diff_abs < right_diff_diff_abs) && (left_diff_diff_abs < mean_qrs_global * diff_qrs_corr))
                
                left_argmin_diff = right_argmin_diff;
                left_min_diff_abs = abs(left_diffs(left_argmin_diff));
                
            elseif ((right_diff_diff_abs < left_diff_diff_abs) && (right_diff_diff_abs < mean_qrs_global))
                
                right_argmin_diff = left_argmin_diff;
                right_min_diff_abs = abs(right_diffs(right_argmin_diff));
                
            end
            
        end
        
        if (left_argmin_diff == right_argmin_diff)
            
            argmin_diff = left_argmin_diff;
            corr_matrix(argmin_diff, lead_id) = del_id;
            
        else
            
            disp('onset and offset out of correspondence');
            lead_id = lead_id
            del_id = del_id
            
        end
    end
end





