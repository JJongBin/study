

// const btnArray = []

// class CopyBtn {
//     constructor(id) {
//         this.id = id;
//         this.btn = document.querySelector(this.id).children[0]
//         this.copyBtn = this.btn.parentNode.previousSibling.previousSibling;
//         this.copyHtmlBtn = this.copyBtn.children[1];
//         this.copyCssBtn = this.copyBtn.children[2];
//     };

//     pushArray () {
//         btnArray.push(this.btn)
//     }
//     checkChild () {
//         const len = this.btn.children.length
//         if (len !== 0){
//         }
//     }
//     copyHtml () {
//     }
//     copyCss () {

//     }
// }

// const btn1 = new CopyBtn("#item-btn-1");
// btn1.pushArray()
// btn1.checkChild()


// const btn2 = new CopyBtn("#item-btn-2");
// btn2.pushArray()
// btn2.checkChild()

// const btn3 = new CopyBtn("#item-btn-3");
// btn3.pushArray()
// btn3.checkChild()

// const btn4 = new CopyBtn("#item-btn-4");
// btn4.pushArray()
// btn4.checkChild()

// const btn5 = new CopyBtn("#item-btn-5");
// btn5.pushArray()
// btn5.checkChild()

// const btn6 = new CopyBtn("#item-btn-6");
// btn6.pushArray()
// btn6.checkChild()


// console.log(btnArray)








const btnArray = []

class CopyBtn {
    constructor(id) {
        this.id = id;
        this.content = document.querySelector(this.id);
        this.copyHtmlBtn = this.content.children[0].children[1]
        this.copyCssBtn = this.content.children[0].children[2]
    };

    pushArray () {
        // btnArray.push(this.btn)
        this.content.addeventlistener
        console.log(this.content)
        console.log(this.copyHtmlBtn)
        console.log(this.copyCssBtn)
        this.content.addEventListener("click", function() {
            alert("hi")
        })
    }
    // checkChild () {
    //     const len = this.btn.children.length
    //     if (len !== 0){
    //     }
    // }
    // copyHtml () {
    // }
    // copyCss () {

    // }
}

const btn1 = new CopyBtn("#content-btn-1");
btn1.pushArray()
// btn1.checkChild()

