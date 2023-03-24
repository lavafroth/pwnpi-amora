function g(html) {
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.children[0];
}

const waitTime = 500
const files = document.querySelector(".files")
const editor = document.querySelector('.editor')
const logs = document.querySelector('.logs')
const documents_icon = document.querySelector('.documents')
const run_icon = document.querySelector('.run')
const add_icon = document.querySelector('.add')
const title = document.querySelector('.editorarea > .title')
let timer

function doApi(message) {
    return fetch('/api', {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify(message)
    })
}
editor.addEventListener('keyup', (_) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
        if (title.value != '') {
            doApi({ 'action': 'store', 'filename': title.value, 'contents': editor.value })
        }
    }, waitTime);
});


function reload_logs() {
    doApi({'action':'logs'}).then(r => r.json()).then(b => {
        logs.innerHTML += b.join('\n')
        logs.innerHTML += '\n'
    })
}

function reload_listing() {
    doApi({ 'action': 'list' }).then(r => r.json()).then(b => {
        files.innerHTML = ''
        b.map(filename => {
            var text = g(`<div  class="text">${filename}</div>`)
            text.addEventListener('click', () => {
                doApi({ 'action': 'load', 'filename': filename }).then(r => r.json()).then(b => {
                    editor.value = b["contents"]
                    title.value = filename
                    title.readOnly = true
                })
            })
            var delete_button = g(`<div class="delete icon"></div>`)
            delete_button.addEventListener('click', () => {
                doApi({ 'action': 'delete', 'filename': filename })
                editor.value = ''
                title.value = ''
                title.readOnly = false
            })
            var entry = g(`<div class="entry"></div>`)
            entry.appendChild(text)
            entry.appendChild(delete_button)
            files.appendChild(entry)
        })
    })
}

title.addEventListener('keypress', (e) => {
    if (e.keyCode==13) {
        title.readOnly = true
        doApi({"action": "create", "filename": title.value})
    }
})

add_icon.addEventListener('click', () => {
    editor.value = ''
    title.value = ''
    title.readOnly = false
    title.focus()
})

documents_icon.addEventListener('click', () => {
    const classList = files.classList
    if (classList.contains("show")) {
        files.classList.replace('show', 'hide')
    } else if (classList.contains("hide")) {
        files.classList.replace('hide', 'show')
    } else {
        files.classList.add('hide')
    }
});

run_icon.addEventListener('click', () => {
    if (title.value != "") {
        doApi({"action": "run", "filename": title.value})
    }
})

reload_listing()
setInterval(reload_listing, 2000)
setInterval(reload_logs, 2000)
