// Hide empty links (missing subtitle)
$('a[href=""]').hide();

// IntentBridge for Android
//if (navigator.userAgent.indexOf('Android') > 0) {
if (true) {
    $('#movies > .movie').each(function() {

        var movie_element = $(this);
        var subtitle_element = movie_element.find('.subtitle_path');
        var subtitle_path = subtitle_element.attr('href');
        if (!subtitle_path) {
            // No subtitle, no magic
            return;
        }

        subtitle_path = subtitle_element[0].href;
        var movie_path = movie_element.find('.movie_path')[0].href;
        var extras = JSON.stringify([
            {
                "name": "subs",
                "type": "android.net.Uri[]",
                "value": [subtitle_path]
            }
        ]);
        var le_url = 'http://phunehehe.github.io/IntentBridge/android.intent.action.VIEW/' +
                     encodeURIComponent(movie_path) +
                     '/' +
                     encodeURIComponent(extras);
        var links_element = movie_element.find('.links')[0];

        // Replace the subtitle link with IntentBridge
        subtitle_element.hide();
        $('<a/>', {
            href: le_url,
            text: 'Xem!'
        }).appendTo(links_element);
    });
}
