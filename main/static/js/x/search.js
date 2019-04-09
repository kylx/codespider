$(function () {
    $( '#table' ).searchable({
        searchType: 'search-table'
    });
    
    $( '#searchable-container' ).searchable({
        searchField: '#container-search',
        selector: '.row',
        childSelector: '.col-lg-4',
        show: function(elem) {
            elem.slideDown(100);
        },
        hide: function( elem ) {
            elem.slideUp(100);
        }
    })
});