clear all;

base_name = 'qtdb';
rate = 250.0;

leads = {'lead_ii', 'lead_v5'};

tolerance = 0.15;

num_leads = 2;
start_record = 1;
num_records = 105;

qrs_rec_det = 0;
p_rec_det = 0;
t_rec_det = 0;

qrs_TP = zeros(num_leads, 1);
qrs_FN = zeros(num_leads, 1);
qrs_FP = zeros(num_leads, 1);
qrs_Se = zeros(num_leads, 1);
qrs_PPV = zeros(num_leads, 1);

p_TP = zeros(num_leads, 1);
p_FN = zeros(num_leads, 1);
p_FP = zeros(num_leads, 1);
p_Se = zeros(num_leads, 1);
p_PPV = zeros(num_leads, 1);

t_TP = zeros(num_leads, 1);
t_FN = zeros(num_leads, 1);
t_FP = zeros(num_leads, 1);
t_Se = zeros(num_leads, 1);
t_PPV = zeros(num_leads, 1);

qrs_peak_error_mean_avg = 0;
qrs_peak_error_std_avg = 0;
qrs_onset_error_mean_avg = 0;
qrs_onset_error_std_avg = 0;
qrs_offset_error_mean_avg = 0;
qrs_offset_error_std_avg = 0;

p_peak_error_mean_avg = 0;
p_peak_error_std_avg = 0;
p_onset_error_mean_avg = 0;
p_onset_error_std_avg = 0;
p_offset_error_mean_avg = 0;
p_offset_error_std_avg = 0;

t_peak_error_mean_avg = 0;
t_peak_error_std_avg = 0;
t_offset_error_mean_avg = 0;
t_offset_error_std_avg = 0;

