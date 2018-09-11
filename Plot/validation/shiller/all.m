clear all;

db_path = '../../../Data/shiller';

bd_name = 'shiller';
rate = 500.0;

tolerance = 0.15;

leads = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};
num_leads = size(leads, 2);

fn_dd = sprintf('%s/delineated_by_doc_ids.txt', db_path);
records_ids = importdata(fn_dd);
num_records = size(records_ids, 1);

qrs_num_docs = zeros(num_leads, 1);
qrs_TP = zeros(num_leads, 1);
qrs_FN = zeros(num_leads, 1);
qrs_FP = zeros(num_leads, 1);
qrs_Se = zeros(num_leads, 1);
qrs_PPV = zeros(num_leads, 1);
qrs_Se_all = zeros(num_records, num_leads);
qrs_PPV_all = zeros(num_records, num_leads);

p_num_docs = zeros(num_leads, 1);
p_TP = zeros(num_leads, 1);
p_FN = zeros(num_leads, 1);
p_FP = zeros(num_leads, 1);
p_Se = zeros(num_leads, 1);
p_PPV = zeros(num_leads, 1);
p_Se_all = zeros(num_records, num_leads);
p_PPV_all = zeros(num_records, num_leads);

t_num_docs = zeros(num_leads, 1);
t_TP = zeros(num_leads, 1);
t_FN = zeros(num_leads, 1);
t_FP = zeros(num_leads, 1);
t_Se = zeros(num_leads, 1);
t_PPV = zeros(num_leads, 1);
t_Se_all = zeros(num_records, num_leads);
t_PPV_all = zeros(num_records, num_leads);


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
t_onset_error_mean_avg = 0;
t_onset_error_std_avg = 0;
t_offset_error_mean_avg = 0;
t_offset_error_std_avg = 0;

