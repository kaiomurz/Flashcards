/* To do
use different font sizes for english and chinese  xxx
pinyin and english on different lines with pinyin italicised xxx
E2C xxx
repeat missed items xxx
Record time taken and display in end message
get total at begnning on load
change total box to running count on start
send back missed items and update data frame
Flip/correct/incorrect icons
add radicals
repeat missed
implement SRt

*/

//Global variables
var characters = null;
var characters_keys = null;
var current_key = null;
var flash_lang = null;
var correct_count = 0;
var incorrect_count = 0;
var total_count = 0;
var e2c;
var start_time;
var end_time;

console.log('javascript loaded');

// SHUFFLE ARRAY 
function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      let j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
  }

// FLASH DISPLAY
  function flash_display(flash_lang){
    switch (flash_lang) {
        case 'm':
            document.getElementById("flash").innerHTML = "<div class='mandarin'>" + characters[current_key]["Mandarin"] + "</div>";
            break;
        case 'e':
            document.getElementById("flash").innerHTML = "<div class='english'>" + characters[current_key]["English"] + "</div>";
            break
        case 'ep':
            document.getElementById("flash").innerHTML = 
            "<div class='ep'>"+
            "<label class='pinyin'>"+characters[current_key]["Pinyin"] +"</label>"+
            "<br>" + 
            "<label class='englishC2E'>" + characters[current_key]["English"] + "</label>"
            "</div>";
            break;
        case 'mp':
            document.getElementById("flash").innerHTML = 
            "<div class='mp'>"+
            "<label class='mandarin'>"+characters[current_key]["Mandarin"] +"</label>"+
            "<br>" + 
            "<label class='pinyin'>" + characters[current_key]["Pinyin"] + "</label>"
            "</div>";
            break;
    }
}

// START 

function start(){

    start_time = Date.now()
    
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            execute(this)
        }
    }

    var missed = "false";
    e2c = document.getElementById("E2C").checked;
    var number = document.getElementById("number").value;
    console.log('e2c',e2c);
    if(number == ""){
        number = 'empty';
    }

    var url = "/start?missed="+missed+"&number="+number;
    console.log(url);

    xhttp.open("GET",url,true);
    xhttp.send();

    
    }

// EXECUTE
function execute(xhttp) {
    
    characters = JSON.parse(xhttp.responseText);
    characters_keys = [Object.keys(characters)][0]; 
    shuffle(characters_keys);
    total_count = characters_keys.length
    current_key = characters_keys.shift();
    correct_count = 0;
    incorrect_count = 0;
    if(e2c){
        flash_lang = 'e'
        flash_display(flash_lang)
    } else {
        flash_lang = 'm'
        flash_display(flash_lang)
    }
    
}    


// END MESSAGE
function end_message(){
    time_in_minutes = Math.round((Date.now()-start_time)/60000);
    document.getElementById("flash").innerHTML = "End of session. <br> Time taken: "+time_in_minutes+" minutes";
    document.getElementById("flash").style.fontSize = "70px";
}

// FLIP
function flip(){

    if(e2c){
        if(flash_lang=='e'){
            flash_lang = 'mp'
            flash_display(flash_lang)
        }else{
            flash_lang='e'
            flash_display(flash_lang)
        }
    } else {
        if(flash_lang=='m'){
            flash_lang = 'ep'
            flash_display(flash_lang)
        }else{
            flash_lang='m'
            flash_display(flash_lang)
        }

    }

}

// CORRECT 
function correct(){ //code for end of session + send back to server and alter dataframe OR repeat missed items
    
    if(characters_keys.length!=0){
        correct_count++;
        current_key = characters_keys.shift();

        if(e2c){
            flash_lang = 'e'
            flash_display(flash_lang)
        } else {
            flash_lang = 'm'
            flash_display(flash_lang)
        }

    } else {
        correct_count++;
        end_message()
        
        /*
        end_time = Date.now()

        document.getElementById("flash").innerHTML = "You got "+correct_count+" out of "+total_count+" right";
        document.getElementById("flash").style.fontSize = "50px";
        */
        
    }
    

}



// INCORRECT 
function incorrect(){
    characters_keys.push(current_key)
    if(characters_keys.length !=0){
        incorrect_count++;
        current_key = characters_keys.shift();
        if(e2c){
            flash_lang = 'e'
            flash_display(flash_lang)
        } else {
            flash_lang = 'm'
            flash_display(flash_lang)
        }

        /*
        document.getElementById("flash").innerHTML = "<label id='mandarin'>" + characters[current_key]["Mandarin"] + "</label>";
        flash_lang = 'M';*/
    }else {
        incorrect_count++;
        end_message();
        /*
        document.getElementById("flash").innerHTML = "You got "+correct_count+" out of "+total_count+" right";
        document.getElementById("flash").style.fontSize = "50px";
        */
    }
    

}

