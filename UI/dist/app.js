Dropzone.autoDiscover = false;

function init() {
    console.log("Aalo")
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    

    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        
        var url = "/api/classify_image";

        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
            console.log(data);
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }

            //Dictionary for mapping name returned by classifier to Name to be displayed
            let players = {"mahendra_dhoni": "M.S Dhoni", "neeraj_chopra": "Neeraj Chopra", "pv_sindhu": "P.V. Sindhu", "smriti_mandana": "Smriti Mandana", "virat_kohli": "Virat Kohli"};
            
            let match = null;
            let bestScore = -1;
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].Probability);
                if(maxScoreForThisClass>bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }

            let name=players[match.Name]
            //Dictionary to get info of player
            let info={
                "M.S Dhoni":"Born July 7, 1981, Ranchi, Bihar [now Jharkhand] state, India Indian cricketer whose rise to prominence in the early 21st century culminated in his captaincy of the Indian national team that won the one-day Cricket World Cup in 2011.",
                "Neeraj Chopra":"Born 24 December 1997 is an Indian athlete, who is the Olympic champion and World champion in Men's javelin throw. He is the first Asian athlete to win an Olympic gold medal in javelin and the first Asian to win gold in his event at the World Championship",
                "P.V. Sindhu":"Born 5 July 1995 is an Indian badminton player. Considered one of India's most successful sportspersons, Sindhu has won medals at various tournaments such as the Olympics and on the BWF circuit, including a gold at the 2019 World Championships.",
                "Smriti Mandana":"Born 18 July 1996 is an Indian cricketer who represents the Indian women's national team.In June 2018, the Board of Control for Cricket in India (BCCI) awarded her 'the Best Women's International Cricketer' in BCCI awards.",
                "Virat Kohli":"Born November 5, 1988, Delhi, India is an Indian international cricketer and also a former captain of the Indian cricket team in all three international formats. Kohli plays for the Royal Challengers Bangalore (RCB) in IPL."
            }

            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`#${match.Name}`).html());
                $("#player_name").html(`${name}`);
                $("#player_info").html(`${info[name]}`);
            }
            // dz.removeFile(file);            
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();


    init();
});