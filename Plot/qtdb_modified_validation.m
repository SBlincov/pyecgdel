clear all;

base_name = 'qtdb';
rate = 250.0;

leads = {'lead_ii', 'lead_v5'};

tolerance = 0.15;

num_leads = 2;
start_record = 1;
num_records = 105;

qrs_records_detected = num_records;
p_records_detected = num_records;
t_records_detected = num_records;

qrs_onset_TP = 0;
qrs_peak_TP = 0;
qrs_offset_TP = 0;

qrs_onset_FN = 0;
qrs_peak_FN = 0;
qrs_offset_FN = 0;

qrs_onset_FP = 0;
qrs_peak_FP = 0;
qrs_offset_FP = 0;

qrs_onset_Se = 0;
qrs_peak_Se = 0;
qrs_offset_Se = 0;

qrs_onset_PPV = 0;
qrs_peak_PPV = 0;
qrs_offset_PPV = 0;

p_onset_TP = 0;
p_peak_TP = 0;
p_offset_TP = 0;

p_onset_FN = 0;
p_peak_FN = 0;
p_offset_FN = 0;

p_onset_FP = 0;
p_peak_FP = 0;
p_offset_FP = 0;

p_onset_Se = 0;
p_peak_Se = 0;
p_offset_Se = 0;

p_onset_PPV = 0;
p_peak_PPV = 0;
p_offset_PPV = 0;

t_onset_TP = 0;
t_peak_TP = 0;
t_offset_TP = 0;

t_onset_FN = 0;
t_peak_FN = 0;
t_offset_FN = 0;

t_onset_FP = 0;
t_peak_FP = 0;
t_offset_FP = 0;

t_onset_Se = 0;
t_peak_Se = 0;
t_offset_Se = 0;