for record_id = 1:num_records 
    
    record = records_ids(record_id)
    record_path = sprintf('record_%d', record);
    
    for lead_id = 1:num_leads
                
        lead = leads{lead_id};
        lead_path = sprintf('%s', lead);
        
        qrs_onsets = {};
        qrs_peaks = {};
        qrs_offsets = {};
        
        p_onsets = {};
        p_peaks = {};
        p_offsets = {};
        
        t_peaks = {};
        t_offsets = {};
        
        %################################ QRS #################################
        fn = sprintf('%s/%s/%s/qrs_delineation.txt', db_path, record_path, lead_path);
        qrs_del = importdata(fn);
        
        qrs_onset = zeros(size(qrs_del, 1), 1);
        qrs_peak = zeros(size(qrs_del, 1), 1);
        qrs_offset = zeros(size(qrs_del, 1), 1);
        
        for i = 1:size(qrs_del, 1)
            qrs_onset(i) = qrs_del(i, 1);
            qrs_peak(i) = qrs_del(i, 2);
            qrs_offset(i) = qrs_del(i, 3);
        end
        
        fn = sprintf('%s/%s/%s/qrs_delineation_doc.txt', db_path, record_path, lead_path);
        qrs_del_doc = importdata(fn);

        qrs_onset_doc = zeros(size(qrs_del_doc, 1), 1);
        qrs_onset_doc_remains = [];
        qrs_peak_doc = zeros(size(qrs_del_doc, 1), 1);
        qrs_peak_doc_remains = [];
        qrs_offset_doc = zeros(size(qrs_del_doc, 1), 1);
        qrs_offset_doc_remains = [];
        
        for i = 1:size(qrs_del_doc, 1)
            qrs_onset_doc(i) = qrs_del_doc(i, 1);
            qrs_peak_doc(i) = qrs_del_doc(i, 2);
            qrs_offset_doc(i) = qrs_del_doc(i, 3);
        end
        
        qrs_num_docs = size(qrs_del_doc, 1);
        
        if size(qrs_peak, 1) > 0 && qrs_num_docs > 0
            
            qrs_diffs = zeros(qrs_num_docs, 1);
            qrs_our_ids = [];
            qrs_num_hits = 0;
            for i = 1:qrs_num_docs
                curr_diff = qrs_peak - qrs_peak_doc(i);
                [min_diff, min_diff_id] = min(abs(curr_diff));
                qrs_diffs(i) = min_diff;
                if(min_diff  / rate < tolerance)
                    qrs_num_hits = qrs_num_hits + 1;
                    qrs_our_ids = vertcat(qrs_our_ids, min_diff_id);
                    
                    qrs_onset_doc_remains = vertcat(qrs_onset_doc_remains, qrs_onset_doc(i));
                    qrs_peak_doc_remains = vertcat(qrs_peak_doc_remains, qrs_peak_doc(i));
                    qrs_offset_doc_remains = vertcat(qrs_offset_doc_remains, qrs_offset_doc(i));
                end
            end
            
            if qrs_num_hits > 0
            
                curr_points = zeros(size(qrs_our_ids, 1), 1);
                for point_id = 1:size(qrs_our_ids, 1)
                    curr_points(point_id) = qrs_peak(qrs_our_ids(point_id));
                end
                curr_diff = curr_points - qrs_peak_doc_remains;
                qrs_peak_error_mean_avg = qrs_peak_error_mean_avg + mean(curr_diff) / rate;
                qrs_peak_error_std_avg = qrs_peak_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(qrs_our_ids, 1), 1);
                for point_id = 1:size(qrs_our_ids, 1)
                    curr_points(point_id) = qrs_onset(qrs_our_ids(point_id));
                end
                curr_diff = curr_points - qrs_onset_doc_remains;
                qrs_onset_error_mean_avg = qrs_onset_error_mean_avg + mean(curr_diff) / rate;
                qrs_onset_error_std_avg = qrs_onset_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(qrs_our_ids, 1), 1);
                for point_id = 1:size(qrs_our_ids, 1)
                    curr_points(point_id) = qrs_offset(qrs_our_ids(point_id));
                end
                curr_diff = curr_points - qrs_offset_doc_remains;
                qrs_offset_error_mean_avg = qrs_offset_error_mean_avg + mean(curr_diff) / rate;
                qrs_offset_error_std_avg = qrs_offset_error_std_avg + std(curr_diff) / rate;
            end
            
            curr_TP = size(qrs_our_ids, 1);
            qrs_TP(lead_id) = qrs_TP(lead_id) + curr_TP;
            
            curr_FN = max(0, (qrs_num_docs - size(qrs_our_ids, 1)));
            qrs_FN(lead_id) = qrs_FN(lead_id) + curr_FN;
            
            curr_FP = size(qrs_peak, 1) - size(qrs_our_ids, 1);
            qrs_FP(lead_id) = qrs_FP(lead_id) + curr_FP;
            
            qrs_Se_all(record_id, lead_id) = curr_TP / (curr_TP + curr_FN);
            qrs_PPV_all(record_id, lead_id) = curr_TP / (curr_TP + curr_FP);
            
        elseif qrs_num_docs == 0
            qrs_FP(lead_id) = qrs_FP(lead_id) + size(qrs_peak, 1);
            
            qrs_Se_all(record_id, lead_id) = 0.0;
            qrs_PPV_all(record_id, lead_id) = 0.0;
        else
            qrs_FN(lead_id) = qrs_FN(lead_id) + qrs_num_docs;
            
            qrs_Se_all(record_id, lead_id) = 0.0;
            qrs_PPV_all(record_id, lead_id) = 0.0;
        end
        
        %################################# P ##################################
        fn = sprintf('%s/%s/%s/p_delineation.txt', db_path, record_path, lead_path);
        p_del = importdata(fn);
        
        p_onset = zeros(size(p_del, 1), 1);
        p_peak = zeros(size(p_del, 1), 1);
        p_offset = zeros(size(p_del, 1), 1);
        
        for i = 1:size(p_del, 1)
            p_onset(i) = p_del(i, 1);
            p_peak(i) = p_del(i, 2);
            p_offset(i) = p_del(i, 3);
        end
        
        fn = sprintf('%s/%s/%s/p_delineation_doc.txt', db_path, record_path, lead_path);
        p_del_doc = importdata(fn);
        
        p_onset_doc = zeros(size(p_del_doc, 1), 1);
        p_onset_doc_remains = [];
        p_peak_doc = zeros(size(p_del_doc, 1), 1);
        p_peak_doc_remains = [];
        p_offset_doc = zeros(size(p_del_doc, 1), 1);
        p_offset_doc_remains = [];
        
        for i = 1:size(p_del_doc, 1)
            p_onset_doc(i) = p_del_doc(i, 1);
            p_peak_doc(i) = p_del_doc(i, 2);
            p_offset_doc(i) = p_del_doc(i, 3);
        end
        
        p_num_docs = size(p_del_doc, 1);
        
        if size(p_peak, 1) > 0 && p_num_docs > 0
            
            p_diffs = zeros(p_num_docs, 1);
            p_our_ids = [];
            p_num_hits = 0;
            for i = 1:p_num_docs
                curr_diff = p_peak - p_peak_doc(i);
                [min_diff, min_diff_id] = min(abs(curr_diff));
                p_diffs(i) = min_diff;
                if(min_diff  / rate < tolerance)
                    p_num_hits = p_num_hits + 1;
                    p_our_ids = vertcat(p_our_ids, min_diff_id);
                    
                    p_onset_doc_remains = vertcat(p_onset_doc_remains, p_onset_doc(i));
                    p_peak_doc_remains = vertcat(p_peak_doc_remains, p_peak_doc(i));
                    p_offset_doc_remains = vertcat(p_offset_doc_remains, p_offset_doc(i));
                end
            end
            
            if p_num_hits > 0
                
                curr_points = zeros(size(p_our_ids, 1), 1);
                for point_id = 1:size(p_our_ids, 1)
                    curr_points(point_id) = p_peak(p_our_ids(point_id));
                end
                curr_diff = curr_points - p_peak_doc_remains;
                p_peak_error_mean_avg = p_peak_error_mean_avg + mean(curr_diff) / rate;
                p_peak_error_std_avg = p_peak_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(p_our_ids, 1), 1);
                for point_id = 1:size(p_our_ids, 1)
                    curr_points(point_id) = p_onset(p_our_ids(point_id));
                end
                curr_diff = curr_points - p_onset_doc_remains;
                p_onset_error_mean_avg = p_onset_error_mean_avg + mean(curr_diff) / rate;
                p_onset_error_std_avg = p_onset_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(p_our_ids, 1), 1);
                for point_id = 1:size(p_our_ids, 1)
                    curr_points(point_id) = p_offset(p_our_ids(point_id));
                end
                curr_diff = curr_points - p_offset_doc_remains;
                p_offset_error_mean_avg = p_offset_error_mean_avg + mean(curr_diff) / rate;
                p_offset_error_std_avg = p_offset_error_std_avg + std(curr_diff) / rate;
                
            end
            
            curr_TP = size(p_our_ids, 1);
            p_TP(lead_id) = p_TP(lead_id) + curr_TP;
            
            curr_FN = max(0, (p_num_docs - size(p_our_ids, 1)));
            p_FN(lead_id) = p_FN(lead_id) + curr_FN;
            
            curr_FP = size(p_peak, 1) - size(p_our_ids, 1);
            p_FP(lead_id) = p_FP(lead_id) + curr_FP;
            
            p_Se_all(record_id, lead_id) = curr_TP / (curr_TP + curr_FN);
            p_PPV_all(record_id, lead_id) = curr_TP / (curr_TP + curr_FP);
            
        elseif p_num_docs == 0
            p_FP(lead_id) = p_FP(lead_id) + size(p_peak, 1);
            
            p_Se_all(record_id, lead_id) = 0.0;
            p_PPV_all(record_id, lead_id) = 0.0;
        else
            p_FN(lead_id) = p_FN(lead_id) + p_num_docs;
            
            p_Se_all(record_id, lead_id) = 0.0;
            p_PPV_all(record_id, lead_id) = 0.0;
        end
        
        %################################# T ##################################
        
        fn = sprintf('%s/%s/%s/t_delineation.txt', db_path, record_path, lead_path);
        t_del = importdata(fn);
        
        t_onset = zeros(size(t_del, 1), 1);
        t_peak = zeros(size(t_del, 1), 1);
        t_offset = zeros(size(t_del, 1), 1);
        
        for i = 1:size(t_del, 1)
            t_onset(i) = t_del(i, 1);
            t_peak(i) = t_del(i, 2);
            t_offset(i) = t_del(i, 3);
        end
        
        fn = sprintf('%s/%s/%s/t_delineation_doc.txt', db_path, record_path, lead_path);
        t_del_doc = importdata(fn);
        
        t_onset_doc = zeros(size(t_del_doc, 1), 1);
        t_onset_doc_remains = [];
        t_peak_doc = zeros(size(t_del_doc, 1), 1);
        t_peak_doc_remains = [];
        t_offset_doc = zeros(size(t_del_doc, 1), 1);
        t_offset_doc_remains = [];
        
        for i = 1:size(t_del_doc, 1)
            t_onset_doc(i) = t_del_doc(i, 1);
            t_peak_doc(i) = t_del_doc(i, 2);
            t_offset_doc(i) = t_del_doc(i, 3);
        end
        
        t_num_docs = size(t_del_doc, 1);
        
        if size(t_peak, 1) > 0 && t_num_docs > 0
            
            t_diffs = zeros(t_num_docs, 1);
            t_our_ids = [];
            t_num_hits = 0;
            for i = 1:t_num_docs
                curr_diff = t_peak - t_peak_doc(i);
                [min_diff, min_diff_id] = min(abs(curr_diff));
                t_diffs(i) = min_diff;
                if(min_diff  / rate < tolerance)
                    t_num_hits = t_num_hits + 1;
                    t_our_ids = vertcat(t_our_ids, min_diff_id);
                    
                    t_onset_doc_remains = vertcat(t_onset_doc_remains, t_onset_doc(i));
                    t_peak_doc_remains = vertcat(t_peak_doc_remains, t_peak_doc(i));
                    t_offset_doc_remains = vertcat(t_offset_doc_remains, t_offset_doc(i));
                end
            end
            
            if t_num_hits > 0
                
                curr_points = zeros(size(t_our_ids, 1), 1);
                for point_id = 1:size(t_our_ids, 1)
                    curr_points(point_id) = t_peak(t_our_ids(point_id));
                end
                curr_diff = curr_points - t_peak_doc_remains;
                t_peak_error_mean_avg = t_peak_error_mean_avg + mean(curr_diff) / rate;
                t_peak_error_std_avg = t_peak_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(t_our_ids, 1), 1);
                for point_id = 1:size(t_our_ids, 1)
                    curr_points(point_id) = t_onset(t_our_ids(point_id));
                end
                curr_diff = curr_points - t_onset_doc_remains;
                t_onset_error_mean_avg = t_onset_error_mean_avg + mean(curr_diff) / rate;
                t_onset_error_std_avg = t_onset_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(t_our_ids, 1), 1);
                for point_id = 1:size(t_our_ids, 1)
                    curr_points(point_id) = t_offset(t_our_ids(point_id));
                end
                curr_diff = curr_points - t_offset_doc_remains;
                t_offset_error_mean_avg = t_offset_error_mean_avg + mean(curr_diff) / rate;
                t_offset_error_std_avg = t_offset_error_std_avg + std(curr_diff) / rate;
                
            end
            
            curr_TP = size(t_our_ids, 1);
            t_TP(lead_id) = t_TP(lead_id) + curr_TP;
            
            curr_FN = max(0, (t_num_docs - size(t_our_ids, 1)));
            t_FN(lead_id) = t_FN(lead_id) + curr_FN;
            
            curr_FP = size(t_peak, 1) - size(t_our_ids, 1);
            t_FP(lead_id) = t_FP(lead_id) + curr_FP;
            
            t_Se_all(record_id, lead_id) = curr_TP / (curr_TP + curr_FN);
            t_PPV_all(record_id, lead_id) = curr_TP / (curr_TP + curr_FP);
            
        elseif t_num_docs == 0
            t_FP(lead_id) = t_FP(lead_id) + size(t_peak, 1);
            
            t_Se_all(record_id, lead_id) = 0.0;
            t_PPV_all(record_id, lead_id) = 0.0;
        else
            t_FN(lead_id) = t_FN(lead_id) + t_num_docs;
            
            t_Se_all(record_id, lead_id) = 0.0;
            t_PPV_all(record_id, lead_id) = 0.0;
        end
    end
