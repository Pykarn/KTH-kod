// Compressed data
window.__compressedData__widget_ozdgpgyd = "%7B%22searchFilter%22%3A%7B%22filterLabel%22%3A%22%22%2C%22placeholder%22%3A%22S%C3%B6k%20p%C3%A5%20KTH%3As%20webbplats%22%2C%22includeLinks%22%3Atrue%2C%22searchUrl%22%3A%22https%3A%2F%2Fwww.kth.se%2Fsearch%22%2C%22noscript%22%3Afalse%7D%2C%22language%22%3A%22sv%22%2C%22widgetId%22%3A%22widget_ozdgpgyd%22%2C%22loggedInUser%22%3Afalse%2C%22defaultSearchUrl%22%3A%22https%3A%2F%2Fwww.kth.se%2Fsearch%22%2C%22studentSeSearchUrl%22%3A%22https%3A%2F%2Fwww.kth.se%2Fstudent%2Fsearch%22%2C%22studentEnSearchUrl%22%3A%22https%3A%2F%2Fwww.kth.se%2Fen%2Fstudent%2Fsearch%22%2C%22intraSearchUrl%22%3A%22https%3A%2F%2Fintra.kth.se%2Fsearch%22%7D";

// searchpaths
window.searchPaths = {"web":{"suggest":{"uri":"https://www.kth.se/search/web-suggest","method":"POST"}}}

if (window.searchWidgetIds) {
    window.searchWidgetIds.push({widgetId: 'widget_ozdgpgyd', rendered:false })
} else {
    window.searchWidgetIds = [{widgetId: 'widget_ozdgpgyd', rendered:false }]
}

document.dispatchEvent(new Event("widgetDataLoaded"));