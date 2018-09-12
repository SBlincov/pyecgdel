clear all;

base_name = 'shiller';
freq = 500.0;

record = 2517;

leads = {'lead_i', 'lead_ii', 'lead_iii', 'lead_avr', 'lead_avl', 'lead_avf', 'lead_v1', 'lead_v2', 'lead_v3', 'lead_v4', 'lead_v5', 'lead_v6'};
lead_ids = 1:12;

is_filtered = 1;
is_del = 1;
wdc_scales = [1 3 4 5];
x_axis_type = 0;

markerWidth = 10;

for i = 1:size(lead_ids, 2)
    
    lead_id = lead_ids(i);
    
    fig_ecg = figure;
    propertyeditor(fig_ecg)
    
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
    for i = 1:size(ecg_lead)
        if (x_axis_type == 0)
            times(i) = (i - 1);
        else
            times(i) = (i - 1) / freq;
        end
    end
    
    hLine = plot(times, ecg_lead, 'k', 'LineWidth', 2);
    legend(hLine, 'ECG');
    set(gca, 'FontSize', 18);
    grid on;
    hold all;
    
    if is_del == 1
        file_name_qrs_del = sprintf('%s%s%sqrs_delineation.txt', db_path, record_path, lead_path);
        qrs_del = importdata(file_name_qrs_del);

        times_onset     = zeros(size(qrs_del, 1), 1);
        times_peak      = zeros(size(qrs_del, 1), 1);
        times_offset    = zeros(size(qrs_del, 1), 1);
        vals_onset      = zeros(size(qrs_del, 1), 1);
        vals_peak       = zeros(size(qrs_del, 1), 1);
        vals_offset     = zeros(size(qrs_del, 1), 1);

        for i = 1:size(qrs_del, 1)
            times_onset(i)  = times(qrs_del(i, 1) + 1);
            times_peak(i)   = times(qrs_del(i, 2) + 1);
            times_offset(i) = times(qrs_del(i, 3) + 1);

            vals_onset(i)   = ecg_lead(qrs_del(i, 1) + 1);
            vals_peak(i)    = ecg_lead(qrs_del(i, 2) + 1);
            vals_offset(i)  = ecg_lead(qrs_del(i, 3) + 1);
        end

        hLine = plot(times_onset, vals_onset,  '>', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', 'r');
        set(gca, 'FontSize', 18);
        set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
        hold all;

        hLine = plot(times_peak, vals_peak,  'o', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', 'r');
        set(gca, 'FontSize', 18);
        set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
        hold all;

        hLine = plot(times_offset, vals_offset, '<', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', 'r');
        set(gca, 'FontSize', 18);
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

        for i = 1:size(p_del, 1)
            times_onset(i)  = times(p_del(i, 1) + 1);
            times_peak(i)   = times(p_del(i, 2) + 1);
            times_offset(i) = times(p_del(i, 3) + 1);

            vals_onset(i)   = ecg_lead(p_del(i, 1) + 1);
            vals_peak(i)    = ecg_lead(p_del(i, 2) + 1);
            vals_offset(i)  = ecg_lead(p_del(i, 3) + 1);
        end

        hLine = plot(times_onset, vals_onset,  '>', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', 'green');
        set(gca, 'FontSize', 18);
        set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
        hold all;

        hLine = plot(times_peak, vals_peak,  'o', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', 'green');
        set(gca, 'FontSize', 18);
        set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
        hold all;

        hLine = plot(times_offset, vals_offset, '<', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', 'green');
        set(gca, 'FontSize', 18);
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

        for i = 1:size(t_del, 1)
            times_onset(i)      = times(t_del(i, 1) + 1);
            times_peak(i)       = times(t_del(i, 2) + 1);
            times_offset(i)     = times(t_del(i, 3) + 1);

            vals_onset(i)       = ecg_lead(t_del(i, 1) + 1);
            vals_peak(i)        = ecg_lead(t_del(i, 2) + 1);
            vals_offset(i)      = ecg_lead(t_del(i, 3) + 1);
        end

        hLine = plot(times_onset, vals_onset,  '>', 'MarkerSize', markerWidth, 'Color',  'k', 'LineWidth', 1, 'MarkerFaceColor', 'cyan');
        set(gca, 'FontSize', 18);
        set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
        hold all;

        hLine = plot(times_peak, vals_peak,  'o', 'MarkerSize', markerWidth, 'Color',  'k', 'LineWidth', 1, 'MarkerFaceColor', 'cyan');
        set(gca, 'FontSize', 18);
        set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
        hold all;

        hLine = plot(times_offset, vals_offset, '<', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', 'cyan');
        set(gca, 'FontSize', 18);
        set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
        hold all;

        if exist(sprintf('%s%s/original_del/', db_path, record_path), 'dir')

            file_name = sprintf('%s%s/original_del/json_R_P_ON.txt', db_path, record_path);
            data = importdata(file_name);
            json_r_p_on_indexes = zeros(size(data,1), 1);
            json_r_p_on_times = zeros(size(data,1), 1);
            json_r_p_on_vals = zeros(size(data,1), 1);
            for dump_id = 1:size(data,1)
                json_r_p_on_indexes(dump_id) = floor(data(dump_id) * freq);
                json_r_p_on_times(dump_id) = times(json_r_p_on_indexes(dump_id) + 1);
                json_r_p_on_vals(dump_id) = ecg_lead(json_r_p_on_indexes(dump_id) + 1);
            end

            hLine = plot(json_r_p_on_times, json_r_p_on_vals, '>', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', [1 0.84 0]);
            set(gca, 'FontSize', 18);
            set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
            hold all;

            file_name = sprintf('%s%s/original_del/json_R_T_OFF.txt', db_path, record_path);
            data = importdata(file_name);
            json_r_t_off_indexes = zeros(size(data,1), 1);
            json_r_t_off_times = zeros(size(data,1), 1);
            json_r_t_off_vals = zeros(size(data,1), 1);
            for dump_id = 1:size(data,1)
                json_r_t_off_indexes(dump_id) = floor(data(dump_id) * freq);
                json_r_t_off_times(dump_id) = times(json_r_t_off_indexes(dump_id) + 1);
                json_r_t_off_vals(dump_id) = ecg_lead(json_r_t_off_indexes(dump_id) + 1);
            end

            hLine = plot(json_r_t_off_times, json_r_t_off_vals, '<', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', [1 0.84 0]);
            set(gca, 'FontSize', 18);
            set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
            hold all;

            file_name = sprintf('%s%s/original_del/json_R_QRS_ON.txt', db_path, record_path);
            data = importdata(file_name);
            json_r_qrs_on_indexes = zeros(size(data,1), 1);
            json_r_qrs_on_times = zeros(size(data,1), 1);
            json_r_qrs_on_vals = zeros(size(data,1), 1);
            for dump_id = 1:size(data,1)
                json_r_qrs_on_indexes(dump_id) = floor(data(dump_id) * freq);
                json_r_qrs_on_times(dump_id) = times(json_r_qrs_on_indexes(dump_id) + 1);
                json_r_qrs_on_vals(dump_id) = ecg_lead(json_r_qrs_on_indexes(dump_id) + 1);
            end

            hLine = plot(json_r_qrs_on_times, json_r_qrs_on_vals, '>', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', [0.85 0.7 1]);
            set(gca, 'FontSize', 18);
            set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
            hold all;

            file_name = sprintf('%s%s/original_del/json_R_QRS_OFF.txt', db_path, record_path);
            data = importdata(file_name);
            json_r_qrs_off_indexes = zeros(size(data,1), 1);
            json_r_qrs_off_times = zeros(size(data,1), 1);
            json_r_qrs_off_vals = zeros(size(data,1), 1);
            for dump_id = 1:size(data,1)
                json_r_qrs_off_indexes(dump_id) = floor(data(dump_id) * freq);
                json_r_qrs_off_times(dump_id) = times(json_r_qrs_off_indexes(dump_id) + 1);
                json_r_qrs_off_vals(dump_id) = ecg_lead(json_r_qrs_off_indexes(dump_id) + 1);
            end

            hLine = plot(json_r_qrs_off_times, json_r_qrs_off_vals, '<', 'MarkerSize', markerWidth, 'Color', 'k', 'LineWidth', 1, 'MarkerFaceColor', [0.85 0.7 1]);
            set(gca, 'FontSize', 18);
            set(get(get(hLine,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
            hold all; 
        end
        
        
        
        file_name_wdc = sprintf('%s%s%swdc.txt', db_path, record_path, lead_path);
        wdc = importdata(file_name_wdc);
        
        wdc_num = size(wdc, 2);
        
        for wdc_scale_id = 1:size(wdc_scales, 2)
            
            wdc_scale = wdc_scales(wdc_scale_id);
            
            curr_wdc = wdc(:,wdc_scale);
            hLine = plot(times(1:size(wdc, 1)), curr_wdc, 'LineWidth', 0.5);
            legend(hLine, sprintf('wdc #%d', wdc_scale));
            set(gca, 'FontSize', 18);
            hold all;
        end
        
    end
    
    grid on;
    legend('-DynamicLegend');
    propertyeditor(fig_ecg)
    
    title(lead_name, 'Interpreter', 'latex');
    
end
