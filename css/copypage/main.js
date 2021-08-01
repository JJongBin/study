// 버튼 클릭시 코드가 복사

const btnArray = []

class CopyBtn {
    constructor(id) {
        this.id = id;
        this.btn = document.querySelector(this.id).children[0]
        this.copyBtn = this.btn.parentNode.previousSibling.previousSibling;
        this.copyHtmlBtn = this.copyBtn.children[1];
        this.copyCssBtn = this.copyBtn.children[2];
    };

    pushArray () {
        btnArray.push(this.btn)
        console.log(this.copyHtmlBtn)
    }
    checkChild () {
        const len = this.btn.children.length
        if (len !== 0){
        }
    }
    copyHtml () {
        const html = this.btn;
        this.copyHtmlBtn.addEventListener("click", function () {
            // window.clipboardData.setData("Text", html)
            let cloenHtml = html.cloneNode(true);
            // console.dir(cloenHtml)
            // console.log(typeof cloenHtml.outerHTML)
            // console.log(typeof cloenHtml)
            
            let createInput = document.createElement("textarea");
            createInput.innerHTML= cloenHtml.outerHTML;
            // console.log(createInput)
            // console.log(createInput.value)
            
            createInput.select();
            document.execCommand('copy');
            // createInput.blur(); 


            //textarea를 따로 생성해서 코드를 넣어두어야 하나???
            //된거 같은데 os 환경에서 안되는건가?

        })
    }
    copyCss () {
        this.copyCssBtn.addEventListener("click", function () {
            alert("Css");
        })
        
    }
}

const btn1 = new CopyBtn("#item-btn-1");
btn1.pushArray()
btn1.checkChild()
btn1.copyHtml()
btn1.copyCss()


const btn2 = new CopyBtn("#item-btn-2");
btn2.pushArray()
btn2.checkChild()
btn2.copyHtml()
btn2.copyCss()

const btn3 = new CopyBtn("#item-btn-3");
btn3.pushArray()
btn3.checkChild()
btn3.copyHtml()
btn3.copyCss()

const btn4 = new CopyBtn("#item-btn-4");
btn4.pushArray()
btn4.checkChild()
btn4.copyHtml()
btn4.copyCss()

const btn5 = new CopyBtn("#item-btn-5");
btn5.pushArray()
btn5.checkChild()
btn5.copyHtml()
btn5.copyCss()

const btn6 = new CopyBtn("#item-btn-6");
btn6.pushArray()
btn6.checkChild()
btn6.copyHtml()
btn6.copyCss()


console.log(btnArray)


