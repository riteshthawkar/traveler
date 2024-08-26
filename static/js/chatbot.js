
var converter = new showdown.Converter();

function loadChatBlock(){
    $(".chat-container").append(
                `
                    <div class="load-chat-block" style="width: 100%; display: flex; flex-direction: column; align-items: flex-start; gap: 0px; background-color: white; border: 0px solid #dbdbdb; padding: 10px;">
                        <div style="width: fit-content; margin-bottom: 5px; display: flex; align-items: center; gap: 10px;">
                            <span style=" display: flex; align-items: center; justify-content: center; border-radius: 50px; border: 2px solid #dbdbdb; padding: 8px; background-color: white;">
                                <i class="fa fa-cubes text-dark" ></i>
                            </span>
                            <span style="color: gray; font-size: 16px; font-weight: 500;">Lawa.ai</span>
                        </div>
                        <p class="load-message-content" style="padding: 0px 10px 0px 50px; border-top-left-radius: 0; color: rgb(215, 215, 215); font-size: 16px; font-weight: 500;">
                            Searching....
                        </p>
                    </div>
                `
            );
}

function appendQuestion(question){

    if(!$(".start-block").hasClass("d-none")){
        $(".start-block").slideUp(200);
        $(".start-block").addClass("d-none");
    }
    
    $(".chat-container").append(
        `
            <div class="chat-block" style="width: 100%; display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-start; gap: 0px; align-self: flex-end; padding: 15px 10px 20px 10px; background-color: rgb(234, 234, 234); border-radius:10px;">
                <div style="width: fit-content; display: flex; align-items: center; justify-content: flex-end; gap: 10px;;">
                    <span style="display: flex; align-items: center; justify-content: center; border-radius: 50px; border: 2px solid #dbdbdb; padding: 8px; background-color: white;">
                        <i class="far fa-user text-dark" ></i>
                    </span>
                    <span style="color: gray; font-size: 16px; font-weight: 500;">You</span>
                </div>
                <p class="message-content" style="width: calc(100% - 100px); margin: auto; color: rgb(57, 57, 57); color:black; font-weight: 600; font-size: 16px;">
                    ${question}
                </p>
            </div>
        `
    );

    $(".chat-container").animate({
        scrollTop: $('.chat-container')[0].scrollHeight
    }, 1000);
}

function askQuestion(question){
    
    appendQuestion(question);
    
    $("#question-box").text("");

    setTimeout(loadChatBlock, 600);

    let prev_chats = sessionStorage.getItem("chats");
    if(prev_chats){
        chats = JSON.parse(prev_chats)
        chats.push({
            "type": "question",
            "content": question
        })
        sessionStorage.setItem("chats", JSON.stringify(chats));
    }
}

function fetchAnswer(question) {
    const URL = "" + encodeURIComponent(question);

    return new Promise((resolve, reject) => {
        $.ajax({
            url: "/chat/",
            type: 'POST',
            data: {
                'question': question,
            },
            dataType: 'json',
            success: function(response) {
                resolve(response["answer"]);
                
            },
            error: function(error) {
                reject("Something went wrong! Please try again.");
            }
        });
    });
}

function appendAnswer(answer){
    $(".load-chat-block").remove();
    $(".chat-container").append(
        `
            <div class="chat-block w-100" style="width: 100%; display: flex; flex-direction: column; align-items: flex-start; gap: 0px; background-color: white; border: 0px solid #dbdbdb; padding: 10px;">
                <div style="width: fit-content; margin-bottom: 5px; display: flex; align-items: center; gap: 10px;">
                    <span style=" display: flex; align-items: center; justify-content: center; border-radius: 50px; border: 2px solid #dbdbdb; padding: 8px; background-color: white;">
                        <i class="fa fa-cubes text-dark" ></i>
                    </span>
                    <span style="color: gray; font-size: 16px; font-weight: 500;">Lawa.ai</span>
                </div>
                <p class="message-content" style="width: calc(100% - 100px); height: 100%; margin: auto; font-size: 16px; font-weight: 500; text-wrap: pretty;">
                    
                </p>
            </div>
        `
    );
    $(".message-content").last().html(answer);

    $(".chat-container").animate({
            scrollTop: $('.chat-container')[0].scrollHeight
    }, 1000);

}


function provideAnswer(question) {
    let model_response;
    fetchAnswer(question).then(answer => {
        model_response = converter.makeHtml(answer);
        appendAnswer(model_response)

        let prev_chats = sessionStorage.getItem("chats");
        if(prev_chats){
            chats = JSON.parse(prev_chats)
            chats.push({
                "type": "answer",
                "content": model_response
            })
            sessionStorage.setItem("chats", JSON.stringify(chats));
        }

    }).catch(error => {
        model_response = error;
        appendAnswer(model_response)

        let prev_chats = sessionStorage.getItem("chats");
        if(prev_chats){
            chats = JSON.parse(prev_chats)
            chats.push({
                "type": "answer",
                "content": "Something went wrong! Please try again"
            })
            sessionStorage.setItem("chats", JSON.stringify(chats));
        }
    });

}

function openchatbot(){
    $(".main-chat-container").removeClass("hide-chatbot");
    $(".main-chat-container").addClass("show-chatbot");
    $(".startchatbtn").addClass("d-none");
}

$(".startchatbtn").click(openchatbot)

$(".closechatbot").click(function(){
    $(".main-chat-container").removeClass("show-chatbot");
    $(".main-chat-container").addClass("hide-chatbot");
    $(".startchatbtn").removeClass("d-none");
})

function provideQuestionToAnswer(){
    let question = $("#question-box").text();
    askQuestion(question);
    provideAnswer(question);
}

$(".sendbtn").click(provideQuestionToAnswer)

$(document).ready(()=>{

    $("#question-box").text("Write your question here...");
    $("#question-box").text("")

    $('#question-box').on('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            provideQuestionToAnswer();
        }
    });

    let prev_chats = sessionStorage.getItem("chats");
    if(prev_chats){
        chats = JSON.parse(prev_chats)
        for(let item of chats){
            if(item['type']=="answer"){
                appendAnswer(item['content'])
            }else{
                appendQuestion(item['content'])
            }
        }
    }else{
        sessionStorage.setItem("chats", JSON.stringify([]))
    }

})

$(".question-item").on("click", (e)=>{
    let exampleQuestion = e.target.innerHTML;
    $("#question-box").text(exampleQuestion);
    $(".sendbtn").click();
})

