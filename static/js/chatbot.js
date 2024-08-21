
var converter = new showdown.Converter();

function loadChatBlock(){
    $(".chat-container").append(
                `
                    <div class="load-chat-block" style="width: 100%; display: flex; flex-direction: column; align-items: flex-start; gap: 0px; background-color: white; border: 0px solid #dbdbdb; padding: 10px;">
                        <div style="width: fit-content; margin-bottom: 5px; display: flex; align-items: center; gap: 10px;">
                            <span style=" display: flex; align-items: center; justify-content: center; border-radius: 50px; border: 2px solid #dbdbdb; padding: 8px; background-color: white;">
                                <svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M11.4615 20H4C3.44772 20 3 19.5523 3 19V8C3 5.79086 4.79086 4 7 4H17C19.2091 4 21 5.79086 21 8V11.3846" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M7 14H10" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M7 10H13" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <circle cx="16.5" cy="15.5" r="2.5" stroke="#000000" stroke-width="2"></circle> <path d="M18.5 17.5L21.5 20.5" stroke="#000000" stroke-width="2" stroke-linecap="round"></path> </g></svg>
                            </span>
                            <span style="color: gray; font-size: 16px; font-weight: 500;">WebLLM</span>
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
            <div class="chat-block" style="width: 100%; display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-start; gap: 0px; align-self: flex-end; padding: 15px 10px 20px 10px; background-color: rgb(234, 234, 234);">
                <div style="width: fit-content; display: flex; align-items: center; justify-content: flex-end; gap: 10px;;">
                    <span style="display: flex; align-items: center; justify-content: center; border-radius: 50px; border: 2px solid #dbdbdb; padding: 8px; background-color: white;">
                        <svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M12 14.0709C11.6734 14.0242 11.3395 14 11 14C7.13401 14 4 17.134 4 21H14M17.997 18C18.997 17 19.997 16.6046 19.997 15.5C19.997 14.3954 19.1016 13.5 17.997 13.5C17.0651 13.5 16.282 14.1374 16.06 15M17.997 21H18.007M15 7C15 9.20914 13.2091 11 11 11C8.79086 11 7 9.20914 7 7C7 4.79086 8.79086 3 11 3C13.2091 3 15 4.79086 15 7Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
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
                        <svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M11.4615 20H4C3.44772 20 3 19.5523 3 19V8C3 5.79086 4.79086 4 7 4H17C19.2091 4 21 5.79086 21 8V11.3846" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M7 14H10" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M7 10H13" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <circle cx="16.5" cy="15.5" r="2.5" stroke="#000000" stroke-width="2"></circle> <path d="M18.5 17.5L21.5 20.5" stroke="#000000" stroke-width="2" stroke-linecap="round"></path> </g></svg>
                    </span>
                    <span style="color: gray; font-size: 16px; font-weight: 500;">WebLLM</span>
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
        console.log(model_response);
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
    $(".chat-container-wrapper").removeClass("hide-chatbot");
    $(".chat-container-wrapper").addClass("show-chatbot");
    $(".startchatbtn").addClass("d-none");
}

$(".startchatbtn").click(openchatbot)

$(".closechatbot").click(function(){
    $(".chat-container-wrapper").removeClass("show-chatbot");
    $(".chat-container-wrapper").addClass("hide-chatbot");
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



