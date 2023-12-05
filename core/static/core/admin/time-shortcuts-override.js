const PRESET_HOURS = [
    // 7, 8, 9, 10 pm
    12 + 7,
    12 + 8,
    12 + 9,
    12 + 10,
    12 + 11,
]

// https://stackoverflow.com/a/51102998
$(document).ready(function () {
    if(typeof window.DateTimeShortcuts === 'undefined') {
        return;
    }

    DateTimeShortcuts.clockHours.default_ = [];
    PRESET_HOURS.forEach(hour => {
        let verbose_name = new Date(1970, 1, 1, hour, 0, 0).strftime('%H:%M');
        DateTimeShortcuts.clockHours.default_.push([verbose_name, hour])
    })
});