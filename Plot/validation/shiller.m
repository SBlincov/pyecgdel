clear all;

db_path = '../../Data/shiller';

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

p_num_docs = zeros(num_leads, 1);
p_TP = zeros(num_leads, 1);
p_FN = zeros(num_leads, 1);
p_FP = zeros(num_leads, 1);
p_Se = zeros(num_leads, 1);
p_PPV = zeros(num_leads, 1);

t_num_docs = zeros(num_leads, 1);
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

for id = 1:num_records 
    
    record = records_ids(id)
    record_path = sprintf('record_%d', record);
    
    for lead_id = 1:num_leads
                
        lead = leads{lead_id};
        lead_path = sprintf('%s', lead);
        
        qrs_ids = {};
        qrs_onsets = {};
        qrs_peaks = {};
        qrs_offsets = {};
        
        p_ids = {};
        p_onsets = {};
        p_peaks = {};
        p_offsets = {};
        
        t_ids = {};
        t_peaks = {};
        t_offsets = {};
        
        %################################ QRS #################################
        file_name_qrs_del = sprintf('%s/%s/%s/qrs_delineation.txt', db_path, record_path, lead_path);
        qrs_del = importdata(file_name_qrs_del);
        
        qrs_onset = zeros(size(qrs_del, 1), 1);
        qrs_peak = zeros(size(qrs_del, 1), 1);
        qrs_offset = zeros(size(qrs_del, 1), 1);
        
        for i = 1:size(qrs_del, 1)
            qrs_onset(i) = qrs_del(i, 1);
            qrs_peak(i) = qrs_del(i, 2);
            qrs_offset(i) = qrs_del(i, 3);
        end
        
        qrs_onsets{lead_id} = qrs_onset;
        qrs_peaks{lead_id} = qrs_peak;
        qrs_offsets{lead_id} = qrs_offset;
        
        file_name_qrs_del = sprintf('%s/%s/%s/qrs_delineation_doc.txt', db_path, record_path, lead_path);
        qrs_del_doc = importdata(file_name_qrs_del);

        qrs_onset_doc = zeros(size(qrs_del_doc, 1), 1);
        qrs_onset_doc_rem = [];
        qrs_peak_doc = zeros(size(qrs_del_doc, 1), 1);
        qrs_peak_doc_rem = [];
        qrs_offset_doc = zeros(size(qrs_del_doc, 1), 1);
        qrs_offset_doc_rem = [];
        
        for i = 1:size(qrs_del_doc, 1)
            qrs_onset_doc(i) = qrs_del_doc(i, 1);
            qrs_peak_doc(i) = qrs_del_doc(i, 2);
            qrs_offset_doc(i) = qrs_del_doc(i, 3);
        end
        
        qrs_num_doc_records = size(qrs_del_doc, 1);
        qrs_num_docs = qrs_num_doc_records;
        
        if size(qrs_peak, 1) > 0 && qrs_num_docs > 0
            
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
                    
                    qrs_onset_doc_rem = vertcat(qrs_onset_doc_rem, qrs_onset_doc(i));
                    qrs_peak_doc_rem = vertcat(qrs_peak_doc_rem, qrs_peak_doc(i));
                    qrs_offset_doc_rem = vertcat(qrs_offset_doc_rem, qrs_offset_doc(i));
                end
            end
            
            qrs_ids{lead_id} = qrs_hits_records_id;
            
            curr_ids = qrs_ids{lead_id};
            
            if qrs_num_hits > 0
            
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = qrs_peaks{lead_id}(curr_ids(point_id));
                end
                curr_diff = curr_points - qrs_peak_doc_rem;
                qrs_peak_error_mean_avg = qrs_peak_error_mean_avg + mean(curr_diff) / rate;
                qrs_peak_error_std_avg = qrs_peak_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = qrs_onsets{lead_id}(curr_ids(point_id));
                end
                curr_diff = curr_points - qrs_onset_doc_rem;
                qrs_onset_error_mean_avg = qrs_onset_error_mean_avg + mean(curr_diff) / rate;
                qrs_onset_error_std_avg = qrs_onset_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = qrs_offsets{lead_id}(curr_ids(point_id));
                end
                curr_diff = curr_points - qrs_offset_doc_rem;
                qrs_offset_error_mean_avg = qrs_offset_error_mean_avg + mean(curr_diff) / rate;
                qrs_offset_error_std_avg = qrs_offset_error_std_avg + std(curr_diff) / rate;
                
            end
            
            if(size(qrs_ids{lead_id}, 1) > 0)
                
                curr_TP = size(qrs_ids{lead_id}, 1);
                qrs_TP(lead_id) = qrs_TP(lead_id) + curr_TP;
                
                curr_FN = max(0, (qrs_num_docs - size(qrs_ids{lead_id}, 1)));
                qrs_FN(lead_id) = qrs_FN(lead_id) + curr_FN;
                
                curr_FP = ((qrs_ids{lead_id}(end) - qrs_ids{lead_id}(1) + 1) - size(qrs_ids{lead_id}, 1));
                qrs_FP(lead_id) = qrs_FP(lead_id) + curr_FP;
            end
            
        elseif qrs_num_docs == 0
            qrs_FP(lead_id) = qrs_FP(lead_id) + size(qrs_peak, 1);
        else
            qrs_FN(lead_id) = qrs_FN(lead_id) + qrs_num_docs;
        end
        
        %################################# P ##################################
        file_name_p_del = sprintf('%s/%s/%s/p_delineation.txt', db_path, record_path, lead_path);
        p_del = importdata(file_name_p_del);
        
        p_onset = zeros(size(p_del, 1), 1);
        p_peak = zeros(size(p_del, 1), 1);
        p_offset = zeros(size(p_del, 1), 1);
        
        for i = 1:size(p_del, 1)
            p_onset(i) = p_del(i, 1);
            p_peak(i) = p_del(i, 2);
            p_offset(i) = p_del(i, 3);
        end
        
        p_onsets{lead_id} = p_onset;
        p_peaks{lead_id} = p_peak;
        p_offsets{lead_id} = p_offset;
        
        file_name_p_del = sprintf('%s/%s/%s/p_delineation_doc.txt', db_path, record_path, lead_path);
        p_del_doc = importdata(file_name_p_del);
        
        
        p_onset_doc = zeros(size(p_del_doc, 1), 1);
        p_onset_doc_rem = [];
        p_peak_doc = zeros(size(p_del_doc, 1), 1);
        p_peak_doc_rem = [];
        p_offset_doc = zeros(size(p_del_doc, 1), 1);
        p_offset_doc_rem = [];
        
        for i = 1:size(p_del_doc, 1)
            p_onset_doc(i) = p_del_doc(i, 1);
            p_peak_doc(i) = p_del_doc(i, 2);
            p_offset_doc(i) = p_del_doc(i, 3);
        end
        
        p_num_doc_records = size(p_del_doc, 1);
        p_num_docs = p_num_doc_records;
        
        if size(p_peak, 1) > 0 && p_num_docs > 0
            
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
                    
                    p_onset_doc_rem = vertcat(p_onset_doc_rem, p_onset_doc(i));
                    p_peak_doc_rem = vertcat(p_peak_doc_rem, p_peak_doc(i));
                    p_offset_doc_rem = vertcat(p_offset_doc_rem, p_offset_doc(i));
                end
            end
            
            p_ids{lead_id} = p_hits_records_id;
            
            curr_ids = p_ids{lead_id};
            
            if p_num_hits > 0
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = p_peaks{lead_id}(curr_ids(point_id));
                end
                curr_diff = curr_points - p_peak_doc_rem;
                p_peak_error_mean_avg = p_peak_error_mean_avg + mean(curr_diff) / rate;
                p_peak_error_std_avg = p_peak_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = p_onsets{lead_id}(curr_ids(point_id));
                end
                curr_diff = curr_points - p_onset_doc_rem;
                p_onset_error_mean_avg = p_onset_error_mean_avg + mean(curr_diff) / rate;
                p_onset_error_std_avg = p_onset_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = p_offsets{lead_id}(curr_ids(point_id));
                end
                curr_diff = curr_points - p_offset_doc_rem;
                p_offset_error_mean_avg = p_offset_error_mean_avg + mean(curr_diff) / rate;
                p_offset_error_std_avg = p_offset_error_std_avg + std(curr_diff) / rate;
                
            end
            
            if(size(p_ids{lead_id}, 1) > 0)
                
                curr_TP = size(p_ids{lead_id}, 1);
                p_TP(lead_id) = p_TP(lead_id) + curr_TP;
                
                curr_FN = max(0, (p_num_docs - size(p_ids{lead_id}, 1)));
                p_FN(lead_id) = p_FN(lead_id) + curr_FN;
                
                curr_FP = ((p_ids{lead_id}(end) - p_ids{lead_id}(1) + 1) - size(p_ids{lead_id}, 1));
                p_FP(lead_id) = p_FP(lead_id) + curr_FP;
            end
        elseif p_num_docs == 0
            p_FP(lead_id) = p_FP(lead_id) + size(p_peak, 1);
        else
            p_FN(lead_id) = p_FN(lead_id) + p_num_docs;
        end
        
        %################################# T ##################################
        
        file_name_t_del = sprintf('%s/%s/%s/t_delineation.txt', db_path, record_path, lead_path);
        t_del = importdata(file_name_t_del);
        
        t_peak = zeros(size(t_del, 1), 1);
        t_offset = zeros(size(t_del, 1), 1);
        
        for i = 1:size(t_del, 1)
            t_peak(i) = t_del(i, 2);
            t_offset(i) = t_del(i, 3);
        end
        
        t_peaks{lead_id} = t_peak;
        t_offsets{lead_id} = t_offset;
        
        file_name_t_del = sprintf('%s/%s/%s/t_delineation_doc.txt', db_path, record_path, lead_path);
        t_del_doc = importdata(file_name_t_del);
        
        t_peak_doc = zeros(size(t_del_doc, 1), 1);
        t_peak_doc_rem = [];
        t_offset_doc = zeros(size(t_del_doc, 1), 1);
        t_offset_doc_rem = [];
        
        for i = 1:size(t_del_doc, 1)
            t_peak_doc(i) = t_del_doc(i, 2);
            t_offset_doc(i) = t_del_doc(i, 3);
        end
        
        t_num_doc_records = size(t_del_doc, 1);
        t_num_docs = t_num_doc_records;
        
        if size(p_peak, 1) > 0 && t_num_docs > 0
            
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
                    
                    t_peak_doc_rem = vertcat(t_peak_doc_rem, t_peak_doc(i));
                    t_offset_doc_rem = vertcat(t_offset_doc_rem, t_offset_doc(i));
                end
            end
            
            t_ids{lead_id} = t_hits_records_id;
            
            curr_ids = t_ids{lead_id};
            
            if t_num_hits > 0
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = t_peaks{lead_id}(curr_ids(point_id));
                end
                curr_diff = curr_points - t_peak_doc_rem;
                t_peak_error_mean_avg = t_peak_error_mean_avg + mean(curr_diff) / rate;
                t_peak_error_std_avg = t_peak_error_std_avg + std(curr_diff) / rate;
                
                curr_points = zeros(size(curr_ids, 1), 1);
                for point_id = 1:size(curr_ids, 1)
                    curr_points(point_id) = t_offsets{lead_id}(curr_ids(point_id));
                end
                curr_diff = curr_points - t_offset_doc_rem;
                t_offset_error_mean_avg = t_offset_error_mean_avg + mean(curr_diff) / rate;
                t_offset_error_std_avg = t_offset_error_std_avg + std(curr_diff) / rate;
                
            end
            
            if(size(t_ids{lead_id}, 1) > 0)
                
                
                curr_TP = size(t_ids{lead_id}, 1);
                t_TP(lead_id) = t_TP(lead_id) + curr_TP;
                
                curr_FN = max(0, (t_num_docs - size(t_ids{lead_id}, 1)));
                t_FN(lead_id) = t_FN(lead_id) + curr_FN;
                
                curr_FP = ((t_ids{lead_id}(end) - t_ids{lead_id}(1) + 1) - size(t_ids{lead_id}, 1));
                t_FP(lead_id) = t_FP(lead_id) + curr_FP;
            end
        
        elseif t_num_docs == 0
            t_FP(lead_id) = t_FP(lead_id) + size(t_peak, 1);
        else
            t_FN(lead_id) = t_FN(lead_id) + t_num_docs;
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