end


qrs_TP = qrs_TP;
qrs_FN = qrs_FN;
qrs_FP = qrs_FP;
for lead_id = 1:num_leads
    qrs_Se(lead_id) = qrs_TP(lead_id) / (qrs_TP(lead_id) + qrs_FN(lead_id));
    qrs_PPV(lead_id) = qrs_TP(lead_id) / (qrs_TP(lead_id) + qrs_FP(lead_id));
end

qrs_Se_mean = mean(qrs_Se)
qrs_PPV_mean = mean(qrs_PPV)

p_TP = p_TP;
p_FN = p_FN;
p_FP = p_FP;
for lead_id = 1:num_leads
    p_Se(lead_id) = p_TP(lead_id) / (p_TP(lead_id) + p_FN(lead_id));
    p_PPV(lead_id) = p_TP(lead_id) / (p_TP(lead_id) + p_FP(lead_id));
end

p_Se_mean = mean(p_Se)
p_PPV_mean = mean(p_PPV)

t_TP = t_TP;
t_FN = t_FN;
t_FP = t_FP;
for lead_id = 1:num_leads
    t_Se(lead_id) = t_TP(lead_id) / (t_TP(lead_id) + t_FN(lead_id));
    t_PPV(lead_id) = t_TP(lead_id) / (t_TP(lead_id) + t_FP(lead_id));