for record = start_record : start_record + num_records - 1 
    
    record = record
    
    qrs_num_docs = 0;
    qrs_opt_num_hits = 0;
    qrs_ids = {};
    qrs_onsets = {};
    qrs_peaks = {};
    qrs_offsets = {};
    
    p_num_docs = 0;
    p_opt_num_hits = 0;
    p_ids = {};
    p_onsets = {};
    p_peaks = {};
    p_offsets = {};
    
    t_num_docs = 0;
    t_opt_num_hits = 0;
    t_ids = {};
    t_peaks = {};
    t_offsets = {};
    
    is_qrs = 1;
    is_p = 1;
    is_t = 1;
    
    for lead_id = 1:2
        
        lead = leads{lead_id};
        
        db_path = sprintf('../Data/%s/', base_name);
        record_path = sprintf('record_%d/', record);
        lead_path = sprintf('%s/', lead);
        
        
        %################################ QRS #################################
        file_name_qrs_del = sprintf('%s%s%sqrs_delineation.txt', db_path, record_path, lead_path);
        qrs_del = importdata(file_name_qrs_del);
        
        qrs_onset = zeros(size(qrs_del, 1), 1);
        qrs_peak = zeros(size(qrs_del, 1), 1);
        qrs_offset = zeros(size(qrs_del, 1), 1);
        
        for i = 1:size(qrs_del, 1)
            qrs_onset(i) = qrs_del(i, 1) + 1;
            qrs_peak(i) = qrs_del(i, 2) + 1;
            qrs_offset(i) = qrs_del(i, 3) + 1;
        end
        
        qrs_onsets{lead_id} = qrs_onset;
        qrs_peaks{lead_id} = qrs_peak;
        qrs_offsets{lead_id} = qrs_offset;
        
        file_name_qrs_del = sprintf('%s%s%sqrs_doctor1_delineation.txt', db_path, record_path, lead_path);
        qrs_del_doc = importdata(file_name_qrs_del);
        
        if size(qrs_del_doc, 1) == 0
            is_qrs = 0;
        end
        
        if is_qrs == 1
            qrs_onset_doc = zeros(size(qrs_del_doc, 1), 1);
            qrs_peak_doc = zeros(size(qrs_del_doc, 1), 1);
            qrs_offset_doc = zeros(size(qrs_del_doc, 1), 1);
            
            for i = 1:size(qrs_del_doc, 1)
                qrs_onset_doc(i) = qrs_del_doc(i, 1);
                qrs_peak_doc(i) = qrs_del_doc(i, 2);
                qrs_offset_doc(i) = qrs_del_doc(i, 3);
            end
            
            qrs_num_doc_records = size(qrs_del_doc, 1);
            qrs_num_docs = qrs_num_doc_records;
            
            qrs_diffs = zeros(qrs_num_doc_records, 1);
            qrs_our_records_id = zeros(qrs_num_doc_records, 1);
            qrs_hits_records_id = [];
            qrs_num_hits = 0;
            for i = 1:qrs_num_doc_records
                curr_diff = qrs_peak - qrs_peak_doc(i);
                [min_diff, min_diff_id] = min(abs(curr_diff));
                qrs_diffs(i) = min_diff;
                qrs_our_records_id(i) = min_diff_id;
                if(min_diff  / rate < tolerance)
                    qrs_num_hits = qrs_num_hits + 1;
                    qrs_hits_records_id = vertcat(qrs_hits_records_id, min_diff_id);
                end
            end
            
            qrs_ids{lead_id} = qrs_hits_records_id;
            
            if (qrs_num_hits > qrs_opt_num_hits)
                qrs_opt_num_hits = qrs_num_hits;
            end
            
            if(size(qrs_ids{lead_id}, 1) > 0)
                qrs_TP(lead_id) = qrs_TP(lead_id) + size(qrs_ids{lead_id}, 1);
                qrs_FN(lead_id) = qrs_FN(lead_id) + (qrs_num_docs - size(qrs_ids{lead_id}, 1));
                qrs_FP(lead_id) = qrs_FP(lead_id) + ((qrs_ids{lead_id}(end) - qrs_ids{lead_id}(1) + 1) - size(qrs_ids{lead_id}, 1));
            end
        
        end
        
        %################################# P ##################################
        file_name_p_del = sprintf('%s%s%sp_delineation.txt', db_path, record_path, lead_path);
        p_del = importdata(file_name_p_del);
        
        p_onset = zeros(size(p_del, 1), 1);
        p_peak = zeros(size(p_del, 1), 1);
        p_offset = zeros(size(p_del, 1), 1);
        
        for i = 1:size(p_del, 1)
            p_onset(i) = p_del(i, 1) + 1;
            p_peak(i) = p_del(i, 2) + 1;
            p_offset(i) = p_del(i, 3) + 1;
        end
        
        p_onsets{lead_id} = p_onset;
        p_peaks{lead_id} = p_peak;
        p_offsets{lead_id} = p_offset;
        
        file_name_p_del = sprintf('%s%s%sp_doctor1_delineation.txt', db_path, record_path, lead_path);
        p_del_doc = importdata(file_name_p_del);
        
        if size(p_del_doc, 1) == 0
            is_p = 0;
        end
        
        if(is_p == 1)
            p_onset_doc = zeros(size(p_del_doc, 1), 1);
            p_peak_doc = zeros(size(p_del_doc, 1), 1);
            p_offset_doc = zeros(size(p_del_doc, 1), 1);
            
            for i = 1:size(p_del_doc, 1)
                p_onset_doc(i) = p_del_doc(i, 1);
                p_peak_doc(i) = p_del_doc(i, 2);
                p_offset_doc(i) = p_del_doc(i, 3);
            end
            
            p_num_doc_records = size(p_del_doc, 1);
            p_num_docs = p_num_doc_records;
            
            p_diffs = zeros(p_num_doc_records, 1);
            p_our_records_id = zeros(p_num_doc_records, 1);
            p_hits_records_id = [];
            p_num_hits = 0;
            for i = 1:p_num_doc_records
                curr_diff = p_peak - p_peak_doc(i);
                [min_diff, min_diff_id] = min(abs(curr_diff));
                p_diffs(i) = min_diff;
                p_our_records_id(i) = min_diff_id;
                if(min_diff  / rate < tolerance)
                    p_num_hits = p_num_hits + 1;
                    p_hits_records_id = vertcat(p_hits_records_id, min_diff_id);
                end
            end
            
            p_ids{lead_id} = p_hits_records_id;
            
            if (p_num_hits > p_opt_num_hits)
                p_opt_num_hits = p_num_hits;
            end
            
            if(size(p_ids{lead_id}, 1) > 0)
                p_TP(lead_id) = p_TP(lead_id) + size(p_ids{lead_id}, 1);
                p_FN(lead_id) = p_FN(lead_id) + (p_num_docs - size(p_ids{lead_id}, 1));
                p_FP(lead_id) = p_FP(lead_id) + ((p_ids{lead_id}(end) - p_ids{lead_id}(1) + 1) - size(p_ids{lead_id}, 1));
            end
            
        end
        
        %################################# T ##################################
        
        file_name_t_del = sprintf('%s%s%st_delineation.txt', db_path, record_path, lead_path);
        t_del = importdata(file_name_t_del);
        
        t_peak = zeros(size(t_del, 1), 1);
        t_offset = zeros(size(t_del, 1), 1);
        
        for i = 1:size(t_del, 1)
            t_peak(i) = t_del(i, 2) + 1;
            t_offset(i) = t_del(i, 3) + 1;
        end
        
        t_peaks{lead_id} = t_peak;
        t_offsets{lead_id} = t_offset;
        
        file_name_t_del = sprintf('%s%s%st_doctor1_delineation.txt', db_path, record_path, lead_path);
        t_del_doc = importdata(file_name_t_del);
        
        if size(t_del_doc, 1) == 0
            is_t = 0;
        end
        
        if(is_t == 1)
            t_peak_doc = zeros(size(t_del_doc, 1), 1);
            t_offset_doc = zeros(size(t_del_doc, 1), 1);
            
            for i = 1:size(t_del_doc, 1)
                t_peak_doc(i) = t_del_doc(i, 1);
                t_offset_doc(i) = t_del_doc(i, 2);
            end
            
            t_num_doc_records = size(t_del_doc, 1);
            t_num_docs = t_num_doc_records;
            
            t_diffs = zeros(t_num_doc_records, 1);
            t_our_records_id = zeros(t_num_doc_records, 1);
            t_hits_records_id = [];
            t_num_hits = 0;
            for i = 1:t_num_doc_records
                curr_diff = t_peak - t_peak_doc(i);
                [min_diff, min_diff_id] = min(abs(curr_diff));
                t_diffs(i) = min_diff;
                t_our_records_id(i) = min_diff_id;
                if(min_diff  / rate < tolerance)
                    t_num_hits = t_num_hits + 1;
                    t_hits_records_id = vertcat(t_hits_records_id, min_diff_id);
                end
            end
            
            t_ids{lead_id} = t_hits_records_id;
            
            if (t_num_hits > t_opt_num_hits)
                t_opt_num_hits = t_num_hits;
            end
            
            if(size(t_ids{lead_id}, 1) > 0)
                t_TP(lead_id) = t_TP(lead_id) + size(t_ids{lead_id}, 1);
                t_FN(lead_id) = t_FN(lead_id) + (t_num_docs - size(t_ids{lead_id}, 1));
                t_FP(lead_id) = t_FP(lead_id) + ((t_ids{lead_id}(end) - t_ids{lead_id}(1) + 1) - size(t_ids{lead_id}, 1));
            end
            
        end
        
    end
    
    is_our_qrs = 1;
    for lead_id = 1:2
         if ~(is_qrs == 1 && size(qrs_ids{lead_id}, 1) > 0)
             is_our_qrs = 0;
         end
    end
    
    if is_qrs == 1 && is_our_qrs == 1
        
        qrs_rec_det = qrs_rec_det + 1;
        
        qrs_peak_diffs = [];
        for i = 1:qrs_num_docs
            
            abs_dist = 9999999999;
            dist = abs_dist;
            
            for lead_id = 1:2
                curr_ids = qrs_ids{lead_id};
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = qrs_peaks{lead_id}(curr_ids(point_id));
                end
                
                curr_diff = curr_points - qrs_peak_doc(i);
                [abs_min_diff, min_diff_id] = min(abs(curr_diff));
                min_diff = curr_diff(min_diff_id);
                
                if abs_min_diff < abs_dist
                    abs_dist = abs_min_diff;
                    dist = min_diff;
                end
            end
            
            if(abs_dist / rate < tolerance)
                qrs_peak_diffs = vertcat(qrs_peak_diffs, dist);
            end
        end
        qrs_peak_error_mean_avg = qrs_peak_error_mean_avg + mean(qrs_peak_diffs) / rate;
        qrs_peak_error_std_avg = qrs_peak_error_std_avg + std(qrs_peak_diffs) / rate;
        
        
        qrs_onset_diffs = [];
        for i = 1:qrs_num_docs
            
            abs_dist = 9999999999;
            dist = abs_dist;
            
            for lead_id = 1:2
                curr_ids = qrs_ids{lead_id};
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = qrs_onsets{lead_id}(curr_ids(point_id));
                end
                
                curr_diff = curr_points - qrs_onset_doc(i);
                [abs_min_diff, min_diff_id] = min(abs(curr_diff));
                min_diff = curr_diff(min_diff_id);
                
                if abs_min_diff < abs_dist
                    abs_dist = abs_min_diff;
                    dist = min_diff;
                end
            end
            
            if(abs_dist / rate < tolerance)
                qrs_onset_diffs = vertcat(qrs_onset_diffs, dist);
            end
        end
        
        qrs_onset_error_mean_avg = qrs_onset_error_mean_avg + mean(qrs_onset_diffs) / rate;
        qrs_onset_error_std_avg = qrs_onset_error_std_avg + std(qrs_onset_diffs) / rate;
        
        qrs_offset_diffs = [];
        for i = 1:qrs_num_docs
            
            abs_dist = 9999999999;
            dist = abs_dist;
            
            for lead_id = 1:2
                curr_ids = qrs_ids{lead_id};
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = qrs_offsets{lead_id}(curr_ids(point_id));
                end
                
                curr_diff = curr_points - qrs_offset_doc(i);
                [abs_min_diff, min_diff_id] = min(abs(curr_diff));
                min_diff = curr_diff(min_diff_id);
                
                if abs_min_diff < abs_dist
                    abs_dist = abs_min_diff;
                    dist = min_diff;
                end
            end
            
            if(abs_dist / rate < tolerance)
                qrs_offset_diffs = vertcat(qrs_offset_diffs, dist);
            end
        end
        
        qrs_offset_error_mean_avg = qrs_offset_error_mean_avg + mean(qrs_offset_diffs) / rate;
        qrs_offset_error_std_avg = qrs_offset_error_std_avg + std(qrs_offset_diffs) / rate;
        
    end
    
    
    is_our_p = 1;
    for lead_id = 1:2
         if ~(is_p == 1 && size(p_ids{lead_id}, 1) > 0)
             is_our_p = 0;
         end
    end
    
    if is_p == 1 && is_our_p == 1
        
        p_rec_det = p_rec_det + 1;
        
        p_peak_diffs = [];
        for i = 1:p_num_docs
            
            abs_dist = 9999999999;
            dist = abs_dist;
            
            for lead_id = 1:2
                curr_ids = p_ids{lead_id};
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = p_peaks{lead_id}(curr_ids(point_id));
                end
                
                curr_diff = curr_points - p_peak_doc(i);
                [abs_min_diff, min_diff_id] = min(abs(curr_diff));
                min_diff = curr_diff(min_diff_id);
                
                if abs_min_diff < abs_dist
                    abs_dist = abs_min_diff;
                    dist = min_diff;
                end
            end
            
            if(abs_dist / rate < tolerance)
                p_peak_diffs = vertcat(p_peak_diffs, dist);
            end
        end
        
        p_peak_error_mean_avg = p_peak_error_mean_avg + mean(p_peak_diffs) / rate;
        p_peak_error_std_avg = p_peak_error_std_avg + std(p_peak_diffs) / rate;
        
        p_onset_diffs = [];
        for i = 1:p_num_docs
            
            abs_dist = 9999999999;
            dist = abs_dist;
            
            for lead_id = 1:2
                curr_ids = p_ids{lead_id};
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = p_onsets{lead_id}(curr_ids(point_id));
                end
                
                curr_diff = curr_points - p_onset_doc(i);
                [abs_min_diff, min_diff_id] = min(abs(curr_diff));
                min_diff = curr_diff(min_diff_id);
                
                if abs_min_diff < abs_dist
                    abs_dist = abs_min_diff;
                    dist = min_diff;
                end
            end
            
            if(abs_dist / rate < tolerance)
                p_onset_diffs = vertcat(p_onset_diffs, dist);
            end
        end
        
        p_onset_error_mean_avg = p_onset_error_mean_avg + mean(p_onset_diffs) / rate;
        p_onset_error_std_avg = p_onset_error_std_avg + std(p_onset_diffs) / rate;
        
        p_offset_diffs = [];
        for i = 1:p_num_docs
            
            abs_dist = 9999999999;
            dist = abs_dist;
            
            for lead_id = 1:2
                curr_ids = p_ids{lead_id};
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = p_offsets{lead_id}(curr_ids(point_id));
                end
                
                curr_diff = curr_points - p_offset_doc(i);
                [abs_min_diff, min_diff_id] = min(abs(curr_diff));
                min_diff = curr_diff(min_diff_id);
                
                if abs_min_diff < abs_dist
                    abs_dist = abs_min_diff;
                    dist = min_diff;
                end
            end
            
            if(abs_dist / rate < tolerance)
                p_offset_diffs = vertcat(p_offset_diffs, dist);
            end
        end
        
        p_offset_error_mean_avg = p_offset_error_mean_avg + mean(p_offset_diffs) / rate;
        p_offset_error_std_avg = p_offset_error_std_avg + std(p_offset_diffs) / rate;
        
    end
    
    
    is_our_t = 1;
    for lead_id = 1:2
         if ~(is_t == 1 && size(t_ids{lead_id}, 1) > 0)
             is_our_t = 0;
         end
    end
    
    if is_t == 1 && is_our_t == 1
        
        t_rec_det = t_rec_det + 1;
        
        t_peak_diffs = [];
        for i = 1:t_num_docs
            
            abs_dist = 9999999999;
            dist = abs_dist;
            
            for lead_id = 1:2
                curr_ids = t_ids{lead_id};
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = t_peaks{lead_id}(curr_ids(point_id));
                end
                
                curr_diff = curr_points - t_peak_doc(i);
                [abs_min_diff, min_diff_id] = min(abs(curr_diff));
                min_diff = curr_diff(min_diff_id);
                
                if abs_min_diff < abs_dist
                    abs_dist = abs_min_diff;
                    dist = min_diff;
                end
            end
            
            if(abs_dist / rate < tolerance)
                t_peak_diffs = vertcat(t_peak_diffs, dist);
            end
        end
        t_peak_error_mean_avg = t_peak_error_mean_avg + mean(t_peak_diffs) / rate;
        t_peak_error_std_avg = t_peak_error_std_avg + std(t_peak_diffs) / rate;
        
        t_offset_diffs = [];
        for i = 1:t_num_docs
            
            abs_dist = 9999999999;
            dist = abs_dist;
            
            for lead_id = 1:2
                curr_ids = t_ids{lead_id};
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = t_offsets{lead_id}(curr_ids(point_id));
                end
                
                curr_diff = curr_points - t_offset_doc(i);
                [abs_min_diff, min_diff_id] = min(abs(curr_diff));
                min_diff = curr_diff(min_diff_id);
                
                if abs_min_diff < abs_dist
                    abs_dist = abs_min_diff;
                    dist = min_diff;
                end
            end
            
            if(abs_dist / rate < tolerance)
                t_offset_diffs = vertcat(t_offset_diffs, dist);
            end
        end
        
        t_offset_error_mean_avg = t_offset_error_mean_avg + mean(t_offset_diffs) / rate;
        t_offset_error_std_avg = t_offset_error_std_avg + std(t_offset_diffs) / rate;
    end
    
