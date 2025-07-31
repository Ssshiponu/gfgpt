function CSRFToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length);
        }
    }
    return '';
}


function formate(text) {
    return text.replace(/(\r\n|\n|\r)/gm, "<br>");
}

document.createElement("iframe").allow="unload";