end


t_Se_mean = mean(t_Se)
t_PPV_mean = mean(t_PPV)

qrs_peak_error_mean_avg = qrs_peak_error_mean_avg / (num_leads * num_records)
qrs_peak_error_std_avg = qrs_peak_error_std_avg / (num_leads * num_records)
qrs_onset_error_mean_avg = qrs_onset_error_mean_avg / (num_leads * num_records)
qrs_onset_error_std_avg = qrs_onset_error_std_avg / (num_leads * num_records)
qrs_offset_error_mean_avg = qrs_offset_error_mean_avg / (num_leads * num_records)
qrs_offset_error_std_avg = qrs_offset_error_std_avg / (num_leads * num_records)

p_peak_error_mean_avg = p_peak_error_mean_avg / (num_leads * num_records)
p_peak_error_std_avg = p_peak_error_std_avg / (num_leads * num_records)
p_onset_error_mean_avg = p_onset_error_mean_avg / (num_leads * num_records)
p_onset_error_std_avg = p_onset_error_std_avg / (num_leads * num_records)
p_offset_error_mean_avg = p_offset_error_mean_avg / (num_leads * num_records)
p_offset_error_std_avg = p_offset_error_std_avg / (num_leads * num_records)

t_peak_error_mean_avg = t_peak_error_mean_avg / (num_leads * num_records)
t_peak_error_std_avg = t_peak_error_std_avg / (num_leads * num_records)
t_offset_error_mean_avg = t_offset_error_mean_avg / (num_leads * num_records)
t_offset_error_std_avg = t_offset_error_std_avg / (num_leads * num_records)

