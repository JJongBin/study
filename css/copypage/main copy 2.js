function task(id) {
    const content = document.querySelector(id)
    const copyHtmlBtn = content.children[0].children[1]
    const copyCssBtn = content.children[0].children[2]
    console.log(content)
    console.log(copyHtmlBtn)
    console.log(copyCssBtn)
    copyHtmlBtn.addEventListener("click", function () {
        alert("hi")
    })
}
task("#content-btn-1")