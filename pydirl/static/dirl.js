var suffix = ['B', 'KB','MB', 'GB', 'TB', 'PB']
function populate_table(entries){
    var table = $('table').first();

    //dirs
    dirs = entries['dirs']
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
    }

    //files
    files = entries['files']
    for( var file in files ){
        h_size = human_readable_size(files[file]['size'])
        append_table_element(file,
                             file,
                             'glyphicon glyphicon-unchecked',
                             h_size);
    }
}

function append_table_element(name, url, icon_class, size=null, downloadUrl=null){
    var row = $('#template #table-row tr').first().clone();
    row.find('.icon i').first().addClass(icon_class)
    row_name = row.find('.name a').first();
    row_name.text(name);
    row_name.attr('href', url);
    if(size !== null)
        row.find('.size').first().text(size);
    console.log(downloadUrl)
    if(downloadUrl != null){
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


populate_table(entries);
