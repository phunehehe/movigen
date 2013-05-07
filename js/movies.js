// Hide empty links (missing subtitle)
$('a[href=""]').hide();


// IntentBridge


function makeLink(action, target, extras) {
    return [
        'http://phunehehe.github.io/IntentBridge',
        action,
        encodeURIComponent(target),
        encodeURIComponent(JSON.stringify(extras))
    ].join('/');
}


//if (navigator.userAgent.indexOf('Android') > 0) {
if (true) {

    $('#movies > .movie').each(function() {

        var movieElement = $(this);
        var subtitleElement = movieElement.find('.subtitlePath');
        var subtitlePath = subtitleElement.attr('href');
        if (!subtitlePath) {
            // No subtitle, no magic
            return;
        }

        subtitlePath = subtitleElement[0].href;
        var moviePath = movieElement.find('.moviePath')[0].href;

        var extras = [
            {
                'name': 'subs',
                'type': 'android.net.Uri[]',
                'value': [subtitlePath]
            }
        ];

        var leUrl = makeLink('android.intent.action.VIEW',
                             moviePath,
                             extras);

        var linkElement = movieElement.find('.links')[0];

        // Replace the subtitle link with IntentBridge
        subtitleElement.hide();
        $('<a/>', {
            href: leUrl,
            text: 'Xem!'
        }).appendTo(linkElement);
    });
}
