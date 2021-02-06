async function call_api(addr, json) {
    var resp = await fetch(addr, {
        method: "POST",
        body: JSON.stringify(json), 
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return resp;
}

function display_md_latex(el) {
    el.css({display: "block"});
    const tm = texmath.use(katex);
    const md = markdownit().use(tm, { engine: katex,
                                    delimiters:'dollars',
                                    katexOptions: { macros: {"\\RR": "\\mathbb{R}"} }
                                    });

    el.html(md.render(el.html()));
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}