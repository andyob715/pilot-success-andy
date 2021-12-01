const max_income = {
    1:30,
    2:80,
    3:50,
    4:130,
    5:20,
    6:20,
    7:16,
    8:20,
    9:20
}


function calchours()
{
    let course_input = document.getElementById("course_input").value
    let start_month = document.getElementById("start_month").value
    let classes_taken = document.getElementById("classes_taken").value
    let expected_days = document.getElementById("expected_days").value
    
    console.log("course_input",course_input)
    console.log("start_month",start_month)
    console.log("classes_taken",classes_taken)
    console.log("expected_days",expected_days)
    
    for (const [course, hours] of Object.entries(max_income)) {
        if (course === course_input) {
          var flight_hours = hours;
          console.log(flight_hours)
        }
      }
    json_obj = JSON.stringify({
        course_input_json: course_input,
        start_month_json: start_month,
        classes_taken_json: classes_taken,
        expected_days_json: expected_days,
        max_flight_hours:flight_hours
    })

    console.log(json_obj)

    fetch("/predict", {
        method: "POST", 
        body: json_obj,
        headers:
            {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            } 
    }).then(resp=>{
        return resp.json()

    }).then(resp=>{
        console.log(resp)
        document.getElementById("prediction").innerHTML=resp.Prediction.toFixed(2)
        document.getElementById("income_pct").innerHTML=resp.Income_Pct.toFixed(2)
        console.log(resp.Prediction)
        console.log(resp.Income_Pct);
    })
}