t_onset_PPV = 0;
t_peak_PPV = 0;
t_offset_PPV = 0;

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
    qrs_ids = {};
    qrs_onsets = {};
    qrs_peaks = {};
    qrs_offsets = {};
    
    p_num_docs = 0;
    p_ids = {};
    p_onsets = {};
    p_peaks = {};
    p_offsets = {};
    
    t_num_docs = 0;
    t_ids = {};
    t_peaks = {};
    t_offsets = {};
    
    is_qrs = 1;
    is_p = 1;
    is_t = 1;
    
    db_path = sprintf('../Data/%s/', base_name);
    record_path = sprintf('record_%d/', record);
    
    rr_mean = zeros(2, 1);
    
    %################################ QRS #################################
    
    for lead_id = 1:2
        
        lead = leads{lead_id};
        lead_path = sprintf('%s/', lead);
        
        file_name_qrs_del = sprintf('%s%s%sqrs_delineation.txt', db_path, record_path, lead_path);
        qrs_del = importdata(file_name_qrs_del);
        
        if size(qrs_del, 1) == 0
            is_qrs = 0;
        end
        
        qrs_onset = zeros(size(qrs_del, 1), 1);
        qrs_peak = zeros(size(qrs_del, 1), 1);
        qrs_offset = zeros(size(qrs_del, 1), 1);
        
        qrs_onset(1) = qrs_del(1, 1) + 1;
        qrs_peak(1) = qrs_del(1, 2) + 1;
        qrs_offset(1) = qrs_del(1, 3) + 1;
        
        for i = 2:size(qrs_del, 1)
            qrs_onset(i) = qrs_del(i, 1) + 1;
            qrs_peak(i) = qrs_del(i, 2) + 1;
            qrs_offset(i) = qrs_del(i, 3) + 1;
            rr_mean(lead_id) = rr_mean(lead_id) + (qrs_peak(i) - qrs_peak(i-1));
        end
        
        rr_mean(lead_id) = rr_mean(lead_id) / size(qrs_del, 1);
        
        qrs_onsets{lead_id} = qrs_onset;
        qrs_peaks{lead_id} = qrs_peak;
        qrs_offsets{lead_id} = qrs_offset;
        
    end
    
    file_name_qrs_del = sprintf('%s%s%sqrs_delineation_doc.txt', db_path, record_path, lead_path);
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
        
        for lead_id = 1:2
            peak_id = 1;
            while (qrs_peaks{1, lead_id}(peak_id) < qrs_peak_doc(1)) && (abs(qrs_peaks{1, lead_id}(peak_id)- qrs_peak_doc(1)) / rate > tolerance)
                qrs_onsets{1, lead_id}(peak_id) = [];
                qrs_peaks{1, lead_id}(peak_id) = [];
                qrs_offsets{1, lead_id}(peak_id) = [];
            end
        end
        
        for qrs_doc_id = 2:qrs_num_doc_records
            if (qrs_peak_doc(qrs_doc_id) - qrs_peak_doc(qrs_doc_id - 1)) > 1.5 * mean(rr_mean)
                for lead_id = 1:2
                    peak_id = 1;
                    while (qrs_peaks{1, lead_id}(peak_id) < qrs_peak_doc(qrs_doc_id - 1)) && (abs(qrs_peaks{1, lead_id}(peak_id)- qrs_peak_doc(qrs_doc_id - 1)) / rate > tolerance)
                        peak_id = peak_id + 1;
                    end
                    peak_id = peak_id + 1;
                    while ((peak_id <= size(qrs_peaks{1, lead_id}, 1) && qrs_peaks{1, lead_id}(peak_id) < qrs_peak_doc(qrs_doc_id)) && (abs(qrs_peaks{1, lead_id}(peak_id)- qrs_peak_doc(qrs_doc_id)) / rate > tolerance))
                        qrs_onsets{1, lead_id}(peak_id) = [];
                        qrs_peaks{1, lead_id}(peak_id) = [];
                        qrs_offsets{1, lead_id}(peak_id) = [];
                    end
                end
            end
        end
        
        for lead_id = 1:2
            peak_id_curr = peak_id;
            while (peak_id <= size(qrs_peaks{1, lead_id}, 1)) && (qrs_peaks{1, lead_id}(peak_id_curr) < qrs_peak_doc(end)) && (abs(qrs_peaks{1, lead_id}(peak_id_curr)- qrs_peak_doc(end)) / rate > tolerance)
                peak_id_curr = peak_id_curr + 1;
            end
            peak_id_curr = peak_id_curr + 1;
            while (size(qrs_peaks{1, lead_id}, 1) > peak_id_curr - 1) && (qrs_peaks{1, lead_id}(peak_id_curr) > qrs_peak_doc(end))
                qrs_onsets{1, lead_id}(peak_id_curr) = [];
                qrs_peaks{1, lead_id}(peak_id_curr) = [];
                qrs_offsets{1, lead_id}(peak_id_curr) = [];
            end
        end
        
        qrs_onset_diffs = {};
        qrs_peak_diffs = {};
        qrs_offset_diffs = {};
        
        qrs_onset_diffs_ids = {};
        qrs_peak_diffs_ids = {};
        qrs_offset_diffs_ids = {};
        
        for lead_id = 1:2
            qrs_onset_diffs_curr = zeros(size(qrs_onsets{1, lead_id}, 1), 1);
            qrs_peak_diffs_curr = zeros(size(qrs_peaks{1, lead_id}, 1), 1);
            qrs_offset_diffs_curr = zeros(size(qrs_offsets{1, lead_id}, 1), 1);
            
            qrs_onset_diffs_ids_curr = zeros(size(qrs_onsets{1, lead_id}, 1), 1);
            qrs_peak_diffs_ids_curr = zeros(size(qrs_peaks{1, lead_id}, 1), 1);
            qrs_offset_diffs_ids_curr = zeros(size(qrs_offsets{1, lead_id}, 1), 1);
            
            for i = 1:min([size(qrs_peaks{1, 1}, 1) size(qrs_peaks{1, 2}, 1) size(qrs_peak_doc, 1)])
                
                curr_onset_diff = qrs_onsets{1, lead_id} - qrs_onset_doc(i);
                curr_peak_diff = qrs_peaks{1, lead_id} - qrs_peak_doc(i);
                curr_offset_diff = qrs_offsets{1, lead_id} - qrs_offset_doc(i);
                
                [min_onset_diff, min_onset_diff_id] = min(abs(curr_onset_diff));
                [min_peak_diff, min_peak_diff_id] = min(abs(curr_peak_diff));
                [min_offset_diff, min_offset_diff_id] = min(abs(curr_offset_diff));
                
                qrs_onset_diffs_curr(i) = curr_onset_diff(min_onset_diff_id);
                qrs_peak_diffs_curr(i) = curr_peak_diff(min_peak_diff_id);
                qrs_offset_diffs_curr(i) = curr_offset_diff(min_offset_diff_id);
                
                qrs_onset_diffs_ids_curr(i) = min_onset_diff_id;
                qrs_peak_diffs_ids_curr(i) = min_peak_diff_id;
                qrs_offset_diffs_ids_curr(i) = min_offset_diff_id;
            end
            qrs_onset_diffs{lead_id} = qrs_onset_diffs_curr;
            qrs_peak_diffs{lead_id} = qrs_peak_diffs_curr;
            qrs_offset_diffs{lead_id} = qrs_offset_diffs_curr;
            
            qrs_onset_diffs_ids{lead_id} = qrs_onset_diffs_ids_curr;
            qrs_peak_diffs_ids{lead_id} = qrs_peak_diffs_ids_curr;
            qrs_offset_diffs_ids{lead_id} = qrs_offset_diffs_ids_curr;
        end
        
        qrs_onset_diffs_min = zeros(size(qrs_onsets{1, 1}, 1), 1);
        qrs_peak_diffs_min = zeros(size(qrs_peaks{1, 1}, 1), 1);
        qrs_offset_diffs_min = zeros(size(qrs_offsets{1, 1}, 1), 1);
        
        for i = 1:qrs_num_doc_records
            
            qrs_onset_diff_id_curr = find(qrs_onset_diffs_ids{1, 1} == i);
            if size(qrs_onset_diff_id_curr, 1) > 0
                qrs_onset_diffs_min_curr = 1000;
                for j = 1:size(qrs_onset_diff_id_curr, 1)
                    if abs(qrs_onset_diffs{1, 1}(qrs_onset_diff_id_curr(j))) < abs(qrs_onset_diffs_min_curr)
                        qrs_onset_diffs_min_curr = qrs_onset_diffs{1, 1}(qrs_onset_diff_id_curr(j));
                        qrs_onset_diff_id_min = qrs_onset_diff_id_curr(j);
                    end
                end
                qrs_onset_diffs_min(i) = qrs_onset_diffs_min_curr;
                
                qrs_onset_diff_id_lead_2 = find(qrs_onset_diffs_ids{1, 2} == i);
                if size(qrs_onset_diff_id_lead_2, 1) > 0
                    qrs_onset_diffs_min_curr = 1000;
                    for j = 1:size(qrs_onset_diff_id_lead_2, 1)
                        if abs(qrs_onset_diffs{1, 2}(qrs_onset_diff_id_lead_2(j))) < abs(qrs_onset_diffs_min_curr)
                            qrs_onset_diffs_min_curr = qrs_onset_diffs{1, 2}(qrs_onset_diff_id_lead_2(j));
                            qrs_onset_diff_id_min = qrs_onset_diff_id_lead_2(j);
                        end
                    end
                end
                if abs(qrs_onset_diffs_min_curr) < abs(qrs_onset_diffs_min(i))
                    qrs_onset_diffs_min(i) = qrs_onset_diffs_min_curr;
                end
            end
            
            qrs_peak_diff_id_curr = find(qrs_peak_diffs_ids{1, 1} == i);
            if size(qrs_peak_diff_id_curr, 1) > 0
                qrs_peak_diffs_min_curr = 1000;
                for j = 1:size(qrs_peak_diff_id_curr, 1)
                    if abs(qrs_peak_diffs{1, 1}(qrs_peak_diff_id_curr(j))) < abs(qrs_peak_diffs_min_curr)
                        qrs_peak_diffs_min_curr = qrs_peak_diffs{1, 1}(qrs_peak_diff_id_curr(j));
                        qrs_peak_diff_id_min = qrs_peak_diff_id_curr(j);
                    end
                end
                qrs_peak_diffs_min(i) = qrs_peak_diffs_min_curr;
                
                qrs_peak_diff_id_lead_2 = find(qrs_peak_diffs_ids{1, 2} == i);
                if size(qrs_peak_diff_id_lead_2, 1) > 0
                    qrs_peak_diffs_min_curr = 1000;
                    for j = 1:size(qrs_peak_diff_id_lead_2, 1)
                        if abs(qrs_peak_diffs{1, 2}(qrs_peak_diff_id_lead_2(j))) < abs(qrs_peak_diffs_min_curr)
                            qrs_peak_diffs_min_curr = qrs_peak_diffs{1, 2}(qrs_peak_diff_id_lead_2(j));
                            qrs_peak_diff_id_min = qrs_peak_diff_id_lead_2(j);
                        end
                    end
                end
                if abs(qrs_peak_diffs_min_curr) < abs(qrs_peak_diffs_min(i))
                    qrs_peak_diffs_min(i) = qrs_peak_diffs_min_curr;
                end
            end
            
            qrs_offset_diff_id_curr = find(qrs_offset_diffs_ids{1, 1} == i);
            if size(qrs_offset_diff_id_curr, 1) > 0
                qrs_offset_diffs_min_curr = 1000;
                for j = 1:size(qrs_offset_diff_id_curr, 1)
                    if abs(qrs_offset_diffs{1, 1}(qrs_offset_diff_id_curr(j))) < abs(qrs_offset_diffs_min_curr)
                        qrs_offset_diffs_min_curr = qrs_offset_diffs{1, 1}(qrs_offset_diff_id_curr(j));
                        qrs_offset_diff_id_min = qrs_offset_diff_id_curr(j);
                    end
                end
                qrs_offset_diffs_min(i) = qrs_offset_diffs_min_curr;
                
                qrs_offset_diff_id_lead_2 = find(qrs_offset_diffs_ids{1, 2} == i);
                if size(qrs_offset_diff_id_lead_2, 1) > 0
                    qrs_offset_diffs_min_curr = 1000;
                    for j = 1:size(qrs_offset_diff_id_lead_2, 1)
                        if abs(qrs_offset_diffs{1, 2}(qrs_offset_diff_id_lead_2(j))) < abs(qrs_offset_diffs_min_curr)
                            qrs_offset_diffs_min_curr = qrs_offset_diffs{1, 2}(qrs_offset_diff_id_lead_2(j));
                            qrs_offset_diff_id_min = qrs_offset_diff_id_lead_2(j);
                        end
                    end
                end
                if abs(qrs_offset_diffs_min_curr) < abs(qrs_offset_diffs_min(i))
                    qrs_offset_diffs_min(i) = qrs_offset_diffs_min_curr;
                end
            end
        end
        
        qrs_onset_num_hits = 0;
        qrs_peak_num_hits = 0;
        qrs_offset_num_hits = 0;
        
        qrs_onset_diffs_min_hits = zeros;
        qrs_peak_diffs_min_hits = zeros;
        qrs_offset_diffs_min_hits = zeros;
        
        qrs_onset_diffs_min_hits_count = 1;
        qrs_peak_diffs_min_hits_count = 1;
        qrs_offset_diffs_min_hits_count = 1;
        
        for i = 1:size(qrs_onset_diffs_min, 1)
            curr_min = qrs_onset_diffs_min(i);
            if curr_min / rate < tolerance
                qrs_onset_num_hits = qrs_onset_num_hits + 1;
                qrs_onset_diffs_min_hits(qrs_onset_diffs_min_hits_count) = curr_min;
                qrs_onset_diffs_min_hits_count = qrs_onset_diffs_min_hits_count + 1;
            end
        end
        for i = 1:size(qrs_peak_diffs_min, 1)
            curr_min = qrs_peak_diffs_min(i);
            if curr_min / rate < tolerance
                qrs_peak_num_hits = qrs_peak_num_hits + 1;
                qrs_peak_diffs_min_hits(qrs_peak_diffs_min_hits_count) = curr_min;
                qrs_peak_diffs_min_hits_count = qrs_peak_diffs_min_hits_count + 1;
            end
        end
        for i = 1:size(qrs_offset_diffs_min, 1)
            curr_min = qrs_offset_diffs_min(i);
            if curr_min / rate < tolerance
                qrs_offset_num_hits = qrs_offset_num_hits + 1;
                qrs_offset_diffs_min_hits(qrs_offset_diffs_min_hits_count) = curr_min;
                qrs_offset_diffs_min_hits_count = qrs_offset_diffs_min_hits_count + 1;
            end
        end
        
        qrs_onset_TP = qrs_onset_TP + qrs_onset_num_hits;
        qrs_peak_TP = qrs_peak_TP + qrs_peak_num_hits;
        qrs_offset_TP = qrs_offset_TP + qrs_offset_num_hits;
        
        qrs_onset_FN = qrs_onset_FN + abs(qrs_num_doc_records - qrs_onset_num_hits);
        qrs_peak_FN = qrs_peak_FN + abs(qrs_num_doc_records - qrs_peak_num_hits);
        qrs_offset_FN = qrs_offset_FN + abs(qrs_num_doc_records - qrs_offset_num_hits);
        
        qrs_onset_FP = qrs_onset_FP + (max(size(qrs_onsets{1, 1}, 1), size(qrs_onsets{1, 2}, 1)) - qrs_onset_num_hits);
        qrs_peak_FP = qrs_peak_FP + (max(size(qrs_peaks{1, 1}, 1), size(qrs_peaks{1, 2}, 1)) - qrs_peak_num_hits);
        qrs_offset_FP = qrs_offset_FP + (max(size(qrs_offsets{1, 1}, 1), size(qrs_offsets{1, 2}, 1)) - qrs_offset_num_hits);
    else
        qrs_records_detected = qrs_records_detected - 1;
    end
    
    %################################ P #################################
    
    for lead_id = 1:2
        
        lead = leads{lead_id};
        lead_path = sprintf('%s/', lead);
        
        file_name_p_del = sprintf('%s%s%sp_delineation.txt', db_path, record_path, lead_path);
        p_del = importdata(file_name_p_del);
        
        if size(p_del, 1) == 0
            is_p = 0;
        end
        
        p_onset = zeros(size(p_del, 1), 1);
        p_peak = zeros(size(p_del, 1), 1);
        p_offset = zeros(size(p_del, 1), 1);
        
        p_onset(1) = p_del(1, 1) + 1;
        p_peak(1) = p_del(1, 2) + 1;
        p_offset(1) = p_del(1, 3) + 1;
        
        for i = 2:size(p_del, 1)
            p_onset(i) = p_del(i, 1) + 1;
            p_peak(i) = p_del(i, 2) + 1;
            p_offset(i) = p_del(i, 3) + 1;
        end
        
        p_onsets{lead_id} = p_onset;
        p_peaks{lead_id} = p_peak;
        p_offsets{lead_id} = p_offset;
        
    end
    
    file_name_p_del = sprintf('%s%s%sp_delineation_doc.txt', db_path, record_path, lead_path);
    p_del_doc = importdata(file_name_p_del);
    
    if size(p_del_doc, 1) == 0
        is_p = 0;
    end
    
    if is_p == 1
        p_onset_doc = zeros(size(p_del_doc, 1), 1);
        p_peak_doc = zeros(size(p_del_doc, 1), 1);
        p_offset_doc = zeros(size(p_del_doc, 1), 1);
        
        for i = 1:size(p_del_doc, 1)
            p_onset_doc(i) = p_del_doc(i, 1);
            p_peak_doc(i) = p_del_doc(i, 2);
            p_offset_doc(i) = p_del_doc(i, 3);
        end
        
        p_num_doc_records = size(p_del_doc, 1);
        
        for lead_id = 1:2
            peak_id = 1;
            while (p_peaks{1, lead_id}(peak_id) < p_peak_doc(1)) && (abs(p_peaks{1, lead_id}(peak_id)- p_peak_doc(1)) / rate > tolerance)
                p_onsets{1, lead_id}(peak_id) = [];
                p_peaks{1, lead_id}(peak_id) = [];
                p_offsets{1, lead_id}(peak_id) = [];
            end
        end
        
        for p_doc_id = 2:p_num_doc_records
            if (p_peak_doc(p_doc_id) - p_peak_doc(p_doc_id - 1)) > 1.5 * mean(rr_mean)
                for lead_id = 1:2
                    peak_id = 1;
                    while (p_peaks{1, lead_id}(peak_id) < p_peak_doc(p_doc_id - 1)) && (abs(p_peaks{1, lead_id}(peak_id)- p_peak_doc(p_doc_id - 1)) / rate > tolerance)
                        peak_id = peak_id + 1;
                    end
                    peak_id = peak_id + 1;
                    while (peak_id <= size(p_peaks{1, lead_id}, 1)) && (p_peaks{1, lead_id}(peak_id) < p_peak_doc(p_doc_id)) && (abs(p_peaks{1, lead_id}(peak_id)- p_peak_doc(p_doc_id)) / rate > tolerance)
                        p_onsets{1, lead_id}(peak_id) = [];
                        p_peaks{1, lead_id}(peak_id) = [];
                        p_offsets{1, lead_id}(peak_id) = [];
                    end
                end
            end
        end
        
        for lead_id = 1:2
            peak_id_curr = peak_id;
            while (peak_id <= size(p_peaks{1, lead_id}, 1)) && (p_peaks{1, lead_id}(peak_id_curr) < p_peak_doc(end)) && (abs(p_peaks{1, lead_id}(peak_id_curr)- p_peak_doc(end)) / rate > tolerance)
                peak_id_curr = peak_id_curr + 1;
            end
            peak_id_curr = peak_id_curr + 1;
            while (size(p_peaks{1, lead_id}, 1) > peak_id_curr - 1) && (p_peaks{1, lead_id}(peak_id_curr) > p_peak_doc(end))
                p_onsets{1, lead_id}(peak_id_curr) = [];
                p_peaks{1, lead_id}(peak_id_curr) = [];
                p_offsets{1, lead_id}(peak_id_curr) = [];
            end
        end
        
        p_onset_diffs = {};
        p_peak_diffs = {};
        p_offset_diffs = {};
        
        p_onset_diffs_ids = {};
        p_peak_diffs_ids = {};
        p_offset_diffs_ids = {};
        
        for lead_id = 1:2
            
            p_onset_diffs_curr = zeros(size(p_onsets{1, lead_id}, 1), 1);
            p_peak_diffs_curr = zeros(size(p_peaks{1, lead_id}, 1), 1);
            p_offset_diffs_curr = zeros(size(p_offsets{1, lead_id}, 1), 1);
            
            p_onset_diffs_ids_curr = zeros(size(p_onsets{1, lead_id}, 1), 1);
            p_peak_diffs_ids_curr = zeros(size(p_peaks{1, lead_id}, 1), 1);
            p_offset_diffs_ids_curr = zeros(size(p_offsets{1, lead_id}, 1), 1);
            
            for i = 1:min([size(p_peaks{1, 1}, 1) size(p_peaks{1, 2}, 1) size(p_peak_doc, 1)])
                
                curr_onset_diff = p_onsets{1, lead_id} - p_onset_doc(i);
                curr_peak_diff = p_peaks{1, lead_id} - p_peak_doc(i);
                curr_offset_diff = p_offsets{1, lead_id} - p_offset_doc(i);
                
                [min_onset_diff, min_onset_diff_id] = min(abs(curr_onset_diff));
                [min_peak_diff, min_peak_diff_id] = min(abs(curr_peak_diff));
                [min_offset_diff, min_offset_diff_id] = min(abs(curr_offset_diff));
                
                p_onset_diffs_curr(i) = curr_onset_diff(min_onset_diff_id);
                p_peak_diffs_curr(i) = curr_peak_diff(min_peak_diff_id);
                p_offset_diffs_curr(i) = curr_offset_diff(min_offset_diff_id);
                
                p_onset_diffs_ids_curr(i) = min_onset_diff_id;
                p_peak_diffs_ids_curr(i) = min_peak_diff_id;
                p_offset_diffs_ids_curr(i) = min_offset_diff_id;
            end
            
            p_onset_diffs{lead_id} = p_onset_diffs_curr;
            p_peak_diffs{lead_id} = p_peak_diffs_curr;
            p_offset_diffs{lead_id} = p_offset_diffs_curr;
            
            p_onset_diffs_ids{lead_id} = p_onset_diffs_ids_curr;
            p_peak_diffs_ids{lead_id} = p_peak_diffs_ids_curr;
            p_offset_diffs_ids{lead_id} = p_offset_diffs_ids_curr;
        end
        
        p_onset_diffs_min = zeros(size(p_onsets{1, 1}, 1), 1);
        p_peak_diffs_min = zeros(size(p_peaks{1, 1}, 1), 1);
        p_offset_diffs_min = zeros(size(p_offsets{1, 1}, 1), 1);
        
        for i = 1:p_num_doc_records
            
            p_onset_diff_id_curr = find(p_onset_diffs_ids{1, 1} == i);
            if size(p_onset_diff_id_curr, 1) > 0
                p_onset_diffs_min_curr = 100;
                for j = 1:size(p_onset_diff_id_curr, 1)
                    if abs(p_onset_diffs{1, 1}(p_onset_diff_id_curr(j))) < abs(p_onset_diffs_min_curr)
                        p_onset_diffs_min_curr = p_onset_diffs{1, 1}(p_onset_diff_id_curr(j));
                        p_onset_diff_id_min = p_onset_diff_id_curr(j);
                    end
                end
                p_onset_diffs_min(i) = p_onset_diffs_min_curr;
                
                p_onset_diff_id_lead_2 = find(p_onset_diffs_ids{1, 2} == i);
                if size(p_onset_diff_id_lead_2, 1) > 0
                    p_onset_diffs_min_curr = 1000;
                    for j = 1:size(p_onset_diff_id_lead_2, 1)
                        if abs(p_onset_diffs{1, 2}(p_onset_diff_id_lead_2(j))) < abs(p_onset_diffs_min_curr)
                            p_onset_diffs_min_curr = p_onset_diffs{1, 2}(p_onset_diff_id_lead_2(j));
                            p_onset_diff_id_min = p_onset_diff_id_lead_2(j);
                        end
                    end
                end
                if abs(p_onset_diffs_min_curr) < abs(p_onset_diffs_min(i))
                    p_onset_diffs_min(i) = p_onset_diffs_min_curr;
                end
            end
            
            p_peak_diff_id_curr = find(p_peak_diffs_ids{1, 1} == i);
            if size(p_peak_diff_id_curr, 1) > 0
                p_peak_diffs_min_curr = 100;
                for j = 1:size(p_peak_diff_id_curr, 1)
                    if abs(p_peak_diffs{1, 1}(p_peak_diff_id_curr(j))) < abs(p_peak_diffs_min_curr)
                        p_peak_diffs_min_curr = p_peak_diffs{1, 1}(p_peak_diff_id_curr(j));
                        p_peak_diff_id_min = p_peak_diff_id_curr(j);
                    end
                end
                p_peak_diffs_min(i) = p_peak_diffs_min_curr;
                
                p_peak_diff_id_lead_2 = find(p_peak_diffs_ids{1, 2} == i);
                if size(p_peak_diff_id_lead_2, 1) > 0
                    p_peak_diffs_min_curr = 1000;
                    for j = 1:size(p_peak_diff_id_lead_2, 1)
                        if abs(p_peak_diffs{1, 2}(p_peak_diff_id_lead_2(j))) < abs(p_peak_diffs_min_curr)
                            p_peak_diffs_min_curr = p_peak_diffs{1, 2}(p_peak_diff_id_lead_2(j));
                            p_peak_diff_id_min = p_peak_diff_id_lead_2(j);
                        end
                    end
                end
                if abs(p_peak_diffs_min_curr) < abs(p_peak_diffs_min(i))
                    p_peak_diffs_min(i) = p_peak_diffs_min_curr;
                end
            end
            
            p_offset_diff_id_curr = find(p_offset_diffs_ids{1, 1} == i);
            if size(p_offset_diff_id_curr, 1) > 0
                p_offset_diffs_min_curr = 100;
                for j = 1:size(p_offset_diff_id_curr, 1)
                    if abs(p_offset_diffs{1, 1}(p_offset_diff_id_curr(j))) < abs(p_offset_diffs_min_curr)
                        p_offset_diffs_min_curr = p_offset_diffs{1, 1}(p_offset_diff_id_curr(j));
                        p_offset_diff_id_min = p_offset_diff_id_curr(j);
                    end
                end
                p_offset_diffs_min(i) = p_offset_diffs_min_curr;
                
                p_offset_diff_id_lead_2 = find(p_offset_diffs_ids{1, 2} == i);
                if size(p_offset_diff_id_lead_2, 1) > 0
                    p_offset_diffs_min_curr = 1000;
                    for j = 1:size(p_offset_diff_id_lead_2, 1)
                        if abs(p_offset_diffs{1, 2}(p_offset_diff_id_lead_2(j))) < abs(p_offset_diffs_min_curr)
                            p_offset_diffs_min_curr = p_offset_diffs{1, 2}(p_offset_diff_id_lead_2(j));
                            p_offset_diff_id_min = p_offset_diff_id_lead_2(j);
                        end
                    end
                end
                if abs(p_offset_diffs_min_curr) < abs(p_offset_diffs_min(i))
                    p_offset_diffs_min(i) = p_offset_diffs_min_curr;
                end
            end
        end
        
        p_onset_num_hits = 0;
        p_peak_num_hits = 0;
        p_offset_num_hits = 0;
        
        p_onset_diffs_min_hits = zeros;
        p_peak_diffs_min_hits = zeros;
        p_offset_diffs_min_hits = zeros;
        
        p_onset_diffs_min_hits_count = 1;
        p_peak_diffs_min_hits_count = 1;
        p_offset_diffs_min_hits_count = 1;
        
        for i = 1:size(p_onset_diffs_min, 1)
            curr_min = p_onset_diffs_min(i);
            if curr_min / rate < tolerance
                p_onset_num_hits = p_onset_num_hits + 1;
                p_onset_diffs_min_hits(p_onset_diffs_min_hits_count) = curr_min;
                p_onset_diffs_min_hits_count = p_onset_diffs_min_hits_count + 1;
            end
        end
        for i = 1:size(p_peak_diffs_min, 1)
            curr_min = p_peak_diffs_min(i);
            if curr_min / rate < tolerance
                p_peak_num_hits = p_peak_num_hits + 1;
                p_peak_diffs_min_hits(p_peak_diffs_min_hits_count) = curr_min;
                p_peak_diffs_min_hits_count = p_peak_diffs_min_hits_count + 1;
            end
        end
        for i = 1:size(p_offset_diffs_min, 1)
            curr_min = p_offset_diffs_min(i);
            if curr_min / rate < tolerance
                p_offset_num_hits = p_offset_num_hits + 1;
                p_offset_diffs_min_hits(p_offset_diffs_min_hits_count) = curr_min;
                p_offset_diffs_min_hits_count = p_offset_diffs_min_hits_count + 1;
            end
        end
        
        p_onset_TP = p_onset_TP + p_onset_num_hits;
        p_peak_TP = p_peak_TP + p_peak_num_hits;
        p_offset_TP = p_offset_TP + p_offset_num_hits;
        
        p_onset_FN = p_onset_FN + abs(p_num_doc_records - p_onset_num_hits);
        p_peak_FN = p_peak_FN + abs(p_num_doc_records - p_peak_num_hits);
        p_offset_FN = p_offset_FN + abs(p_num_doc_records - p_offset_num_hits);
        
        p_onset_FP = p_onset_FP + (max(size(p_onsets{1, 1}, 1), size(p_onsets{1, 2}, 1)) - p_onset_num_hits);
        p_peak_FP = p_peak_FP + (max(size(p_peaks{1, 1}, 1), size(p_peaks{1, 2}, 1)) - p_peak_num_hits);
        p_offset_FP = p_offset_FP + (max(size(p_offsets{1, 1}, 1), size(p_offsets{1, 2}, 1)) - p_offset_num_hits);
    else 
        p_records_detected = p_records_detected - 1;
    end
    
    %################################ T #################################
    
    for lead_id = 1:2
        
        lead = leads{lead_id};
        lead_path = sprintf('%s/', lead);
        
        file_name_t_del = sprintf('%s%s%st_delineation.txt', db_path, record_path, lead_path);
        t_del = importdata(file_name_t_del);
        
        if size(t_del, 1) == 0
            is_t = 0;
        end
        
        t_peak = zeros(size(t_del, 1), 1);
        t_offset = zeros(size(t_del, 1), 1);
        
        t_peak(1) = t_del(1, 2) + 1;
        t_offset(1) = t_del(1, 3) + 1;
        
        for i = 2:size(t_del, 1)
            t_peak(i) = t_del(i, 2) + 1;
            t_offset(i) = t_del(i, 3) + 1;
        end
        
        t_peaks{lead_id} = t_peak;
        t_offsets{lead_id} = t_offset;
        
    end
    
    file_name_t_del = sprintf('%s%s%st_delineation_doc.txt', db_path, record_path, lead_path);
    t_del_doc = importdata(file_name_t_del);
    
    if size(t_del_doc, 1) == 0
        is_t = 0;
    end
    
    if is_t == 1
        t_peak_doc = zeros(size(t_del_doc, 1), 1);
        t_offset_doc = zeros(size(t_del_doc, 1), 1);
        
        for i = 1:size(t_del_doc, 1)
            t_peak_doc(i) = t_del_doc(i, 1);
            t_offset_doc(i) = t_del_doc(i, 2);
        end
        
        t_num_doc_records = size(t_del_doc, 1);
        
        for lead_id = 1:2
            peak_id = 1;
            while (t_peaks{1, lead_id}(peak_id) < t_peak_doc(1)) && (abs(t_peaks{1, lead_id}(peak_id)- t_peak_doc(1)) / rate > tolerance)
                t_peaks{1, lead_id}(peak_id) = [];
                t_offsets{1, lead_id}(peak_id) = [];
            end
        end
        
        for t_doc_id = 2:t_num_doc_records
            if (t_peak_doc(t_doc_id) - t_peak_doc(t_doc_id - 1)) > 1.5 * mean(rr_mean)
                for lead_id = 1:2
                    peak_id = 1;
                    while (t_peaks{1, lead_id}(peak_id) < t_peak_doc(t_doc_id - 1)) && (abs(t_peaks{1, lead_id}(peak_id)- t_peak_doc(t_doc_id - 1)) / rate > tolerance)
                        peak_id = peak_id + 1;
                    end
                    peak_id = peak_id + 1;
                    while (peak_id <= size(t_peaks{1, lead_id}, 1)) && (t_peaks{1, lead_id}(peak_id) < t_peak_doc(t_doc_id)) && (abs(t_peaks{1, lead_id}(peak_id)- t_peak_doc(t_doc_id)) / rate > tolerance)
                        t_peaks{1, lead_id}(peak_id) = [];
                        t_offsets{1, lead_id}(peak_id) = [];
                    end
                end
            end
        end
        
        for lead_id = 1:2
            peak_id_curr = peak_id;
            while (peak_id <= size(t_peaks{1, lead_id}, 1)) && (t_peaks{1, lead_id}(peak_id_curr) < t_peak_doc(end)) && (abs(t_peaks{1, lead_id}(peak_id_curr)- t_peak_doc(end)) / rate > tolerance)
                peak_id_curr = peak_id_curr + 1;
            end
            peak_id_curr = peak_id_curr + 1;
            while (size(t_peaks{1, lead_id}, 1) > peak_id_curr - 1) && (t_peaks{1, lead_id}(peak_id_curr) > t_peak_doc(end))
                t_peaks{1, lead_id}(peak_id_curr) = [];
                t_offsets{1, lead_id}(peak_id_curr) = [];
            end
        end
        
        t_peak_diffs = {};
        t_offset_diffs = {};
        
        t_peak_diffs_ids = {};
        t_offset_diffs_ids = {};
        
        for lead_id = 1:2
            
            t_peak_diffs_curr = zeros(size(t_peaks{1, lead_id}, 1), 1);
            t_offset_diffs_curr = zeros(size(t_offsets{1, lead_id}, 1), 1);
            
            t_peak_diffs_ids_curr = zeros(size(t_peaks{1, lead_id}, 1), 1);
            t_offset_diffs_ids_curr = zeros(size(t_offsets{1, lead_id}, 1), 1);
            
            for i = 1:min([size(t_peaks{1, 1}, 1) size(t_peaks{1, 2}, 1) size(t_peak_doc, 1)])
                
                curr_peak_diff = t_peaks{1, lead_id} - t_peak_doc(i);
                curr_offset_diff = t_offsets{1, lead_id} - t_offset_doc(i);
                
                [min_peak_diff, min_peak_diff_id] = min(abs(curr_peak_diff));
                [min_offset_diff, min_offset_diff_id] = min(abs(curr_offset_diff));
                
                t_peak_diffs_curr(i) = curr_peak_diff(min_peak_diff_id);
                t_offset_diffs_curr(i) = curr_offset_diff(min_offset_diff_id);
                
                t_peak_diffs_ids_curr(i) = min_peak_diff_id;
                t_offset_diffs_ids_curr(i) = min_offset_diff_id;
            end
            
            t_peak_diffs{lead_id} = t_peak_diffs_curr;
            t_offset_diffs{lead_id} = t_offset_diffs_curr;
            
            t_peak_diffs_ids{lead_id} = t_peak_diffs_ids_curr;
            t_offset_diffs_ids{lead_id} = t_offset_diffs_ids_curr;
        end
        
        t_peak_diffs_min = zeros(size(t_peaks{1, 1}, 1), 1);
        t_offset_diffs_min = zeros(size(t_offsets{1, 1}, 1), 1);
        
        for i = 1:t_num_doc_records
            
            t_peak_diff_id_curr = find(t_peak_diffs_ids{1, 1} == i);
            if size(t_peak_diff_id_curr, 1) > 0
                t_peak_diffs_min_curr = 100;
                for j = 1:size(t_peak_diff_id_curr, 1)
                    if abs(t_peak_diffs{1, 1}(t_peak_diff_id_curr(j))) < abs(t_peak_diffs_min_curr)
                        t_peak_diffs_min_curr = t_peak_diffs{1, 1}(t_peak_diff_id_curr(j));
                        t_peak_diff_id_min = t_peak_diff_id_curr(j);
                    end
                end
                t_peak_diffs_min(i) = t_peak_diffs_min_curr;
                
                t_peak_diff_id_lead_2 = find(t_peak_diffs_ids{1, 2} == i);
                if size(t_peak_diff_id_lead_2, 1) > 0
                    t_peak_diffs_min_curr = 1000;
                    for j = 1:size(t_peak_diff_id_lead_2, 1)
                        if abs(t_peak_diffs{1, 2}(t_peak_diff_id_lead_2(j))) < abs(t_peak_diffs_min_curr)
                            t_peak_diffs_min_curr = t_peak_diffs{1, 2}(t_peak_diff_id_lead_2(j));
                            t_peak_diff_id_min = t_peak_diff_id_lead_2(j);
                        end
                    end
                end
                if abs(t_peak_diffs_min_curr) < abs(t_peak_diffs_min(i))
                    t_peak_diffs_min(i) = t_peak_diffs_min_curr;
                end
            end
            
            t_offset_diff_id_curr = find(t_offset_diffs_ids{1, 1} == i);
            if size(t_offset_diff_id_curr, 1) > 0
                t_offset_diffs_min_curr = 100;
                for j = 1:size(t_offset_diff_id_curr, 1)
                    if abs(t_offset_diffs{1, 1}(t_offset_diff_id_curr(j))) < abs(t_offset_diffs_min_curr)
                        t_offset_diffs_min_curr = t_offset_diffs{1, 1}(t_offset_diff_id_curr(j));
                        t_offset_diff_id_min = t_offset_diff_id_curr(j);
                    end
                end
                t_offset_diffs_min(i) = t_offset_diffs_min_curr;
                
                t_offset_diff_id_lead_2 = find(t_offset_diffs_ids{1, 2} == i);
                if size(t_offset_diff_id_lead_2, 1) > 0
                    t_offset_diffs_min_curr = 1000;
                    for j = 1:size(t_offset_diff_id_lead_2, 1)
                        if abs(t_offset_diffs{1, 2}(t_offset_diff_id_lead_2(j))) < abs(t_offset_diffs_min_curr)
                            t_offset_diffs_min_curr = t_offset_diffs{1, 2}(t_offset_diff_id_lead_2(j));
                            t_offset_diff_id_min = t_offset_diff_id_lead_2(j);
                        end
                    end
                end
                if abs(t_offset_diffs_min_curr) < abs(t_offset_diffs_min(i))
                    t_offset_diffs_min(i) = t_offset_diffs_min_curr;
                end
            end
        end
        
        t_peak_num_hits = 0;
        t_offset_num_hits = 0;

        t_peak_diffs_min_hits = zeros;
        t_offset_diffs_min_hits = zeros;

        t_peak_diffs_min_hits_count = 1;
        t_offset_diffs_min_hits_count = 1;
        
        for i = 1:size(t_peak_diffs_min, 1)
            curr_min = t_peak_diffs_min(i);
            if curr_min / rate < tolerance
                t_peak_num_hits = t_peak_num_hits + 1;
                t_peak_diffs_min_hits(t_peak_diffs_min_hits_count) = curr_min;
                t_peak_diffs_min_hits_count = t_peak_diffs_min_hits_count + 1;
            end
        end
        for i = 1:size(t_offset_diffs_min, 1)
            curr_min = t_offset_diffs_min(i);
            if curr_min / rate < tolerance
                t_offset_num_hits = t_offset_num_hits + 1;
                t_offset_diffs_min_hits(t_offset_diffs_min_hits_count) = curr_min;
                t_offset_diffs_min_hits_count = t_offset_diffs_min_hits_count + 1;
            end
        end
        
        t_peak_TP = t_peak_TP + t_peak_num_hits;
        t_offset_TP = t_offset_TP + t_offset_num_hits;
        
        t_peak_FN = t_peak_FN + abs(t_num_doc_records - t_peak_num_hits);
        t_offset_FN = t_offset_FN + abs(t_num_doc_records - t_offset_num_hits);
        
        t_peak_FP = t_peak_FP + (max(size(t_peaks{1, 1}, 1), size(t_peaks{1, 2}, 1)) - t_peak_num_hits);
        t_offset_FP = t_offset_FP + (max(size(t_offsets{1, 1}, 1), size(t_offsets{1, 2}, 1)) - t_offset_num_hits);
    else
        t_records_detected = t_records_detected - 1;
    end
    
    %################################ MEAN CALCULATING #################################
    
    qrs_onset_error_mean_avg = qrs_onset_error_mean_avg + mean(qrs_onset_diffs_min_hits) / rate;
    qrs_peak_error_mean_avg = qrs_peak_error_mean_avg + mean(qrs_peak_diffs_min_hits) / rate;
    qrs_offset_error_mean_avg = qrs_offset_error_mean_avg + mean(qrs_offset_diffs_min_hits) / rate;
    
    qrs_onset_error_std_avg = qrs_onset_error_std_avg + std(qrs_onset_diffs_min_hits) / rate;
    qrs_peak_error_std_avg = qrs_peak_error_std_avg + std(qrs_peak_diffs_min_hits) / rate;
    qrs_offset_error_std_avg = qrs_offset_error_std_avg + std(qrs_offset_diffs_min_hits) / rate;
    
    p_onset_error_mean_avg = p_onset_error_mean_avg + mean(p_onset_diffs_min_hits) / rate;
    p_peak_error_mean_avg = p_peak_error_mean_avg + mean(p_peak_diffs_min_hits) / rate;
    p_offset_error_mean_avg = p_offset_error_mean_avg + mean(p_offset_diffs_min_hits) / rate;
    
    p_onset_error_std_avg = p_onset_error_std_avg + std(p_onset_diffs_min_hits) / rate;
    p_peak_error_std_avg = p_peak_error_std_avg + std(p_peak_diffs_min_hits) / rate;
    p_offset_error_std_avg = p_offset_error_std_avg + std(p_offset_diffs_min_hits) / rate;

    t_peak_error_mean_avg = t_peak_error_mean_avg + mean(t_peak_diffs_min_hits) / rate;
    t_offset_error_mean_avg = t_offset_error_mean_avg + mean(t_offset_diffs_min_hits) / rate;

    t_peak_error_std_avg = t_peak_error_std_avg + std(t_peak_diffs_min_hits) / rate;
    t_offset_error_std_avg = t_offset_error_std_avg + std(t_offset_diffs_min_hits) / rate;
    
