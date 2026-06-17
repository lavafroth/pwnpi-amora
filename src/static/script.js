function g(html) {
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.children[0];
}

const waitTime = 500
const files = document.querySelector("aside")
const editor = document.querySelector('[data-code]')
const logs = document.querySelector('[data-logs]')
const title = document.querySelector('main > section > input')
const newOrSave = document.querySelector('#newOrSave')
let timer

function doApi(message) {
    return fetch('/api', {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify(message)
    })
}


editor.addEventListener("keydown", (e) => {
  if (e.keyCode === 9) {
    e.preventDefault();

    editor.setRangeText(
      "  ",
      editor.selectionStart,
      editor.selectionStart,
      "end"
    );
  }
});

editor.addEventListener('keyup', (_) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
        if (title.value != '') {
            doApi({ 'action': 'store', 'filename': title.value, 'contents': editor.value })
        }
    }, waitTime);
});


function reload_logs() {
    doApi({'action':'logs'}).then(r => r.json()).then(body => {
        body.map(entry => {
            logs.value += entry + '\n'
            logs.scrollTo(0, logs.scrollHeight)
        })
    })
}

function reload_listing() {
    doApi({ 'action': 'list' }).then(r => r.json()).then(b => {
        files.innerHTML = ''
        b.map(filename => {
            const text = g(`<button data-name></button>`)
            text.innerText = filename

            text.addEventListener('click', () => {
                doApi({ 'action': 'load', 'filename': filename }).then(r => r.json()).then(b => {
                    editor.value = b["contents"]
                    title.value = filename
                    title.readOnly = true
                })
            })
            const delete_button = g(`<button>Delete</button>`)
            delete_button.addEventListener('click', () => {
                doApi({ 'action': 'delete', 'filename': filename })
            })
            const run_button = g(`<button>Run</button>`)
            run_button.addEventListener('click', () => {
                doApi({"action": "run", "filename": filename})
            })
            const entry = g(`<article></article>`)
            entry.appendChild(text)
            entry.appendChild(delete_button)
            entry.appendChild(run_button)
            files.appendChild(entry)
        })
    })
}

title.addEventListener('keypress', (e) => {
    if (e.keyCode==13) {
        addNewFile()
    }
})

function addNewFile() {
    title.readOnly = true
    doApi({"action": "create", "filename": title.value})
    newOrSave.innerText = "New"
    editor.readOnly = false
    editor.focus()
}

newOrSave.addEventListener('click', function(event) {
    if (title.readOnly) {
        editor.value = ''
        title.value = ''
        editor.readOnly = true
        title.readOnly = false
        newOrSave.innerText = "Save"
        title.focus()
        return
    }
    addNewFile()

})

function run() {
    if (title.value !== "") {
        doApi({"action": "run", "filename": title.value})
    } else {
        doApi({"action": "run", "contents": editor.value})
    }
}

reload_listing()
setInterval(reload_listing, 2000)
setInterval(reload_logs, 2000)
