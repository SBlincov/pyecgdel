clear all;

base_name = 'shiller';
freq = 500.0;

record = 3147;

leads = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};
lead_ids = 1:12;
num_leads = size(lead_ids, 2);

y_start = 0.09;
y_total = 0.9;
y_size = 0.074;
y_shift = 0.001; 

is_filtered = 1;

x_axis_type = 0;

width_marker = 5;
size_font = 15;

fig = figure;
propertyeditor(fig);

for i = 1:num_leads
    
    lead_id = lead_ids(i);
    
    lead = leads{lead_id};
    lead_name = lead(6:end);
   
    db_path = sprintf('../Data/%s/', base_name);
    record_path = sprintf('record_%d/', record);
    lead_path = sprintf('%s/', lead);
    
    if is_filtered
        file_name_ecg = sprintf('%s%s%sfiltrated.txt', db_path, record_path, lead_path);
    else
        file_name_ecg = sprintf('%s%s%soriginal.txt', db_path, record_path, lead_path);
    end
    
    ecg_lead = importdata(file_name_ecg);
    
    times = zeros(size(ecg_lead, 1), 1);
    for time_id = 1:size(ecg_lead)
        if (x_axis_type == 0)
            times(time_id) = (time_id - 1);
        else
            times(time_id) = (time_id - 1) / freq;
        end
    end
    
    subplot(num_leads, 1, i);
    hLine = plot(times, ecg_lead, 'k', 'LineWidth', 1);
    set(gca, 'FontSize', size_font);
    set(get(get(hLine, 'Annotation'), 'LegendInformation'), 'IconDisplayStyle', 'off');
    set(gca, 'FontSize', size_font); 
    xlim([times(1) times(end)]);
    if (i ~= num_leads)
        set(gca,'xticklabel',{[]})
    end
    if (i == num_leads)
        set(gca, 'FontSize', size_font);
        xlabel(sprintf('%d', record), 'Interpreter', 'latex');
    end
    set(gca,'yticklabel',{[]})
    y_low_lim = min(ecg_lead) - (max(ecg_lead) - min(ecg_lead)) * 0.1;
    y_high_lim = max(ecg_lead) + (max(ecg_lead) - min(ecg_lead)) * 0.1;
    ylim([y_low_lim y_high_lim]);
    y_curr_start = y_start + y_total + y_shift - (i) * (y_size + y_shift);
    ylabel(lead_name, 'Interpreter', 'latex');
    set(gca, 'Position', [0.1 y_curr_start 0.85 y_size]);
    grid on;
    hold all;
    
    file_name_qrs_del = sprintf('%s%s%sqrs_delineation.txt', db_path, record_path, lead_path);
    qrs_del = importdata(file_name_qrs_del);
    
    times_onset     = zeros(size(qrs_del, 1), 1);
    times_peak      = zeros(size(qrs_del, 1), 1);
    times_offset    = zeros(size(qrs_del, 1), 1);
    vals_onset      = zeros(size(qrs_del, 1), 1);
    vals_peak       = zeros(size(qrs_del, 1), 1);
    vals_offset     = zeros(size(qrs_del, 1), 1);
    
    for del_id = 1:size(qrs_del, 1)
        times_onset(del_id)  = times(qrs_del(del_id, 1) + 1);
        times_peak(del_id)   = times(qrs_del(del_id, 2) + 1);
        times_offset(del_id) = times(qrs_del(del_id, 3) + 1);
        
        vals_onset(del_id)   = ecg_lead(qrs_del(del_id, 1) + 1);
        vals_peak(del_id)    = ecg_lead(qrs_del(del_id, 2) + 1);
        vals_offset(del_id)  = ecg_lead(qrs_del(del_id, 3) + 1);
    end
    
    hLine = plot(times_onset, vals_onset,  '>', 'MarkerSize', width_marker, 'Color', 'k', 'LineWidth', 0.1, 'MarkerFaceColor', 'r');
    set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
    hold all;
    
    hLine = plot(times_peak, vals_peak,  'o', 'MarkerSize', width_marker, 'Color', 'k', 'LineWidth', 0.1, 'MarkerFaceColor', 'r');
    set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
    hold all;
    
    hLine = plot(times_offset, vals_offset, '<', 'MarkerSize', width_marker, 'Color', 'k', 'LineWidth', 0.1, 'MarkerFaceColor', 'r');
    set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
    hold all;
    
    
    file_name_p_del = sprintf('%s%s%sp_delineation.txt', db_path, record_path, lead_path);
    p_del = importdata(file_name_p_del);
    
    times_onset     = zeros(size(p_del, 1), 1);
    times_peak      = zeros(size(p_del, 1), 1);
    times_offset    = zeros(size(p_del, 1), 1);
    vals_onset      = zeros(size(p_del, 1), 1);
    vals_peak       = zeros(size(p_del, 1), 1);
    vals_offset     = zeros(size(p_del, 1), 1);
    
    for del_id = 1:size(p_del, 1)
        times_onset(del_id)  = times(p_del(del_id, 1) + 1);
        times_peak(del_id)   = times(p_del(del_id, 2) + 1);
        times_offset(del_id) = times(p_del(del_id, 3) + 1);
        
        vals_onset(del_id)   = ecg_lead(p_del(del_id, 1) + 1);
        vals_peak(del_id)    = ecg_lead(p_del(del_id, 2) + 1);
        vals_offset(del_id)  = ecg_lead(p_del(del_id, 3) + 1);
    end
    
    hLine = plot(times_onset, vals_onset,  '>', 'MarkerSize', width_marker, 'Color', 'k', 'LineWidth', 0.1, 'MarkerFaceColor', 'green');
    set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
    hold all;
    
    hLine = plot(times_peak, vals_peak,  'o', 'MarkerSize', width_marker, 'Color', 'k', 'LineWidth', 0.1, 'MarkerFaceColor', 'green');
    set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
    hold all;
    
    hLine = plot(times_offset, vals_offset, '<', 'MarkerSize', width_marker, 'Color', 'k', 'LineWidth', 0.1, 'MarkerFaceColor', 'green');
    set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
    hold all;
    
    
    file_name_t_del = sprintf('%s%s%st_delineation.txt', db_path, record_path, lead_path);
    t_del = importdata(file_name_t_del);
    
    times_onset     = zeros(size(t_del, 1), 1);
    times_peak      = zeros(size(t_del, 1), 1);
    times_offset    = zeros(size(t_del, 1), 1);
    vals_onset      = zeros(size(t_del, 1), 1);
    vals_peak       = zeros(size(t_del, 1), 1);
    vals_offset     = zeros(size(t_del, 1), 1);
    
    for del_id = 1:size(t_del, 1)
        times_onset(del_id)      = times(t_del(del_id, 1) + 1);
        times_peak(del_id)       = times(t_del(del_id, 2) + 1);
        times_offset(del_id)     = times(t_del(del_id, 3) + 1);
        
        vals_onset(del_id)       = ecg_lead(t_del(del_id, 1) + 1);
        vals_peak(del_id)        = ecg_lead(t_del(del_id, 2) + 1);
        vals_offset(del_id)      = ecg_lead(t_del(del_id, 3) + 1);
    end
    
    hLine = plot(times_onset, vals_onset,  '>', 'MarkerSize', width_marker, 'Color',  'k', 'LineWidth', 0.1, 'MarkerFaceColor', 'cyan');
    set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
    hold all;
    
    hLine = plot(times_peak, vals_peak,  'o', 'MarkerSize', width_marker, 'Color',  'k', 'LineWidth', 0.1, 'MarkerFaceColor', 'cyan');
    set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
    hold all;
    
    hLine = plot(times_offset, vals_offset, '<', 'MarkerSize', width_marker, 'Color', 'k', 'LineWidth', 0.1, 'MarkerFaceColor', 'cyan');
    set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
    
end
