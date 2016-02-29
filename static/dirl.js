
function populate_table(entries){
    var table = $('table').first();

    //dirs
    dirs = entries['dirs']
    for( var dir in dirs ){
        append_table_element(dir, dir+'/' , dirs[dir]['size']);
    }

    //files
    files = entries['files']
    for( var file in files ){
        append_table_element(file, file, files[file]['size']);
    }
}


function append_table_element(name, url, size){
    var row = $('#table-row tr').first().clone();
    row_name = row.find('.name').first()
    row_name.text(name);
    row_name.attr('href', url);
    row.find('.size').first().text(size);
    row.appendTo('table');
}

populate_table(entries);