end

qrs_onset_Se = qrs_onset_TP / (qrs_onset_TP + qrs_onset_FN);
qrs_peak_Se = qrs_peak_TP / (qrs_peak_TP + qrs_peak_FN);
qrs_offset_Se = qrs_offset_TP / (qrs_offset_TP + qrs_offset_FN);

qrs_onset_PPV = qrs_onset_TP / (qrs_onset_TP + qrs_onset_FP);
qrs_peak_PPV = qrs_peak_TP / (qrs_peak_TP + qrs_peak_FP);
qrs_offset_PPV = qrs_offset_TP / (qrs_offset_TP + qrs_offset_FP);

qrs_onset_Se = qrs_onset_Se
qrs_peak_Se = qrs_peak_Se
qrs_offset_Se = qrs_offset_Se

qrs_onset_PPV = qrs_onset_PPV
qrs_peak_PPV = qrs_peak_PPV
qrs_offset_PPV = qrs_offset_PPV

p_onset_Se = p_onset_TP / (p_onset_TP + p_onset_FN);
p_peak_Se = p_peak_TP / (p_peak_TP + p_peak_FN);
p_offset_Se = p_offset_TP / (p_offset_TP + p_offset_FN);

p_onset_PPV = p_onset_TP / (p_onset_TP + p_onset_FP);
p_peak_PPV = p_peak_TP / (p_peak_TP + p_peak_FP);
p_offset_PPV = p_offset_TP / (p_offset_TP + p_offset_FP);

