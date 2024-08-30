// Initialize Socket.IO client
const socket = io.connect('wss://ritesh-hf-web-agent.hf.space', {
    transports: ['websocket']
});

// Empty response variable to keep track of response
var response="";

// Converter for Markdown to HTML
var converter = new showdown.Converter();

// Function to load a chat block indicating that the system is searching
function loadChatBlock(){
    let lastMessageElement = $(".chat-container div:last-child");
    if(lastMessageElement.hasClass("response-block")){
        return;
    }
    $(".chat-container").append(
        `
        <div class="chat-block load-chat-block w-100" style="width: 100%; display: flex; flex-direction: column; align-items: flex-start; gap: 0px; background-color: white; border: 0px solid #dbdbdb; padding: 10px;">
            <div style="width: fit-content; margin-bottom: 5px; display: flex; align-items: center; gap: 15px;">
                <span style="display: flex; align-items: center; justify-content: center; border-radius: 50px; border: 2px solid #000000; background-color: white;">
                    <svg width="28" height="28" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M15 0C6.71573 0 0 6.71573 0 15C0 23.2843 6.71573 30 15 30C23.2843 30 30 23.2843 30 15C30 6.71573 23.2843 0 15 0ZM15 24C10.0295 24 6 19.9705 6 15C6 10.0294 10.0295 6 15 6C19.9706 6 24 10.0294 24 15C24 16.4397 23.6619 17.8004 23.0609 19.0072C22.9012 19.3279 22.848 19.6945 22.9406 20.0405L23.4766 22.044C23.7093 22.9137 22.9137 23.7093 22.044 23.4767L20.0406 22.9406C19.6945 22.848 19.3279 22.9012 19.0072 23.0608C17.8005 23.662 16.4397 24 15 24ZM15.1566 7.60664C15.1566 11.7488 18.5144 15.1066 22.6566 15.1066C18.5144 15.1066 15.1566 18.4645 15.1566 22.6066C15.1566 18.4645 11.7987 15.1066 7.65659 15.1066C11.7987 15.1066 15.1566 11.7488 15.1566 7.60664Z" fill="black"/>
                    </svg>
                </span>
                <span class="d-block" style="color: gray; font-size: 16px; font-weight: 500;">Lawa.ai</span>
            </div>
            <div class="pl-5">
                <div class="message-content pr-2" style="width: 100%; height: 100%; margin: auto; font-weight: 500; text-wrap: pretty;">
                     Searching....
                </div>
            </div>
        </div>
        `
    );
}

// Function to append a user’s question to the chat container
function appendQuestion(question){
    if(!$(".start-block").hasClass("d-none")){
        $(".start-block").slideUp(200);
        $(".start-block").addClass("d-none");
        $(".start-block").removeClass("d-flex");
    }
    
    $(".chat-container").append(
        `
        <div class="chat-block question-block bg-secondary" style="width: 100%; display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-start; gap: 0px; align-self: flex-end; padding: 15px 10px 20px 10px; border-radius:20px;">
            <div style="width: fit-content; display: flex; align-items: center; justify-content: flex-end; gap: 15px;;">
                <span style="display: flex; align-items: center; justify-content: center; border-radius: 50px; border: 1px solid #dbdbdb; padding: 8px; background-color: white;">
                    <i class="fa fa-user text-dark" ></i>
                </span>
                <span class="d-block" style="color: gray; font-size: 16px; font-weight: 500;">You</span>
            </div>
            <div class="pl-5">
                <div class="message-content pr-2" style="width: 100%; margin: auto; color: rgb(57, 57, 57); color:black; font-weight: 600; font-size: 16px; text-wrap: pretty;">
                    ${question}
                </div>
            </div>
        </div>
        `
    );

    $(".chat-container").animate({
        scrollTop: $('.chat-container')[0].scrollHeight
    }, 1000);
}

// Function to handle sending a question via Socket.IO and receiving an answer
function provideQuestionToAnswer(){

    response = "";

    let question = $("#question-box").text();
    appendQuestion(question);
    $("#question-box").text("");

    setTimeout(loadChatBlock, 600);

    // Emit question via Socket.IO
    socket.emit('message', { question: question, session_id: 'abc123'  });

    // Save chat history
    let prev_chats = sessionStorage.getItem("chats");
    if(prev_chats){
        chats = JSON.parse(prev_chats);
        chats.push({
            "type": "question",
            "content": question
        });
        sessionStorage.setItem("chats", JSON.stringify(chats));
    }
}