end


qrs_TP = qrs_TP
qrs_FN = qrs_FN
qrs_FP = qrs_FP
for lead_id = 1:num_leads
    qrs_Se(lead_id) = qrs_TP(lead_id) / (qrs_TP(lead_id) + qrs_FN(lead_id));
    qrs_PPV(lead_id) = qrs_TP(lead_id) / (qrs_TP(lead_id) + qrs_FP(lead_id));
end
qrs_Se = qrs_Se
qrs_PPV = qrs_PPV

p_TP = p_TP
p_FN = p_FN
p_FP = p_FP
for lead_id = 1:num_leads
    p_Se(lead_id) = p_TP(lead_id) / (p_TP(lead_id) + p_FN(lead_id));
    p_PPV(lead_id) = p_TP(lead_id) / (p_TP(lead_id) + p_FP(lead_id));
end
p_Se = p_Se
p_PPV = p_PPV

t_TP = t_TP
t_FN = t_FN
t_FP = t_FP
for lead_id = 1:num_leads
    t_Se(lead_id) = t_TP(lead_id) / (t_TP(lead_id) + t_FN(lead_id));
    t_PPV(lead_id) = t_TP(lead_id) / (t_TP(lead_id) + t_FP(lead_id));
end
t_Se = t_Se
t_PPV = t_PPV

