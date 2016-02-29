var suffix = ['B', 'KB','MB', 'GB', 'TB', 'PB']
function populate_table(entries){
    var table = $('table').first();

    //dirs
    dirs = entries['dirs']
    for( var dir in dirs ){
        h_size = human_readable_size(dirs[dir]['size'])
        append_table_element(dir,
                             dir+'/',
                             'glyphicon glyphicon-folder-open',
                             h_size[0] + h_size[1]);
    }

    //files
    files = entries['files']
    for( var file in files ){
        h_size = human_readable_size(files[file]['size'])
        append_table_element(file,
                             file,
                             'glyphicon glyphicon-unchecked',
                             h_size[0] + h_size[1]);
    }
}

function append_table_element(name, url, icon_class, size){
    var row = $('#table-row tr').first().clone();
    row.find('.icon i').first().addClass(icon_class)
    row_name = row.find('.name a').first();
    row_name.text(name);
    row_name.attr('href', url);
    row.find('.size').first().text(size);
    row.appendTo('table tbody');
}

function human_readable_size(byte_size){
    var suffix_idx = 0;
    var size = byte_size;
    while((size / 1024) >= 1){
        suffix_idx++;
        size = size / 1024;
    }
    size = Math.round(size * 100) / 100
    return [size, suffix[suffix_idx]]
}


populate_table(entries);
