clear all;

base_name = 'qtdb';
freq = 250.0;

record = 2;

is_filtered = 0;
markerWidth = 12;
wdc_scale = 1;

leads = {'lead_ii', 'lead_v5'};

for lead_id = 1:2
    
    fig_ecg = figure;
    propertyeditor(fig_ecg)
    lead = leads{lead_id};
  
    db_path = sprintf('../Data/%s/', base_name);
    record_path = sprintf('record_%d/', record);
    lead_path = sprintf('%s/', lead);
    
    if is_filtered
        file_name_ecg = sprintf('%s%s%sfiltrated.txt', db_path, record_path, lead_path);
    else
        file_name_ecg = sprintf('%s%s%soriginal.txt', db_path, record_path, lead_path);
    end
    
    ecg_lead = importdata(file_name_ecg);
    
    for i = 1:size(ecg_lead)
        %times(i) = (i - 1);
        times(i) = (i - 1) / freq;
    end
    
    hLine = plot(times, ecg_lead, 'k', 'LineWidth', 2);
    legend(hLine, 'ECG');
    set(gca, 'FontSize', 18);
    grid on;
    hold all;
    
    
    file_name_qrs_del = sprintf('%s%s%sqrs_delineation.txt', db_path, record_path, lead_path);
    qrs_del = importdata(file_name_qrs_del);
    
    times_qrs_onset = zeros(size(qrs_del, 1), 1);
    times_qrs_peak = zeros(size(qrs_del, 1), 1);
    times_qrs_offset = zeros(size(qrs_del, 1), 1);
    vals_qrs_onset = zeros(size(qrs_del, 1), 1);
    vals_qrs_peak = zeros(size(qrs_del, 1), 1);
    vals_qrs_offset = zeros(size(qrs_del, 1), 1);
    
    for i = 1:size(qrs_del, 1)
        times_qrs_onset(i) = times(qrs_del(i, 1) + 1);
        times_qrs_peak(i) = times(qrs_del(i, 2) + 1);
        times_qrs_offset(i) = times(qrs_del(i, 3) + 1);
        
        vals_qrs_onset(i) = ecg_lead(qrs_del(i, 1) + 1);
        vals_qrs_peak(i) = ecg_lead(qrs_del(i, 2) + 1);
        vals_qrs_offset(i) = ecg_lead(qrs_del(i, 3) + 1);
    end
    
    hLine = plot(times_qrs_onset, vals_qrs_onset,  '>', 'MarkerSize', markerWidth, 'Color', 'r', 'MarkerFaceColor', 'r');
    legend(hLine, sprintf('onset qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_qrs_peak, vals_qrs_peak,  'o', 'MarkerSize', markerWidth, 'Color', 'r', 'MarkerFaceColor', 'r');
    legend(hLine, sprintf('peak qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_qrs_offset, vals_qrs_offset, '<', 'MarkerSize', markerWidth, 'Color', 'r', 'MarkerFaceColor', 'r');
    legend(hLine, sprintf('offset qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    file_name_p_del = sprintf('%s%s%sp_delineation.txt', db_path, record_path, lead_path);
    p_del = importdata(file_name_p_del);
    
    times_p_onset = zeros(size(p_del, 1), 1);
    times_p_peak = zeros(size(p_del, 1), 1);
    times_p_offset = zeros(size(p_del, 1), 1);
    vals_p_onset = zeros(size(p_del, 1), 1);
    vals_p_peak = zeros(size(p_del, 1), 1);
    vals_p_offset = zeros(size(p_del, 1), 1);
    
    for i = 1:size(p_del, 1)
        times_p_onset(i) = times(p_del(i, 1) + 1);
        times_p_peak(i) = times(p_del(i, 2) + 1);
        times_p_offset(i) = times(p_del(i, 3) + 1);
        
        vals_p_onset(i) = ecg_lead(p_del(i, 1) + 1);
        vals_p_peak(i) = ecg_lead(p_del(i, 2) + 1);
        vals_p_offset(i) = ecg_lead(p_del(i, 3) + 1);
    end
    
    hLine = plot(times_p_onset, vals_p_onset,  '>', 'MarkerSize', markerWidth, 'Color', [0 0.5 0], 'MarkerFaceColor',  [0 0.5 0]);
    legend(hLine, sprintf('onset p'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_p_peak, vals_p_peak,  'o', 'MarkerSize', markerWidth, 'Color', [0 0.5 0], 'MarkerFaceColor',  [0 0.5 0]);
    legend(hLine, sprintf('peak p'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_p_offset, vals_p_offset, '<', 'MarkerSize', markerWidth, 'Color', [0 0.5 0], 'MarkerFaceColor',  [0 0.5 0]);
    legend(hLine, sprintf('offset p'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    file_name_t_del = sprintf('%s%s%st_delineation.txt', db_path, record_path, lead_path);
    t_del = importdata(file_name_t_del);
    
    times_t_onset = zeros(size(t_del, 1), 1);
    times_t_peak = zeros(size(t_del, 1), 1);
    times_t_offset = zeros(size(t_del, 1), 1);
    vals_t_onset = zeros(size(t_del, 1), 1);
    vals_t_peak = zeros(size(t_del, 1), 1);
    vals_t_offset = zeros(size(t_del, 1), 1);
    
    for i = 1:size(t_del, 1)
        times_t_onset(i) = times(t_del(i, 1) + 1);
        times_t_peak(i) = times(t_del(i, 2) + 1);
        times_t_offset(i) = times(t_del(i, 3) + 1);
        
        vals_t_onset(i) = ecg_lead(t_del(i, 1) + 1);
        vals_t_peak(i) = ecg_lead(t_del(i, 2) + 1);
        vals_t_offset(i) = ecg_lead(t_del(i, 3) + 1);
    end
    
    hLine = plot(times_t_onset, vals_t_onset,  '>', 'MarkerSize', markerWidth, 'Color', [0 0.45 0.74], 'MarkerFaceColor',  [0 0.45 0.74]);
    legend(hLine, sprintf('onset t'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_t_peak, vals_t_peak,  'o', 'MarkerSize', markerWidth, 'Color', [0 0.45 0.74], 'MarkerFaceColor',  [0 0.45 0.74]);
    legend(hLine, sprintf('peak t'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_t_offset, vals_t_offset, '<', 'MarkerSize', markerWidth, 'Color', [0 0.45 0.74], 'MarkerFaceColor',  [0 0.45 0.74]);
    legend(hLine, sprintf('offset t'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    file_name_qrs_del = sprintf('%s%s%sqrs_doctor1_delineation.txt', db_path, record_path, lead_path);
    qrs_del = importdata(file_name_qrs_del);
    
    times_qrs_onset = zeros(size(qrs_del, 1), 1);
    times_qrs_peak = zeros(size(qrs_del, 1), 1);
    times_qrs_offset = zeros(size(qrs_del, 1), 1);
    vals_qrs_onset = zeros(size(qrs_del, 1), 1);
    vals_qrs_peak = zeros(size(qrs_del, 1), 1);
    vals_qrs_offset = zeros(size(qrs_del, 1), 1);
    
    for i = 1:size(qrs_del, 1)
        times_qrs_onset(i) = times(qrs_del(i, 1));
        times_qrs_peak(i) = times(qrs_del(i, 2));
        times_qrs_offset(i) = times(qrs_del(i, 3));
        
        vals_qrs_onset(i) = ecg_lead(qrs_del(i, 1));
        vals_qrs_peak(i) = ecg_lead(qrs_del(i, 2));
        vals_qrs_offset(i) = ecg_lead(qrs_del(i, 3));
    end
    
    hLine = plot(times_qrs_onset, vals_qrs_onset,  '>', 'MarkerSize', 8, 'Color', 'y', 'MarkerFaceColor', [1 0.84 0]);
    legend(hLine, sprintf('onset qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_qrs_peak, vals_qrs_peak,  'o', 'MarkerSize', 8, 'Color', 'y', 'MarkerFaceColor', [1 0.84 0]);
    legend(hLine, sprintf('peak qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_qrs_offset, vals_qrs_offset, '<', 'MarkerSize', 8, 'Color', 'y', 'MarkerFaceColor', [1 0.84 0]);
    legend(hLine, sprintf('offset qrs'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    
    file_name_p_del = sprintf('%s%s%sp_doctor1_delineation.txt', db_path, record_path, lead_path);
    p_del = importdata(file_name_p_del);
    
    times_p_onset = zeros(size(p_del, 1), 1);
    times_p_peak = zeros(size(p_del, 1), 1);
    times_p_offset = zeros(size(p_del, 1), 1);
    vals_p_onset = zeros(size(p_del, 1), 1);
    vals_p_peak = zeros(size(p_del, 1), 1);
    vals_p_offset = zeros(size(p_del, 1), 1);
    
    for i = 1:size(p_del, 1)
        times_p_onset(i) = times(p_del(i, 1));
        times_p_peak(i) = times(p_del(i, 2));
        times_p_offset(i) = times(p_del(i, 3));
        
        vals_p_onset(i) = ecg_lead(p_del(i, 1));
        vals_p_peak(i) = ecg_lead(p_del(i, 2));
        vals_p_offset(i) = ecg_lead(p_del(i, 3));
    end
    
    hLine = plot(times_p_onset, vals_p_onset,  '>', 'MarkerSize', 8, 'Color', [0 1.0 0], 'MarkerFaceColor',  [0.47 0.67 0.19]);
    legend(hLine, sprintf('onset p'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_p_peak, vals_p_peak,  'o', 'MarkerSize', 8, 'Color', [0 1.0 0], 'MarkerFaceColor',  [0.47 0.67 0.19]);
    legend(hLine, sprintf('peak p'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_p_offset, vals_p_offset, '<', 'MarkerSize', 8, 'Color', [0 1.0 0], 'MarkerFaceColor',  [0.47 0.67 0.19]);
    legend(hLine, sprintf('offset p'));
    set(gca, 'FontSize', 18);
    hold all;
    
    
    file_name_t_del = sprintf('%s%s%st_doctor1_delineation.txt', db_path, record_path, lead_path);
    t_del = importdata(file_name_t_del);
    
    times_t_peak = zeros(size(t_del, 1), 1);
    times_t_offset = zeros(size(t_del, 1), 1);
    vals_t_peak = zeros(size(t_del, 1), 1);
    vals_t_offset = zeros(size(t_del, 1), 1);
    
    for i = 1:size(t_del, 1)
        times_t_peak(i) = times(t_del(i, 1));
        times_t_offset(i) = times(t_del(i, 2));
        
        vals_t_peak(i) = ecg_lead(t_del(i, 1));
        vals_t_offset(i) = ecg_lead(t_del(i, 2));
    end
    

    hLine = plot(times_t_peak, vals_t_peak,  'o', 'MarkerSize', 8, 'Color', [0 0.1 1.0], 'MarkerFaceColor',  [0.3 0.75 0.93]);
    legend(hLine, sprintf('peak t'));
    set(gca, 'FontSize', 18);
    hold all;
    hLine = plot(times_t_offset, vals_t_offset, '<', 'MarkerSize', 8, 'Color', [0 0.1 1.0], 'MarkerFaceColor',  [0.3 0.75 0.93]);
    legend(hLine, sprintf('offset t'));
    set(gca, 'FontSize', 18);
    hold all;
    
    grid on;
    
    propertyeditor(fig_ecg)
    
end