qrs_peak_error_mean_avg = qrs_peak_error_mean_avg / qrs_rec_det
qrs_peak_error_std_avg = qrs_peak_error_std_avg / qrs_rec_det
qrs_onset_error_mean_avg = qrs_onset_error_mean_avg / qrs_rec_det
qrs_onset_error_std_avg = qrs_onset_error_std_avg / qrs_rec_det
qrs_offset_error_mean_avg = qrs_offset_error_mean_avg / qrs_rec_det
qrs_offset_error_std_avg = qrs_offset_error_std_avg / qrs_rec_det

p_peak_error_mean_avg = p_peak_error_mean_avg / p_rec_det
p_peak_error_std_avg = p_peak_error_std_avg / p_rec_det
p_onset_error_mean_avg = p_onset_error_mean_avg / p_rec_det
p_onset_error_std_avg = p_onset_error_std_avg / p_rec_det
p_offset_error_mean_avg = p_offset_error_mean_avg / p_rec_det
p_offset_error_std_avg = p_offset_error_std_avg / p_rec_det

t_peak_error_mean_avg = t_peak_error_mean_avg / t_rec_det
t_peak_error_std_avg = t_peak_error_std_avg / t_rec_det
t_offset_error_mean_avg = t_offset_error_mean_avg / t_rec_det
t_offset_error_std_avg = t_offset_error_std_avg / t_rec_det

t_Se = t_Se
t_Se = t_Se