p_onset_Se = p_onset_Se
p_peak_Se = p_peak_Se
p_offset_Se = p_offset_Se

p_onset_PPV = p_onset_PPV
p_peak_PPV = p_peak_PPV
p_offset_PPV = p_offset_PPV

t_peak_Se = t_peak_TP / (t_peak_TP + t_peak_FN);
t_offset_Se = t_offset_TP / (t_offset_TP + t_offset_FN);

t_peak_PPV = t_peak_TP / (t_peak_TP + t_peak_FP);
t_offset_PPV = t_offset_TP / (t_offset_TP + t_offset_FP);

t_peak_Se = t_peak_Se
t_offset_Se = t_offset_Se

t_peak_PPV = t_peak_PPV
t_offset_PPV = t_offset_PPV

qrs_peak_error_mean_avg = qrs_peak_error_mean_avg / qrs_records_detected
qrs_peak_error_std_avg = qrs_peak_error_std_avg / qrs_records_detected
qrs_onset_error_mean_avg = qrs_onset_error_mean_avg / qrs_records_detected
qrs_onset_error_std_avg = qrs_onset_error_std_avg / qrs_records_detected
qrs_offset_error_mean_avg = qrs_offset_error_mean_avg / qrs_records_detected
qrs_offset_error_std_avg = qrs_offset_error_std_avg / qrs_records_detected

p_peak_error_mean_avg = p_peak_error_mean_avg / p_records_detected
p_peak_error_std_avg = p_peak_error_std_avg / p_records_detected
p_onset_error_mean_avg = p_onset_error_mean_avg / p_records_detected
p_onset_error_std_avg = p_onset_error_std_avg / p_records_detected
p_offset_error_mean_avg = p_offset_error_mean_avg / p_records_detected
p_offset_error_std_avg = p_offset_error_std_avg / p_records_detected

t_peak_error_mean_avg = t_peak_error_mean_avg / t_records_detected
t_peak_error_std_avg = t_peak_error_std_avg / t_records_detected
t_offset_error_mean_avg = t_offset_error_mean_avg / t_records_detected
t_offset_error_std_avg = t_offset_error_std_avg / t_records_detected