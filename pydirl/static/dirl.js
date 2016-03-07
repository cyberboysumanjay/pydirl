var suffix = ['B', 'KB','MB', 'GB', 'TB', 'PB']

function populate_table(entries){
    var table = $('table').first();

    //dirs
    dirs = entries['dirs'];
    var n_dirs = 0;
    for( var dir in dirs ){
        if(dirs[dir]['size'] === null)
            h_size = null
        else
            h_size = human_readable_size(dirs[dir]['size'])
        append_table_element(dir,
                             dir+'/',
                             'glyphicon glyphicon-folder-open',
                             size=h_size,
                             downloadUrl=dir+'/?download=true');
        n_dirs += 1;
    }

    //files
    files = entries['files']
    var n_files = 0;
    for( var file in files ){
        h_size = human_readable_size(files[file]['size'])
        append_table_element(file,
                             file,
                             'glyphicon glyphicon-unchecked',
                             h_size);
        n_files += 1;
    }

    if ((n_dirs + n_files) === 0){
       console.log('The folder is empty folder');
       show_message('This folder is empty');
    }
    console.log('Number of folders: '+ n_dirs);
    console.log('Number of files: '+ n_files);
}

function append_table_element(name, url, icon_class, size, downloadUrl){
    var row = $('#template #table-row tr').first().clone();
    row.find('.icon i').first().addClass(icon_class)
    row_name = row.find('.name a').first();
    row_name.text(name);
    row_name.attr('href', url);
    if(size)
        row.find('.size').first().text(size);
    console.log(downloadUrl)
    if(downloadUrl){
        download_button = $('#template a.download-button').first().clone();
        download_button.attr('href', downloadUrl)
        download_button.appendTo(row.find('.toolbox'))
    }
    row.appendTo('table tbody');
}

function human_readable_size(byte_size){
    var suffix_idx = 0;
    var size = byte_size;
    while((size / 1024) >= 1){
        suffix_idx++;
        size = size / 1024;
    }
    size = Math.round(size * 100) / 100;
    return size+' '+suffix[suffix_idx];
}

function show_message(msg, alert_class){
    if (alert_class === undefined)
        alert_class = 'alert-warning';
    var row = $('#template #alert-message').first().clone();
    row.find('div .alert').first().addClass(alert_class);
    row.find('p').first().text(msg);
    $('table').replaceWith(row);
}

populate_table(entries);