// Function to append an answer to the chat container
function appendAnswer(answer){
    
    let lastElement = $(".chat-container .chat-block:last-child");

    if(lastElement.hasClass("response-block")){
        $(".chat-container .chat-block:last-child").find(".message-content").html(answer)
    }
    else{
        $(".load-chat-block").remove();
        $(".chat-container").append(
            `
            <div class="chat-block response-block w-100" style="width: 100%; display: flex; flex-direction: column; align-items: flex-start; gap: 0px; background-color: white; border: 0px solid #dbdbdb; padding: 10px;">
                <div style="width: fit-content; margin-bottom: 5px; display: flex; align-items: center; gap: 15px;">
                    <span style=" display: flex; align-items: center; justify-content: center; border-radius: 50px; border: 2px solid #000000; background-color: white;">
                        <svg width="28" height="28" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M15 0C6.71573 0 0 6.71573 0 15C0 23.2843 6.71573 30 15 30C23.2843 30 30 23.2843 30 15C30 6.71573 23.2843 0 15 0ZM15 24C10.0295 24 6 19.9705 6 15C6 10.0294 10.0295 6 15 6C19.9706 6 24 10.0294 24 15C24 16.4397 23.6619 17.8004 23.0609 19.0072C22.9012 19.3279 22.848 19.6945 22.9406 20.0405L23.4766 22.044C23.7093 22.9137 22.9137 23.7093 22.044 23.4767L20.0406 22.9406C19.6945 22.848 19.3279 22.9012 19.0072 23.0608C17.8005 23.662 16.4397 24 15 24ZM15.1566 7.60664C15.1566 11.7488 18.5144 15.1066 22.6566 15.1066C18.5144 15.1066 15.1566 18.4645 15.1566 22.6066C15.1566 18.4645 11.7987 15.1066 7.65659 15.1066C11.7987 15.1066 15.1566 11.7488 15.1566 7.60664Z" fill="black"/>
                        </svg>
                    </span>
                    <span class="d-block" style="color: gray; font-size: 16px; font-weight: 500;">Lawa.ai</span>
                </div>
                <div class="pl-5">
                    <div class="message-content pr-2" style="width: 100%; height: 100%; margin: auto; font-weight: 500; text-wrap: pretty;">
                        ${ answer }
                    </div>
                </div>
            </div>
            `
        );
    }

    $(".chat-container").scrollTop($(".chat-container")[0].scrollHeight);
}

// Function to handle the answer received from the server
socket.on('response', (data) => {
    response += data;
    model_response = converter.makeHtml(response);
    appendAnswer(model_response);

    let prev_chats_1 = sessionStorage.getItem("chats");
    if(prev_chats_1){
        chats = JSON.parse(prev_chats_1);
        chats.push({
            "type": "answer",
            "content": model_response
        });
        sessionStorage.setItem("chats", JSON.stringify(chats));
    }
});

// Open the chatbot interface
function openchatbot(){
    $(".main-chat-container").removeClass("hide-chatbot");
    $(".main-chat-container").addClass("show-chatbot");
    $(".startchatbtn").addClass("d-none");
    $(".startchatbtn").removeClass("d-flex");
}

// Close the chatbot interface
$(".startchatbtn").click(openchatbot);

$(".closechatbot").click(function(){
    $(".main-chat-container").removeClass("show-chatbot");
    $(".main-chat-container").addClass("hide-chatbot");
    $(".startchatbtn").removeClass("d-none");
    $(".startchatbtn").addClass("d-flex");
});

// Send the question and get the answer
$(".sendbtn").click(provideQuestionToAnswer);

// Handle the Enter key press in the question box
$(document).ready(() => {
    $("#question-box").text("Write your question here...");
    $("#question-box").text("");

    $('#question-box').on('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            provideQuestionToAnswer();
        }
    });

    // Load previous chats from session storage
    let prev_chats = sessionStorage.getItem("chats");
    if(prev_chats){
        chats = JSON.parse(prev_chats);
        for(let item of chats){
            if(item['type'] === "answer"){
                appendAnswer(item['content']);
            } else {
                appendQuestion(item['content']);
            }
        }
    } else {
        sessionStorage.setItem("chats", JSON.stringify([]));
    }
    $(".chat-container").scrollTop($(".chat-container")[0].scrollHeight);
});

// Handle connection errors
socket.on('connect_error', (error) => {
    console.error("Connection error:", error);
    appendMessage("Sorry, there was a problem connecting to the server. Please try again later.", 'bot');
});

// Handle disconnection
socket.on('disconnect', (reason) => {
    console.warn("connected to server:", reason);
    let prev_chats_1 = sessionStorage.getItem("chats");
    if(prev_chats_1){
        chats = JSON.parse(prev_chats_1);
        chats.push({
            "type": "answer",
            "content": response
        });
        sessionStorage.setItem("chats", JSON.stringify(chats));
    }
    response = "";
});

// Handle disconnection
socket.on('disconnect', (reason) => {
    console.warn("Disconnected from server:", reason);
    appendAnswer("You have been disconnected from the server. Please refresh the page to reconnect.", 'bot');
});

// Clear the chat container
$(".clearBtn").click(() => {
    $('.chat-container').find('.chat-block').remove();
    $(".start-block").removeClass('d-none');
    $(".start-block").addClass('d-flex');
    $(".start-block").slideDown();
    sessionStorage.setItem("chats", JSON.stringify([]));
});

// Handle click on example questions
$(".question-item").on("click", (e) => {
    let exampleQuestion = e.target.innerHTML;
    $("#question-box").text(exampleQuestion);
    $(".sendbtn").click();
});
